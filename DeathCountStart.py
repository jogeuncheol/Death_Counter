import threading
import cv2
import numpy as np
import mss
import time
from time import sleep


class DeathCountStart(threading.Thread):
    def __init__(self, game_type, c_init):
        threading.Thread.__init__(self)
        self.game_type = game_type
        self.lower_red1 = (0, 67, 80)
        self.upper_red1 = (5, 255, 255)
        self.lower_red2 = (170, 67, 80)
        self.upper_red2 = (180, 255, 255)
        self.c_init = c_init

    def run(self):
        with mss.mss() as sct:
            frame_number = 0
            while self.c_init.key == 1:
                start = time.time()
                # start_time = time.perf_counter()
                # __red color mask__
                # __DARK SOULS 1, 2, 3__ __DEMONS SOULS REMAKE__ __SEKIRO SHADOW DIE TWICE__
                # img_ori = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGRA2RGB)
                img_ori = np.array(sct.grab(sct.monitors[1]))
                original_image = img_ori
                img_ori = cv2.resize(
                    img_ori,
                    dsize=(960, 540),
                    interpolation=cv2.INTER_AREA
                ) # 이미지 리사이즈 디버그 용이

                img_hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
                img_mask = cv2.inRange(img_hsv, self.lower_red1, self.upper_red1)
                img_mask2 = cv2.inRange(img_hsv, self.lower_red2, self.upper_red2)
                img_mask3 = img_mask + img_mask2
                img_result = cv2.bitwise_and(img_ori, img_ori, mask=img_mask3)
                contours, _ = cv2.findContours(img_mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                height, width, channels = img_ori.shape
                resol_w_rate = width / 1920
                resol_h_rate = height / 1080
                # print(height, width, resol_h_rate, resol_w_rate)
                # 사각형 박스
                fX = []
                centers = []
                center_append = centers.append
                D = []
                D_append = D.append
                contour_array = []
                contour_array_append = contour_array.append
                blue_box = []
                blue_box_append = blue_box.append
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)  # 수직인 사각형 생성
                    if self.game_type == "souls" and 70 * resol_h_rate < h < 140 * resol_h_rate and 10 * resol_w_rate < w < 110 * resol_w_rate:
                        contour_array_append([x, y, w, h])
                    elif self.game_type == "sekiro" and 200 < h < 350 and 50 < w < 350:
                        contour_array_append([x, y, w, h])
                    elif self.game_type == "ring" and 50 * resol_h_rate < h < 80 * resol_h_rate and 10 * resol_w_rate < w < 80 * resol_w_rate:
                        contour_array_append([x, y, w, h])
                        M = cv2.moments(cnt)
                        try:
                            cX = int(M['m10'] / M['m00'])
                            cY = int(M['m01'] / M['m00'])
                            # centers.append([cX, cY])
                            center_append([cX, cY])
                            cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        except ZeroDivisionError:
                            print('######')
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
                        # print('######')
                    # print("avg : ", avg)
                    for i in range(len(contour_array)):
                        # __ contour_array[i][1] : contours y position
                        sub = avg - contour_array[i][1]
                        if sub < 0: # sub = int(np.sqrt(sub * sub))
                            sub *= -1
                        if sub > 80 * resol_h_rate:
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
                    # print('######')
                # print("len contour_array : ", len(contour_array))
                # print("contour_array : ", contour_array)
                for i in range(len(contour_array)):
                    # print("i : ", i)
                    # __ (average - contour_y position) < 50 ? bluebox.append : next
                    sub = avg - contour_array[i][1]
                    if sub < 0: # sub = int(np.sqrt(sub * sub))
                        sub *= -1
                    if sub < 50 * resol_h_rate:
                        blue_box_append(contour_array[i])
                        # blue_box.append(contour_array[i])
                        # __debug : check bounding box
                        cv2.rectangle(
                            img_ori,
                            (contour_array[i][0], contour_array[i][1]),
                            (contour_array[i][0] + contour_array[i][2], contour_array[i][1] + contour_array[i][3]),
                            (255, 0, 0), 2)
                    # ### contour 사이의 거리[D]를 구함 & contour 들의 수직 비율이 일정해야 함.
                if len(blue_box) >= 2:  # ##if len(centers) >= 2: if len(contour_array) >= 2:
                    for idx in range(len(blue_box) - 1):
                        dx = blue_box[idx][0] - blue_box[idx + 1][0]
                        dy = blue_box[idx][1] - blue_box[idx + 1][1]
                        D.append(int(np.sqrt(dx * dx + dy * dy)))
                # print("D : ", D)
                for i in range(len(D)):
                    if self.game_type == "souls" and D[i] < 80 * resol_w_rate * 2: # __ souls
                        fX.append(D[i])
                    elif self.game_type == "sekiro" and 160 < D[i] < 165: # __ sekiro
                        fX.append(D[i])
                    elif self.game_type == "ring" and D[i] < 50 * resol_w_rate * 2:
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
                # cv2.imshow("display", img_ori)
                # print("FPS : {:.2f}".format(1 / (time.time() - start)))
                frame_number += 1

    def save_death_count(self, original_image):
        # save_img = original_image
        self.c_init.death_count += 1
        # time_now = datetime.datetime.now()
        # time_path = time_now.strftime("%Y-%m-%d_%H%M%S_")
        # save_img_path = "save_img/" + time_path + str(death_count) + ".png"
        # cv2.imwrite(save_img_path, save_img)
        # UI.death_count = self.death_count
        # print("class UI() private variable : ", UI.death_count)
        with open(self.c_init.output_path, "w", encoding='utf-8') as f:
            f.write("YOU DIED : " + str(self.c_init.death_count))
        sleep(5)