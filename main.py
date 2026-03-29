import os
import telebot
import google.generativeai as genai

# === SOZLAMALAR (Agent buni limit yangilanishi bilan to'ldiradi) ===
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')  # BotFather'dan olingan token
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')  # Google AI Studio'dan olingan API key

# === AGENT UCHUN ESLATMA: Iltimos, Token va API keyni sozlang ===
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("❌ XATO: TELEGRAM_TOKEN yoki GEMINI_API_KEY topilmadi!")
    print("Limit yangilanishi bilan Agent bularni sozlashi kerak.")
    exit() # Agar kalitlar bo'lmasa, botni to'xtatish

# === GOOGLE GEMINI SOZLASI ===
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Biz 'gemini-1.5-flash' modelidan foydalanamiz, u tezroq va bepul limitlari yaxshi.
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"❌ Gemini AI'ni sozlashda xato: {e}")
    exit()

# === TELEGRAM BOT SOZLASI ===
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# === BOT LOGIKASI ===

# 1. '/start' buyrug'ini qabul qilish
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Assalomu alaykum! Men Ajavob botman. 👋\n\n"
        "Menga har qanday matematik misolni (matn ko'rinishida) yozing, "
        "men uni Google Gemini AI yordamida yechib beraman."
    )
    bot.reply_to(message, welcome_text)

# 2. Matnli xabarlarni qabul qilish va AI'ga yuborish
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_question = message.text
    chat_id = message.chat.id
    
    # Foydalanuvchiga bot o'ylayotganini ko'rsatish
    wait_message = bot.send_message(chat_id, "O'ylayapman... Bir soniya kutib turing...")

    try:
        # AI'ga so'rov yuborish
        # Prompt: AI'ga bizning matematika o'qituvchisi sifatida javob berishini aytamiz
        prompt = f"""
Siz matematika o'qituvchisi sifatida foydalanuvchining savoliga tushunarli va batafsil javob berishingiz kerak.
Foydalanuvchining savoli: {user_question}
Iltimos, yechimni qadamma-qadam va qulay formatda yozing.
Javob o'zbek tilida bo'lishi shart.
"""
        response = model.generate_content(prompt)
        ai_answer = response.text

        # Kutilayotgan xabarni AI javobi bilan almashtirish
        bot.edit_message_text(ai_answer, chat_id, wait_message.message_id)

    except Exception as e:
        # Xatolik bo'lsa foydalanuvchiga xabar berish
        error_text = f"❌ Kechirasiz, javobni olishda xatolik yuz berdi: {str(e)}"
        bot.edit_message_text(error_text, chat_id, wait_message.message_id)

# 3. Botni ishga tushirish (Polling)
if __name__ == '__main__':
    print("✅ Bot ishga tushdi...")
    bot.infinity_polling()

