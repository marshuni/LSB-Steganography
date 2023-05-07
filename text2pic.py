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

