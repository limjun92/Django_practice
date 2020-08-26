from django.db import models

# Create your models here.

class AiClass(models.Model):
    class_num = models.IntegerField()
    lecturer = models.CharField(max_length=30)
    class Meta:
        # 정렬을 해준다 class_num을 기준으로
        ordering = ['class_num']

class AiStudents(models.Model):
    class_num = models.IntegerField()
    name = models.CharField(max_length =30)
    phone_num = models.CharField(max_length=30)