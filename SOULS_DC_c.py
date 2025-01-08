# from PIL import ImageGrab
from time import sleep
import datetime
import tkinter
import threading
import cv2
import numpy as np
import mss
import os

# testing 67, 67
lower_red1 = (0, 67, 80)
upper_red1 = (5, 255, 255)
lower_red2 = (170, 67, 80)
upper_red2 = (180, 255, 255)

you_died = False
death_count = 0
key = 0

output_path = os.getcwd().replace('\\', '/') + '/YOU_DIED.txt'
try:
    f = open(output_path, 'r', encoding='utf-8')
except:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("YOU DIED : 0\n")
else:
    died_str = f.readlines()
    died_str = died_str[-1].split(' ')
    death_count = int(died_str[-1])
finally:
    f.close()


class UI(tkinter.Tk):
    global death_count
    program_quit = 0
    __counting_status = 0

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.after(0, self.die_counter)

        self.t_label = tkinter.Label(self, text="YOU DIED ", font=("times", "16"))
        self.t_label.place(x=50, y=260-260)
        self.d_label = tkinter.IntVar(self, death_count)
        self.sub_window = None
        count_label = tkinter.Label(self, textvariable=self.d_label, font=("times", "16"))
        count_label.place(x=200, y=260-260)

        died_label = tkinter.Label(text="Prepare To ELDEN RING", font=("times"))
        died_label.place(x=50, y=290-260)
        end_label = tkinter.Label(text="2022.02.25", font=("times"))
        end_label.place(x=93, y=417-260)

        up_btn1 = tkinter.Button(self, text="up", width=2, command=self.dc_up)
        up_btn1.place(x=202, y=323-260)
        dn_btn1 = tkinter.Button(self, text="dn", width=2, command=self.dc_dn)
        dn_btn1.place(x=229, y=323-260)

        button1 = tkinter.Button(self, text="ELDEN RING", width=16, command = self.start_elden_cap)
        button1.place(x=5, y=323-260)
        button2 = tkinter.Button(self, text="SOULS", width=16, command = self.start_cap)
        button2.place(x=5, y=353-260)
        button3 = tkinter.Button(self, text="STOP", width=16, command = self.check_end1)
        button3.place(x=131, y=353-260)
        button4 = tkinter.Button(self, text="SEKIRO", width=16, command=self.start_skr_cap)
        button4.place(x=5, y=383-260)
        button5 = tkinter.Button(self, text="RESET", width=16, command=self.reset_data)
        button5.place(x=131, y=383-260)
        button6 = tkinter.Button(self, text="TOP WINDOW", width=34, command=self.create_top_level_window)
        button6.place(x=5, y=185)

    def die_counter(self):
        self.d_label.set(death_count)
        # print("die_counter fn : ", self.d_label.get())
        self.after(1000, self.die_counter)

    def dc_up(self):
        global death_count
        death_count += 1
        self.d_label.set(death_count)

    def dc_dn(self):
        global death_count
        if death_count > 0:
            death_count -= 1
        self.d_label.set(death_count)

    def reset_data(self):
        global death_count
        death_count = 0
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%Y-%m-%d_%H%M%S_") + "YOU DIED : 0\n"
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(time_str)

    def start_cap(self):
        global key

        self.t_label.config(fg="red")
        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            death_count_t = DeathCountStart("souls", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_elden_cap(self):
        global key

        self.t_label.config(fg="red")
        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            death_count_t = DeathCountStart("ring", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_skr_cap(self):
        global key

        self.t_label.config(fg="red")
        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            death_count_t = DeathCountStart("sekiro", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def check_end1(self):
        global death_count
        global key

        self.t_label.config(fg="black")
        if key == 1:
            key = 0
            self.__counting_status = 0
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%Y-%m-%d_%H%M%S_") + "YOU DIED : " + str(death_count) + "\n"
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(time_str)

    def create_top_level_window(self):
        self.sub_window = tkinter.Toplevel(window)
        self.sub_window.geometry('260x50+0+0')
        self.sub_window.attributes('-topmost', 'true')
        self.sub_window.resizable(width=False, height=False)

        t_label = tkinter.Label(self.sub_window, text="YOU DIED ", font=("times", "16"))
        t_label.place(x=50, y=260 - 260)
        you_died_label = tkinter.Label(self.sub_window, textvariable=self.d_label, font=("times", "16"))
        you_died_label.place(x=200, y=260-260)


class DeathCountStart(threading.Thread):
    def __init__(self, game_type, program_quit):
        threading.Thread.__init__(self)
        self.game_type = game_type
        self.program_quit = program_quit

    def run(self):
        global key
        with mss.mss() as scr:
            while key == 1:
                # start = time.time()
                # __red color mask__
                # __DARK SOULS 1, 2, 3__ __DEMONS SOULS REMAKE__ __SEKIRO SHADOW DIE TWICE__
                # img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGRA2RGB)
                img_ori = np.array(scr.grab(scr.monitors[1]))
                original_image = img_ori
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
                        avg = 0
                    # print("avg : ", avg)
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
                    avg = 0
                # print("len contour_array : ", len(contour_array))
                # print("contour_array : ", contour_array)
                for i in range(len(contour_array)):
                    # print("i : ", i)
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
                # print("D : ", D)
                for i in range(len(D)):
                    if self.game_type == "souls" and D[i] < 160 * w_rate: # __ souls
                        fX.append(D[i])
                    elif self.game_type == "sekiro" and 160 < D[i] < 165: # __ sekiro
                        fX.append(D[i])
                    elif self.game_type == "ring" and D[i] < 50 * w_rate * 2:
                        fX.append(D[i])
                # print(fX)
                if self.game_type == "souls" and 5 < len(fX) < 9: # __ souls
                    self.save_death_count(original_image)
                elif self.game_type == "sekiro" and len(fX) == 1: # __ sekiro
                    self.save_death_count(original_image)
                elif self.game_type == "ring" and 5 < len(fX) < 9: # __ elden ring
                    self.save_death_count(original_image)
                contour_array.clear()
                blue_box.clear()
                D.clear()
                fX.clear()
                # print("FPS : {:.2f}".format(1 / (time.time() - start)))

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

    def save_death_count(self, original_image):
        global death_count
        global output_path
        death_count += 1
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("YOU DIED : " + str(death_count) + "\n")
        time_now = datetime.datetime.now()
        time_path = time_now.strftime("%Y-%m-%d_%H%M%S_")
        save_img_path = "save_img/" + time_path + str(death_count) + ".png"
        cv2.imwrite(save_img_path, original_image)
        sleep(5)


window = UI()
window.title("유다희")
window.geometry("260x220+0+0")

gif_label = tkinter.Label(window)
gif_label.place(x=0, y=0)

window.resizable(width=False, height=False)
window.mainloop()
