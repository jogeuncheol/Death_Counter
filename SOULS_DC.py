from PIL import ImageGrab
from time import sleep
import tkinter
import threading
import cv2
import numpy as np
#pyinstaller --icon=icon.ico --onefile --noconsole DSDCX.py

lower_red1 = (0, 67, 67)
upper_red1 = (5, 255, 255)
lower_red2 = (170, 67, 67)
upper_red2 = (180, 255, 255)

low_black = (0, 0, 0)
upper_black = (0, 255, 50)

with open("유다희.txt", "w") as f:
    f.write('0')

you_died = False
died_counter = 0
x1, y1, x2, y2 = 310, 310, 1530, 750
key = 0
global frames


class UI(tkinter.Tk):
    def __init__(self):
        global died_counter
        tkinter.Tk.__init__(self)

        self.t_label = tkinter.Label(self, text = "YOU DIED ", font = ("times", "16"))
        self.t_label.place(x = 50, y = 260)
        self.d_label = tkinter.IntVar(self, died_counter)
        self.count_label = tkinter.Label(self, textvariable = self.d_label, font = ("times", "16"))
        self.count_label.place(x=200, y=260)

        self.died_label = tkinter.Label(text="Prepare To ELDEN RING", font = ("times"))
        self.died_label.place(x=50, y=290)

        self.button2 = tkinter.Button(self, text = "SOULS", width = 17, command = self.start_cap)
        self.button2.place(x=0, y=323)
        self.button3 = tkinter.Button(self, text = "STOP", width = 17, command = self.check_end1)
        self.button3.place(x=130, y=323)
        self.button4 = tkinter.Button(self, text="SEKIRO", width=17, command=self.start_skr_cap)
        self.button4.place(x=0, y=353)
        self.button5 = tkinter.Button(self, text="RESET", width= 17, command=self.reset_data)
        self.button5.place(x=130, y= 353)

    def die_counter(self):
        self.d_label.set(died_counter)
        #print(self.d_label.get())
        self.after(1000, self.die_counter)

    def start_cap(self):
        global key
        global frames

        key = 1
        frames = [tkinter.PhotoImage(file="C:/Users/blueq/PycharmProjects/SKRDC/icon1_save3.gif",
                                     format="gif -index %i" % (i)).subsample(2) for i in range(21)]
        self.after(0, self.die_counter)
        self.after(100, draw_gif, 0)
        capture_box().start()

    def start_skr_cap(self):
        global key
        global frames

        key = 1
        frames = [tkinter.PhotoImage(file="C:/Users/blueq/PycharmProjects/SKRDC/icon1_save3.gif",
                                     format="gif -index %i" % (i)).subsample(2) for i in range(21)]
        self.after(0, self.die_counter)
        self.after(100, draw_gif, 0)
        cap_skr().start()

    def check_end1(self):
        global frames
        global key

        frames = [tkinter.PhotoImage(file="C:/Users/blueq/PycharmProjects/SKRDC/icon1_save3.gif",
                                     format="gif -index %i" % (i)).subsample(2) for i in range(1)]
        self.after(100, draw_gif, 0)
        if key == 1:
            key = 0

    def reset_data(self):
        global died_counter

        if died_counter != 0:
            died_counter = 0


class capture_box(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global key
            global died_counter

            # red color mask ## DARK SOULS ## DEMONS SOULS REMAKE ##
            img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGRA2RGB)
            img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
            img_mask = cv2.inRange(img_hsv, lower_red1, upper_red1)
            img_mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
            img_mask3 = img_mask + img_mask2
            img_result = cv2.bitwise_and(img_ori, img_ori, mask=img_mask3)
            contours, _ = cv2.findContours(img_mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # black color mask ## MORTAL SHELL ##
            # img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)
            # img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
            # img_gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
            # img_mask = cv2.inRange(img_hsv, low_black, upper_black)
            # # img_result = cv2.bitwise_and(img_ori, img_ori, mask = img_mask)
            # img_result = img_gray
            # contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 사각형 박스
            i = 0
            fX = []
            centers = []
            D = []
            x, y, w, h = 0, 0, 0, 0
            contour_array = []
            bluebox = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)  # 수직인 사각형 생성
                if 70 < h < 140 and 10 < w < 110:
                    contour_array.append([x, y, w, h])
                    M = cv2.moments(cnt)
                    try:
                        cX = int(M['m10'] / M['m00'])
                        cY = int(M['m01'] / M['m00'])
                        centers.append([cX, cY])
                        cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    except ZeroDivisionError:
                        print('######')
            # print(len(contour_array))
            for i in range(len(contour_array) - 1):
                index = i
                for j in range(i + 1, len(contour_array)):
                    # print(centers[j])
                    if contour_array[index][0] > contour_array[j][0]:
                        index = j
                contour_array[i], contour_array[index] = contour_array[index], contour_array[i]
            # print(contour_array)
            sum = 0
            avg = 0
            for i in range(len(contour_array)):
                sum = sum + contour_array[i][1]
            try:
                avg = int(sum / len(contour_array))
            except ZeroDivisionError:
                print('######')
            print(avg)

            for i in range(len(contour_array)):
                sub = avg - contour_array[i][1]
                sub = int(np.sqrt(sub * sub))
                print(sub)
                if sub < 50:
                    bluebox.append(contour_array[i])
                    cv2.rectangle(
                        img_result,
                        (contour_array[i][0], contour_array[i][1]),
                        (contour_array[i][0] + contour_array[i][2], contour_array[i][1] + contour_array[i][3]),
                        (255, 0, 0), 2)
                # ### contour 사이의 거리[D]를 구함 & contour 들의 수직 비율이 일정해야 함.
            if len(bluebox) >= 2:  # ##if len(centers) >= 2: if len(contour_array) >= 2:
                for idx in range(len(bluebox) - 1):
                    # print(idx)
                    dx = bluebox[idx][0] - bluebox[idx + 1][0]
                    dy = bluebox[idx][1] - bluebox[idx + 1][1]
                    D.append(int(np.sqrt(dx * dx + dy * dy)))
            for i in range(len(D)):
                if D[i] < 160:
                    fX.append(D[i])
            print(fX)

            if 5 < len(fX) < 9:
                died_counter += 1
                with open("유다희.txt", "w") as f:
                    f.write(str(died_counter))
                sleep(5)

            img_resize = cv2.resize(img_result, dsize=(0, 0), fx=0.5, fy=0.5)
            cv2.imshow("capture", img_resize)

            # text_img = pytesseract.image_to_string(img_result, lang='eng')
            # print(text_img)
            # img_resize = cv2.resize(img_result, dsize=(0, 0), fx=0.5, fy=0.5)
            #
            # cv2.imshow("capture", img_resize)
            #

            cv2.waitKey(1)
            if key == 0:
                cv2.destroyAllWindows()
                break


class cap_skr(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global key
            global died_counter

            # red color mask ## DARK SOULS ##
            img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGRA2RGB)
            img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
            img_mask = cv2.inRange(img_hsv, lower_red1, upper_red1)
            img_mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
            img_mask3 = img_mask + img_mask2
            img_result = cv2.bitwise_and(img_ori, img_ori, mask=img_mask3)
            contours, _ = cv2.findContours(img_mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # black color mask ## MORTAL SHELL ##
            # img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)
            # img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
            # img_gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
            # img_mask = cv2.inRange(img_hsv, low_black, upper_black)
            # # img_result = cv2.bitwise_and(img_ori, img_ori, mask = img_mask)
            # img_result = img_gray
            # contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 사각형 박스
            i = 0
            fX = []
            centers = []
            D = []
            x, y, w, h = 0, 0, 0, 0
            contour_array = []
            bluebox = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)  # 수직인 사각형 생성
                if 200 < h < 350 and 50 < w < 350:
                    contour_array.append([x, y, w, h])
                    M = cv2.moments(cnt)
                    try:
                        cX = int(M['m10'] / M['m00'])
                        cY = int(M['m01'] / M['m00'])
                        centers.append([cX, cY])
                        cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    except ZeroDivisionError:
                        print('######')
            # print(len(contour_array))

            for i in range(len(contour_array) - 1):
                index = i
                for j in range(i + 1, len(contour_array)):
                    # print(centers[j])
                    if contour_array[index][0] > contour_array[j][0]:
                        index = j
                contour_array[i], contour_array[index] = contour_array[index], contour_array[i]
            # print(contour_array)
            sum = 0
            avg = 0
            for i in range(len(contour_array)):
                sum = sum + contour_array[i][1]
            try:
                avg = int(sum / len(contour_array))
            except ZeroDivisionError:
                print('######')
            # print(avg)

            for i in range(len(contour_array)):
                sub = avg - contour_array[i][1]
                sub = int(np.sqrt(sub * sub))
                print("sub : ", sub)
                if sub < 50:
                    bluebox.append(contour_array[i])
                    cv2.rectangle(
                        img_result,
                        (contour_array[i][0], contour_array[i][1]),
                        (contour_array[i][0] + contour_array[i][2], contour_array[i][1] + contour_array[i][3]),
                        (255, 0, 0), 2)
                # ### contour 사이의 거리[D]를 구함 & contour들의 수직 비율이 일정해야 함.
            print("bluebox : ", bluebox)
            if len(bluebox) == 2:  # if len(centers) >= 2: if len(contour_array) >= 2:
                for idx in range(len(bluebox) - 1):
                    # print(idx)
                    dx = bluebox[idx][0] - bluebox[idx + 1][0]
                    dy = bluebox[idx][1] - bluebox[idx + 1][1]
                    D.append(int(np.sqrt(dx * dx + dy * dy)))
            print(D)
            for i in range(len(D)):
                if 160 < D[i] < 165:
                    fX.append(D[i])
            print(fX)

            # if len(fX) > 5 and len(fX) < 9:
            if len(fX) == 1:
                print("died count : ", died_counter)
                died_counter += 1
                with open("죽.txt", "w") as f:
                    f.write(str(died_counter))
                sleep(5)

            img_resize = cv2.resize(img_result, dsize=(0, 0), fx=0.5, fy=0.5)
            cv2.imshow("skr_capture", img_resize)

            # text_img = pytesseract.image_to_string(img_result, lang='eng')
            # print(text_img)
            # img_resize = cv2.resize(img_result, dsize=(0, 0), fx=0.5, fy=0.5)
            #
            # cv2.imshow("capture", img_resize)
            #

            cv2.waitKey(1)
            if key == 0:
                cv2.destroyAllWindows()
                break


window = UI()
window.title("유다희")
window.geometry("260x390+0+0")
frames = [tkinter.PhotoImage(file="C:/Users/blueq/PycharmProjects/SKRDC/icon1_save3.gif",
                             format="gif -index %i" %(i)).subsample(2) for i in range(1)]
# frames = tkinter.PhotoImage(file = "C:/Users/blueq/PycharmProjects/DSDXC/icon1.png").subsample(2)


def draw_gif(ind):
    try:
        frame = frames[ind]
        ind += 1
        gif_label.configure(image=frame)
        window.after(100, draw_gif, ind)
    except Exception:
        ind = 0
        window.after(0, draw_gif, ind)

# def draw_png(ind):
#     gif_label.configure(image=frames)
#     window.after(100, draw_png, ind)


gif_label = tkinter.Label(window)
gif_label.place(x=0, y=0)
window.after(0, draw_gif, 0)

window.resizable(width = False, height = False)

window.mainloop()