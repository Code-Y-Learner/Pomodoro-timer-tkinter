from tkinter import *
from tkinter import messagebox
import math
import itertools
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
pause = False
toggle_pause_unpause = itertools.cycle(["pause","unpause"])
toggle_start_reset = itertools.cycle(["Reset","Start"])
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    logo.config(text='Timer',fg=GREEN)
    canvas.itemconfig(timer_text,text="00:00")
    check.config(text='')
    global  reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN* 60
    short_break_sec = SHORT_BREAK_MIN *60
    long_break_sec = LONG_BREAK_MIN* 60
    if reps ==8:
        count_down(long_break_sec)#long
        logo.config(text='Finish',fg=RED)
        ask = messagebox.askquestion(title="Alarm", message="Finish")
        reset_timer()
    elif reps % 2 ==0:
        count_down(short_break_sec)#short_break_sec
        logo.config(text='Break',fg=PINK)
        on_pause_unpause_button_clicked()
        ask = messagebox.askquestion(title="Alarm", message="Take a break")
        if ask == 'yes':
            on_pause_unpause_button_clicked()

    elif reps ==1:
        count_down(work_sec)#work_sec
        logo.config(text='Work',fg=GREEN)
    else:
        count_down(work_sec)#work_sec
        logo.config(text='Work',fg=GREEN)
        on_pause_unpause_button_clicked()
        ask = messagebox.askquestion(title="Alarm", message="Go back to work")
        if ask == 'yes':
            on_pause_unpause_button_clicked()


def on_pause_unpause_button_clicked():
    action = next(toggle_pause_unpause)
    global pause
    if action == 'pause':
        pause = True
    elif action == 'unpause':
        pause = False

def toggle():
    start_reset_now = next(toggle_start_reset)
    start_button.config(text=start_reset_now)
    if start_reset_now == 'Reset':
        start_timer()
    elif start_reset_now == 'Start':
        reset_timer()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = '0'+str(count_sec)
    if count_sec ==0:
        count_sec ='00'

    canvas.itemconfig(timer_text,text = f"{count_min}:{count_sec}")
    if count >0:
        global timer
        if pause == False:
            timer = window.after(1000,count_down,count - 1)
        elif pause == True:
            timer = window.after(0,count_down,count)
    else:
        start_timer()
        check_time = math.floor((reps-1) / 2)
        check.config(text = '✓'*check_time)



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Pomodoro')
window.wm_attributes("-topmost", 1)
window.config(padx=10,pady=10,bg=YELLOW)

#canvas
canvas = Canvas(width=100,height=112,bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(50,56,image=tomato_img)
timer_text = canvas.create_text(50,70,text='00:00',fill='white',font=(FONT_NAME,22,'bold'))
canvas.grid(column=1,row=1)



#label
logo = Label(text='Timer',fg=GREEN,bg=YELLOW,font=(FONT_NAME,27,'bold'))
logo.grid(column=1,row=0)

check = Label(bg=YELLOW,fg=GREEN,font=(FONT_NAME,11))
check.grid(column=1,row=3)
#button
start_button = Button(text="Start",command=toggle,highlightthickness=0)
start_button.grid(column=0,row=2)


pause_button = Button(text='pause',command=on_pause_unpause_button_clicked,highlightthickness=0)
pause_button.grid(column=2,row=2)



window.mainloop()