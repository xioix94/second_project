import os
import random
path_dir = 'D:\kkj\web\django\second_project\crawling\data'

file_list  = []
for item in os.listdir(path_dir):
    if '.txt' in item:
        file_list.append(item)

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
        f = open('data/' + item, 'r', encoding='euc-kr')
        bd, sp, sw, bit, acid = round(random.uniform(0, 1), 2), [], 0, 0, 0
        content = f.readlines()
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
        round(content[20][start:end])

        # 씁쓸함(smooth tannic) bit

        # 신맛(soft acidic) acid

        f.close()
    except: 
        print("안되에    " + item)
        pass
