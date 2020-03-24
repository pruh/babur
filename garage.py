#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from concurrent.futures import ThreadPoolExecutor


GPIO.setmode(GPIO.BCM)
garage_door_pin = 25
GPIO.setup(garage_door_pin, GPIO.OUT)
executor = ThreadPoolExecutor(max_workers=2)


def open_close(action: str) -> None:
    executor.submit(open_close_bg, (action))


def open_close_bg(action: str) -> None:
    # set to high to 500ms
    GPIO.output(garage_door_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(garage_door_pin, GPIO.LOW)
