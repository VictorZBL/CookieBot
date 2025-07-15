import cv2
import numpy as np 
import mss
import pyautogui
import time
import sys
import ctypes
from pynput import keyboard

# Глобальные переменные
sct = mss.mss()
running = True 
morchinik_count = 0
## Дай бог угадал с коордами
cookie_top = 110
cookie_left = 0
cookie_width = 575
cookie_height = 640
# Функция обработки нажатия esc, которая прерывает выполнение 
def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc: 
            print("Клавиша нажата. Останавливаю скрипт...")
            running = False
            return False 
    except AttributeError:
        pass

def morchinik_count_add(a):
    global morchinik_count
    morchinik_count += a
    print(morchinik_count)

def click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()

def click_at_morchinik(check_massive, mask, img):
    for i in range (0, len(check_massive)):
        center_of_check_box = [(check_massive[i][0].start + check_massive[i][0].stop) / 2, 
                                    (check_massive[i][1].start + check_massive[i][1].stop) / 2]
        if cv2.countNonZero(mask[check_massive[i][1].start - cookie_top:
                            check_massive[i][1].stop - cookie_top, 
                            check_massive[i][0]]) > 1100:
            pyautogui.moveTo(center_of_check_box[0], center_of_check_box[1], 0.01)
            click()
            click()
            click()
            morchinik_count_add(1)

def set_check_blocks(img):
    h, w = img.shape[:2]
    n = int(cookie_width * 0.145)
    m = int(cookie_height * 0.145)
    check_massive = []
    # Разметка для удобства
    for x in range(0, w, n):
        for y in range(0, h, m):
            check_massive.append((slice(x, x + n), slice(y, y + m)))

    return check_massive 

def test_show(img):
    h, w = img.shape[:2]
    n = int(cookie_width * 0.145)
    m = int(cookie_height * 0.145)
    # Разметка для удобства
    for y in range(0, h, m):
        cv2.line(img, (0, y), (w, y), (0, 255, 0), 1)  
  
    for x in range(0, w, n):
        cv2.line(img, (x, 0), (x, h), (0, 255, 0), 1)


    cv2.imshow('Image', img)

def c_vision(img):
    ## Маска ##
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # полностью исключена печенька
    lower_red = np.array([5,180,0])
    upper_red = np.array([7,210,200])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # cv2.imshow('Image', mask)
    test_show(img)
    return mask

def get_screenshot(mon):
    img = np.asarray(sct.grab(mon))
    check_massive = set_check_blocks(img)
    while running:
        mask = c_vision(img)         
        click_at_morchinik(check_massive, mask, img)
        img = np.asarray(sct.grab(mon))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break




def main():
    print("Пуск")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    mon = {"top": cookie_top, "height": cookie_height, 
           "left": cookie_left, "width": cookie_width}
    get_screenshot(mon)

    print("Смерть")
    sys.exit(0)

if __name__ == "__main__":
    main()
