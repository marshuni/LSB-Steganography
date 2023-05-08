import struct
import sys
from PIL import Image, ImageFont, ImageDraw

class Converter:
    def TextSplit(self,text, length):
        return [text[i:i+length] for i in range(0, len(text), length)]

    def Text2Pic(self,raw,width,height) -> Image:
        sections = raw.split(sep='\n')
        text = ""
        margin = 10 if width>64 else 2

        size = 14
        for siz in [8,9,10,12,14,16,20,22,24,26,28,36,48,72,144]:
            column = (width-margin*2)/siz
            line = len(raw)/column + len(sections)
            if line*(siz+4)<height:
                size = siz

        for section in sections:
            for line in self.TextSplit(section,int((width-margin*2)/size)):
                text += line+'\n'
        
        image = Image.new("L", (width, height),255)
        draw = ImageDraw.Draw(image)
        # Available Font：Simsun.ttc / YaHeiConsolas.ttf
        # Put your own font file into ./Fonts/ 
        font = ImageFont.truetype("./Fonts/Simsun.ttc", size)

        draw.multiline_text((margin, margin/2), text, font=font, fill="#000000",spacing=4)
        return image
    
    def ImgDecompose(self,img,mode):
        data = []
        bytes = []
        for arg in img.size:
            bytes += [b for b in struct.pack("i",arg)]
        if mode == "L":
            bytes += [b for b in img.convert("L").getdata()]
        for b in bytes:
            for i in range(7,-1,-1):
                data.append((b >> i) & 0x1)
        if mode == "1":
            data += [int(bool(b)) for b in img.convert("1").getdata()]
        return data

    def ImgAssemble(self,data,mode):
        size = b""
        size_bytes = data[:64]
        
        for idx in range(0,8):
            byte = 0
            for i in range(0,8):
                byte = (byte<<1) + size_bytes[idx*8+i]
            # encode()函数在使用默认unicode编码时可能会产生额外的字符'\xc2'，需要改换编码
            size = size + chr(byte).encode('latin-1')
        width,height = struct.unpack("i",size[:4])[0],struct.unpack("i",size[4:8])[0]

        if width>8192 or height>8192:
            print("[-] Fatal error: File corrupted.")
            sys.exit()
        img = Image.new("L",(width,height))

        if mode == "L":
            img_bytes = data[64:(width*height)*8+64]
            imgdata = []
            for idx in range(0,int(len(img_bytes)/8)):
                byte = 0
                for i in range(0,8):
                    byte = (byte<<1) + img_bytes[idx*8+i]
                imgdata.append(byte)
            img.putdata(imgdata)
        elif mode == "1":
            img = img.convert("1")
            img.putdata(data[64:width*height+64])
            
        return img


