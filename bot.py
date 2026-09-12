from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import google.generativeai as genai

# توکن ربات تلگرام و کلید هوش مصنوعی
TELEGRAM_TOKEN = "8678378437:AAEkxYaX5mEYfYqtySyJxal4vdKKNmyk_FI"
GEMINI_API_KEY = "AQ.Ab8RN6K34S1MB-Wzu3Xc8VjJCzZC2tt8SVls3C_OsFeJvJe5zw"

# تنظیمات هوش مصنوعی جمنای
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 🎵✨\n"
        "به ربات هوشمند موزیک خوش آمدید.\n\n"
        "اسم هر آهنگی رو که می‌خوای بفرست تا اول متن انگلیسیشو برام پیدا کنم و بعد بتونی به هر زبونی که خواستی ترجمه‌اش کنی!"
    )

async def handle_song_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song_name = update.message.text
    waiting_msg = await update.message.reply_text("🔍 در حال جستجوی متن آهنگ...")

    try:
        prompt = f"Find and write the exact lyrics for the song: {song_name}. If you don't know the exact lyrics, write a clean version or information about it. Keep it nicely formatted."
        response = model.generate_content(prompt)
        lyrics = response.text

        context.user_data['last_lyrics'] = lyrics

        keyboard = [
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇹🇷 ترکی", callback_data="lang_tr")
            ],
            [
                InlineKeyboardButton("🇫🇷 فرانسوی", callback_data="lang_fr"),
                InlineKeyboardButton("🇩🇪 آلمانی", callback_data="lang_de"),
                InlineKeyboardButton("🇸🇦 عربی", callback_data="lang_ar")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await waiting_msg.edit_text(
            f"🎵 متن اصلی آهنگ:\n\n{lyrics}\n\n👇 حالا زبان مورد نظر برای ترجمه را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    except Exception as e:
        await waiting_msg.edit_text("❌ متأسفانه در یافتن متن آهنگ خطایی رخ داد. لطفاً دوباره امتحان کن.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lyrics = context.user_data.get('last_lyrics')
    if not lyrics:
        await query.edit_message_text("❌ اطلاعات آهنگ منقضی شده است. لطفاً دوباره اسم آهنگ را بفرستید.")
        return

    lang_code = query.data.split('_')[1]
    
    lang_names = {
        'fa': 'فارسی 🇮🇷',
        'tr': 'ترکی 🇹🇷',
        'fr': 'فرانسوی 🇫🇷',
        'de': 'آلمانی 🇩🇪',
        'ar': 'عربی 🇸🇦'
    }
    
    target_lang = lang_names.get(lang_code, 'فارسی')

    await query.edit_message_text(f"⏳ در حال ترجمه به {target_lang}...")

    try:
        translation_prompt = f"Translate the following song lyrics into {target_lang}. Keep the formatting nice:\n\n{lyrics}"
        response = model.generate_content(translation_prompt)
        translated_text = response.text

        result_message = (
            f"🎵 متن اصلی:\n{lyrics[:500]}...\n\n"
            f"🌐 ترجمه به {target_lang}:\n\n{translated_text}"
        )

        keyboard = [
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇹🇷 ترکی", callback_data="lang_tr")
            ],
            [
                InlineKeyboardButton("🇫🇷 فرانسوی", callback_data="lang_fr"),
                InlineKeyboardButton("🇩🇪 آلمانی", callback_data="lang_de"),
                InlineKeyboardButton("🇸🇦 عربی", callback_data="lang_ar")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(result_message, reply_markup=reply_markup, parse_mode="Markdown")

    except Exception as e:
        await query.edit_message_text("❌ خطایی در ترجمه رخ داد.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_song_request))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Smart Music Bot is running...")
    app.run_polling()
    import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# این بخش یک وب‌سرور سبک می‌سازد تا رندر پورت را باز ببیند
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# اجرای سرور در پس‌زمینه (قبل از استارت ربات)
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # کدهای اصلی اجرای ربات خودت (مثل run_polling یا infinity_polling) 
    # باید دقیقاً پایین همین بخش قرار داشته باشند تا با هم اجرا شوند.

