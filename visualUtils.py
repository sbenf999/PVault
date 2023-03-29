import time
import sys
import itertools
import random
import os
import socket
import requests
from time import sleep

def moving_ellipsis(content):
    print(content, end="")

    time.sleep(0.5)
    for i in range(3):
        print('.', end='', flush=True)
        time.sleep(1)

    print("\n")

def print_text(text: str, sleep_time: float = 0.0) -> None:
    """
    Prints the text to the console character by character. RPG style.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.021)
    if sleep_time != 0.0:
        time.sleep(sleep_time)

def spinner(start=" Checking accounts: ", end="Finished"):
    cycle = ['-', '/', '|', '\\', ' ']
    spinner = itertools.cycle(cycle)
    c = 0
    sys.stdout.write(start)
    while c < len(cycle):
        sys.stdout.write(next(spinner))
        sleep(0.3)   # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')
        c += 1
    sys.stdout.write(end)
    print("\n")

def loading_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)                     
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end='\r')

    if iteration == total:
        print()

def menu_art(selection):
    if selection == 1:
        print()
        logo_ = "o888o           888    88ooo88 8o  888o88 8o  o888o   888o"
        size = os.get_terminal_size()
        partition = int((size[0]-len(logo_))/2)
        spacer = ' '*partition
        print(spacer + "oooooooooo  ooooo  oooo                       o888    o8  \n" + spacer +" 888    888  888    88  ooooooo  oooo  oooo    888  o888oo\n" + spacer +" 888oooo88    888  88   ooooo888  888   888    888   888  \n" + spacer +" 888           88888  888    888  888   888    888   888\n" + spacer +"o888o           888    88ooo88 8o  888o88 8o  o888o   888o\n"+ spacer)  

def screen_line():
    middle = '<Type "Help" to get started!>'
    size = os.get_terminal_size()
    partition = int((size[0]-len(middle))/2)
    spacer = '_'*partition
    print(f'{spacer}{middle}{spacer}')            
