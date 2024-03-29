from PIL import Image
from enum import Enum
import io
import sys
import os

STOP_CHARACTER = ">"

class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2



def read(path,note_path,channel):

    print("Reading channel " + str(channel) +". (0=Red,1=Green,2=Blue)")

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
    
    print("Writing " +str(len(output)) + " characters to " + note_path + " from image " + path)

    with io.open(note_path,"a+",encoding="utf-8") as f:
        f.write(output)
        f.close()


output = "output.txt"


if len(sys.argv)>1:

  if os.path.isfile(sys.argv[1]):
    open(output, 'w').close()
    input_image = sys.argv[1]

    read(input_image,output,Colour.RED.value)
    read(input_image,output,Colour.GREEN.value)
    read(input_image,output,Colour.BLUE.value)

    print("Write complete. Outputted text is at " + output)
  else:
    print('Image path "' + sys.argv[1]  + '" cannot be located')

  
 


else:
  print("Image file must be passed as a command line argument (python3 readdemo.py puppy.png)")



