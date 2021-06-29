import os
import random

# 'D:\\ringa\\web\\second_project\\crawling'에서 작업 중
path_dir = './data/'
file_list  = []
for item in os.listdir(path_dir):
    if '.txt' in item:
        file_list.append(item)

# 이미지 String 변환
image_path_dir = './images/'
image_str_list  = []
for item in os.listdir(image_path_dir):
    image_str_list.append(item)
        
# 맥주 이름
titles = []
for item in file_list:
    start = 0
    end = 0
    for i in range(len(item)):
        if item[i] == '_':
            start = i + 1
    for i in range(start, len(item)):
        if item[i] == '.':
            end = i
    titles.append(item[start:end])


# 바디감(light bold) bd
# 탄산감(sparkling) sp
# 달콤함(dry sweet) sw
# 씁쓸함(smooth tannic) bit
# 신맛(soft acidic) acid

beer_state_sort = {}
# beer state sort 딕셔너리
# beer state sort = {'맥주이름' : [맛 구분]}
# 맛 구분 = [['바디감'  ???] , ['탄산감' : ???], ['달콤함' : ???], ['씁쓸함' : ???], ['신맛' : ???]]



for item in file_list:
    try:
        f = open('./data/' + item, 'r', encoding='euc-kr')
        bd, sp, sw, bit, acid = round(random.uniform(0, 1), 2), [], 0, 0, 0
        content = f.readlines()
        
        # 맥주 이름
        start = 0
        end = 0
        for i in range(len(item)):
            if item[i] == '_':
                start = i + 1
        for i in range(start, len(item)):
            if item[i] == '.':
                end = i
        title = (item[start:end])

        # 이미지 파일 이름
        image_name = image_str_list.pop()

        # 각 맛 구분 찾아내기
        # 탄산감(sparkling) sp
        start = 0
        end = 0
        for j in range(len(content[53])):
            if content[53][j] == '!':
                start = j + 4
                break
        for j in range(start, len(content[53])):
            if content[53][j] == '번':
                end = j
                break
        sp.append((content[53][start:end]))

    
        start = 0
        end = 0
        for j in range(len(content[54])):
            if content[54][j] == '!':
                start = j + 4
                break
        for j in range(start, len(content[54])):
            if content[54][j] == '번':
                end = j
                break
        sp.append((content[54][start:end]))

        sp = list(map(float, sp))
        if sp[0] == sp[1] == 0:
            sp = 0
        else:
            sp = round(sp[0] / (sp[0] + sp[1]), 2)

        # 달콤함(dry sweet) sw
        start = 0
        end = 0
        for j in range(len(content[20])):
            if content[20][j] == ':':
                start = j+2
                break
        for j in range(start, len(content[20])):
            if content[20][j] == '%':
                end = j
                break
        sw = round(0.01 * float(content[20][start:end]), 2)

        # 씁쓸함(smooth tannic) bit
        start = 0
        end = 0
        for j in range(len(content[21])):
            if content[21][j] == ':':
                start = j+2
                break
        for j in range(start, len(content[21])):
            if content[21][j] == '%':
                end = j
                break
        bit = round(0.01 * float(content[21][start:end]), 2)

        # 신맛(soft acidic) acid
        start = 0
        end = 0
        for j in range(len(content[30])):
            if content[30][j] == ':':
                start = j+2
                break
        for j in range(start, len(content[30])):
            if content[30][j] == '%':
                end = j
                break
        acid = round(0.01 * float(content[30][start:end]),2)

        # 알코올 도수
        alcohol = round(random.uniform(4, 10), 2)

        beer_state_sort[title] = [image_name, title ,bd, sp, sw, bit, acid, alcohol]

        f.close()
    except: 
        print("Error    " + item)
        pass

for title in titles:
    if title in beer_state_sort.keys(): 
        print(beer_state_sort[title])

    numbering = [i for i in range(150)]
    count = 0
    for i in beer_state_sort.values():
        str = "insert into app_product values ({}, '{}', '{}', {}, {}, {}, {}, {}, {}, {});".format(numbering[count], i[1], i[0], i[2], i[3], i[4], i[5], i[6], i[7], 0)
        count += 1
        print(str)