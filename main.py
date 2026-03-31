import telebot
import google.generativeai as genai

# KONFIGURATSIYA (To'g'ridan-to'g'ri kod ichida)
TELEGRAM_TOKEN = '8755643277:AAEdLlmZAG2jgEaO3IHh31LRJk0XfJ6aI6o'
GEMINI_API_KEY = 'AIzaSyDc8M5vYtKyr5qbun7YgIsin4Kepke7e6Y'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Botni sozlash
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# START BUYRUG'I
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing!")

# XABARLARNI QAYTA ISHLASH
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_question = message.text
    chat_id = message.chat.id
    
    # "O'ylayapman" xabarini yuborish
    wait_message = bot.send_message(chat_id, "⏳ O'ylayapman...")
    
    try:
        # Gemini-dan javob olish
        response = model.generate_content(user_question)
        ai_answer = response.text
        
        # "O'ylayapman"ni o'chirib, javobni yozish
        bot.edit_message_text(ai_answer, chat_id, wait_message.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik yuz berdi: {str(e)}", chat_id, wait_message.message_id)

# Botni yurgizish
if __name__ == '__main__':
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()


