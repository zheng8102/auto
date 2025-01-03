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
    start_time = time.time()  # 记录程序开始时间
    click_tal =0
    while click_tal < 14000:
        try:
            # 检查是否按下 Esc 键
            if keyboard.is_pressed('esc'):
                print("\n检测到Esc键，程序正在停止...")
                break

            # 检查是否运行了 1 小时
            elapsed_time = time.time() - start_time
            if elapsed_time >= 3600:  # 3600秒 = 1小时
                print("\n已运行1小时，按下F5...")
                pyautogui.press('f5')  # 模拟按下F5
                print("正在休息5分钟...")
                time.sleep(120)  # 休息5分钟
                start_time = time.time()  # 重置开始时间

            # 生成新的随机坐标
            x, y = generate_random_coordinate(coordinate_range, last_coord, max_distance=100)
            last_coord = (x, y)
            
            # 随机生成移动时间（0.05到0.35秒之间）
            move_duration = random.uniform(0.05, 0.35)
            
            # 移动到选定的坐标
            pyautogui.moveTo(x, y, duration=move_duration)
            
            # 点击
            pyautogui.click()  
            click_tal += 1

            print(f"点击坐标: ({x}, {y}), 移动时间: {move_duration:.2f}秒,第{click_tal}次点击", end='\r')
            # 添加一个短暂的随机延迟，模拟人类操作的不规则性
            time.sleep(random.uniform(0.05, 0.2))
            
        except KeyboardInterrupt:
            print("\n程序已停止")
            break

if __name__ == "__main__":
    main()
