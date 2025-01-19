import pyautogui
import random
import time
import keyboard
from datetime import datetime, timedelta

# 设置 pyautogui 的安全选项
pyautogui.FAILSAFE = True  # 启用故障安全
pyautogui.PAUSE = 0.05  # 减少操作间隔到0.05秒

def refresh_page():
    """刷新页面并等待"""
    print("刷新页面...")
    pyautogui.press('f5')
    print("等待页面加载 (3分钟)...")
    time.sleep(180)  # 等待3分钟

def move_and_click(x, y, duration=0.2):
    """移动到指定位置并点击"""
    try:
        # 获取当前鼠标位置
        current_x, current_y = pyautogui.position()
        
        # 如果目标位置与当前位置相差太远，使用分段移动
        distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
        if distance > 300:
            # 创建中间点
            mid_x = current_x + (x - current_x) // 2
            mid_y = current_y + (y - current_y) // 2
            # 先移动到中间点
            pyautogui.moveTo(mid_x, mid_y, duration=duration/2)
        
        # 移动到目标位置
        pyautogui.moveTo(x, y, duration=duration)
        
        # 随机点击行为
        click_type = random.random()
        if click_type < 0.6:  # 60% 概率单击
            pyautogui.click(button='left')
            print(f"左键单击: ({x}, {y})")
        elif click_type < 0.8:  # 20% 概率双击
            pyautogui.doubleClick(button='left')
            print(f"左键双击: ({x}, {y})")
        else:  # 20% 概率连续双击
            pyautogui.doubleClick(button='left')
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.doubleClick(button='left')
            print(f"连续双击: ({x}, {y})")
            
    except Exception as e:
        print(f"点击操作失败: {e}")

def get_random_position(x_min, x_max, y_min, y_max, last_pos=None):
    """获取随机位置，可以基于上一个位置"""
    if last_pos:
        # 在上一个位置附近随机
        max_offset = 200
        new_x = last_pos[0] + random.randint(-max_offset, max_offset)
        new_y = last_pos[1] + random.randint(-max_offset, max_offset)
        # 确保在范围内
        new_x = max(x_min, min(new_x, x_max))
        new_y = max(y_min, min(new_y, y_max))
        return new_x, new_y
    else:
        return random.randint(x_min, x_max), random.randint(y_min, y_max)

def main():
    # 定义点击区域范围
    CLICK_AREA = {
        'x_min': 128,
        'x_max': 1016,
        'y_min': 467,
        'y_max': 1088
    }
    
    print("程序已启动")
    print("按 'p' 暂停/继续")
    print("按 'q' 退出程序")
    print(f"点击区域: X({CLICK_AREA['x_min']}-{CLICK_AREA['x_max']}) Y({CLICK_AREA['y_min']}-{CLICK_AREA['y_max']})")
    
    paused = False
    last_position = None
    click_count = 0
    start_time = datetime.now()
    last_refresh_time = start_time
    
    while True:
        try:
            current_time = datetime.now()
            
            # 检查是否超过12000次点击
            if click_count >= 12000:
                print(f"已达到{click_count}次点击，程序退出")
                break
            
            # 检查是否需要休息和刷新
            if (current_time - last_refresh_time) >= timedelta(hours=1):
                print("运行满1小时，开始休息5分钟...")
                time.sleep(300)  # 休息5分钟
                refresh_page()
                last_refresh_time = current_time
                continue
            
            # 检查退出条件
            if keyboard.is_pressed('q'):
                print(f"程序已退出，共完成{click_count}次点击")
                break
                
            # 检查暂停条件
            if keyboard.is_pressed('p'):
                paused = not paused
                print("程序已暂停" if paused else "程序已继续")
                time.sleep(0.3)
                continue
                
            if paused:
                time.sleep(0.1)
                continue
            
            # 获取随机位置
            x, y = get_random_position(
                CLICK_AREA['x_min'], 
                CLICK_AREA['x_max'],
                CLICK_AREA['y_min'], 
                CLICK_AREA['y_max'],
                last_position
            )
            
            # 移动并点击
            move_and_click(x, y, duration=random.uniform(0.1, 0.3))
            click_count += 1
            
            # 打印进度
            if click_count % 100 == 0:
                print(f"已完成 {click_count} 次点击")
            
            last_position = (x, y)
            
            # 随机等待时间
            wait_time = random.uniform(0.3, 1.0)
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
