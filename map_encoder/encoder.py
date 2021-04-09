import pygame, json
from pygame import Rect as r
pygame.init()
import importlib

def string_rect(rect_obj):
    end_rect = None
    rect_obj = rect_obj.split("(")[1]
    rect_obj_size = len(rect_obj)
    rect_obj = rect_obj[: rect_obj_size - 2]
    rect_obj = rect_obj.split(",")
    final_rect = []
    for val in rect_obj:
        final_rect.append(int(val))
    end_rect = pygame.Rect(final_rect)
    return end_rect
def encode(json_file="map.json"):
    with open(json_file) as f:
        data = json.load(f)
        f.close
    game_map = []
    for item in data:
        entire_item = data[item]
        end_item = {}
        end_item["rect"] = string_rect(entire_item['rect'])
        end_item["image"] = entire_item['image']
        game_map.append(end_item)
    return game_map
print(encode())
