import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
)

img = cv2.imread(file_path)
if img is None:
    print("Image not loaded correctly")
    exit()

flag = False
ix = -1
iy = -1
draft = []

def crop(event, x, y, flags, params):

    global flag, ix, iy, draft
    
    if event == 1:
        flag = True
        ix = x
        iy = y

    elif event == 0:
        if flag == True:
            temp_img = img.copy()
            width = abs(x - ix)
            height = abs(y - iy)
            cv2.setWindowTitle("window", f"{height}x{width}")
            cv2.rectangle(temp_img, pt1 = (ix, iy), pt2 = (x, y), thickness = 3, color = (0, 255, 0))
            cv2.imshow("window", temp_img)

    elif event == 4:
        fx = x
        fy = y

        flag = False
        if (ix != fx and iy != fy):
            cropped = img[min(iy, fy):max(iy, fy), min(ix, fx):max(ix, fx)]
            cv2.imshow("new_window", cropped)
            cv2.waitKey(1)
            draft.append(cropped)
        else:
            print("No region selected")

cv2.namedWindow(winname="window")
cv2.waitKey(100)
cv2.setMouseCallback("window", crop)

while True:
    if not flag:
        cv2.imshow("window", img)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cv2.destroyAllWindows()

for pics, imgs in enumerate(draft):
    cv2.imshow(f"crop{pics}", imgs)
cv2.waitKey(0)
try:
    save = int(input("Which picture do you want to save?"))
    name = input("What should be the name of your save file?")
    cv2.imwrite(name+".jpg", draft[save])
except (TypeError, ValueError, IndexError):
    print("Please enter a valid number")
cv2.destroyAllWindows()
