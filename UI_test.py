import tkinter
import DeathCountStart
DCS = DeathCountStart.DeathCountStart


class Init(object):
    def __init__(self, gif_name, gif_frame):
        self.gif_img = gif_name
        self.gif_frame = gif_frame
        self.lower_red1 = (0, 67, 80)
        self.upper_red1 = (5, 255, 255)
        self.lower_red2 = (170, 67, 80)
        self.upper_red2 = (180, 255, 255)
        self.you_died = False
        self.death_count = 0
        self.key = 0
        self.frames = None

    def cheange_gif(self, gif_name, gif_frame):
        self.gif_img = gif_name
        self.gif_frame = gif_frame


class UI(tkinter.Tk):
    def __init__(self):
        self.c_init = Init('./ELDENRING_TITLE.gif', 7)
        tkinter.Tk.__init__(self)
        self.gif_after = 0
        self.gif_frame = self.c_init.gif_frame
        self.after(0, self.died_counter)

        t_label = tkinter.Label(self, text="YOU DIED", font=("times", "16"))
        t_label.place(x=50, y=260)
        self.d_label = tkinter.IntVar(self, self.c_init.death_count)
        count_label = tkinter.Label(self, textvariable=self.d_label, font=("times", "16"))
        count_label.place(x=200, y=260)

        died_label = tkinter.Label(text="Prepare To ELDEN RING", font = ("times"))
        died_label.place(x=50, y=290)
        end_label = tkinter.Label(text="2022.02.25", font=("times"))
        end_label.place(x=93, y=417)

        up_btn1 = tkinter.Button(self, text="up", width=2, command=self.dc_up)
        up_btn1.place(x=202, y=323)
        dn_btn1 = tkinter.Button(self, text="dn", width=2, command=self.dc_dn)
        dn_btn1.place(x=230, y=323)

        button1 = tkinter.Button(self, text="ELDEN RING", width=16, command=self.start_elden_cap)
        button1.place(x=5, y=323)
        button2 = tkinter.Button(self, text="SOULS", width=16, command=self.start_cap)
        button2.place(x=5, y=353)
        button3 = tkinter.Button(self, text="STOP", width=16, command=self.check_end1)
        button3.place(x=131, y=353)
        button4 = tkinter.Button(self, text="SEKIRO", width=16, command=self.start_skr_cap)
        button4.place(x=5, y=383)
        button5 = tkinter.Button(self, text="RESET", width= 16, command=self.reset_data)
        button5.place(x=131, y=383)

    def died_counter(self):
        self.d_label.set(self.c_init.death_count)
        self.after(1000, self.died_counter)

    def dc_up(self):
        self.c_init.death_count += 1
        self.d_label.set(self.c_init.death_count)

    def dc_dn(self):
        if self.c_init.death_count > 0:
            self.c_init.death_count -= 1
        self.d_label.set(self.c_init.death_count)

    def reset_data(self):
        self.c_init.death_count = 0

    def start_cap(self):
        if self.__counting_status == 0:
            self.__counting_status = 1
            self.c_init.key = 1
            self.c_init.cheange_gif("./icon1_save3.gif", 21)
            self.c_init.frames = [tkinter.PhotoImage(
                file=self.c_init.gif_img,
                format="gif -index {}".format(i)
            ).subsample(2) for i in range(self.gif_frame)]

            self.after_cancel(self.gif_after)
            self.gif_after = self.after(self.gif_frame, self.draw_gif, 0, 1)
            death_count_t = DCS("souls", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_elden_cap(self):
        if self.__counting_status == 0:
            self.__counting_status = 1
            self.c_init.key = 1
            self.c_init.cheange_gif('./ELDENRING_TITLE.gif', 7)
            self.c_init.frames = [tkinter.PhotoImage(
                file=self.c_init.gif_img,
                format="gif -index {}".format(i)
            ).subsample(2) for i in range(self.c_init.gif_frame)]

            self.after_cancel(self.gif_after)
            self.gif_after = self.after(self.gif_frame, self.draw_gif, 0, 1)
            death_count_t = DCS("ring", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def start_skr_cap(self):
        global key
        global frames
        global gif_img
        global gif_frame

        if self.__counting_status == 0:
            self.__counting_status = 1
            key = 1
            gif_img = "./icon1_save3.gif"
            self.gif_frame = 21
            frames = [tkinter.PhotoImage(
                file=self.c_init.gif_img,
                format="gif -index {}".format(i)
            ).subsample(2) for i in range(self.c_init.gif_frame)]
            self.after_cancel(self.gif_after)
            self.gif_after = self.after(self.gif_frame, self.draw_gif, 0, 1)
            death_count_t = DCS("sekiro", self.program_quit)
            death_count_t.daemon = True
            death_count_t.start()

    def check_end1(self):
        global frames
        global key

        frames = [tkinter.PhotoImage(file=gif_img,
                                     format="gif -index 0").subsample(2)]
        self.after_cancel(self.gif_after)  # 이전 after 제거
        self.gif_after = self.after(100, self.draw_gif, 0, 0)
        if key == 1:
            key = 0
            self.__counting_status = 0

    def draw_gif(self, idx, flag):
        if idx == self.gif_frame:
            idx = 0
        frame = frames[idx]
        gif_label.configure(image=frame)
        if flag == 0:
            return 0
        idx += 1
        self.after_cancel(self.gif_after)  # 이전 after 제거
        self.gif_after = self.after(100, self.draw_gif, idx, 1)


if __name__ == '__main__':
    window = UI()
    window.title("유다희")
    window.geometry("260x450+0+0")
    frames = [tkinter.PhotoImage(
        file=window.c_init.gif_img,
        format="gif -index 0"
    ).subsample(2)]
    gif_label = tkinter.Label(window)
    gif_label.place(x=0, y=0)
    # window.gif_after = window.after(0, window.draw_gif, 0, 0)
    window.resizable(width=False, height=False)
    window.mainloop()