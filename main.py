from PIL import Image
from enum import Enum
import math

STOP_CHARACTER = ">"

class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def read_data(path,note_path,channel):

    output = ""

    im = Image.open(path)
    rgb_im = im.convert('RGB')
    width,height = rgb_im.size
    current_bit = ""
    bit_count = 0
    for i in range(0,height):
        stop_char=False
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
            
                if new_chr != STOP_CHARACTER:
                    output+=new_chr
                else:
                    stop_char = True
                    break
                
                current_bit=""
        if stop_char:
            break
    
    file1 = open(note_path,"a+")                 
    file1.write(output)
    file1.close()
    

def write_data(input_path,output_path,note,channel):
    im = Image.open(input_path)

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

    newim.save(output_path)

def unicode_to_ascii(text):

    pairs = [["“","\""],["”","\""],["’","'"],["—","-"]]

    for pair in pairs:
        text=text.replace(pair[0],pair[1])
    return text


def split_text(text):

    text = unicode_to_ascii(text)

    text_length = math.floor(len(text)/3)

    return [text[0:text_length]+STOP_CHARACTER,text[text_length:text_length*2]+STOP_CHARACTER,text[text_length*2:-1]+STOP_CHARACTER] 


def write(input_text_path,input_image_path,output_image_path):

    f = open(input_text_path, "r")
    note = f.read()
    note_split = split_text(note)
    print("bum")
    print(len(note_split[0]))
    print(len(note_split[1]))
    print(len(note_split[2]))

    write_data(input_image_path,output_image_path, note_split[0],Colour.RED.value)

    write_data(output_image_path,output_image_path, note_split[1],Colour.GREEN.value)

    write_data(output_image_path,output_image_path, note_split[2],Colour.BLUE.value)

def read(input_path,output_path):


    open(output_path, 'w').close()
    read_data(input_path,output_path,Colour.RED.value)
    read_data(input_path,output_path,Colour.GREEN.value)
    read_data(input_path,output_path,Colour.BLUE.value)


        
write("pride_raw.txt","house_s.png","newWrite.png")
read("newWrite.png","newOutput.txt")