import zipfile
import time
import threading

zfile = zipfile.ZipFile("流浪d球2.zip", 'r')

cnt = 0
 
def extract(password, file):
    # if stops somewhere, that might be the correct answer, just stop this program and use it to extract manually
    try:
        global cnt
        password = str(password)
        print(cnt, password)
        file.extractall(path='.', pwd=password.encode('utf-8'))
        print("the password is {}".format(password))
    except Exception as e:
        print(e)
 
ps = ['1237', '147', '12379', '146', '146', '146', '5']

def dfs(i, cur):
    if i >= len(ps):
        global cnt
        cnt += 1
        extract(cur, zfile)
        return

    for c in ps[i]:
        dfs(i+1, cur+c)
 
if __name__ == '__main__':
    dfs(0, '')