from PIL import Image
import string

def read(file):
    im = Image.open(file)
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
                new_chr = chr(int(current_bit,2))
                if new_chr.isalnum() or new_chr.isspace() or new_chr in string.punctuation:
                    print(new_chr,end="")
                else:
                    print()
                    return
                current_bit=""
    print()

def write(file,note):
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
                if(color[2]%2==0):
                    newimdata.append(color)
                else:
                    new_color = list(color)
                    if new_color[2] == 0:
                        new_color[2]+=1
                    else:
                        new_color[2]-=1
                    newimdata.append(tuple(new_color))
            else:
                if(color[2]%2!=0):
                    newimdata.append(color)
                else:
                    new_color = list(color)
                    new_color[2]-=1
                  
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

note = "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo."    
write("water.png", note)
read("write.png")

        
