import urllib.request
import os
import pandas as pd # pip install pandas openpyxl
from pushbullet import Pushbullet # pip install pushbullet.py

# API KEY PushBullet (https://www.pushbullet.com/)
API_KEY = "YOUR_API_KEY"

# Get Link to Chatfile from Pushbullet
pb = Pushbullet(API_KEY)
pushes = pb.get_pushes()
latest = pushes[0]

# Download Chatfile
url = latest['file_url']
file_path = "chat.txt"
urllib.request.urlretrieve(url, file_path)

# read file by lines
with open(file_path, mode='r', encoding="utf8") as f:
    data = f.readlines()

# FOUND ON GITHUB: https://gist.github.com/kwcooper/a21ba58272d3cdf26310cc02ee4b168f
# parse text, create list of lists structure & remove first whatsapp info message
dataset = data[1:]
cleaned_data = []
for line in dataset:
    # Check, whether it is a new line or not
    # If the following characters are in the line -> assumption it is NOT a new line
    if '/' in line and ':' in line and ',' in line and '-' in line:
        # grab the info and cut it out
        date = line.split(",")[0]
        line2 = line[len(date):]
        time = line2.split("-")[0][2:]
        line3 = line2[len(time):]
        name = line3.split(":")[0][4:]
        line4 = line3[len(name):]
        message = line4[6:-1] # strip newline charactor
        cleaned_data.append([date, time, name, message])

    # else, assumption -> new line. Append new line to previous 'message'
    else:
        new = cleaned_data[-1][-1] + " " + line
        cleaned_data[-1][-1] = new

# Create the DataFrame
df = pd.DataFrame(cleaned_data, columns = ['Date', 'Time', 'Name', 'Message'])

# Save it!
df.to_excel('chat_history.xlsx', index=False)
