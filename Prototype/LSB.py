import struct
import sys
import random
from PIL import Image

from converter import Converter
from crypter import XorImgCrypter


def SetBit(var, num, value):
	mask = 1 << num
	var &= ~mask
	if value:
		var |= mask
	return var

def Embed(imgFile,payload):
    src_img = Image.open(imgFile).convert("RGBA")
    width,height = src_img.size

    max_size = width*height*3.0/1024
    print ("[*] Input image size: %dx%d pixels." % (width, height))
    print ("[*] Usable payload size: %.2f KB." % (max_size))

    while(len(payload)%3):
        payload.append(0)
    payload_size = len(payload)/1024.0
    print ("[+] Payload size: %.3f KB " % payload_size)

    if (payload_size > max_size - 4):
        print("[-] Cannot embed. File too large")
        sys.exit()

    steg_img = Image.new('RGBA',(width,height))


    index = 0
    for h in range(height):
        for w in range(width):
            (r,g,b,a) = src_img.getpixel((w,h))
            if index < len(payload):
                r = SetBit(r,0,payload[index])
                g = SetBit(g,0,payload[index+1])
                b = SetBit(b,0,payload[index+2])
            else:
                r = SetBit(r,0,random.randint(0,1))
                g = SetBit(g,0,random.randint(0,1))
                b = SetBit(b,0,random.randint(0,1))
            steg_img.putpixel((w,h),(r,g,b,a))
            index += 3

    print ("[+] Embedded successfully!")
    return steg_img

def Extract(imgFile):
    src_img = Image.open(imgFile).convert("RGBA")
    width,height = src_img.size
    print ("[*] Input image size: %dx%d pixels." % (width, height))

    data = []
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = src_img.getpixel((w, h))
            data.append(r & 1)
            data.append(g & 1)
            data.append(b & 1)
    return data




converter = Converter()
crypter = XorImgCrypter()
with open("./Test/滕王阁序.txt","r",encoding="utf-8") as file:
    text = file.readline()

srcimg = converter.Text2Pic(text,768,1024,24)
srcimg.save("./Test/test.png")

cryimg = crypter.ImgEncrypt(srcimg,1024)
cryimg.save("./Test/crypt.png")

data = converter.ImgDecompose_1(srcimg)

steg_img = Embed("./Test/avatar.png",data)
steg_img.save("./Test/avatar-stego.png", "PNG")

extdata = Extract("./Test/avatar-stego.png")
extimg = converter.ImgAssemble_1(extdata)
extimg.save("./Test/avatar-extract.png")

