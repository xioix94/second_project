from django.db import models


class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    sex = models.BooleanField()  # 남자 0 여자 1
    image = models.CharField(max_length=1000)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()


class Board_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    bold = models.FloatField()  # 바디감
    sparkling = models.FloatField()  # 탄산감
    sweet = models.FloatField()  # 달콤함
    tannic = models.FloatField()  # 씁쓸함
    acidic = models.FloatField()  # 신맛
    alcohol = models.FloatField()  # 알콜 도수


class Product_Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField()
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()
