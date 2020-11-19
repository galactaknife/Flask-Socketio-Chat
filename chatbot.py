import datetime

def analyze(message):
    message.strip("//")
    if "time" in message:
        return datetime.datetime.now().strftime("%a, %b %d %Y, %I:%M:%S %p")
    return "Not a command"
