from PIL import Image
from enum import Enum

class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def read(path,note_path,channel):

    output = ""

    im = Image.open(path)
    rgb_im = im.convert('RGB')
    width,height = rgb_im.size
    print(width,height)
    current_bit = ""
    bit_count = 0
    for i in range(0,height):
        for j in range(0,width):
            pixel = list(rgb_im.getpixel((j, i)))

            if pixel[channel] % 2 == 0:
                current_bit+='1'
            else:
                current_bit+='0'
            bit_count+=1
            if bit_count == 8:
                bit_count = 0
                new_chr = chr(int(current_bit,2))
            
                if new_chr != ">":
                    output+=new_chr
                else:
                    file1 = open(note_path,"a+")                 
                    file1.write(output)
                    file1.close()
                    print("hit stop character")
                    return
                current_bit=""

    file1 = open(note_path,"a+")                 
    file1.write(output)
    file1.close()

output = "output.txt"
open('output.txt', 'w').close()
#pixels("write.png",Colour.RED.value)
read("Example.png",output,Colour.RED.value)
read("Example.png",output,Colour.GREEN.value)
read("Example.png",output,Colour.BLUE.value)