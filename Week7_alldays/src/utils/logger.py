import datetime

def log(message):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {message}")