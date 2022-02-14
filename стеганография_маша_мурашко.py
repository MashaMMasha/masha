from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import pathlib
from PIL import Image
from tkinter import Tk, Text, BOTH, W, N, E, S, messagebox, filedialog, NS


def clicked1():
    img_original = filedialog.askopenfilename()
    img_encrypted = filedialog.askopenfilename()
    decryption(img_original, img_encrypted)

def clicked2():
    messagebox.showinfo('Инструкция', 'Для того, чтобы поместить текст в изображение нажмите кнопку "Зашифровать текст" и прикрепите сначала текст, который вы хотите зашифровать, а потом изображение, в которе текст будет спрятан. В тексте могут использоваться маленькие и большие латинские буквы, основные знаки препинания, цифры. Если вы хотите получить зашифрованный текст, то нажмите на кнопку "Расшифровать текст" и прикрепите два изображения, исходное и зашифрованное. Текст будет выведен на экран')

def clicked():
    text_file = filedialog.askopenfilename()
    img_file = filedialog.askopenfilename()
    shifr(text_file, img_file)


def png_decryption(x, y):
    r, g, b, a = x
    r1, g1, b1, a1 = y
    count = 0
    count += abs(r - r1) + abs(g - g1) + abs(b - b1)
    k = abs(a - a1)
    if k == 1:
        count += 96
    elif k == 2:
        count += 64
    elif k == 3:
        count += 45
    elif k == 4:
        count = 44
    elif k == 5:
        count = 32
    elif k == 6:
        count = 33
    elif k == 7:
        count = 63
    elif k == 8:
        count += 48
    elif k == 9:
        count = 10
    return count


def jpg_decryption(x, y):
    r, g, b = x
    r1, g1, b1 = y
    count = abs(r - r1) + abs(g - g1) * 2
    k = abs(b - b1)
    if k == 2:
        count += 64
    elif k == 1:
        count += 96
    elif k == 3:
        count += 45
    elif k == 4:
        count = 44
    elif k == 5:
        count = 32
    elif k == 6:
        count = 33
    elif k == 7:
        count = 63
    elif k == 8:
        count += 48
    elif k == 9:
        count = 10
    return count


def f(x, z):
    if x + z <= 255:
        z += x
    else:
        z -= x
    return z


def jpg(i, pixel, text):
    r, g, b = pixel
    s = ord(text[i])
    if 97 <= s <= 122:
        s -= 96
        b = f(1, b)
    elif 65 <= s <= 90:
        s -= 64
        b = f(2, b)
    elif 48 <= s <= 57:
        s -= 48
        b = f(8, b)
    elif s == 33:
        s = 1
        b = f(6, b)
    elif s == 63:
        s = 1
        b = f(7, b)
    elif s == 46:
        s = 1
        b = f(3, b)
    elif s == 44:
        s = 1
        b = f(4, b)
    elif s == 32:
        s = 1
        b = f(5, b)
    elif s == 10:
        s = 1
        b = f(9, b)
    x = s // 3
    z = s - x - x
    r = f(z, r)
    g = f(x, g)
    return r, g, b


def png(i, pixel, text):
    r, g, b, a = pixel
    s = ord(text[i])
    if 97 <= s <= 122:
        s -= 96
        a = f(1, a)
    elif 65 <= s <= 90:
        s -= 64
        a = f(2, a)
    elif s == 46:
        s -= 45
        a = f(3, a)
    elif s == 44:
        s = 1
        a = f(4, a)
    elif s == 32:
        s = 1
        a = f(5, a)
    elif 48 <= s <= 57:
        s -= 64
        a = f(8, a)
    elif s == 33:
        s = 1
        a = f(6, a)
    elif s == 63:
        s = 1
        a = f(7, a)
    elif s == 10:
        s = 1
        a = f(9, a)
    x = s // 3
    y = (s - x) // 2
    z = s - x - y
    r = f(x, r)
    g = f(y, g)
    b = f(z, b)
    return r, g, b, a


def shifr(text_name, img):
    img_format = img[-3:]
    if img_format == 'png':
        image = Image.open(img).convert('RGBA')
    else:
        image = Image.open(img)
    text = open(text_name, 'r')
    lines = text.readlines()
    text = '\n'.join([line.strip() for line in lines])
    pix = list(image.getdata())
    for i, pixel in enumerate(pix):
        if i < len(text):
            if img_format == 'png':
                r, g, b, a = png(i, pixel, text)
                pix[i] = (r, g, b, a)
            else:
                r, g, b = jpg(i, pixel, text)
                pix[i] = (r, g, b)

        else:
            break
    image.putdata(pix)
    name_final_image = 'final_image.' + img_format
    image.save(name_final_image, 'PNG')
    image.putdata(pix)
    print('Зашифрованное изображение было сохранено на ваше устройство под именем final_image')
    window.destroy()



def decryption(Img_original_name, Img_result_name):
    img_original_format = Img_original_name[-3:]
    img_result_format = Img_result_name[-3:]
    if img_original_format == 'png':
        image_original = Image.open(Img_original_name).convert('RGBA')
        image_result = Image.open(Img_result_name).convert('RGBA')
    else:
        image_original = Image.open(Img_original_name)
        image_result = Image.open(Img_result_name)
    pix_original = list(image_original.getdata())
    pix_result = list(image_result.getdata())
    text = ''
    if img_original_format == 'png':
        for i in range(len(pix_original)):
            r, g, b, a = pix_original[i]
            r1, g1, b1, a1 = pix_result[i]
            if a1 != a:
                text += chr(png_decryption(pix_original[i], pix_result[i]))
            else:
                break
    else:
        for i in range(len(pix_original)):
            r, g, b = pix_original[i]
            r1, g1, b1 = pix_result[i]
            
            if b1 != b:
                text += chr(jpg_decryption(pix_original[i], pix_result[i]))
            else:
                break
    print(text)
    window.destroy()

if __name__ == "__main__":
    window = Tk()
    window.title("Стеганография")
    fontExample = tkFont.Font(family="Arial", size=19, weight="bold", slant="italic")
    window.geometry('365x275')
    PURPLE = '#f3e1f7'
    WHITE = '#fafafa'
    VIOLET = '#640573'
    window['background'] = PURPLE
    lbl = Label(window, text="   ")
    lbl.grid(column=0, row=0)
    btn = Button(window, text="Зашифровать текст!", font=fontExample, command=clicked)
    btn.grid(column=2, row=1, sticky=E+W+S+N+NS, pady=4, padx=5)
    btn1 = Button(window, text="Расшифровать текст!", font=fontExample, command=clicked1)
    btn1.grid(column=2, row=2, sticky=E+W+S+N+NS, pady=4, padx=5)
    btn2 = Button(window, text="Закрыть окно", font=fontExample, command=window.destroy)
    btn2.grid(column=2, row=4, sticky=E+W+S+N+NS, pady=4, padx=5)
    btn3 = Button(window, text="Инструкция", font=fontExample, command=clicked2)
    btn3.grid(column=2, row=3, sticky=E+W+S+N+NS, pady=4, padx=5)
    lbl['background'] = PURPLE
    btn['background'] = VIOLET
    btn['foreground'] = WHITE
    btn1['background'] = VIOLET
    btn1['foreground'] = WHITE
    btn2['background'] = VIOLET
    btn2['foreground'] = WHITE
    btn3['background'] = VIOLET
    btn3['foreground'] = WHITE
    window.mainloop()
