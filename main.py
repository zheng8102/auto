import pyautogui
import random
import time
import keyboard
import math

def generate_random_coordinate(coordinate_range, last_coord=None):
    if last_coord:
        # 生成基于上一个坐标的随机偏移
        max_offset = 100
        offset_x = random.randint(-max_offset, max_offset)
        offset_y = random.randint(-max_offset, max_offset)
        new_x = max(coordinate_range['x_min'], min(last_coord[0] + offset_x, coordinate_range['x_max']))
        new_y = max(coordinate_range['y_min'], min(last_coord[1] + offset_y, coordinate_range['y_max']))
    else:
        # 如果没有上一个坐标，则在整个范围内随机生成
        new_x = random.randint(coordinate_range['x_min'], coordinate_range['x_max'])
        new_y = random.randint(coordinate_range['y_min'], coordinate_range['y_max'])
    return new_x, new_y

def bezier(t, p0, p1, p2):
    return (1-t)**2 * p0 + 2*(1-t)*t * p1 + t**2 * p2

def simulate_human_move(start_x, start_y, end_x, end_y, duration):
    # 创建一个控制点，使路径更自然
    control_x = random.randint(min(start_x, end_x), max(start_x, end_x))
    control_y = random.randint(min(start_y, end_y), max(start_y, end_y))
    
    steps = int(duration * 60)  # 60 FPS
    for i in range(steps + 1):
        t = i / steps
        x = bezier(t, start_x, control_x, end_x)
        y = bezier(t, start_y, control_y, end_y)
        pyautogui.moveTo(x, y)
        time.sleep(duration / steps)

def is_in_safe_zone(x, y):
    # 定义一个在操作范围之外的安全区域
    return x < 439 or x > 1327 or y < 310 or y > 1096
def main():
    coordinate_range = {
        'x_min': 439,
        'x_max': 1327,
        'y_min': 310,
        'y_max': 1096
    }
    last_coord = None
    paused = False

    print("程序已启动。按 'p' 键暂停/继续，按 'q' 键退出。")

    while True:
        if keyboard.is_pressed('q'):
            print("程序已退出。")
            break

        if keyboard.is_pressed('p'):
            paused = not paused
            print("程序已暂停" if paused else "程序已继续")
            time.sleep(0.5)  # 防止多次触发
            continue  # 跳过本次循环的剩余部分

        if paused:
            time.sleep(0.1)  # 如果暂停，小睡一下继续检查键盘输入
            continue

        current_x, current_y = pyautogui.position()
        
        if is_in_safe_zone(current_x, current_y):
            print("鼠标进入安全区域，程序暂停。移出安全区域以继续。")
            while is_in_safe_zone(*pyautogui.position()):
                time.sleep(0.1)
                if keyboard.is_pressed('q'):
                    print("程序已退出。")
                    return
            print("鼠标已移出安全区域，程序继续。")
        
        new_x, new_y = generate_random_coordinate(coordinate_range, last_coord)
        move_duration = random.uniform(0.5, 2.0)
        simulate_human_move(current_x, current_y, new_x, new_y, move_duration)

        # 随机执行点击或双击操作
        if random.random() < 0.3:  # 30% 的概率执行操作
            if random.random() < 0.7:  # 70% 的概率是单击，30% 的概率是双击
                pyautogui.click()
                print(f"单击在 ({new_x}, {new_y})")
            else:
                pyautogui.doubleClick()
                print(f"双击在 ({new_x}, {new_y})")
        else:
            print(f"移动到 ({new_x}, {new_y})")

        last_coord = (new_x, new_y)
        time.sleep(random.uniform(1, 5))  # 在操作之间随机等待1-5秒

if __name__ == "__main__":
    main()
