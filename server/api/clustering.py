import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import re

from sklearn.utils import shuffle
from app.models import Category, Product, User
from django.views.decorators.csrf import csrf_exempt
from app.models import Product_Comment
import pickle
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

# recommand.html에서 받은 데이터로 모델만 가져와서 결과값(군집) 추출 후 반환
def return_cluster(list1): # list1에는 5가지 맛 + 도수 = 6가지 기준

    comments = Product_Comment.objects.select_related('product').filter(Category=0)       # 일단 맥주만
    content_list = []

    # 데이터 베이스의 모든 주류 
    for comment in comments:
        content_list.append([comment.bold, comment.sparkling, comment.sparkling, comment.tannic, comment.acidic, comment.product.alcohol, comment.product.kmeans])
    content_list.append(list1)
    content_list = pd.DataFrame(content_list)
    content_list.columns = ['bold', 'sparkling', 'sparkling', 'tannic', 'acidic', 'alcohol']

    # 알코올 정규화 0 ~ 1
    scaler = MinMaxScaler()
    content_list.alcohol = scaler.fit_transform(pd.DataFrame(content_list.alcohol))
    content_list.alcohol = round(content_list.alcohol, 2)

    # lightGBM 모델을 통한 군집 예측
    X = content_list.iloc[:, :-1]
    y = content_list.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, shuffle=False)

    clf = LGBMClassifier()
    clf.fit(X_train, y_train)

    y_pred=clf.predict(X_test)
    result = y_pred[-1]

    return result

# product.kmeans 최신화
def update_cluster():

    comments = Product_Comment.objects.select_related('product').filter(Category=0)       # 일단 맥주만
    content_list = []

    # 데이터 베이스의 모든 주류 
    for comment in comments:
        content_list.append([comment.bold, comment.sparkling, comment.sparkling, comment.tannic, comment.acidic, comment.product.alcohol, comment.product.kmeans])
    content_list = pd.DataFrame(content_list)
    content_list.columns = ['bold', 'sparkling', 'sparkling', 'tannic', 'acidic', 'alcohol']

    # 알코올 정규화 0 ~ 1
    scaler = MinMaxScaler()
    content_list.alcohol = scaler.fit_transform(pd.DataFrame(content_list.alcohol))
    content_list.alcohol = round(content_list.alcohol, 2)

    # kmeans clustering을 통한 최신 군집 생성
    kmeans = KMeans(n_clusters=5).fit(content_list)

    cluster_group = kmeans.labels_[:-1]

    # label update
    for idx, comment in enumerate(comments):
        comment.product.kmeans = cluster_group[idx]
        comment.product.save()

    return 
