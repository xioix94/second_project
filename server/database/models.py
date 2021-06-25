from django.db import models

class User(models.Model):
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_alias = models.CharField(max_length=100)
    user_sex = models.BooleanField()
    user_image = models.CharField(max_length=1000)

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    

class Board(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    board_title = models.CharField(max_length=100)
    board_content = models.CharField(max_length=2000)
    board_time = models.DateTimeField()

class Board_Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    board_comment_content = models.CharField(max_length=2000)
    board_comment_time = models.DateTimeField()

class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_image = models.CharField(max_length=1000)

class Product_Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_comment_score = models.FloatField() # 있을 수도?
    product_commnet_content = models.CharField(max_length=2000)
    product_comment_time = models.DateTimeField()

class Taste(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    taste_name = models.CharField(max_length=100)
    taste_value = models.FloatField() # 있을 수도?
