from django.db import models
from acc.models import User


# Create your models here.

class Product(models.Model):
    product = models.CharField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    shortcon = models.TextField(max_length=30)
    content = models.TextField()
    pubdate = models.DateTimeField()
    picture = models.ImageField(upload_to= "product/", blank=True, null=True)
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

    def summary(self):
        if len(self.content) > 20:
            return f"{self.content[:20]} ...자세히 보기"
        return self.content

    def __str__(self):
        return f"{self.product}_{self.seller}"

    def getpic(self):
        if self.picture:
            return self.picture.url
        return "/media/noimage.jpg"

    def cate_choice(self) :
        
        return f"{self.category_choice[1]}"

    def cate_name(self) : 
        cho = self.cate

        return f"{self.cate}"

# class Reply(models.Model):
#     board = models.ForeignKey(Product, on_delete=models.CASCADE)
#     replyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()

#     def __str__(self):
#       return f"{self.product}_{self.replyer}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.product}_{self.replyer}"
