import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

from app.models import Model_Info, Product
from app.models import Product_Comment
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
import joblib
from datetime import date

# all_model = LGBMClassifier() # category = 0
# beer_model = LGBMClassifier() # category = 1
# wine_model = LGBMClassifier() # category = 2
# cocktail_model = LGBMClassifier() # category = 3

# recommand.html에서 받은 데이터로 모델만 가져와서 결과값(군집) 추출 후 반환
def return_cluster(list1, category_id = 1): # list1에는 5가지 맛 + 도수 = 6가지 기준
    # 업데이트 해줌
    model = Model_Info.objects.order_by('-update_time').first()
    now = date.today()
    if (model == None) or (now - model.update_time.date()).days > 7:
        update_cluster(0)
        update_cluster(1)
        # 데이터 추가 후에 주석 해제
        # update_cluster(2)
        # update_cluster(3)
        Model_Info(update_time=now).save()

    if category_id == 0:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category_id=category_id)

    alcohol_list = []
    for product in products:
        alcohol_list.append(product.alcohol)

    alcohol_max = max(alcohol_list)
    alcohol_min = min(alcohol_list)
    
    test = pd.DataFrame([list1])
    test.columns = ['bold', 'sparkling','sweet', 'tannic', 'acidic', 'alcohol']
    test.alcohol = round((test.alcohol - alcohol_min) / (alcohol_max - alcohol_min), 2)

    # LGBM 모델 가져오기 (prediction용)
    if category_id == 0:
        file_name = 'all_model.pkl' 
        model = joblib.load(file_name) 
    elif category_id == 1:
        file_name = 'beer_model.pkl' 
        model = joblib.load(file_name) 
    elif category_id == 2:
        file_name = 'wine_model.pkl' 
        model = joblib.load(file_name) 
    else:
        file_name = 'cocktatil_model.pkl' 
        model = joblib.load(file_name) 

    result = model.predict(test)
    return result[0]

# product.kmeans 최신화
def update_cluster(category_id):
    if category_id == 0:
        comments = Product_Comment.objects.all()
    else:
        comments = Product_Comment.objects.filter(product__category_id = category_id)

    ###################################### clustering ####################################################3
    # 데이터 베이스의 모든 주류 (clustering을 위한 kmeans를 제외한 데이터)
    content_list = []
    for comment in comments:
        content_list.append([comment.bold, comment.sparkling, comment.sweet, comment.tannic, comment.acidic, comment.product.alcohol])
    content_list = pd.DataFrame(content_list)
    content_list.columns = ['bold', 'sparkling', 'sweet', 'tannic', 'acidic', 'alcohol']
    
    # clustering 모델 학습
    # kmeans clustering을 통한 최신 군집 생성
    kmeans = KMeans(n_clusters=5).fit(content_list)

    # clustering 학습을 통해서 나온 결과값(각 데이터에 대한 군집값)
    cluster_group = kmeans.labels_

    # label update
    for idx, comment in enumerate(comments):
        comment.product.kmeans = cluster_group[idx]
        comment.product.save()

    ###################################### LGBM ####################################################3
    # 데이터 베이스의 모든 주류 (LGBM을 위한 kmeans를 포함한 데이터)
    content_list = []
    for comment in comments:
        content_list.append([comment.bold, comment.sparkling, comment.sweet, comment.tannic, comment.acidic, comment.product.alcohol, comment.product.kmeans])
    content_list = pd.DataFrame(content_list)
    content_list.columns = ['bold', 'sparkling', 'sweet', 'tannic', 'acidic', 'alcohol', 'kmeans']
    # 알코올 정규화 0 ~ 1
    scaler = MinMaxScaler()
    content_list.alcohol = scaler.fit_transform(pd.DataFrame(content_list.alcohol))
    content_list.alcohol = round(content_list.alcohol, 2)

    # lightGBM 모델을 통한 군집 예측
    X = content_list.iloc[:, :-1]
    y = content_list.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, shuffle=False)
    
    model = LGBMClassifier()
    model.fit(X_train, y_train)

    if category_id == 0:
        file_name = 'all_model.pkl' 
        joblib.dump(model, file_name)
    elif category_id == 1:
        file_name = 'beer_model.pkl' 
        joblib.dump(model, file_name)
    elif category_id == 2:
        file_name = 'wine_model.pkl' 
        joblib.dump(model, file_name)
    else:
        file_name = 'cocktail_model.pkl' 
        joblib.dump(model, file_name)