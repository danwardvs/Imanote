from PIL import Image
from enum import Enum
import math
import io

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
                current_bit+='0'
            else:
                current_bit+='1'
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
    
    with io.open(note_path,"a+",encoding="utf-8") as f:
        f.write(output)
        f.close()
    

def write_data(input_path,output_path,note,channel):
    
    new_image_data = []
   
    input_image = Image.open(input_path)
   
    ascii_note = list(bytes(note,"utf-8"))

    bit_location = 0
    byte = 0

    for pixel in input_image.getdata():
        
        if byte<len(ascii_note):
            char = format(ascii_note[byte],"08b")
            new_bit = char[bit_location]
           
            if( (new_bit=="0" and pixel[channel]%2==0) or (new_bit=="1" and pixel[channel]%2!=0)):
                new_image_data.append(pixel)
            else:
                new_colour = list(pixel)
                if new_colour[channel] == 0:
                    new_colour[channel]+=1
                else:
                    new_colour[channel]-=1
                new_image_data.append(tuple(new_colour))

        else:
            new_image_data.append(pixel)
        
        bit_location+=1
        if bit_location==8:
            byte+=1
            bit_location=0
        
 
    new_image = Image.new(input_image.mode,input_image.size)
    new_image.putdata(new_image_data)

    new_image.save(output_path)

def clean(note):

    pairs = [["“","\""],["”","\""],["’","'"],["—","-"]]

    for pair in pairs:
        note=note.replace(pair[0],pair[1])
    return note


def split_note(note,add_stop_char):

    ADD_STOP_CHAR = STOP_CHARACTER if add_stop_char else ""

    note = clean(note)
  
    note_length = math.floor(len(note)/3)
    
    return [note[0:note_length]+ADD_STOP_CHAR,note[note_length:note_length*2]+ADD_STOP_CHAR,note[note_length*2:len(note)]+ADD_STOP_CHAR] 


def write(input_text_path,input_image_path,output_image_path):

    f = open(input_text_path, "r")
    note = f.read()
    
    correct_size = check_size(note,input_image_path)

    if correct_size:

        note_split = split_note(note,True)

        print("Writing red channel to "+ output_image_path)
        write_data(input_image_path,output_image_path, note_split[0],Colour.RED.value)
        
        print("Writing green channel to "+ output_image_path)
        write_data(output_image_path,output_image_path, note_split[1],Colour.GREEN.value)
        
        print("Writing blue channel to "+ output_image_path)
        write_data(output_image_path,output_image_path, note_split[2],Colour.BLUE.value)
    else:
        print("Image is too small to contain the text")
    
    return correct_size

def read(input_path,output_path):

    open(output_path, 'w').close()
    read_data(input_path,output_path,Colour.RED.value)
    read_data(input_path,output_path,Colour.GREEN.value)
    read_data(input_path,output_path,Colour.BLUE.value)


def check_size(note,input_image_path):

    im = Image.open(input_image_path)
    width,height = im.size

    print("Text is " +str(len(note)) + " characters long. The image is " + str(width) +"*" + str(height) + " and can contain "+ str(int(width*height*3/8)) + " characters.")

    return (len(note)*8)/3 <= width*height

input_image = "puppy.png"
input_text = "demo/orwell.txt"

output_image = "puppy.png"
output_text = "o.txt"

if write(input_text,input_image,output_image):
    read(output_image,output_text)

