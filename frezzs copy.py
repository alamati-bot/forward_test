import telebot
import requests
import unzip_files
import time

tokkk = "7476729104:AAEu170XzJxZ_lrQh2Cs8rfCS_EXOGD1-Jw"

bot_mark = telebot.TeleBot(tokkk)

def download_file_zip(file_id, file_name, chat_id):
    file_info = bot_mark.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{tokkk}/{file_info.file_path}"

    response = requests.get(file_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
            bot_mark.send_message(chat_id,f"File {file_name} downloaded successfully.")
    else:
        bot_mark.send_message(chat_id,"Failed to download the file.")


@bot_mark.message_handler(func=lambda message: True)
def jdhjsh(message):
    idd = message.chat.id 


@bot_mark.message_handler(content_types=['document'])
def add_new_marks(message):
    idd = message.chat.id 
    file_id = message.document.file_id
    file_name = message.document.file_name
    print(idd)
    time.sleep(7)
    print(file_id)
    time.sleep(4)
    print(file_name)
    

# bot_mark.send_message(-1002200061837,"He loves you too")

bot_mark.polling()