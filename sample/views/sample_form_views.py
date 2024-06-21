from django.shortcuts import render
from django.views.generic.edit import FormView
from ..forms import SampleForm

class SampleFormView(FormView):

    template_name = 'sample/form/form.html'
    form_class    = SampleForm

    def posted_render(self, context, request):
        context.update({'posted_display': True,})
        context_prefix = 'posted_'
        form_fields = [
            'single_checkbox_form',
            'multiple_checkbox_select_form',
            'single_select_form',
            'multiple_select_form',
            'date_form',
            'time_form',
            'date_time_form',]
        for form_field in form_fields:
            context.update({ context_prefix + form_field: request.POST.getlist(form_field), })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # form が送信されたら結果を表示
            context = super().get_context_data(**kwargs)
            context = self.posted_render(context, request)
            return render(request, self.template_name, context=context)
        else:
            request.session['display_post'] = False
            return self.form_invalid(form)