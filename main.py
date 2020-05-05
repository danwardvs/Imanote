from PIL import Image

def read(file):
    im = Image.open("test.png")
    rgb_im = im.convert('RGB')
    width,height = rgb_im.size

    chars = []
    current_bit = ""
    bit_count = 0
    for i in range(0,width):
        for j in range(0,height):
            r, g, b = rgb_im.getpixel((j, i))

            if b % 2 == 0:
                current_bit+='1'
            else:
                current_bit+='0'
            bit_count+=1
            if bit_count == 8:
                bit_count = 0
                print(chr(int(current_bit,2)),end="")
                current_bit=""
    print()

def write(file,note):
    im = Image.open(file)

    newimdata = []
   
    bit_location=0
    ascii_note = list(bytes(note,"utf-8"))
    for i in ascii_note:
        print(format(i, "08b"))
    for color in im.getdata():
        
        newimdata.append( color )
 
    newim = Image.new(im.mode,im.size)
    newim.putdata(newimdata)

    newim.save("write.png")
write("water.png", "Allan is a big butt!")
read("test.png")

        
