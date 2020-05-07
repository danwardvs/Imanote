from PIL import Image
from enum import Enum
import string

class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def pixels(path,channel):
    im = Image.open(path)
    rgb_im = im.convert('RGB')
    width,height = rgb_im.size

    current_bit = ""
    bit_count = 0
    for i in range(0,width):
        for j in range(0,height):
            pixel = list(rgb_im.getpixel((j, i)))

            if pixel[channel] % 2 == 0:
                print('1',end='')
            else:
                print('0',end='')
        print()


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
    

def write(file,note,channel):
    im = Image.open(file)

    newimdata = []
   
    bit_location=0
    ascii_note = list(bytes(note,"utf-8"))

    byte=0
    for color in im.getdata():
        
        if byte<len(ascii_note):
            char = format(ascii_note[byte],"08b")
            new_bit = char[bit_location]
            if new_bit=="1":
                if(color[channel]%2==0):
                    newimdata.append(color)
                else:
                    new_color = list(color)
                    if new_color[channel] == 0:
                        new_color[channel]+=1
                    else:
                        new_color[channel]-=1
                    newimdata.append(tuple(new_color))
            else:
                if(color[channel]%2!=0):
                    newimdata.append(color)
                else:
                    new_color = list(color)
                    new_color[channel]-=1
                  
                    newimdata.append(tuple(new_color))

        else:
            newimdata.append(color)
        
        bit_location+=1
        if bit_location==8:
            byte+=1
            bit_location=0
        
 
    newim = Image.new(im.mode,im.size)
    newim.putdata(newimdata)

    newim.save("write.png")



f = open("p_1.txt", "r")
note = f.read()
write("house_s.png", note,Colour.RED.value)

f = open("p_2.txt", "r")
note = f.read()
write("write.png", note,Colour.GREEN.value)
f = open("p_3.txt", "r")
note = f.read()
write("write.png", note,Colour.BLUE.value)



output = "output.txt"
open('output.txt', 'w').close()
#pixels("write.png",Colour.RED.value)
read("write.png",output,Colour.RED.value)
read("write.png",output,Colour.GREEN.value)
read("write.png",output,Colour.BLUE.value)


        
