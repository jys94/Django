from django.db import models
from acc.models import User


# Create your models here.

class Live(models.Model):
    title = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liseller")
    shortcon = models.TextField(max_length=20)
    content = models.TextField()
    pubdate = models.DateTimeField()
    video = models.FileField(upload_to= "live/", blank=False, null=False)
    viewcount = models.IntegerField(default=0)
    sellcount = models.IntegerField(default=0)
    price = models.IntegerField()
    category_choice = (
        ('ELC', '가전'),
        ('FOD', '음식'),
        ('CLO', '의류'),
        ('LIV', '생필품')
    )
    cate = models.CharField(max_length=3, choices=category_choice)

    def getvideo(self):
        return self.video.url




class Reply(models.Model):
    title = models.ForeignKey(Live, on_delete=models.CASCADE )
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    livecomment = models.TextField()

    def __str__(self):
        return f"{self.title}_{self.viewer}"