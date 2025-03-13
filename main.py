from PIL import Image
from imagewriter import Imagewriter

palette = [
        255, 255, 255, #white
        0, 255, 255, #cyan
        255, 0, 255, #magenta
        255, 255, 0, #yellow
        255, 0, 0, #red
        0, 255, 0, #green
        0, 0, 0, #black
    ]

# Repeat the initial palette to create a full 8-bit (256 colors) palette
full_palette = palette * (256 // len(palette))

print_resolution=(720,576)

IW = Imagewriter()

def main():
    # Open the image file
    image = Image.open("in.jpg")
    output = dither_and_resize(image, full_palette, print_resolution)
    output.save("out.png")
    printer_bytes = IW.print_image(output)
    
    with open("printdata.bin", "wb") as file:
        file.write(printer_bytes)
    

def dither_and_resize(image, palette, resolution):
    p_img = Image.new('P', (512, 512))
    p_img.putpalette(full_palette)

    return image.resize(print_resolution).quantize(palette=p_img).convert('RGB')

    #return conv.resize(print_resolution).convert('RGB')

if __name__ == '__main__':
    main()