from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from sorl.thumbnail import get_thumbnail, delete
from uuid import uuid4
from .settings import RESIZE_WIDTH

def get_attachment_image_path(instance, filename):
    return f'apps/summernote/attachment/image/{instance.pk}/{filename}'

class SummernoteAttachment(models.Model):

    attachment_id = models.UUIDField(
                    primary_key = True,
                    db_index    = True,
                    blank       = False,
                    null        = False,
                    editable    = True,
                    default     = uuid4().hex,)
    image_file = models.ImageField(
                    upload_to    = get_attachment_image_path,
                    blank        = True,
                    null         = True,)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)

    def save(self, *args, **kwargs):
        super().save()
        # 画像のリサイズ処理
        try:
            resize_width  = RESIZE_WIDTH
            if self.image_file.width > resize_width:
                
                new_width  = resize_width
                new_height = int(self.image_file.height*(resize_width/self.image_file.width))
                resized    = get_thumbnail(self.image_file, f'{new_width}x{new_height}',
                                           quality = 99)
                name       = self.image_file.name.split('/')[-1]
                
                self.image_file.save(name, ContentFile(resized.read()), True)
                delete(resized) # キャッシュファイルの削除
        except: pass

    class Meta:
        app_label    = 'summernote'
        db_table     = 'summernote_attachment_model'
        verbose_name = verbose_name_plural = '01_SummernoteAttachment'