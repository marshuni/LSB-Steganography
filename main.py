import sys
import os

from PIL import Image
from converter import Converter
from crypter import XorImgCrypter
from LSB import LSBSteganoser

def hide(img_file,payload_file,mode,seed):
    carrier_img = Image.open(img_file).convert("RGBA")
    width,height = carrier_img.size
    steg_path = os.path.splitext(img_file)[0] + '-steg-' + mode + '.png'
    if mode=='binary':
        mode = '1'
    elif mode=='gray':
        mode = 'L'
    seed = int(seed)

    # Prepare the payload image
    payload_ext = os.path.splitext(payload_file)[1][1:]
    if payload_ext == 'txt':
        with open(payload_file,"r",encoding="utf-8") as payload:
            payload_text = payload.read()
        pwidth = width  if mode == "1" else int(width/3.1)
        pheight = height
        payload_img = Converter().Text2Pic(payload_text,pwidth,pheight)
    elif payload_ext == 'png':
        payload_img = Image.open(payload_file).convert(mode)
    else:
        print("[-] Unsupported payload file format. Try .png or .txt file.")
        sys.exit()

    print("[*] Please preview the payload image and then close tha window.")
    payload_img.show()
    payload_encrypt = XorImgCrypter().ImgEncrypt(payload_img,seed,mode)
    payload_data = Converter().ImgDecompose(payload_encrypt,mode)
    steg_img = LSBSteganoser().Embed(carrier_img,payload_data)
    steg_img.save(steg_path)

def extract(steg_file,output_file,mode,seed):
    if mode=='binary':
        mode = '1'
    elif mode=='gray':
        mode = 'L'
    seed = int(seed)
    steg_img = Image.open(steg_file).convert("RGBA")
    payload_data = LSBSteganoser().Extract(steg_img)
    payload_encrypt = Converter().ImgAssemble(payload_data,mode)
    payload_img = XorImgCrypter().ImgDecrypt(payload_encrypt,seed,mode)

    payload_img.save(output_file)

def check():
    arg = 6
    if sys.argv[4]!="gray" and sys.argv[4]!="binary":
        print("[-] Invalid mode.")
        sys.exit()
    try:
        int(sys.argv[5])
    except:
        print("[-] Invalid seed.")
        sys.exit()
    if len(sys.argv)<6:
        print("[-] Too few arguments provided. Please check your input.")
        sys.exit()
    elif len(sys.argv)>6:
        print("[-] Too many arguments provided. Please check your input.")
        sys.exit()

    img_ext = os.path.splitext(sys.argv[2])[1][1:]
    if img_ext != 'png' and img_ext != 'bmp':
        print("[-] Unsupported carrier image file.")
        sys.exit()
   
def usage(ScriptName):
    print("LSB 隐写工具：可使用该脚本将文本或图片(灰度)藏入载体图像的最低位。脚本用法详见中文文档。")
    print("-------------------")
    print("LSB steganogprahy. You can hide texts or small pics(gray-scale) within least significant bits of images.\n")

    print("Usage:")
    print("  %s hide <img_file> <payload_file> <mode> <seed>" % ScriptName)
    print("  %s extract <stego_file> <output_file> <mode> <seed>\n" % ScriptName)

    print("<mode>: binary | gray")
    print("<seed>: An integer used for shuffling information. The same one needed when restoring the information.")
    print("<output_file>: A .png file.")

    sys.exit()

if __name__ == "__main__":
    if len(sys.argv)<2 or sys.argv[1]=="help":
        usage(sys.argv[0])
    elif sys.argv[1]=="hide":
        check()
        hide(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    elif sys.argv[1]=="extract":
        check()
        extract(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        print("Invalid Command. Use \"%s help\" for help." % sys.argv[0])
    