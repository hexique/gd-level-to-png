from colorama import Fore, Style
from PIL import Image
from random import randint, choice, shuffle
from math import sin, cos, radians, pi
from pyperclip import copy as copy_to_clipboard, paste
from PIL import Image
import json

def save(pixels_2d, path):
    height = len(pixels_2d)
    width = len(pixels_2d[0])
    try:
        flat_pixels = [tuple(pixel) for row in pixels_2d for pixel in row]
    except Exception as e:
        raise(e)
    img = Image.new('RGB', (width, height))
    img.putdata(flat_pixels)
    img.save(path)


def toJSON(level_string):
    result = []

    for object in level_string.split(';'):
        OBJECT = object.split(',')
        if len(OBJECT) <= 2: break
        result.append({})
        for i in range(0, len(OBJECT), 2):
            result[-1][int(OBJECT[i])] = OBJECT[i + 1]

    return result

def fromJSON(array):
    result = ''

    for object in array:
        formated_obj = ''
        for param in list(object.items()):
            formated_obj += f',{param[0]},{param[1]}'
        result += formated_obj[1:] + ';'

    return result

with open('input.txt', 'r', encoding='utf-8') as f:
    level = toJSON(f.read())

with open('colormap.json', 'r', encoding='utf-8') as f:
    colormap = json.load(f)


coords = {}
raw_colors = {}

max_x = 0
max_y = 0

for obj in level:
    x = round((float(obj[2]) - 15) / 30)
    y = round((float(obj[3]) - 15) / 30)

    if (x, y) in coords:
        coords[(x, y)].append(obj)
    else:
        coords[(x, y)] = [obj]

    if x > max_x:
        max_x = int((float(obj[2]) - 15) // 30)
    if y > max_y:
        max_y = int((float(obj[3]) - 15) // 30)

    if obj[1] == '29':
        raw_colors[x] = {'color': (int(obj[7]), int(obj[8]), int(obj[9]), 255), 'duration': float(obj[10]) / 10, 'channel': 'bg'}

raw_colors = dict(sorted(raw_colors.items(), key=lambda item: item[0], reverse=True))

colors = {}
current_color = (149, 26, 255)
for x in range(max_x + 6):
    for x_stamp, stamp in list(raw_colors.items()):
        if x == x_stamp:
            current_color = stamp['color']
        colors[x] = current_color


    
result = []

# x: {color: rgb, dur: dur, channel: channel}

for y in range(max_y+1):
    result.append([colors[x] for x in range(max_x+5)])

print('placing pixels')

for pos, objects in list(coords.items()):
    final_obj_count = {}
    final_color_count = {}
    for obj in objects:
        if obj[1] in final_obj_count:
            final_obj_count[obj[1]] += 1
        else:
            final_obj_count[obj[1]] = 1
        if 21 in list(obj.keys()):
            if obj[21] in final_color_count:
                final_color_count[obj[21]] += 1
            else:
                final_color_count[obj[21]] = 1
        else:
            if 1 in final_color_count:
                final_color_count[1] += 1
            else:
                final_color_count[1] = 1

        final_obj_count = dict(sorted(final_obj_count.items(), key=lambda item: item[1], reverse=True))
        final_color_count = dict(sorted(final_color_count.items(), key=lambda item: item[1], reverse=True))


        if obj[1] in colormap:
            final_pixel = []
            for channelid, channel in list(enumerate(colormap[obj[1]]))[:3]:
                difference = colors[pos[0]][channelid] - channel
                final_pixel.append(round(channel + difference * (255 - colormap[obj[1]][3]) / 255))


        else:
            final_pixel = colors[pos[0]]

        # v = 10 blocks / sec
        # x = x0 + vt
        
        result[-pos[1]-1][pos[0]] = final_pixel

print(f'saving image {len(result[0])}x{len(result)}')
save(result, 'jumper-1.3.png')
print(f'{Fore.GREEN}done')