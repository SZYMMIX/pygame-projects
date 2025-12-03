import pygame 
from os.path import join 

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
SIZE = {'paddle': (40,170), 'ball': (25,25)}
POS = {'player': (WINDOW_WIDTH - 40, WINDOW_HEIGHT / 2), 'opponent': (40, WINDOW_HEIGHT / 2)}
SPEED = {'player': 400, 'opponent': 250, 'ball': 450}
COLORS = {
    'paddle': "#e9e6e6",
    'paddle shadow': "#ffffff",
    'ball': '#e9e6e6',
    'ball shadow': "#ffffff",
    'bg': "#0A0909"
}