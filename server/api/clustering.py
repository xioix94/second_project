import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import re
from app.models import Product, User
from django.views.decorators.csrf import csrf_exempt
from app.models import Product_Comment
import pickle

# 데이터 베이스에서 데이터 가져와서 학습 시키고 군집 및 모델 최신화
def cluster_upgrade():
    return

# recommand.html에서 받은 데이터로 모델만 가져와서 결과값(군집) 추출 후 반환
def return_cluster(list1): # list1에는 5가지 맛 + 도수 = 6가지 기준

    comments = Product_Comment.objects.select_related('product')
    content_list = []

    for comment in comments:
        content_list.append([comment.bold, comment.sparkling, comment.sparkling, comment.tannic, comment.acidic, comment.product.alcohol])
    
    content_list.append(list1)
    content_list = pd.DataFrame(content_list)
    content_list.columns = ['bold', 'sparkling', 'sparkling', 'tannic', 'acidic', 'alcohol']

    scaler = MinMaxScaler()
    content_list.alcohol = scaler.fit_transform(pd.DataFrame(content_list.alcohol))
    content_list.alcohol = round(content_list.alcohol, 2)

    kmeans = KMeans(n_clusters=5).fit(content_list)

    result = kmeans.labels_[-1]

    return result