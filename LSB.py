import sys
import random
from PIL import Image

class LSBSteganoser:
    def SetBit(self,var, num, value):
        mask = 1 << num
        var &= ~mask
        if value:
            var |= mask
        return var
    def Embed(self,src_img,payload):
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
                    r = self.SetBit(r,0,payload[index])
                    g = self.SetBit(g,0,payload[index+1])
                    b = self.SetBit(b,0,payload[index+2])
                else:
                    r = self.SetBit(r,0,random.randint(0,1))
                    g = self.SetBit(g,0,random.randint(0,1))
                    b = self.SetBit(b,0,random.randint(0,1))
                steg_img.putpixel((w,h),(r,g,b,a))
                index += 3

        print ("[+] Embedded successfully!")
        return steg_img
    
    def Extract(self,src_img):
        width,height = src_img.size
        print ("[*] Input image size: %dx%d pixels." % (width, height))

        data = []
        for h in range(height):
            for w in range(width):
                (r, g, b, a) = src_img.getpixel((w, h))
                data.append(r & 1)
                data.append(g & 1)
                data.append(b & 1)
        print ("[+] Extracted successfully!")
        return data
