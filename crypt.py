import numpy as np
from PIL import Image,ImageChops

class XorImgCrypter:
    def ImgEncrypt(self,img_src,seed):
        img = img_src.convert("1")
        img_arr = np.array(img)
        w,h = img_arr.shape

        np.random.seed(seed)
        key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
        keyimg = Image.fromarray(key).convert("1")

        img_encrypt = ImageChops.logical_xor(img,keyimg)
        return img_encrypt

    def ImgDecrypt(self,img_encrypt,seed):
        img_encrypt = img_encrypt.convert("1")
        img_arr = np.array(img_encrypt)
        w,h = img_arr.shape

        np.random.seed(seed)
        key=np.random.randint(0,256,size=[w,h],dtype=np.uint8)
        keyimg = Image.fromarray(key).convert("1")

        img_decrypt = ImageChops.logical_xor(img_encrypt,keyimg)
        return img_decrypt