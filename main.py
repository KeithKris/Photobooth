from PIL import Image

palette = [
        255, 255, 255, #white
        0, 255, 255, #cyan
        255, 0, 255, #magenta
        255, 255, 0, #yellow
        0, 0, 0, #black
    ]

# Repeat the initial palette to create a full 8-bit (256 colors) palette
full_palette = palette * (256 // len(palette))

print_resolution=(720,576)

def main():
    # Open the image file
    image = Image.open("in.jpg")
    output = dither_and_resize(image, full_palette, print_resolution)

def dither_and_resize(image, palette, resolution):
    p_img = Image.new('P', (512, 512))
    p_img.putpalette(full_palette)

    conv = image.quantize(palette=p_img)

    return conv.resize(print_resolution).convert('RGB')

if __name__ == '__main__':
    main()