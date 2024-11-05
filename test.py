from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# دیکشنری برای ذخیره تعداد کلیک و وضعیت دکمه هر کاربر
user_data = {}
# متغیر برای شمارش تعداد کلیک‌های کلیه کاربران
total_click_count = 0

# تابعی برای ارسال پیام با دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # مقداردهی اولیه برای کاربر جدید
    if user_id not in user_data:
        user_data[user_id] = {'click_count': 0, 'click_button_disabled': False}

    # دریافت اطلاعات کاربر از دیکشنری
    click_button_disabled = user_data[user_id]['click_button_disabled']

    # تعریف دکمه‌ها و متن پیام بر اساس وضعیت
    keyboard = []
    if not click_button_disabled:
        keyboard.append([InlineKeyboardButton("موز میشم", callback_data='button_click')])
        message_text = "برای موز شدن کلیک کن."
    else:
        message_text = "موز شدی."

    keyboard.append([InlineKeyboardButton("تعداد موزی ها:", callback_data='show_count')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)

# تابعی برای پردازش کلیک روی دکمه "کلیک کن!"
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global total_click_count
    user_id = update.effective_user.id

    # بررسی و بروزرسانی تعداد کلیک‌ها و وضعیت دکمه برای کاربر
    if user_id in user_data and not user_data[user_id]['click_button_disabled']:
        user_data[user_id]['click_count'] += 1
        user_data[user_id]['click_button_disabled'] = True
        total_click_count += 1  # افزایش تعداد کلیک‌های کلی

    query = update.callback_query
    await query.answer()  # پاسخ سریع به کلیک

    # فراخوانی مجدد دستور /start برای به‌روزرسانی متن و دکمه‌ها
    await start(update, context)

# تابعی برای نمایش تعداد کلیک‌ها
async def show_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # دریافت تعداد کلیک‌ها برای کاربر و تعداد کلی کلیک‌ها
    user_click_count = user_data[user_id]['click_count'] if user_id in user_data else 0

    query = update.callback_query
    await query.answer()  # پاسخ سریع به کلیک
    await query.edit_message_text(text=f"تعداد موز شده ها: {total_click_count}")

# راه‌اندازی ربات
def main():
    # ایجاد یک شیء Application با توکن ربات
    application = Application.builder().token("7635770061:AAHFybSa5rn8T8pmQjFBn7HvNzLY6lzyLWs").build()

    # افزودن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern='button_click'))
    application.add_handler(CallbackQueryHandler(show_count, pattern='show_count'))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()

