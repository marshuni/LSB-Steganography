import struct
from PIL import Image, ImageFont, ImageDraw

class Converter:
    def TextSplit(self,text, length):
        return [text[i:i+length] for i in range(0, len(text), length)]

    def Text2Pic(self,raw,width,height,size) -> Image:
        sections = raw.split(sep='\n')
        text = ""
        margin = 10 if width>64 else 2
        for section in sections:
            for line in self.TextSplit(section,int((width-margin*2)/size)):
                text += line+'\n'
        
        image = Image.new("1", (width, height), 1)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./YaHeiConsolas.ttf", size)

        draw.multiline_text((margin, margin/2), text, font=font, fill="#000000")
        return image
    
    def ImgDecompose_1(self,img):
        data = []
        size = []
        for arg in img.size:
            size += [b for b in struct.pack("i",arg)]
        for b in size:
            for i in range(7,-1,-1):
                data.append((b >> i) & 0x1)

        data += [int(bool(b)) for b in img.convert("1").getdata()]

        return data

    def ImgAssemble_1(self,data):
        size = b""
        size_bytes = data[:64]
        for idx in range(0,8):
            byte = 0
            for i in range(0,8):
                byte = (byte<<1) + size_bytes[idx*8+i]
            size += chr(byte).encode()

        width,height = struct.unpack("i",size[:4])[0],struct.unpack("i",size[4:8])[0]
        
        img = Image.new("1",(width,height))
        img.putdata(data[64:width*height-64])
        return img


