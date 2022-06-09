import pytesseract
from PIL import Image

def img_binarization(image,threshold):
    image = image.convert('L')
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image

def img_noise_reduct(image):
    data = image.getdata()
    w,h = image.size
    count = 0
    for x in range(1,h-1):
        for y in range(1,h-1):
            mid_pixel = data[w*y+x]
            if mid_pixel == 0:
                top_piexl = data[w*(y-1)+x]
                left_piexl = data[w*y+(x-1)]
                right_piexl = data[w*y+(x+1)]
                down_pixel = data[w*(y+1)+x]

                if top_piexl ==0:
                    count += 1
                if left_piexl ==0:
                    count+= 1
                if down_pixel == 0:
                    count += 1
                if right_piexl == 0:
                    count += 1
                if count > 4:
                    image.putpixel((x,y),0)
    return image

def identifyString(image):
    return pytesseract.image_to_string(image)

def main():
    captcha = Image.open('c:\\Users\\David\\Desktop\\testImg4.png')
    captcha.show()
    newImage1 = img_binarization(captcha,150)
    newImage1.show()
    newImage2 = img_noise_reduct(newImage1)
    newImage2.show()
    print(identifyString(newImage2))

if __name__ == '__main__':
    main()