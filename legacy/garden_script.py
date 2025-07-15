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
img = cv2.imread('C:\\Users\\Egor\\Desktop\\CookieBot\\test\\grdn2.png')
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

def click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()

def get_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,0])
    upper_black = np.array([0,0,255])
    
    # lower_black = np.array([0,50,0])
    # upper_black = np.array([179,255,255])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    return mask

def test_shapes(img, mask):
    #find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #create an empty image for contours
    for i in range(0, 10):
        img_contours = np.uint8(np.zeros((mask.shape[0],mask.shape[1])))

        cv2.drawContours(img_contours, contours, i, (255,255,255), 1)

        cv2.imshow('origin', img) # выводим итоговое изображение в окно
        cv2.imshow('res', img_contours) # выводим итоговое изображение в окно

def get_screenshot(mon):
    # img = np.asarray(sct.grab(mon))
    while running:
        mask = get_mask(img)
        # cv2.imshow('Image', img)
        test_shapes(img ,mask)
        # img = np.asarray(sct.grab(mon))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break



def main():
    print("Пуск")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    mon = {"top": 180, "height": 350, 
           "left": 590, "width": 970}
    get_screenshot(mon)

    print("Смерть")
    sys.exit(0)

if __name__ == "__main__":
    main()
