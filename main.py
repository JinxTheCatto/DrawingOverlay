transparency = 0.5
image_offset_x = 0
image_offset_y = 0

import win32api
import win32gui
import win32con
import customtkinter as ctk
from PIL import ImageTk, Image

monitor_width = win32api.GetSystemMetrics(0)
monitor_height = win32api.GetSystemMetrics(1)

def set_clickthrough(hwnd):
    styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_COLORKEY)

overlay = None
canvas = None
def toggle_overlay():
    global overlay, canvas
    if overlay is None:
        overlay = ctk.CTkToplevel()

        overlay.geometry(f"{monitor_width}x{monitor_height}+0+0")
        overlay.overrideredirect(True)
        overlay.config(bg="#000000")
        overlay.attributes("-alpha", 0.5) # Transparency
        overlay.attributes("-topmost", True)
        overlay.attributes("-transparentcolor", "black")
        overlay.resizable(False, False)
        set_clickthrough(overlay.winfo_id())
        canvas = ctk.CTkCanvas(overlay, width=1920, height=1080, bg="black", highlightbackground="black")
        canvas.pack()
    else:
        overlay.destroy()
        canvas.destroy()
        overlay = None
        canvas = None
toggle_overlay()

image = ImageTk.PhotoImage(Image.open("image.png"))
image_width = image.width()
image_height = image.height()
canvas.create_image((monitor_width // 2) - image_width // 2, (monitor_height // 2) - image_height // 2, anchor='nw', image=image)

def update_image(image_pos_x=0, image_pos_y=0, image_transparency=0.5):
    overlay.attributes("-alpha", image_transparency)
    canvas.delete("all")
    canvas.create_image(((monitor_width // 2) - image_width // 2) + image_pos_x, ((monitor_height // 2) - image_height // 2) + image_pos_y, anchor='nw', image=image)

while True:
    update_image(image_pos_x=image_offset_x, image_pos_y=image_offset_y, image_transparency=transparency)
    overlay.update()

print("EOS")