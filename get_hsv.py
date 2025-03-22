import cv2
import numpy as np

# Функция-заглушка для Trackbars
def nothing(x):
    pass

# Загрузка изображения
img = cv2.imread('C:/Users/Zayebalo/Desktop/CookieBot/scr.png')
if img is None:
    print("Ошибка: файл не найден или не может быть прочитан.")
    exit()

# Преобразование изображения в HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Создание окна для Trackbars
cv2.namedWindow('Trackbars')

# Создание Trackbars для нижних и верхних границ HSV
cv2.createTrackbar('Lower H', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Lower S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Lower V', 'Trackbars', 0, 255, nothing)

cv2.createTrackbar('Upper H', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Upper S', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'Trackbars', 255, 255, nothing)

while True:
    # Получение текущих значений Trackbars
    lower_h = cv2.getTrackbarPos('Lower H', 'Trackbars')
    lower_s = cv2.getTrackbarPos('Lower S', 'Trackbars')
    lower_v = cv2.getTrackbarPos('Lower V', 'Trackbars')

    upper_h = cv2.getTrackbarPos('Upper H', 'Trackbars')
    upper_s = cv2.getTrackbarPos('Upper S', 'Trackbars')
    upper_v = cv2.getTrackbarPos('Upper V', 'Trackbars')

    # Определение нижних и верхних границ HSV
    lower_range = np.array([lower_h, lower_s, lower_v])
    upper_range = np.array([upper_h, upper_s, upper_v])

    # Создание маски
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Применение маски к изображению
    result = cv2.bitwise_and(img, img, mask=mask)

    # Отображение результатов
    cv2.imshow('Original Image', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # Выход по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закрытие окон
cv2.destroyAllWindows()