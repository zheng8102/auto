import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        positionStr = f"X: {x} Y: {y}"
        print(positionStr)
        time.sleep(1)  # 等待10秒
except KeyboardInterrupt:
    print('\n退出.')


