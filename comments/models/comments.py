from django.contrib.auth import get_user_model
from django.db import models
from base.tasks import send_comment_updates, resize_image_task
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from base.custom_validators import FileValidator, TextValidator
from base.model import BaseModel
from base.utils.file_manager import get_extensions_and_type

User = get_user_model()

class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[TextValidator()])
    rating = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True, blank=True
    )

    def get_upload_url(self, filename: str):
        return f"media/{self.user.id}/{filename}"

    file = models.FileField(upload_to=get_upload_url, null=True, blank=True, validators=[FileValidator()])


    def get_children(self):
        return Comment.objects.filter(parent=self)

    def __str__(self):
        return f"{self.user.username}{self.text}"

    def __repr__(self):
        return f"Comment(id={self.id}, user={self.user.id}, parent={self.parent.id})"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            file_extension, mime_type = get_extensions_and_type(self.file.name)
            if mime_type == 'image':
                resize_image_task.delay(self.file.path, file_extension)


@receiver(post_save, sender=Comment)
def on_save(sender, instance, **kwargs):
    send_comment_updates.delay()

@receiver(post_delete, sender=Comment)
def on_delete(sender, instance, **kwargs):
    send_comment_updates.delay()

