from django.db import models
from django.db.models import QuerySet
from apps.summernote.models import SummernoteAttachment
from apps.summernote.help_text import help_text

# 一括削除が行われた場合には model の delete() を通らず
# こちらの QuerySet の　delete() を通る
class SampleSummernotePostQuerySet(QuerySet):
    
    def delete(self, *args, **kwargs):
        # 紐付けられた SummernoteAttachment の削除
        for self_obj in self:
            for related_object in self_obj.attachment_id.all():
                related_object.delete()
        super().delete(*args, **kwargs)

class SampleSummernotePostManager(models.Manager):
    
    def __init__(self, *args, **kwargs):
        self.query_set = SampleSummernotePostQuerySet
        super(SampleSummernotePostManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.query_set(self.model)

class SampleSummernotePost(models.Model):

    post_text = models.TextField(help_text=help_text)
    attachment_id = models.ManyToManyField(
                    SummernoteAttachment,
                    related_name='related_sample_summernote_post_attachment_id',)
    
    objects = SampleSummernotePostManager()
    
    def delete(self, *args, **kwargs):
        # 紐付けられた SummernoteAttachment の削除
        for related_object in self.attachment_id.all():
            related_object.delete()
        super().delete(*args, **kwargs)

    class Meta:
        app_label    = 'sample'
        db_table     = 'sample_summernote_post_model'
        verbose_name = verbose_name_plural = '01_SummernotePost'