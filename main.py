import os
import telebot
import google.generativeai as genai

# SOZLAMALAR
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("XATO: TELEGRAM_TOKEN yoki GEMINI_API_KEY topilmadi!")
    exit()

# GOOGLE GEMINI SOZLASI
genai.configure(api_key=GEMINI_API_KEY)
# Pro modeli barqaror ishlaydi
model = genai.GenerativeModel('gemini-1.5-flash')

# TELEGRAM BOT SOZLASI
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# BOT LOGIKASI
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Asadbek Norboyev tomonidan yaratilgan aqlli yordamchi botman. Savolingizni yuboring.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_question = message.text
    chat_id = message.chat.id
    
    wait_message = bot.send_message(chat_id, "O'ylayapman...")

    try:
        # AI-ga kim yaratganini eslatib turuvchi topshiriq
        prompt = f"Sen Asadbek Norboyev tomonidan yaratilgan aqlli yordamchi botsan. Savolga o'zbek tilida aniq javob ber. Savol: {user_question}"
        
        response = model.generate_content(prompt)
        ai_answer = response.text
        bot.edit_message_text(ai_answer, chat_id, wait_message.message_id)
    except Exception as e:
        bot.edit_message_text(f"Xatolik yuz berdi: {str(e)}", chat_id, wait_message.message_id)

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()

