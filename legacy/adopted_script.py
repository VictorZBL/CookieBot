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

##############################################################################
#   Получение сегмента экрана, адоптированое под разные разрешения
##############################################################################
# Принимает процентные пропорции области экрана 
# И возвращает координаты
# (x_отступ, y)
def get_working_area(y_start_percent, y_end_percent, 
                     x_start_percent, x_end_percent):
    screen_width, screen_height = pyautogui.size()
    x_start = int(screen_width * x_start_percent / 100)
    y_start = int(screen_height * y_start_percent / 100)
    x_end = int(screen_width * x_end_percent / 100)
    y_end = int(screen_height * y_end_percent / 100)
    return(y_start, y_end, x_start, x_end)

def get_center(area):
    y_start, y_end, x_start, x_end = area
    center_x = (x_end - x_start) // 2
    center_y = (y_end - y_start) // 2
    return(center_x, center_y)

# y_stars:y_end, x_start:x_end
def adjust_for_scaling(y_start, y_end, x_start, x_end):
    user32 = ctypes.windll.user32
    hdc = user32.GetDC(0)
    scaling = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
    user32.ReleaseDC(0, hdc)
    scaling_factor = scaling / 96.0
    return(int(y_start * scaling_factor), int(y_end * scaling_factor),
           int(x_start * scaling_factor), int(x_end * scaling_factor))

# cookie_top = 30
# cookie_left = 0
# cookie_width = 575
# cookie_height = 825
## Дай бог угадал с коордами
cookie_area = get_working_area(2.2, 76.5, 0, 30)
print(cookie_area)

cookie_center = get_center(cookie_area)
print(cookie_center)
##############################################################################

# Получение координат блоков для проверки на морщинника
def set_check_blocks(cookie_area):
    i = cookie_area[0]
    j = cookie_area[2]
    check_massive = []
    box_res = int(cookie_area[1]*0.1)
    while(i < cookie_area[1]-box_res):
        while(j < cookie_area[3]-box_res):
            check_massive.append((slice(i,i+box_res), slice(j,j+box_res)))
            j+=box_res
        i+=box_res
        j = cookie_area[2] 
    return check_massive 
check_massive = set_check_blocks(cookie_area)
print(check_massive)
def test_show(img):
    h, w = img.shape[:2]
    n = int(cookie_area[1]*0.1)
    # Разметка для удобства
    for y in range(0, h, n):
        cv2.line(img, (0, y), (w, y), (0, 255, 0), 1)    
    for x in range(0, w, n):
        cv2.line(img, (x, 0), (x, h), (0, 255, 0), 1)
    
    cv2.imshow('Image', img)

def c_vision(img, check_box):
    ## Маска ################################################
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([5,150,0])
    upper_red = np.array([7,210,200])

    # полностью исключена печенька
    lower_red = np.array([5,180,0])
    upper_red = np.array([7,210,200])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    ########################################################## 
        
    # Центр чек бокса
    center_of_check_box = [(check_box[0].start + check_box[0].stop) / 2, 
                           (check_box[1].start + check_box[1].stop) / 2]
    # print(center_of_check_box[0],center_of_check_box[1])
    print(np.sum(mask[check_box]))

    # if np.sum(mask[check_box]) >= 280000:
    #     pyautogui.moveTo(center_of_check_box[1],center_of_check_box[0], 0.5)
    #     print("Морщ!")
    cv2.imshow('Image', mask)

def get_screenshot(mon):
    while running:
        img = np.asarray(sct.grab(mon))
        test_show(img)

        index_of_check_box = 0
        while index_of_check_box < len(check_massive):
            img = np.asarray(sct.grab(mon))
            # c_vision(img, check_massive[34])
            index_of_check_box += 1        

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break




def main():
    print("Пуск")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    mon = {"top": cookie_area[0], "height": cookie_area[1], 
           "left": cookie_area[2], "width": cookie_area[3]}
    
    get_screenshot(mon)

    print("Смерть")
    sys.exit(0)

if __name__ == "__main__":
    main()