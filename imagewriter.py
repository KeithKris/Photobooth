from PIL import Image

class Imagewriter:
    RESET = bytes([27,99])
    BLACK = bytes([27, 75, 48])
    YELLOW = bytes ([27, 75, 49])
    MAGENTA = bytes ([27, 75, 50])
    CYAN = bytes ([27, 75, 51])
    GRAPHIC_START = bytes ([27, 71])
    CPI9 = bytes ([27, 110])
    LINE_FEED_PITCH_16 = bytes ([27, 84, ord('1'), ord('6')])
    CR = bytes([13])
    LF = bytes([10])
    
    def print_bytes(self, color, bytes_to_print):
        return_bytes = bytearray(color + self.GRAPHIC_START + bytes(str(len(bytes_to_print)), encoding="utf-8") + bytes_to_print)
        return(return_bytes)
        
    def is_print_color(self, rgb, target_color):
        if (rgb == (0, 255, 255) and target_color == self.CYAN):
            return True
        if (rgb == (0, 0, 0) and target_color == self.BLACK):
            return True
        if (rgb == (255, 0, 255) and target_color == self.MAGENTA):
            return True
        if (rgb == (255, 255, 0) and target_color == self.YELLOW):
            return True
        if (rgb == (255, 0, 0) and ((target_color == self.YELLOW) or (target_color == self.MAGENTA))):
            return True
        if (rgb == (0, 255, 0) and ((target_color == self.YELLOW) or (target_color == self.CYAN))):
            return True
            
        return False
            
        
    
        
    def get_bytes_for_band(self, color, image, band):
        return_bytes = bytearray()
        for strip in reversed(range(0, image.height)):
            byte_value = 0
            dec_value = 0
            for pixel in range(0, 8):
                #print (f"{(band*8)+pixel} x {strip}")
                if self.is_print_color(image.getpixel((band*8+pixel, strip)), color):
                    dec_value = dec_value + (2 ** pixel)
                byte_value = bin(dec_value)   
            return_bytes.append(dec_value)   
        return return_bytes

    def append_graphics(self, target, graphic_bytes, color):
        num_bytes = len(graphic_bytes)
        target.extend(color)
        target.extend(self.GRAPHIC_START)
        target.extend(f"{num_bytes:04}".encode())
        target.extend(graphic_bytes)
        target.extend(self.CR)
        return target
    
    def print_image(self, image):
        if (not image.size == (720, 576)):
            raise TypeError("Bad resolution. This method only supports 720x576 images")
            
        return_bytes=bytearray(self.RESET)
        return_bytes.extend(self.CPI9)
        return_bytes.extend(self.LINE_FEED_PITCH_16)

        for band in range(0, (image.width//8)):
            
            #print (f"band {band}")
            for color in (self.YELLOW, self.CYAN, self.MAGENTA, self.BLACK):
                graphic_bytes = self.get_bytes_for_band(color, image, band)
                return_bytes = self.append_graphics(return_bytes, graphic_bytes, color)
                
            return_bytes.extend(self.LF)

        return(return_bytes)

