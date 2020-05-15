import requests
import re
import time
import json

import telebot

from telebot import types
from telebot import apihelper

apihelper.proxy = {'http':'http://10.10.1.10:3128'}

def extract_video_data(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
	}
	r = requests.get(url, headers = headers)
	t = r.text.split('<script id="__NEXT_DATA__" type="application/json" crossorigin="anonymous">')[-1].split("</script>")[0]
	return json.loads(t)

def get_video_data(url):
	video_data = extract_video_data(url)

	r = str(requests.get(video_data["props"]["pageProps"]["videoData"]["itemInfos"]["video"]["urls"][0]).content)
	s = r.find("vid:")
	video_data["clear_video_url"] = "https://api2.musical.ly/aweme/v1/playwm/?video_id=" + r[s+4:s+36]
	return video_data

# print(get_video_url(link))

bot = telebot.TeleBot('1218133433:AAFy3NhPnjiYTZ_pCaCUTcnMZogZAmaDbZ0')

@bot.message_handler(content_types=['text'])
def start_message(message):
	if "tiktok.com/" in message.text:
		bot.send_video(message.chat.id, get_video_url(message.text))

@bot.inline_handler(func=lambda query: len(query.query) > 0 and "tiktok.com/" in query.query)
def inline_message(query):
	try:
		video_data = get_video_data(query.query)
		r = types.InlineQueryResultVideo(
				id='1',
				title="TikTok Downloader",
				video_url = video_data["clear_video_url"],
				mime_type = "video/mp4",
				thumb_url = video_data["props"]["pageProps"]["videoObjectPageProps"]["videoProps"]["thumbnailUrl"][0]
		)
		bot.answer_inline_query(query.id, [r])
	except Exception as e:
		print(e)

while True:
	try:
		bot.polling()
	except:
		pass