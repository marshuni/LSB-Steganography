import numpy as np
from PIL import Image,ImageChops

# 使用种子随机生成一个和图像结构一致的随机数组，并将两者进行异或以加密
# 由于PIL库的局限性，进行异或操作的图像必须是二值化图像，不能够进行按位异或。
# 或许可以先在numpy的array形式下异或完再转换成图像？

def ImgEncrypt_xor_1(img_src,seed):
    img = img_src.convert("1")
    img_arr = np.array(img)
    w,h = img_arr.shape

    np.random.seed(seed)
    key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
    keyimg = Image.fromarray(key).convert("1")

    img_encrypt = ImageChops.logical_xor(img,keyimg)
    return img_encrypt

# 使用同样的种子可以对加密的图像解密
def ImgDecrypt_xor_1(img_encrypt,seed):
    img_encrypt = img_encrypt.convert("1")
    img_arr = np.array(img_encrypt)
    w,h = img_arr.shape

    np.random.seed(seed)
    key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
    keyimg = Image.fromarray(key).convert("1")

    img_decrypt = ImageChops.logical_xor(img_encrypt,keyimg)
    return img_decrypt




img_path = r"./Test/txt2pic.png"
img = Image.open(img_path).convert("1")

img_encrypt = ImgEncrypt_xor_1(img,1024)
img_encrypt.save("./Test/XorEncrypt_1.png")

img_decrypt = ImgDecrypt_xor_1(img_encrypt,1024)
img_decrypt.save("./Test/XorDecrypt_1.png")
