import sys

def embed(container_file, data_file) :
    container = open(container_file, "rb").read()
    data = open(data_file, "rb").read()

    # suppose head is 2048 bytes
    if len(data)+2048+3 >= len(container):
        print("Not enough space to save " + data_file)
    else :
        f = open('embeded.jpg', "wb")
        f.write(container[ : len(container)-len(data)-3]) # additional 3 bytes are for storing txt size: maximum should be less than 16M(b'\xff\xff\xff')
        f.write(data)
        f.write(len(data).to_bytes(3, 'big'))
        f.close()

if "__main__" == __name__ :
    try :
        if len(sys.argv) == 3 :
            embed(sys.argv[1], sys.argv[2])
        else :
            print("Usage:\n%s container data output" % sys.argv[0])
    except Exception as err :
        print(err)