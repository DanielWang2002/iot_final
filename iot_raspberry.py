import re
import time
import argparse
import random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

import socket
# 建立socket連線
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP宣告
socket1.bind(("172.20.10.11",9487))
socket1.listen(1)

def run(recevent, device):
    while True:
        recevent = connect_socket.recv(1024)
        if str(recevent,encoding='utf-8') == 'close':
            break
        # 處理接收的資料，將其轉換成list(int)
        s = str(recevent, encoding='utf-8')
        s = s.replace('.', '')
        test = s[1:-1].split(" ")
        for i in range(len(test)): test[i] = int(test[i])
        print(test)
        # 2D Array(8x8): 1代表亮燈，0代表不亮
        arr = [[0] * 8 for i in range(8)]
        for i in range(len(test)):
            for k in range(int(test[i])):
                arr[i][k] = 1

        # 控制MAX7219，將arr中值為1的位置點亮
        with canvas(device) as draw:
            for i in range(8):
                for j in range(8):
                    if arr[i][j] == 1: draw.point((i, j), fill='red')
        time.sleep(0.1)

def getDevice(n, block_orientation, rotate, inreverse):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Created device")
    return device

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        device = getDevice(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
        connect_socket,client_addr = socket1.accept()
        while True:
            recevent = connect_socket.recv(1024)
            if str(recevent,encoding='utf-8') == 'open':
                run(recevent, device)
                connect_socket,client_addr = socket1.accept()

            
    except KeyboardInterrupt:
        pass
