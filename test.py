from PIL import Image,ImageChops

from crypt import XorImgCrypter
from text2pic import Converter

text = "你好世界"
converter = Converter()
crypter = XorImgCrypter()

srcimg = converter.Text2Pic(text,36,36,12)
srcimg.save("./Test/test.png")

cryimg = crypter.ImgEncrypt(srcimg,1024)
cryimg.save("./Test/crypt.png")


