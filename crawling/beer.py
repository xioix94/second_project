import os

path_dir = 'D:\kkj\web\django\second_project\crawling\data'

file_list  = []
for item in os.listdir(path_dir):
    if '.txt' in item:
        file_list.append(item)
count = 0
for item in file_list:
    try:
        
        f = open('data/' + item, 'r', encoding='euc-kr')
        # print(item)
        f.readline()
        f.close()
    except: 
        print("안되에    " + item)
        count += 1
        pass
print(count)