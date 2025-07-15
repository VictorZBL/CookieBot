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
def get_working_area(y_start_percent, y_end_percent, 
                     x_start_percent, x_end_percent):
    screen_width, screen_height = pyautogui.size()
    x_start = int(screen_width * x_start_percent / 100)
    y_start = int(screen_height * y_start_percent / 100)
    x_end = int(screen_width * x_end_percent / 100)
    y_end = int(screen_height * y_end_percent / 100)
    return(y_start, y_end, x_start, x_end)

def get_windows_scaling():
    shcore = ctypes.windll.shcore
    shcore.SetProcessDpiAwareness(1)
    monitor = ctypes.windll.user32.MonitorFromWindow(0, 2)
    scale_factor = ctypes.c_uint()
    shcore.GetScaleFactorForMonitor(monitor, ctypes.byref(scale_factor))
    return scale_factor.value / 100    
    
scale_factor = get_windows_scaling()

cookie_top, cookie_height, cookie_left, cookie_width = get_working_area(10*scale_factor, 60*scale_factor, 0, 30*scale_factor)
# print(cookie_top, cookie_height, cookie_left, cookie_width)

# cookie_top = 115
# cookie_left = 0
# cookie_width = 575
# cookie_height = 630
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

def click_at_morchinik(check_massive, check_massive_screen, mask, img):
    for i in range (0, len(check_massive)):
        center_of_check_box = [(check_massive_screen[i][0].start + check_massive_screen[i][0].stop) / 2, 
                                    (check_massive_screen[i][1].start + check_massive_screen[i][1].stop) / 2]
        check_box_resolution = mask[check_massive[i][1], check_massive[i][0]].shape[1]*mask[check_massive[i][1], check_massive[i][0]].shape[0]
        if cv2.countNonZero(mask[check_massive[i][1], check_massive[i][0]]) > check_box_resolution*0.15:
            # print(cv2.countNonZero(mask[check_massive[i][1], check_massive[i][0]]))
            # print(mask[check_massive[i][1], check_massive[i][0]].shape[1]*mask[check_massive[i][1], check_massive[i][0]].shape[0]) 
            # print()                 
            pyautogui.moveTo(center_of_check_box[0]/scale_factor, center_of_check_box[1]/scale_factor, 0.01)
            click()
            click()
            click()
            morchinik_count_add(1)


def set_check_blocks(img):
    h, w = img.shape[:2]
    n = int(w * 0.145)
    m = int(h * 0.145)
    check_massive = []
    for x in range(0, w, n):
        for y in range(0, h, m):
            check_massive.append((slice(x, x + n), slice(y, y + m)))

    h, w = cookie_height, cookie_width
    n = int(cookie_width*0.145)
    m = int(cookie_height*0.145)
    check_massive_screen = []
    for x in range(0, w, n):
        for y in range(cookie_top, h + m, m):
            check_massive_screen.append((slice(x, x + n), slice(y, y + m)))
    return check_massive, check_massive_screen

def test_show(img):
    h, w = img.shape[:2]
    n = int(cookie_width * 0.145)
    m = int(cookie_height * 0.145)

    n = int(w * 0.145)
    m = int(h * 0.145)
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
    check_massive, check_massive_screen = set_check_blocks(img)
    # print(len(check_massive), len(check_massive_screen))
    while running:
        mask = c_vision(img)         
        click_at_morchinik(check_massive, check_massive_screen, mask, img)
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
