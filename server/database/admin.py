from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Board)
admin.site.register(Board_Comment)
admin.site.register(Product)
admin.site.register(Product_Comment)


