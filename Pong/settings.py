import pygame 
from os.path import join 

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
SIZE = {'paddle': (30,150), 'ball': (23,23)}
POS = {'player': (WINDOW_WIDTH - 40, WINDOW_HEIGHT / 2), 'opponent': (40, WINDOW_HEIGHT / 2)}
SPEED = {'paddle': 400, 'ball': 450}
COLORS = {
    'paddle': "#e9e6e6",
    'paddle shadow': "#ffffff",
    'ball': '#e9e6e6',
    'ball shadow': "#ffffff",
    'bg': "#0A0909",
    'bg detail': "#2c2c2cff"
}