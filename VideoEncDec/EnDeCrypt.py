import sys

# PyInstaller will store data files in a temporary folder called sys._MEIPASS
if hasattr(sys, '_MEIPASS'):
    container_file = os.path.join(sys._MEIPASS, 'ML2.png')
else:
    container_file = 'ML2.png'

png_end = b'\x00\x00\x00\x00IEND\xaeB`\x82'

def kmp(s):
    p = b' ' + png_end # 从1开始
    n = len(p)-1
    m = len(s)-1
    next_ = [0]*int(1e5+10) # 从1开始，i = 1的next肯定为0

    # 求模版串p的next数组
    j = 0
    for i in range(2, n+1):
        while j and p[i] != p[j+1]:
            j = next_[j]
        if p[i] == p[j+1]:
            j += 1 
        next_[i] = j

    j = 0
    for i in range(1, m+1):
        while j and s[i] != p[j+1]:
            j = next_[j]
        if s[i] == p[j+1]:
            j += 1 
        if j == n:
            return i - j
            j = next_[j]

def embed(data_file):
    if data_file.split(".")[-1] == 'jpg':
        # decoding
        container = open(data_file, "rb").read()

        f = open(f'{"".join(data_file.split(".")[:-1])}.mp4', "wb")
        tmp = container[kmp(b' '+container)+len(png_end):]
        print(len(tmp))
        f.write(tmp)
        f.close()
    else:
        # encoding
        container = open(container_file, "rb").read()
        data = open(data_file, "rb").read()

        f = open(f'{data_file.split(".")[0]}.jpg', "wb")
        f.write(container) # additional 3 bytes are for storing txt size: maximum should be less than 16M(b'\xff\xff\xff')
        f.write(data)
        f.close()

if "__main__" == __name__:
    try:
        if len(sys.argv) > 1:
            embed(sys.argv[1])
        else :
            print("Usage:\n%s container data output" % sys.argv[0])
    except Exception as err:
        print(err)