#!/usr/bin/env python3
"""
📚 Akademik Yordam Bot
Kurs ishi, Mustaqil ish, Maqola, Tezis va boshqa xizmatlar uchun zakaz boti.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ─── SOZLAMALAR ───────────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"          # @BotFather dan oling
ADMIN_CHAT_ID = 123456789                  # Sizning Telegram ID (https://t.me/userinfobot)

# ─── BOSQICHLAR ───────────────────────────────────────────────
CHOOSE_SERVICE, GET_TOPIC, GET_PAGES, GET_DEADLINE, GET_CONTACT, CONFIRM = range(6)

# ─── XIZMATLAR ────────────────────────────────────────────────
SERVICES = {
    "kurs_ishi":     "🗂 Kurs ishi",
    "mustaqil_ish":  "✍️ Mustaqil ish",
    "maqola":        "📝 Maqola",
    "tezis":         "✉️ Tezis",
    "referat":       "📑 Referat",
    "esse":          "🗒 Esse",
    "taqdimot":      "📚 Taqdimot / Slayd",
}

PRICES = {
    "kurs_ishi":     "80,000 – 150,000 so'm",
    "mustaqil_ish":  "30,000 – 60,000 so'm",
    "maqola":        "50,000 – 100,000 so'm",
    "tezis":         "40,000 – 80,000 so'm",
    "referat":       "25,000 – 50,000 so'm",
    "esse":          "20,000 – 40,000 so'm",
    "taqdimot":      "30,000 – 70,000 so'm",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ─── /START ───────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("📋 Xizmatlar & Narxlar", callback_data="narxlar")],
        [InlineKeyboardButton("✅ Zakaz berish", callback_data="zakaz")],
        [InlineKeyboardButton("📞 Bog'lanish", callback_data="contact")],
    ]
    await update.message.reply_text(
        "☀️ *Assalomu aleykum!*\n\n"
        "🎓 *Akademik Yordam Markaziga xush kelibsiz!*\n\n"
        "Biz sizga quyidagi ishlarni tayyorlab beramiz:\n"
        "🗂 Kurs ishi  •  ✍️ Mustaqil ish\n"
        "📝 Maqola  •  ✉️ Tezis  •  📑 Referat\n"
        "🗒 Esse  •  📚 Taqdimot / Slayd\n\n"
        "💎 *Sifatli • Tez • Qulay narxda*\n"
        "🏪 24/7 xizmatdamiz!\n\n"
        "Quyidan tanlang 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── NARXLAR ──────────────────────────────────────────────────
async def show_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "💰 *Xizmatlar va Narxlar:*\n\n"
    for key, name in SERVICES.items():
        text += f"{name}\n💵 {PRICES[key]}\n\n"
    text += "📃 _Barcha formatda: PDF, DOCX, PPTX, XLSX_\n"
    text += "🎖 _Narx muzokarali!_"

    keyboard = [[InlineKeyboardButton("✅ Zakaz berish", callback_data="zakaz"),
                 InlineKeyboardButton("🔙 Orqaga", callback_data="back")]]
    await query.edit_message_text(text, parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


# ─── BOG'LANISH ───────────────────────────────────────────────
async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("✅ Zakaz berish", callback_data="zakaz"),
                 InlineKeyboardButton("🔙 Orqaga", callback_data="back")]]
    await query.edit_message_text(
        "📞 *Bog'lanish:*\n\n"
        "✈️ Telegram: @Kursishimustaqilish247\n"
        "🏪 24/7 online xizmatdamiz!\n\n"
        "Yoki quyidagi tugma orqali zakaz bering 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── ORQAGA ───────────────────────────────────────────────────
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📋 Xizmatlar & Narxlar", callback_data="narxlar")],
        [InlineKeyboardButton("✅ Zakaz berish", callback_data="zakaz")],
        [InlineKeyboardButton("📞 Bog'lanish", callback_data="contact")],
    ]
    await query.edit_message_text(
        "☀️ *Assalomu aleykum!*\n\n"
        "🎓 *Akademik Yordam Markaziga xush kelibsiz!*\n\n"
        "Quyidan tanlang 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── ZAKAZ: XIZMAT TANLASH ────────────────────────────────────
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = []
    for key, name in SERVICES.items():
        buttons.append([InlineKeyboardButton(
            f"{name}  |  {PRICES[key]}", callback_data=f"srv_{key}"
        )])
    buttons.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])

    await query.edit_message_text(
        "📋 *Qaysi xizmat kerak?*\n\nQuyidan tanlang 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return CHOOSE_SERVICE


# ─── XIZMAT TANLANDI ──────────────────────────────────────────
async def service_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data.replace("srv_", "")
    context.user_data["service"] = SERVICES[key]
    context.user_data["price"] = PRICES[key]

    await query.edit_message_text(
        f"✅ *{SERVICES[key]}* tanlandi!\n\n"
        "📌 *Mavzuni yozing:*\n"
        "_Masalan: O'zbekistonda iqtisodiy islohotlar_",
        parse_mode="Markdown"
    )
    return GET_TOPIC


# ─── MAVZU ────────────────────────────────────────────────────
async def get_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["topic"] = update.message.text
    await update.message.reply_text(
        "📄 *Necha bet / necha slayd kerak?*\n"
        "_Masalan: 25 bet yoki 15 slayd_",
        parse_mode="Markdown"
    )
    return GET_PAGES


# ─── HAJM ─────────────────────────────────────────────────────
async def get_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pages"] = update.message.text
    await update.message.reply_text(
        "⏰ *Qachonga kerak? (muddati)*\n"
        "_Masalan: 3 kun yoki 20-may_",
        parse_mode="Markdown"
    )
    return GET_DEADLINE


# ─── MUDDAT ───────────────────────────────────────────────────
async def get_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deadline"] = update.message.text
    await update.message.reply_text(
        "📞 *Telefon raqamingiz yoki Telegram username:*\n"
        "_Masalan: +998901234567 yoki @username_",
        parse_mode="Markdown"
    )
    return GET_CONTACT


# ─── KONTAKT ──────────────────────────────────────────────────
async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    d = context.user_data

    summary = (
        "📋 *Zakazingiz:*\n\n"
        f"🔹 Xizmat: *{d['service']}*\n"
        f"🔹 Mavzu: *{d['topic']}*\n"
        f"🔹 Hajm: *{d['pages']}*\n"
        f"🔹 Muddat: *{d['deadline']}*\n"
        f"🔹 Narx: *{d['price']}*\n"
        f"🔹 Kontakt: *{d['contact']}*\n\n"
        "✅ Tasdiqlaysizmi?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Ha, yuborish", callback_data="confirm"),
         InlineKeyboardButton("❌ Bekor", callback_data="cancel")]
    ]
    await update.message.reply_text(summary, parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM


# ─── TASDIQLASH ───────────────────────────────────────────────
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    d = context.user_data
    user = query.from_user

    # Adminга yuborish
    admin_msg = (
        "🔔 *YANGI ZAKAZ!*\n\n"
        f"👤 Mijoz: [{user.full_name}](tg://user?id={user.id})\n"
        f"🆔 ID: `{user.id}`\n"
        f"📱 Username: @{user.username or 'yoq'}\n\n"
        f"🔹 Xizmat: *{d['service']}*\n"
        f"🔹 Mavzu: *{d['topic']}*\n"
        f"🔹 Hajm: *{d['pages']}*\n"
        f"🔹 Muddat: *{d['deadline']}*\n"
        f"🔹 Narx: *{d['price']}*\n"
        f"🔹 Kontakt: *{d['contact']}*"
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_msg,
        parse_mode="Markdown"
    )

    await query.edit_message_text(
        "🎉 *Zakazingiz qabul qilindi!*\n\n"
        "⏳ Tez orada siz bilan bog'lanamiz.\n"
        "✈️ @Kursishimustaqilish247\n\n"
        "Rahmat! 🙏",
        parse_mode="Markdown"
    )
    context.user_data.clear()
    return ConversationHandler.END


# ─── BEKOR QILISH ─────────────────────────────────────────────
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "❌ Zakaz bekor qilindi.\n/start — qaytadan boshlash",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ Bekor qilindi.\n/start — qaytadan boshlash"
        )
    context.user_data.clear()
    return ConversationHandler.END


# ─── MAIN ─────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_order, pattern="^zakaz$")],
        states={
            CHOOSE_SERVICE: [CallbackQueryHandler(service_chosen, pattern="^srv_")],
            GET_TOPIC:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_topic)],
            GET_PAGES:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_pages)],
            GET_DEADLINE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_deadline)],
            GET_CONTACT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            CONFIRM:        [CallbackQueryHandler(confirm_order, pattern="^confirm$")],
        },
        fallbacks=[
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CommandHandler("cancel", cancel),
        ]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(show_prices, pattern="^narxlar$"))
    app.add_handler(CallbackQueryHandler(show_contact, pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(go_back, pattern="^back$"))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
