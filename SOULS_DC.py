from PIL import ImageGrab
from time import sleep
import tkinter
import threading
import cv2
import numpy as np

lower_red1 = (0, 67, 67)
upper_red1 = (5, 255, 255)
lower_red2 = (170, 67, 67)
upper_red2 = (180, 255, 255)

with open("유다희.txt", "w") as f:
    f.write('0')

you_died = False
death_count = 0
key = 0
global frames


class UI(tkinter.Tk):
    global death_count
    program_quit = 0
    __counting_status = 0

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.after(0, self.die_counter)

        t_label = tkinter.Label(self, text = "YOU DIED ", font = ("times", "16"))
        t_label.place(x = 50, y = 260)
        self.d_label = tkinter.IntVar(self, death_count)
        count_label = tkinter.Label(self, textvariable = self.d_label, font = ("times", "16"))
        count_label.place(x=200, y=260)

        died_label = tkinter.Label(text="Prepare To ELDEN RING", font = ("times"))
        died_label.place(x=50, y=290)
        end_label = tkinter.Label(text="2022.02.25", font=("times"))
        end_label.place(x=93, y=417)

        button1 = tkinter.Button(self, text = "ELDEN RING", width = 34, command = self.start_elden_cap)
        button1.place(x=5, y=323)
        button2 = tkinter.Button(self, text = "SOULS", width = 16, command = self.start_cap)
        button2.place(x=5, y=353)
        button3 = tkinter.Button(self, text = "STOP", width = 16, command = self.check_end1)
        button3.place(x=131, y=353)
        button4 = tkinter.Button(self, text="SEKIRO", width=16, command=self.start_skr_cap)
        button4.place(x=5, y=383)
        button5 = tkinter.Button(self, text="RESET", width= 16, command=self.reset_data)
        button5.place(x=131, y=383)

    def die_counter(self):
        self.d_label.set(death_count)
        print("die_counter fn : ", self.d_label.get())
        self.after(1000, self.die_counter)

    def reset_data(self):
        global death_count
        death_count = 0

    def start_cap(self):
        global key
        global frames

        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            frames = [tkinter.PhotoImage(file="./icon1_save3.gif",
                                         format="gif -index %i" % (i)).subsample(2) for i in range(21)]
            self.after(100, draw_gif, 0)
            death_count_t = DeathCountStart("souls", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_elden_cap(self):
        global key
        global frames

        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            frames = [tkinter.PhotoImage(file="./icon1_save3.gif",
                                         format="gif -index %i" % (i)).subsample(2) for i in range(21)]
            self.after(100, draw_gif, 0)
            death_count_t = DeathCountStart("ring", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_skr_cap(self):
        global key
        global frames

        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            frames = [tkinter.PhotoImage(file="./icon1_save3.gif",
                                         format="gif -index %i" % (i)).subsample(2) for i in range(21)]
            self.after(100, draw_gif, 0)
            death_count_t = DeathCountStart("sekiro", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def check_end1(self):
        global frames
        global key

        frames = [tkinter.PhotoImage(file="./icon1_save3.gif",
                                     format="gif -index %i" % (i)).subsample(2) for i in range(1)]
        self.after(100, draw_gif, 0)
        if key == 1:
            key = 0
            self.__counting_status = 0


class DeathCountStart(threading.Thread):
    def __init__(self, game_type, program_quit):
        threading.Thread.__init__(self)
        self.game_type = game_type
        self.program_quit = program_quit

    def run(self):
        global key
        while key == 1:
            # __red color mask__
            # __DARK SOULS 1, 2, 3__ __DEMONS SOULS REMAKE__ __SEKIRO SHADOW DIE TWICE__
            img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGRA2RGB)
            img_ori = cv2.resize(img_ori, dsize=(960, 540), interpolation=cv2.INTER_AREA)
            img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
            img_mask = cv2.inRange(img_hsv, lower_red1, upper_red1)
            img_mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
            img_mask3 = img_mask + img_mask2
            # img_result = cv2.bitwise_and(img_ori, img_ori, mask=img_mask3)
            contours, _ = cv2.findContours(img_mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            height, width, channels = img_ori.shape
            w_rate = width / 1920
            h_rate = height / 1080
            # 사각형 박스
            fX = []
            D = []
            contour_array = []
            blue_box = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)  # 수직인 사각형 생성
                if self.game_type == "souls" \
                        and 70 * h_rate < h < 140 * h_rate \
                        and 10 * w_rate < w < 110 * w_rate:
                    contour_array.append([x, y, w, h])
                elif self.game_type == "sekiro" and 200 < h < 350 and 50 < w < 350:
                    contour_array.append([x, y, w, h])
                elif self.game_type == "ring" and 50 * h_rate < h < 80 * h_rate and 10 * w_rate < w < 80 * w_rate:
                    contour_array.append([x, y, w, h])
                # __ sort countours
            for i in range(len(contour_array) - 1):
                index = i
                for j in range(i + 1, len(contour_array)):
                    # print(centers[j])
                    if contour_array[index][0] > contour_array[j][0]:
                        index = j
                contour_array[i], contour_array[index] = contour_array[index], contour_array[i]
            # __ y position average
            contour_y_sum = 0
            avg = 0
            if self.game_type == "souls" or self.game_type == "ring":
                delete_array = []
                for i in range(len(contour_array)):
                    contour_y_sum = contour_y_sum + contour_array[i][1]
                try:
                    avg = int(contour_y_sum / len(contour_array))
                except ZeroDivisionError:
                    print('######')
                print("avg : ", avg)
                for i in range(len(contour_array)):
                    # __ contour_array[i][1] : contours y position
                    sub = avg - contour_array[i][1]
                    if sub < 0: # sub = int(np.sqrt(sub * sub))
                        sub *= -1
                    if sub > 80 * h_rate:
                        delete_array.append(i)
                for i in reversed(delete_array):
                    del contour_array[i]
                delete_array.clear()

            contour_y_sum = 0
            for i in range(len(contour_array)):
                contour_y_sum = contour_y_sum + contour_array[i][1]
            try:
                avg = int(contour_y_sum / len(contour_array))
            except ZeroDivisionError:
                print('######')
            print("len contour_array : ", len(contour_array))
            print("contour_array : ", contour_array)
            for i in range(len(contour_array)):
                print("i : ", i)
                # __ (average - contour_y position) < 50 ? bluebox.append : next
                sub = avg - contour_array[i][1]
                if sub < 0: # sub = int(np.sqrt(sub * sub))
                    sub *= -1
                if sub < 50 * h_rate:
                    blue_box.append(contour_array[i])
                    # __debug : check bounding box
                    # cv2.rectangle(
                    #     img_result,
                    #     (contour_array[i][0], contour_array[i][1]),
                    #     (contour_array[i][0] + contour_array[i][2], contour_array[i][1] + contour_array[i][3]),
                    #     (255, 0, 0), 2)
                # ### contour 사이의 거리[D]를 구함 & contour 들의 수직 비율이 일정해야 함.
            if len(blue_box) >= 2:  # ##if len(centers) >= 2: if len(contour_array) >= 2:
                for idx in range(len(blue_box) - 1):
                    dx = blue_box[idx][0] - blue_box[idx + 1][0]
                    dy = blue_box[idx][1] - blue_box[idx + 1][1]
                    D.append(int(np.sqrt(dx * dx + dy * dy)))
            print("D : ", D)
            for i in range(len(D)):
                if self.game_type == "souls" and D[i] < 160 * w_rate: # __ souls
                    fX.append(D[i])
                elif self.game_type == "sekiro" and 160 < D[i] < 165: # __ sekiro
                    fX.append(D[i])
                elif self.game_type == "ring" and D[i] < 50 * w_rate * 2:
                    fX.append(D[i])
            print(fX)
            if self.game_type == "souls" and 5 < len(fX) < 9: # __ souls
                self.save_death_count()
            elif self.game_type == "sekiro" and len(fX) == 1: # __ sekiro
                self.save_death_count()
            elif self.game_type == "ring" and 5 < len(fX) < 9: # __ elden ring
                self.save_death_count()
            contour_array.clear()
            blue_box.clear()
            D.clear()
            fX.clear()

            # __OCR test__
            # text_img = pytesseract.image_to_string(img_result, lang='eng')
            # print(text_img)
            # __debug only__
            # img_resize = cv2.resize(img_result, dsize=(0, 0), fx=0.5, fy=0.5)
            # cv2.imshow("capture", img_resize)
            # cv2.waitKey(1)
            # if key == 0:
            #     cv2.destroyAllWindows()
            #     break

    def save_death_count(self):
        global death_count
        death_count += 1
        with open("유다희.txt", "w") as f:
            f.write(str(death_count))
        sleep(5)


window = UI()
window.title("유다희")
window.geometry("260x450+0+0")
frames = [tkinter.PhotoImage(file="./icon1_save3.gif",
                             format="gif -index %i" %(i)).subsample(2) for i in range(1)]


def draw_gif(idx):
    try:
        frame = frames[idx]
        idx += 1
        gif_label.configure(image=frame)
        window.after(100, draw_gif, idx)
    except Exception:
        idx = 0
        window.after(0, draw_gif, idx)


gif_label = tkinter.Label(window)
gif_label.place(x=0, y=0)
window.after(0, draw_gif, 0)

window.resizable(width = False, height = False)
window.mainloop()