# This is a sample Python script.
# https://dev.to/shittu_olumide_/how-to-download-youtube-music-and-videos-with-python-37k5
#
# I use 'argparse', 'pytube' and 'telebot' libraries
#

import telebot              # pip install telebot
from pytube import YouTube  # pip install pytube
import io
from PIL import Image       # pip install pillow
import requests             # pip install request
import json

json_file = "token.json"

class YouTube_Bot:
    def __init__(self, json_file):
        self.load_token(json_file)
        self.bot = telebot.TeleBot(self.bot_token)
        self.channel_id = self.channel_token
        self.privileges = []


    def load_token(self, json_file):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                self.bot_token = data['bot']['token']

                self.channel_token = data['channel']['token']
        except Exception as e:
            print(f"Bot token is NULL, please check file {json_file}")

    @staticmethod
    def audio_download(url):
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True,
                                            abr="128kbps").first()
        # вибираємо потік аудіо з якістю 128kbps

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


    # bot.message_handler(commands=['start'])
    def start_messeges(self, message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name  # https://qna.habr.com/q/410443

        reply = f"Welcome {first_name}!\nI help download music from youtube for you!\nSend link!"
        self.bot.send_message(user_id, reply)

    # @bot.message_handler(func=lambda message: True)
    def send_music(self, message):
        user_id = message.from_user.id
        user_message = message.text
        username = message.from_user.username  # username rxample @user

        action = f"@{username} send link: {user_message}"
        bot_send_to_user = f"Bot send file to @{username}"
        bot_send_to_channel = f"Bot send file to {self.channel_id}"

        text = f"@{username} send link: {user_message}\nBot send file to @{username}\nBot send file to {self.channel_id}"

        print(action)

        try:
            if user_message.startswith(("https://www.youtube.com", "https://youtu.be")):  # with .com or without
                audio_bytes, video_title, cover_bytes = self.audio_download(user_message)
                if audio_bytes:

                    audio_name = f"{video_title}.aac"
                    '''
                    AAC (Advanced Audio Coding, усовершенствованное кодирование звука) – аналог MP3, 
                    который за счет более оптимального алгоритма кодирования позволяет сохранить звучание более качественным. 
                    '''

                    # Скидує користувачу
                    audio_data = audio_bytes.read()
                    user_send = self.bot.send_audio(user_id, audio_data, title=video_title, thumb=cover_bytes,
                                                    performer="YouTube")

                    print(bot_send_to_user)

                    # Скидує аудіо у групу

                    channel_send = self.bot.send_audio(self.channel_token, audio_data, title=video_title, thumb=cover_bytes,
                                                       performer="YouTube")
                    self.bot.send_message(self.channel_token, text, disable_notification=True)
                    print(bot_send_to_channel)

                    return channel_send


                else:
                    self.bot.send_message(user_id, "Please send a valid YouTube link.")
            else:
                self.bot.send_message(user_id, "Please send a valid YouTube link.")
        except Exception as e:
            self.bot.send_message(user_id, "Please send a valid YouTube link.")

    def random_music(self, message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name

        import random
        # https://music.youtube.com/watch?v= VPUpkaHFwWM = 11
        lower_case = "qwertyuiopasdfghjklzxcvbnm"
        upper_case = "QWERTYUIOPASDFGHJKLZXCVBNM"

        gen_url = lower_case + upper_case
        length_url = 11

        url = "https://www.youtube.com/watch?v=" + "".join(random.sample(gen_url, length_url))

        # self.send_music(url)
        self.bot.send_message(user_id, url)


    def run_bot(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_messeges(message)

        @self.bot.message_handler(commands=['random'])
        def random(message):
            self.random_music(message)

        @self.bot.message_handler(func=lambda message: True)
        def music(message):
            self.send_music(message)




        print("Bot is starting!\n")
        self.bot.polling(none_stop=True)



class User(YouTube_Bot):
    pass


if __name__ == '__main__':
    youtube_bot = YouTube_Bot(json_file)
    youtube_bot.run_bot()
