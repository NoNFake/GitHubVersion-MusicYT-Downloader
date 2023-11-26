# This is a sample Python script.
# https://dev.to/shittu_olumide_/how-to-download-youtube-music-and-videos-with-python-37k5
#
# I use 'argparse', 'pytube' and 'telebot' libraries
#

# test for android


import telebot              # pip install telebot
from pytube import YouTube  # pip install pytube
import io
from PIL import Image       # pip install pillow
import requests             # pip install request
import json
# from pydub import AudioSegment


''' Token '''
json_file = "token.json"
with open(json_file, 'r') as f:
    data = json.load(f)
    bot_token = data['bot']['token']

    channel_token = data['channel']['token']

bot = telebot.TeleBot(bot_token)
channel_id = channel_token

print(f"Channel ID: {channel_id}")
print(f"Bot Token: {bot_token}")

def AudioDownload(url):
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True,
                                        abr="128kbps").first()  # вибираємо потік аудіо з якістю 128kbps

    if audio_stream:
        audio_bytes = io.BytesIO()
        audio_stream.stream_to_buffer(audio_bytes)
        audio_bytes.seek(0)

        video_title = video.title

        # отримуємо обкладинку відео
        response = requests.get(video.thumbnail_url)
        img = Image.open(io.BytesIO(response.content))

        cover_bytes = io.BytesIO()

        img.save(cover_bytes, format='JPEG')
        cover_bytes.seek(0)

        return audio_bytes, video_title, cover_bytes
    else:
        return None, None, None


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name  # https://qna.habr.com/q/410443

    reply = f"Welcome {first_name}!\nI help download music from youtube for you!\nSend link!"
    bot.send_message(user_id, reply)


@bot.message_handler(func=lambda message: True)
def music(message):
    user_id = message.from_user.id
    user_message = message.text
    username = message.from_user.username #username rxample @user

    action = f"@{username} send link: {user_message}"
    bot_send_to_user = f"Bot send file to @{username}"
    bot_send_to_channel = f"Bot send file to {channel_id}"

    text = f"@{username} send link: {user_message}\nBot send file to @{username}\nBot send file to {channel_id}"

    print(action)

    if user_message.startswith(("https://www.youtube.com", "https://youtu.be")):  # with .com or without
        audio_bytes, video_title, cover_bytes = AudioDownload(user_message)
        if audio_bytes:

            audio_name = f"{video_title}.aac"
            '''
            AAC (Advanced Audio Coding, усовершенствованное кодирование звука) – аналог MP3, 
            который за счет более оптимального алгоритма кодирования позволяет сохранить звучание более качественным. 
            '''


            # Скидує користувачу
            audio_data = audio_bytes.read()
            user_send = bot.send_audio(user_id, audio_data, title=video_title, thumb=cover_bytes, performer="YouTube")


            print(bot_send_to_user)

            # Скидує аудіо у групу

            channel_send = bot.send_audio(channel_token, audio_data, title=video_title, thumb=cover_bytes, performer="YouTube")
            bot.send_message(channel_token, text, disable_notification=True)
            print(bot_send_to_channel)

            return channel_send


        else:
            bot.send_message(user_id, "Please send a valid YouTube link.")
    else:
        bot.send_message(user_id, "Please send a valid YouTube link.")



if __name__ == '__main__':
    print("Bot is starting!\n")
    bot.polling(none_stop=True)

