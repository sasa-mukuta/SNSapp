from django.db import models

# Create your models here.

class SnsModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    # 画像データの保存先（settings.py記載のものより深い階層に保存したいとき指定）
    images = models.ImageField(upload_to='')
    good = models.IntegerField(null=True, blank=True, default=0)
    read = models.IntegerField(null=True, blank=True, default=0)
    read_user = models.CharField(max_length=100, null=True, blank=True, default='default_user')
