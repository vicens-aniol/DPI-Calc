import ctypes
import os

import win32gui
import win32ui
from PIL import Image


def get_screen_resolution():
    user32 = ctypes.WinDLL('user32')
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def get_screen_scaling():
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dc = user32.GetDC(0)
    pix_per_inch = ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
    print("Horizontal DPI is", ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX))
    print("Vertical DPI is", ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSY))
    user32.ReleaseDC(0, dc)
    return pix_per_inch

def takeScreenShot(window_name, img_name):  # Take Screenshot of specified window name
        hwnd = win32gui.FindWindow(None, window_name)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result == 1:
            # PrintWindow Succeeded
            try:
                im.save(f"tables/{img_name}.png")
            except:
                directory = "tables"
                parent_dir = os.getcwd()
                # Path
                path = os.path.join(parent_dir, directory)
                os.mkdir(path)
                im.save(f"tables/{img_name}.png")

width, height = get_screen_resolution()
scaling = get_screen_scaling()
takeScreenShot('Calculadora', 'calculadora2')

print("Resolución de pantalla: {}x{}".format(width, height))
print("Aumento de pantalla: {} dpi".format(scaling))
