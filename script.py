# Максимум морщинников 12, они спавнятся с шансом 0.001% каждый кадр

## Пока умеет только скринить игру и видель красный у морщинников

import cv2
import numpy as np
import mss
import pyautogui
import time
import sys
from pynput import keyboard

running = True
sct = mss.mss()
# Область с печенькой по коордам
cookie_top = 30
cookie_left = 0
cookie_width = 575
cookie_height = 825
# Область с печенькой    
mon = {"top": cookie_top, "left": cookie_left, 
        "width": cookie_width, "height": cookie_height}

def on_press(key):
    global running
    try:
        if key.char == 'q': 
            print("Клавиша 'q' нажата. Останавливаю скрипт...")
            running = False
            return False 
    except AttributeError:
        pass

def click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()


def c_vision(img, morshinnik):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # morshinnik = morshinnik / 0.25
    center_morshinnik = [(morshinnik[0].start+morshinnik[0].stop)/2, 
                         (morshinnik[1].start+morshinnik[1].stop)/2]

    lower_red = np.array([5,150,0])
    upper_red = np.array([7,210,200])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    cv2.imshow('Image', img)
    # cv2.imshow('Mask', mask)
    # print(center_morshinnik[0],center_morshinnik[1])
    # print(np.sum(mask[morshinnik]))

    # if np.sum(mask[morshinnik]) >= 1000000:
    #     pyautogui.moveTo(center_morshinnik[1],center_morshinnik[0], 0.01)
        # click()
        # click()
        # click()

def get_morshinnik_coords():

    img = np.asarray(sct.grab(mon))
    
    img_height, img_weight = img.shape[:2]

    center_x = img_weight // 2
    center_y = (cookie_height-cookie_top) // 2  

    # Морщинники
    morshinnik1 = (slice(80,270),slice(200,360))

    cv2.line(img, (center_x, 0), (center_x, cookie_height), (0, 255, 0), 2)
    cv2.line(img, (0, center_y), (img_weight, center_y), (0, 255, 0), 2)
    
    cv2.imshow('Image', img)

    print(center_x, center_y)

def get_screenshot():
    # Морщинники
    morshinnik1 = (slice(80,270),slice(200,360))
    # ^^^^^^ Центр сверху ^^^^^^ 
    morshinnik2 = (slice((int)(120+120*0.25),
                         (int)(290+290*0.25)),
                         slice((int)(80+80*0.25),
                               (int)(240+240*0.25))) 
    morshinnik3 = (slice(200,370),slice(0,160)) 
    morshinnik4 = (slice(330,500),slice(0,160)) 
    morshinnik5 = (slice(450,630),slice(0,160)) 
    morshinnik6 = (slice(550,720),slice(80,240)) 

    morshinnik7 = (slice(580,770),slice(200,360)) 
    # ^^^^^^ Центр снизу ^^^^^^ 
    morshinnik8 = (slice(550,740),slice(320,480)) 
    morshinnik9 = (slice(450,670),slice(420,580)) 
    morshinnik10 = (slice(330,520),slice(420,580)) 
    morshinnik11 = (slice(200,390),slice(420,580)) 
    morshinnik12 = (slice(120,310),slice(330,490)) 

    while running:
        img = np.asarray(sct.grab(mon))

        # c_vision(img, morshinnik2)

        get_morshinnik_coords()

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
    
def get_screenshot_bad():
    # Область с печенькой
    mon = {"top": 0, "left": 0, "width": 600, "height": 900}

    # Морщинники
    morshinnik1 = (slice(80,270),slice(200,360))
    # ^^^^^^ Центр сверху ^^^^^^ 
    morshinnik2 = (slice(120,290),slice(80,240)) 
    morshinnik3 = (slice(200,370),slice(0,160)) 
    morshinnik4 = (slice(330,500),slice(0,160)) 
    morshinnik5 = (slice(450,630),slice(0,160)) 
    morshinnik6 = (slice(550,720),slice(80,240)) 

    morshinnik7 = (slice(580,770),slice(200,360)) 
    # ^^^^^^ Центр снизу ^^^^^^ 
    morshinnik8 = (slice(550,740),slice(320,480)) 
    morshinnik9 = (slice(450,670),slice(420,580)) 
    morshinnik10 = (slice(330,520),slice(420,580)) 
    morshinnik11 = (slice(200,390),slice(420,580)) 
    morshinnik12 = (slice(120,310),slice(330,490)) 

    morshinnik_array = [morshinnik1,morshinnik2,morshinnik3,
                        morshinnik4,morshinnik5,morshinnik6,
                        morshinnik7,morshinnik8,morshinnik9,
                        morshinnik10,morshinnik11,morshinnik12,]

    sct = mss.mss()

    while running:
        index_of_morshinnik=0
        while index_of_morshinnik < len(morshinnik_array):
            # print(index_of_morshinnik)
            img = np.asarray(sct.grab(mon))

            c_vision(img, morshinnik_array[index_of_morshinnik])
            index_of_morshinnik += 1

def main():
    print("Пуск")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    get_screenshot()

    print("Смерть")
    sys.exit(0)

if __name__ == "__main__":
    main()


def set_and_show_mask():
    img = cv2.imread('C:/Users/Zayebalo/Desktop/CookieBot/scr2.png')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([5,150,0])
    upper_red = np.array([7,210,200])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('image', img)
    cv2.imshow('mask', mask)
    cv2.imshow('Result', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()