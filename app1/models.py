import boto3
from PIL import Image, ExifTags
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.files.storage import default_storage as storage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from TochkaProject import settings


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     try:
    #         for orientation in ExifTags.TAGS.keys():
    #             if ExifTags.TAGS[orientation] == 'Orientation': break
    #         exif = dict(img.getexif().items())
    #
    #         if exif[orientation] == 3:
    #             img = img.rotate(180, expand=True)
    #         elif exif[orientation] == 6:
    #             img = img.rotate(270, expand=True)
    #         elif exif[orientation] == 8:
    #             img = img.rotate(90, expand=True)
    #
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)
    #     except Exception:
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        image = Image.open(self.image)
        resized_image = image.resize((200, 200), Image.ANTIALIAS)

        fh = storage.open(self.image.name, "wb")
        picture_format = 'png'
        resized_image.save(fh, picture_format)
        fh.close()


class Likes(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField()
    likes = GenericRelation(Likes)
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    content_key = models.CharField(max_length=200, unique=True)

    def generate_download_url(self, ):
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.YANDEX_CLIENT_DOCS_BUCKET_NAME,
                'Key': self.content_key
            }
        )
        return url

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)

        image = Image.open(self.preview)
        resized_image = image.resize((200, 200), Image.ANTIALIAS)

        fh = storage.open(self.preview.name, "wb")
        picture_format = 'png'
        resized_image.save(fh, picture_format)
        fh.close()

    @property
    def total_likes(self):
        return self.likes.count()
