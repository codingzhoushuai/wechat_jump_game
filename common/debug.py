# -*- coding: utf-8 -*-
"""
这是debug的代码，当DEBUG_SWITCH开关开启的时候，会将各种信息存在本地，方便检查故障
"""
import os
import sys
import shutil
import math
from PIL import ImageDraw

# from common import ai
try:
    from common.auto_adb import auto_adb
except ImportError as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)
screenshot_backup_dir = 'screenshot_backups'
adb = auto_adb()


def make_debug_dir(screenshot_backup_dir):
    """
    创建备份文件夹
    """
    if not os.path.isdir(screenshot_backup_dir):
        os.mkdir(screenshot_backup_dir)


def backup_screenshot(ts):
    """
    为了方便失败的时候 debug
    """
    make_debug_dir(screenshot_backup_dir)
    # 如果存在autojump.png文件，将其复制到备份文件夹
    if os.path.exists('autojump.png'):
        shutil.copy(os.path.join(os.getcwd(), 'autojump.png'), os.path.join(os.getcwd(), screenshot_backup_dir, str(ts) + '.png'))


def save_debug_screenshot(ts, im, piece_x, piece_y, board_x, board_y):
    """
    对 debug 图片加上详细的注释
    
    """
    make_debug_dir(screenshot_backup_dir)
    # 创建可以在手机屏幕截图上绘图的对象
    draw = ImageDraw.Draw(im)
    # 绘制棋子中心到棋盘中心的直线
    draw.line((piece_x, piece_y) + (board_x, board_y), fill=2, width=3)
    draw.line((piece_x, 0, piece_x, im.size[1]), fill=(255, 0, 0))
    draw.line((0, piece_y, im.size[0], piece_y), fill=(255, 0, 0))
    draw.line((board_x, 0, board_x, im.size[1]), fill=(0, 0, 255))
    draw.line((0, board_y, im.size[0], board_y), fill=(0, 0, 255))
    # 绘制以棋子中心坐标为中心的20px直径的圆形
    draw.ellipse((piece_x - 10, piece_y - 10, piece_x + 10, piece_y + 10), fill=(255, 0, 0))
    # 绘制以棋盘中心坐标为中心的20px直径的圆形
    draw.ellipse((board_x - 10, board_y - 10, board_x + 10, board_y + 10), fill=(0, 0, 255))
    del draw
    # 将绘制的图片保存到备份文件夹
    im.save(os.path.join(os.getcwd(), screenshot_backup_dir,
                         str(piece_x)+'#'+str(piece_y)+'#'+str(board_x)+'#'+str(board_y)+'#' + str(ts) + '.png'))


def computing_error(last_press_time, target_board_x, target_board_y, last_piece_x, last_piece_y, temp_piece_x,
                    temp_piece_y):
    """
    计算跳跃实际误差
    """
    target_distance = math.sqrt(
        (target_board_x - last_piece_x) ** 2 + (target_board_y - last_piece_y) ** 2)  # 上一轮目标跳跃距离
    actual_distance = math.sqrt((temp_piece_x - last_piece_x) ** 2 + (temp_piece_y - last_piece_y) ** 2)  # 上一轮实际跳跃距离
    jump_error_value = math.sqrt((target_board_x - temp_piece_x) ** 2 + (target_board_y - temp_piece_y) ** 2)  # 跳跃误差

    print(round(target_distance), round(jump_error_value), round(actual_distance), round(last_press_time))
    ''''# 将结果采集进学习字典
    if last_piece_x > 0 and last_press_time > 0:
        ai.add_data(round(actual_distance, 2), round(last_press_time))
        # print(round(actual_distance), round(last_press_time))'''


def dump_device_info():
    """
    显示设备信息
    """
    size_str = adb.get_screen()
    device_str = adb.test_device_detail()
    phone_os_str = adb.test_device_os()
    density_str = adb.test_density()
    print("""**********
Screen: {size}
Density: {dpi}
Device: {device}
Phone OS: {phone_os}
Host OS: {host_os}
Python: {python}
**********""".format(
        size=size_str.replace('\n', ''),
        dpi=density_str.replace('\n', ''),
        device=device_str.replace('\n', ''),
        phone_os=phone_os_str.replace('\n', ''),
        host_os=sys.platform,
        python=sys.version
    ))
