from bs4 import BeautifulSoup
import requests
import urllib
import telebot
from telebot.types import Message
import os.path

TOKEN = 'YOUR_TOKEN'

bot = telebot.TeleBot(TOKEN)

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

# bot.polling()

@bot.message_handler(commands=['start', 'help'])
def echo_digits(message: Message):
	bot.reply_to(message, 'Отправь ссылку на видео из Instagram, чтобы скачать его')
	return


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def insta_video(message: Message):
	print(message.text)
	# bot.reply_to(message, 'Are you dolbaeb? Yes you are dolbaeb Mis Nurullo')
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
	page = requests.get(message.text, headers=headers)
	print(1)

	print(page.text)
	soup = BeautifulSoup(page.text, 'html.parser')
	video_meta = soup.find('meta', property='og:video')
	print(video_meta['content'])
	print(2)

	firstpos=video_meta['content'].rfind("/")
	lastpos=video_meta['content'].rfind(".")
	video_name = video_meta['content'][firstpos+1:lastpos]
	vv = video_name.split('?', 1)
	video_name = vv[0]
	video_link = video_meta['content']
	print(video_name)
	# video = open(video_name, 'rb')
	print(str(message.chat.id) + ' ' + video_name)
	# print(os.path.isfile(video_name))
	if os.path.isfile(video_name)==False:
		urllib.request.urlretrieve(video_link, video_name)
		video = open(video_name, 'rb')
		bot.send_video(message.chat.id, video, timeout=60)
	else:
		video = open(video_name, 'rb')
		bot.send_video(message.chat.id, video, timeout=60)
	return


bot.polling()