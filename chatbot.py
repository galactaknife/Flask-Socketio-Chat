import datetime, random
combinations = []

# If command is detected, analyze message using chatbot
def analyze(message, name):
    message.strip("//").lower()
    # Gets time
    if "time" in message:
        return str(datetime.datetime.now().strftime("%a, %b %d, %Y, %I:%M:%S %p"))
    # Does combination
    elif "combo" in message:
        if "&" in message:
            msg = str(message).replace("combo", '').replace("//", '').replace(' ', '')
            msg = list(msg.split('&'))
            return comboCalc(msg[0], msg[1])
        else:
            return "Missing '&'"
    # Gets random number between parameters
    elif "random" in message:
        if "&" in message:
            msg = str(message).replace("random", '').replace("//", '').replace(' ', '')
            msg = list(msg.split('&'))
            try:
                new = [int(msg[0]), int(msg[1])]
                if abs(max(new) - min(new)) >= 500:
                    return "Max number difference is 500.  Your difference is " + str(abs(max(new) - min(new)))
                else:
                    return str(random.choice(list(range(min(new), max(new)))))
            except:
                return "Enter valid numbers"
        else:
            return "Missing '&'"
    elif "about" in message and "you" in message:
        return "I was created to monitor this chat"
    elif "joke" in message and "tell" in message:
        return random.choice(["Your life", "When life gives you melons, you're probably dyslexic", "I asked my North Korean friend how it was up there, he said he couldn't complain.", "Whiteboards are remarkable", "I want to die peacefully like my grandfather.  Not screaming and yelling like the passengers in his car.", "I have the heart of a lion and a lifetime ban from the Toronto Zoo", "An apple a day keeps the doctor away, only if you aim it well."])
    # Sends image
    elif "image" in message:
        msg = str(message).replace("image", '').replace("//", '', 1).replace(' ', '')
        return "<img width='200' src='"+ msg +"' alt='Image not found'>"
    elif "ban" in message and "chatbot" in message:
        return "Can't ban chatbot"
    elif "ban" in message:
        return "You don't have permission to ban"
    # Changes display settings
    elif "change" in message:
        msg = list(message.split('='))
        # Sets settings to default
        if not len(msg) == 2:
            if "default" in message:
                return "<style>body {color: black !important; background-color: white;} #messages p:nth-child(even) {background-color: #ededed;} #sendArea {background-color: white !important; color: black;} td, th { border: 1px solid black;} #messages p { color: black; font-family: Helvetica; font-size: 13px;} #uploadImage { filter: invert(0%); } .command { background-color: #ebebeb !important; color: black; border-color: #dbdbdb; }</style>Reset your settings to default", "update"
            return "Specify a valid changable element", "update"
        # Changes values
        elif "color" in message:
            return "<style>#messages p { color: " + str(msg[1]) + ";}</style>Your color is now " + str(msg[1]), "update"
        elif "font-size" in message:
            try:
                return "<style>#messages p { font-size:" + str(int(msg[1])) + "px;}</style>Your font size is now " + str(msg[1]), "update"
            except:
                return "Invalid font size", "update"
        elif "font" in message:
            return "<style>#messages p { font-family:" + str(msg[1]) + ";}</style>Your font is now " + str(msg[1]), "update"
        # Changes theme
        elif "theme" in message:
            if "dark" in message:
                return "<style>body {color: gainsboro !important; background-color: #1f1f1f} #messages p:nth-child(even) {background-color: #3b3b3b;} #sendArea {background-color: #4a4a4a !important; color: white;} td, th { border: 1px solid gainsboro;} #messages p { color: white;} #uploadImage { filter: invert(100%); } .command { background-color: #2e2e2e !important; color: white; border-color: #4d4d4d; }</style>Your theme is now dark", "update"
            elif "light" in message:
                return "<style>body {color: black !important; background-color: white} #messages p:nth-child(even) {background-color: #ededed;} #sendArea {background-color: white !important; color: black;} td, th { border: 1px solid black;} #messages p { color: black;} #uploadImage { filter: invert(0%); } .command { background-color: #ebebeb !important; color: black; border-color: #dbdbdb; }</style>Your theme is now light", "update"
            return "Invalid theme.  Valid themes are dark and light"
        return "Specify a valid changable element", "update"
    return "Not a command"

def comboCalc(name1, name2):
  # Checks if combination already exists
  for combo in combinations:
    if name1 in combo["names"] and name2 in combo["names"]:
      return "Match data for " + combo["names"][0] + " and " + combo["names"][1] + ": " + str(combo["calc"]) + '%'
  # If not, create new combination
  new = {"names" : [name1, name2], "calc" : random.choice(list(range(0, 100)))}
  combinations.append(new)
  return "Match data for " + new["names"][0] + " and " + new["names"][1] + ": " + str(new["calc"]) + '%'
