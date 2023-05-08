import numpy as np
from PIL import Image,ImageChops

class XorImgCrypter:
    def ImgEncrypt(self,img,seed,mode):
        img_src = img.convert(mode)
        img_arr = np.array(img_src)
        w,h = img_arr.shape

        np.random.seed(seed)
        key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
        if mode=='L':
            encrypt_arr = np.bitwise_xor(img_arr,key)
            encrypt_img = Image.fromarray(encrypt_arr,'L')
        else:
            keyimg = Image.fromarray(key).convert("1")
            encrypt_img = ImageChops.logical_xor(img_src,keyimg)
        return encrypt_img

    def ImgDecrypt(self,img_encrypt,seed,mode):
        img_encrypt = img_encrypt.convert(mode)
        img_arr = np.array(img_encrypt)
        w,h = img_arr.shape

        np.random.seed(seed)
        key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
        if mode=='L':
            plain_arr = np.bitwise_xor(img_arr,key)
            plain_img = Image.fromarray(plain_arr,'L')
        else:
            keyimg = Image.fromarray(key).convert("1")
            plain_img = ImageChops.logical_xor(img_encrypt,keyimg)
        return plain_img