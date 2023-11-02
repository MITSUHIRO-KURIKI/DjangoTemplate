from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView, DetailView,
)
from django.views.generic.edit import UpdateView
from apps.summernote.converter import modify_fnc, revert_fnc
from ..models import SampleSummernotePost
from ..forms import SampleSummernotePostCreateForm

User = get_user_model()


class SampleSummernotePostCreateView(CreateView):

    model         = SampleSummernotePost
    template_name = 'common/debug/sample/summernote_form/create_or_update.html'
    form_class    = SampleSummernotePostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # SampleSummernotePost 一覧
        sample_summernote_post_model = self.model.objects.all
        # summernote メンション用 リスト
        MENTIONS_LIST = list(User.objects.filter(is_active=True).values_list('unique_account_id', flat=True))
        context.update({
            'sample_summernote_post_model': sample_summernote_post_model,
            'MENTIONS_LIST':                MENTIONS_LIST,
        })
        return context
    
    def summernote_convert(self, object, form):
        # convert(modify_fnc)
        post_text, attachment_model_object = modify_fnc(object.post_text)
        # 置き換え
        object.post_text = post_text
        object.attachment_id.set(attachment_model_object)
        return form

    def form_valid(self, form):
        # self.object に save() されたオブジェクトが格納される
        valid = super().form_valid(form)
        form  = self.summernote_convert(self.object, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sample:summernote_detail',
                       kwargs={'pk': self.object.pk})

class SampleSummernotePostDetailView(DetailView):

    model               = SampleSummernotePost
    template_name       = 'common/debug/sample/summernote_form/detail.html'
    context_object_name = "obj"

    def summernote_decode(self, object):
        # convert(revert_fnc: revert_type='id2url')
        attachment_ids_urls_dict = { attachment_id.attachment_id.hex: attachment_id.image_file.url for attachment_id in object.attachment_id.all() }
        decoded_text             = revert_fnc(object.post_text, 'id2url', attachment_ids_urls_dict)
        return decoded_text
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # summernote_decode(attachment_id -> image file)
        decoded_text = self.summernote_decode(self.object)
        # SampleSummernotePost 一覧
        sample_summernote_post_model = self.model.objects.all
        context.update({
            'decoded_text':                 decoded_text,
            'sample_summernote_post_model': sample_summernote_post_model,
        })
        return context

class SampleSummernotePostUpdateView(UpdateView):

    model               = SampleSummernotePost
    fields              = ('post_text',)
    template_name       = 'common/debug/sample/summernote_form/create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # convert(revert_fnc: revert_type='id2base64')
        decoded_text = revert_fnc(self.object.post_text, 'id2base64')
        # SampleSummernotePost 一覧
        sample_summernote_post_model = self.model.objects.all
        # summernote メンション用 リスト
        MENTIONS_LIST = list(User.objects.filter(is_active=True).values_list('unique_account_id', flat=True))
        context.update({
            'decoded_text':                 decoded_text,
            'sample_summernote_post_model': sample_summernote_post_model,
            'MENTIONS_LIST':                MENTIONS_LIST,
        })
        return context

    def summernote_convert(self, object, form):
        # convert(modify_fnc)
        attachment_ids_list                = [ attachment_id.attachment_id.hex for attachment_id in object.attachment_id.all() ]
        post_text, attachment_model_object = modify_fnc(self.object.post_text, attachment_ids_list)
        # 置き換え
        object.post_text = post_text
        object.attachment_id.set(attachment_model_object)
        return form

    def form_valid(self, form):
        form  = self.summernote_convert(self.object, form)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('sample:summernote_detail',
                       kwargs={'pk': self.kwargs['pk']})

def SampleSummernotePostDeleteView(request, pk):
    obj = get_object_or_404(SampleSummernotePost, pk=pk)
    obj.delete()
    return redirect('sample:summernote_create')