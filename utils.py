import math
import numpy as np
import random
from colorChord import *
from musicpy import chord, play

def find_circle_intersection(circle1, circle2):
    '''
    Define the function to find the intersection points of two circles in a Cartesian coordinate system
    '''

    # Unpack the circle coordinates and radii
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2

    # Calculate the distance between the circle centers
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # If the circles do not intersect, return the closest points on the circles
    if d > r1 + r2:
        print('No intersection! Calculated the closest points.')
        # Calculate the coordinates of the closest points on the circles
        x1_closest = x1 + (x2 - x1) * r1 / d
        y1_closest = y1 + (y2 - y1) * r1 / d
        x2_closest = x2 - (x2 - x1) * r2 / d
        y2_closest = y2 - (y2 - y1) * r2 / d
        return [(x1_closest, y1_closest), (x2_closest, y2_closest)]

    # If one circle is contained within the other, return the closest points on the circles
    elif d < abs(r1 - r2):
        print('Circle contained with the other! Calculated the closest points.')
        if r1 < r2:
            x1_closest = x1 + (x1 - x2) * r1 / d
            y1_closest = y1 + (y1 - y2) * r1 / d
            x2_closest = x2 + (x1 - x2) * r2 / d
            y2_closest = y2 + (y1 - y2) * r2 / d
        else:
            x1_closest = x1 - (x1 - x2) * r1 / d
            y1_closest = y1 - (y1 - y2) * r1 / d
            x2_closest = x2 - (x1 - x2) * r2 / d
            y2_closest = y2 - (y1 - y2) * r2 / d
        return [(x1_closest, y1_closest), (x2_closest, y2_closest)]

    # If the circles intersect, calculate the intersection points
    else:

        # Calculate the distance from the center of circle 1 to the line connecting the intersection points
        a = abs(r1**2 - r2**2 + d**2) / (2 * d)

        # Calculate the coordinates of the midpoint of the line connecting the intersection points
        x_mid = x1 + a * (x2 - x1) / d
        y_mid = y1 + a * (y2 - y1) / d

        # Calculate the distance from the midpoint to the intersection points
        h = math.sqrt(round(r1**2 - a**2, 8))

        # Calculate the coordinates of the intersection points
        x1_intersect = x_mid + h * (y2 - y1) / d
        x2_intersect = x_mid - h * (y2 - y1) / d
        y1_intersect = y_mid - h * (x2 - x1) / d
        y2_intersect = y_mid + h * (x2 - x1) / d
        return [(x1_intersect, y1_intersect), (x2_intersect, y2_intersect)]

def scale_to_range(data: np.ndarray, min_max: tuple) -> np.ndarray:
    '''
    缩放数组到范围中
    '''
    new_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * (min_max[1] - min_max[0]) + min_max[0]
    return new_data

def decide_harmony(last_harmony, harmony_diff, color_diff) -> int:
    '''
    确定下一个和弦的和谐度，如果没有符合条件的就返回上一个和弦的和谐度，以保证运算继续。如果有2个值就随机抽一个
    '''
    # 计算下一个和弦和谐度允许的最大值和最小值
    ceiling = min(last_harmony + color_diff, 10)
    thresh = abs(last_harmony - color_diff)
    
    # 判断可能的的和谐度是否超过上下阈值
    below_ceiling = (ceiling - (last_harmony + harmony_diff) > 0)
    above_thresh = ((last_harmony - harmony_diff) - thresh > 0)

    # 判断并返回相应值
    if not below_ceiling:
        if above_thresh:
            return last_harmony - harmony_diff
        else:
            print('Cannot find required harmony level! Use last chord instead.')
            return last_harmony
    else:
        if above_thresh:
            return random.choice([last_harmony + harmony_diff, last_harmony - harmony_diff])
        else:
            return last_harmony + harmony_diff

def generate_chords(start_chord: Chord or list,
                    color_curve: list or np.ndarray,
                    tension_curve: list or np.ndarray,
                    normalize=True,
                    max_chord_level=4,
                    color_diff_range=(0, 20),
                    tension_range=(0, 10),
                    random_seed=42) -> list:
    '''
    实现给定初始和弦自动生成后续和弦的算法
    '''
    # 固定随机种子
    random.seed(random_seed)

    # 转换chord的格式
    if isinstance(start_chord, list):
        cchord = Chord.init_by_note_name_str(start_chord)
    
    # 将curve转化为array
    color_curve = np.array(color_curve)
    tension_curve = np.array(tension_curve)

    # 缩放曲线
    if normalize:
        color_curve = scale_to_range(color_curve, color_diff_range)
        tension_curve = scale_to_range(tension_curve, tension_range)

    # 得到所有可能和弦的坐标
    chords_dict = all_chord_coordinates(n_notes=list(range(3, max_chord_level)))
    all_x_y = list(chords_dict.values())

    # 迭代求解和弦
    new_chords = [cchord]
    for i in range(len(color_curve)):

        # 求解两圆交点
        x1, y1 = cchord.get_coordinates(method='x_y')
        r1 = color_curve[i]
        x2, y2 = 0, 0
        r2 = decide_harmony(cchord.get_harmony(), tension_curve[i], r1)
        possible_points = find_circle_intersection((x1, y1, r1), (x2, y2, r2))
        print('possible points', possible_points)

        # 寻找离交点最近的和弦
        points_dict = dict()

        for point in possible_points:
            distances = [math.sqrt((point[0] - target[0])**2 + (point[1] - target[1])**2) for target in all_x_y]
            closest_point_index = distances.index(min(distances))
            closest_point_distance = min(distances)

            points_dict[closest_point_index] = closest_point_distance

        
        min_value = min(points_dict.values())

        # 找到离目标点最近的和弦并记录
        new_chord_index = [key for key, value in points_dict.items() if value == min_value][0]
        cchord = list(chords_dict.keys())[new_chord_index]
        print('chord coordinates', cchord.get_coordinates())

        # 更新准备下一轮迭代
        new_chords.append(cchord)
        print('\n')

    return new_chords


def generate_chords_by_color(start_chord: Chord or list,
                             color_curve: list or np.ndarray,
                             normalize=True,
                             max_chord_level=4,
                             color_diff_range=(0, 20),
                             random_seed=42) -> list:
    '''
    实现给定初始和弦和色差曲线后自动生成后续和弦的算法
    '''
    # 固定随机种子
    random.seed(random_seed)

    # 转换chord的格式
    if isinstance(start_chord, list):
        cchord = Chord.init_by_note_name_str(start_chord)
    
    # 将curve转化为array
    color_curve = np.array(color_curve)

    # 缩放曲线
    if normalize:
        color_curve = scale_to_range(color_curve, color_diff_range)

    # 得到所有可能和弦的坐标
    chords_dict = all_chord_coordinates(n_notes=list(range(3, max_chord_level)))
    all_x_y = list(chords_dict.values())

    # 迭代求解和弦
    new_chords = [cchord]
    for i in range(len(color_curve)):

        # 求第一个圆的坐标
        x1, y1 = cchord.get_coordinates(method='x_y')
        r1 = color_curve[i]

        # 寻找离第一个圆最近的和弦
        distances = [abs(math.sqrt((x1 - target[0])**2 + (y1 - target[1])**2) - r1) for target in all_x_y]
        points_dict = dict(zip(range(len(all_x_y)), distances))
        min_distance = min(distances)

        # 找到离目标圆最近的和弦并记录，如有多个随机挑一个
        new_chord_indexs = [key for key, value in points_dict.items() if value == min_distance]
        print(len(new_chord_indexs))
        new_chord_index = random.choice(new_chord_indexs)
        cchord = list(chords_dict.keys())[new_chord_index]
        print('chord coordinates', cchord.get_coordinates())

        # 更新准备下一轮迭代
        new_chords.append(cchord)
        print('\n')

    return new_chords

def play_chords(color_chord_ls, degree=4, interval=0, duration=0.5):
    musicpy_chords = []
    for cchord in color_chord_ls:
        temp = [f'{i}{degree}' if i != 'Fsharp' else f'F#{degree}' for i in cchord.note_names]
        k = chord(temp, interval=interval, duration=duration)
        musicpy_chords.append(k)
    play(musicpy_chords)
    return musicpy_chords