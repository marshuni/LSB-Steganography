import numpy as np
from PIL import Image,ImageChops


def ImgEncrypt(img_src,seed):
    img = img_src.convert("1")
    img_arr = np.array(img)
    w,h = img_arr.shape

    np.random.seed(seed)
    key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
    Image.fromarray(key).show()
    keyimg = Image.fromarray(key).convert("1")

    img_encrypt = ImageChops.logical_xor(img,keyimg)
    return img_encrypt

def ImgDecrypt(img_encrypt,seed):
    img_encrypt = img_encrypt.convert("1")
    img_arr = np.array(img_encrypt)
    w,h = img_arr.shape

    np.random.seed(seed)
    key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
    keyimg = Image.fromarray(key).convert("1")

    img_decrypt = ImageChops.logical_xor(img_encrypt,keyimg)
    return img_decrypt


img_path = r"./test.png"
img = Image.open(img_path).convert("1")

img_encrypt = ImgEncrypt(img,1024)
img_encrypt.show()
img_encrypt.save("encrypt.png")

img_decrypt = ImgDecrypt(img_encrypt,1024)
img_decrypt.show()
