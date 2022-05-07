import sys

def embed(container_file) :
    container = open(container_file, "rb").read()

    size_info_of_txt = container[-3:]
    f = open('decoded.txt', "wb")
    length_of_txt = int.from_bytes(size_info_of_txt, byteorder='big')
    # print(length_of_txt)
    f.write(container[len(container)-length_of_txt-3:-3])
    f.close()

if "__main__" == __name__ :
    try :
        if len(sys.argv) == 2 :
            embed(sys.argv[1])
        else :
            print("Usage:\n%s container data output" % sys.argv[0])
    except Exception as err :
        print(err)