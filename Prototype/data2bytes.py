import struct
from PIL import Image


# 将二值化图片数据分解成二进制字节流
def ImgDecompose_1(img):
    data = []

    size = []
    for arg in img.size:
        size += [b for b in struct.pack("i",arg)]
    for b in size:
        for i in range(7,-1,-1):
            data.append((b >> i) & 0x1)

    data += [int(bool(b)) for b in img.convert("1").getdata()]

    return data

# 将二进制流重新整合为二值化图片文件
def ImgAssemble_1(data):
    size = b""
    size_bytes = data[:64]
    for idx in range(0,8):
        byte = 0
        for i in range(0,8):
            byte = (byte<<1) + size_bytes[idx*8+i]
        size += chr(byte).encode()

    width,height = struct.unpack("i",size[:4])[0],struct.unpack("i",size[4:8])[0]
    
    img = Image.new("1",(width,height))
    img.putdata(data[64:])
    img.show()

    

src = Image.open("./Test/test.png").convert("1")
data = ImgDecompose_1(src)
ImgAssemble_1(data)
