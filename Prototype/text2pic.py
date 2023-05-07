from PIL import Image, ImageFont, ImageDraw

def TextSplit(text, length):
    return [text[i:i+length] for i in range(0, len(text), length)]

def Text2Pic(raw,width,height,size) -> Image:

    sections = raw.split(sep='\n')
    text = ""
    margin = 10 if width>64 else 2
    for section in sections:
        for line in TextSplit(section,int((width-margin*2)/size)):
            text += line+'\n'
    
    image = Image.new("1", (width, height), 1)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./YaHeiConsolas.ttf", size)

    draw.multiline_text((margin, margin/2), text, font=font, fill="#000000")
    return image

text = u"　　These is a sample text.\n这几天心里颇不宁静。今晚在院子里坐着乘凉，忽然想起日日走过的荷塘，在这满月的光里，总该另有一番样子吧。\n　　月亮渐渐地升高了，墙外马路上孩子们的欢笑，已经听不见了；妻在屋里拍着闰儿，迷迷糊糊地哼着眠歌。"
img = Text2Pic(text,512,512,36)
img.save("./Test/txt2pic.png")

