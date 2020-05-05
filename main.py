from PIL import Image
im = Image.open("test.png")
rgb_im = im.convert('RGB')
width,height = rgb_im.size

chars = []
current_bit = ""
bit_count = 0
for i in range(0,width):
    for j in range(0,height):
        r, g, b = rgb_im.getpixel((i, j))
        if b % 2 == 0:
            current_bit+='1'
        else:
            current_bit+='0'
        bit_count+=1
        if bit_count == 7:
            bit_count = 0
            print(current_bit)
            current_bit=""

        
