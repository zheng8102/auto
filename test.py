import random
import math
import pyautogui
import time
import keyboard

def generate_random_coordinate(coordinate_range, last_coord=None, max_distance=100):
    while True:
        x = random.randint(coordinate_range['x_min'], coordinate_range['x_max'])
        y = random.randint(coordinate_range['y_min'], coordinate_range['y_max'])
        new_coord = (x, y)
        
        if last_coord is None:
            return new_coord
        
        distance = math.sqrt((x - last_coord[0])**2 + (y - last_coord[1])**2)
        if distance <= max_distance:
            return new_coord

def main():
    # 定义坐标范围
    coordinate_range = {
        'x_min': 439,
        'x_max': 1327,
        'y_min': 310,
        'y_max': 1096
    }

    last_coord = None

    while True:
        try:
            # 生成新的随机坐标
            if keyboard.is_pressed('esc'):
                print("\n检测到Esc键，程序正在停止...")
                break
            x, y = generate_random_coordinate(coordinate_range, last_coord, max_distance=100)
            last_coord = (x, y)
            
            # 随机生成移动时间（0.1到0.7秒之间）
            move_duration = random.uniform(0.05, 0.35)
            
            # 移动到选定的坐标
            pyautogui.moveTo(x, y, duration=move_duration)
            
            # 点击
            pyautogui.click()  

            print(f"点击坐标: ({x}, {y}), 移动时间: {move_duration:.2f}秒",end='\r')
            
            # 添加一个短暂的随机延迟，模拟人类操作的不规则性
            time.sleep(random.uniform(0.05, 0.2))
            
        except KeyboardInterrupt:
            print("\n程序已停止")
            break

if __name__ == "__main__":
    main()
