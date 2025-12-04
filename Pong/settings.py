import pygame 
from os.path import join 

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
SIZE = {"paddle": (30,150), "ball": (23,23)}
POS = {"player": (WINDOW_WIDTH - 40, WINDOW_HEIGHT / 2), "opponent": (40, WINDOW_HEIGHT / 2)}
SPEED = {'paddle': 400, 'ball': 450}
COLORS = {
    "paddle": (210, 210, 210),
    "paddle shadow": (255, 255, 255),
    "ball": (233, 230, 230),
    "ball shadow": (255, 255, 255),
    "bg": (10, 9, 9),
    "bg detail": (44, 44, 44)
}