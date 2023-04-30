from PIL import Image
from enum import Enum
import io
from datetime import datetime
import sys
import os

STOP_CHARACTER = ">"

class Colour(Enum):
  RED = 0
  GREEN = 1
  BLUE = 2

def read(band):
  output = ""
  current_bit = ""
  bit_count = 0

  for colour in band:
    if colour % 2 == 0:
      current_bit += '0'
    else:
      current_bit += '1'

    bit_count += 1

    if bit_count == 8:
      bit_count = 0
      new_chr = chr(int(current_bit, 2))
      
      if new_chr != STOP_CHARACTER:
        output += new_chr
      else:
        break
      
      current_bit=""

  return output

def main(input_img, output_txt):
  startTime = datetime.now()

  print("Reading and converting image " + input_img)

  image = Image.open(input_img)
  rgb_image = image.convert('RGB')

  print("Splitting channels")
  r_band = list(rgb_image.getdata(Colour.RED.value))
  g_band = list(rgb_image.getdata(Colour.GREEN.value))
  b_band = list(rgb_image.getdata(Colour.BLUE.value))

  print("Reading RED channel")
  r_output = read(r_band)

  print("Reading GREEN channel")
  g_output = read(g_band)

  print("Reading BLUE channel")
  b_output = read(b_band)

  final_output = r_output + g_output + b_output

  print("Writing " +str(len(final_output)) + " characters to " + output_txt + " from image " + input_img)
  open(output_txt, 'w').close()
  with io.open(output_txt,"a+",encoding="utf-8") as f:
    f.write(final_output)
    f.close()

  print("Write complete. Outputted text is at " + output_txt + ". Took " + str(datetime.now() - startTime ))

if len(sys.argv)>1:

  if os.path.isfile(sys.argv[1]):
    main(sys.argv[1], "output.txt")
  else:
    print("Image path " + sys.argv[1]  + " cannot be located")


else:
  print("Image file must be passed as a command line argument (python3 readdemo.py puppy.png)")
