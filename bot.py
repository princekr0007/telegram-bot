import telebot
import requests

from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

BOT_TOKEN = "8856010625:AAGNuLMPIy-w1WI7aSDPcmhJJgj-gVrU_K4"

bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 7503104119

API = "https://tgtonum.xclusor.workers.dev/?key=xclusor&id="

users = {}
plans = {}
creditplans = {}
waiting = {}
temp = {}

# ---------------- START ---------------- #

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            "🔎 ENTER USER ID",
            callback_data="enter"
        )
    )

    markup.row(
        InlineKeyboardButton(
            "👤 MY PLAN",
            callback_data="myplan"
        ),

        InlineKeyboardButton(
            "💎 VIEW PLANS",
            callback_data="plans"
        )
    )

    markup.row(
        InlineKeyboardButton(
            "📞 CONTACT OWNER",
            url="https://t.me/okhmyboy"
        )
    )

    if message.chat.id == ADMIN_ID:

        markup.row(
            InlineKeyboardButton(
                "⚙ ADMIN PANEL",
                callback_data="admin"
            )
        )

    text = """
🔥 PREMIUM LOOKUP BOT 🔥

✅ Fast Fetch
✅ Premium Access
✅ Daily Limits
✅ VIP Unlimited

Choose Option 👇
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# ---------------- CALLBACKS ---------------- #

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    user_id = call.message.chat.id

    # ENTER
    if call.data == "enter":

        if user_id not in users:

            bot.send_message(
                user_id,
                "❌ No Active Subscription"
            )

            return

        if users[user_id]["credits"] != "Unlimited":

            if int(users[user_id]["credits"]) <= 0:

                bot.send_message(
                    user_id,
                    "❌ No Credits Left"
                )

                return

        waiting[user_id] = "lookup"

        bot.send_message(
            user_id,
            "📥 Send User ID"
        )

    # MY PLAN
    elif call.data == "myplan":

        if user_id not in users:

            bot.send_message(
                user_id,
                "❌ No Active Plan"
            )

            return

        u = users[user_id]

        bot.send_message(
            user_id,
            f"""
👤 YOUR PLAN

📦 Plan: {u['plan']}
📅 Days: {u['days']}
💎 Credits: {u['credits']}
"""
        )

    # VIEW PLANS
    elif call.data == "plans":

        markup = InlineKeyboardMarkup(row_width=2)

        markup.add(

            InlineKeyboardButton(
                "📦 Subscription Plans",
                callback_data="subplans"
            ),

            InlineKeyboardButton(
                "🎟 Credit Plans",
                callback_data="creditplans"
            )
        )

        bot.send_message(
            user_id,
            "Choose Plan Type",
            reply_markup=markup
        )

    # SUB PLANS
    elif call.data == "subplans":

        if len(plans) == 0:

            bot.send_message(
                user_id,
                "❌ No Subscription Plans"
            )

            return

        text = "📦 SUBSCRIPTION PLANS\n\n"

        for p in plans:

            text += f"""
📦 {p}
📅 Days: {plans[p]['days']}
💎 Credits: {plans[p]['credits']}
💰 Price: {plans[p]['price']}

"""

        bot.send_message(
            user_id,
            text
        )

    # CREDIT PLANS
    elif call.data == "creditplans":

        if len(creditplans) == 0:

            bot.send_message(
                user_id,
                "❌ No Credit Plans"
            )

            return

        text = "🎟 CREDIT PLANS\n\n"

        for p in creditplans:

            text += f"""
🎟 {p}
💎 Credits: {creditplans[p]['credits']}
💰 Price: {creditplans[p]['price']}

"""

        bot.send_message(
            user_id,
            text
        )

    # ADMIN PANEL
    elif call.data == "admin":

        if user_id != ADMIN_ID:
            return

        markup = InlineKeyboardMarkup(row_width=2)

        buttons = [

            InlineKeyboardButton(
                "➕ ADD PLAN",
                callback_data="addplan"
            ),

            InlineKeyboardButton(
                "🎟 ADD CREDIT PLAN",
                callback_data="creditplan"
            ),

            InlineKeyboardButton(
                "➖ REMOVE PLAN",
                callback_data="removeplan"
            ),

            InlineKeyboardButton(
                "❌ REMOVE CREDIT PLAN",
                callback_data="removecreditplan"
            ),

            InlineKeyboardButton(
                "👤 ADD USER",
                callback_data="adduser"
            ),

            InlineKeyboardButton(
                "❌ REMOVE USER",
                callback_data="removeuser"
            ),

            InlineKeyboardButton(
                "💎 ADD CREDITS",
                callback_data="credits"
            ),

            InlineKeyboardButton(
                "📊 TOTAL USERS",
                callback_data="stats"
            ),

            InlineKeyboardButton(
                "📢 BROADCAST",
                callback_data="broadcast"
            )
        ]

        markup.add(*buttons)

        bot.send_message(
            user_id,
            "⚙ ADMIN PANEL",
            reply_markup=markup
        )

    # ADD PLAN
    elif call.data == "addplan":

        waiting[user_id] = "plan_days"

        bot.send_message(
            user_id,
            "📅 Send Plan Days"
        )

    # ADD CREDIT PLAN
    elif call.data == "creditplan":

        waiting[user_id] = "credit_plan"

        bot.send_message(
            user_id,
            "Send Like:\nName Credits Price"
        )

    # REMOVE PLAN
    elif call.data == "removeplan":

        if len(plans) == 0:

            bot.send_message(
                user_id,
                "❌ No Plans"
            )

            return

        markup = InlineKeyboardMarkup()

        for p in plans:

            markup.row(
                InlineKeyboardButton(
                    p,
                    callback_data=f"delete_{p}"
                )
            )

        bot.send_message(
            user_id,
            "Select Plan",
            reply_markup=markup
        )

    # REMOVE CREDIT PLAN
    elif call.data == "removecreditplan":

        if len(creditplans) == 0:

            bot.send_message(
                user_id,
                "❌ No Credit Plans"
            )

            return

        markup = InlineKeyboardMarkup()

        for p in creditplans:

            markup.row(
                InlineKeyboardButton(
                    p,
                    callback_data=f"deletecredit_{p}"
                )
            )

        bot.send_message(
            user_id,
            "Select Credit Plan",
            reply_markup=markup
        )

    elif call.data.startswith("delete_"):

        p = call.data.replace("delete_", "")

        if p in plans:

            del plans[p]

            bot.send_message(
                user_id,
                "✅ Plan Removed"
            )

    elif call.data.startswith("deletecredit_"):

        p = call.data.replace("deletecredit_", "")

        if p in creditplans:

            del creditplans[p]

            bot.send_message(
                user_id,
                "✅ Credit Plan Removed"
            )

    # ADD USER
    elif call.data == "adduser":

        waiting[user_id] = "adduser"

        bot.send_message(
            user_id,
            "📥 Send User ID"
        )

    # REMOVE USER
    elif call.data == "removeuser":

        waiting[user_id] = "removeuser"

        bot.send_message(
            user_id,
            "Send User ID"
        )

    # ADD CREDITS
    elif call.data == "credits":

        waiting[user_id] = "credits"

        bot.send_message(
            user_id,
            "Send:\nUSER_ID AMOUNT"
        )

    # STATS
    elif call.data == "stats":

        total = len(users)

        bot.send_message(
            user_id,
            f"👥 Total Users: {total}"
        )

    # BROADCAST
    elif call.data == "broadcast":

        waiting[user_id] = "broadcast"

        bot.send_message(
            user_id,
            "Send Broadcast Message"
        )

    # UNLIMITED
    elif call.data == "unlimited":

        temp[user_id]["credits"] = "Unlimited"

        waiting[user_id] = "plan_name"

        bot.send_message(
            user_id,
            "📦 Send Plan Name"
        )

    # LIMITED
    elif call.data == "limited":

        waiting[user_id] = "plan_credits"

        bot.send_message(
            user_id,
            "💎 Send Credits Per Day"
        )

# ---------------- MESSAGES ---------------- #

@bot.message_handler(func=lambda m: True)
def messages(message):

    user_id = message.chat.id
    text = message.text

    if user_id not in waiting:
        return

    mode = waiting[user_id]

    # LOOKUP
    if mode == "lookup":

        msg = bot.send_message(
            user_id,
            "⏳ Fetching Data..."
        )

        try:

            r = requests.get(API + text)

            data = r.json()

            number = data.get("number", "")

            if number == "":

                bot.edit_message_text(
                    "❌ Failed (Number Not Available)",
                    user_id,
                    msg.message_id
                )

            else:

                bot.edit_message_text(
                    f"✅ Successfully Fetched\n\n📱 {number}",
                    user_id,
                    msg.message_id
                )

                if users[user_id]["credits"] != "Unlimited":

                    users[user_id]["credits"] = int(users[user_id]["credits"]) - 1

        except:

            bot.edit_message_text(
                "❌ Failed To Fetch",
                user_id,
                msg.message_id
            )

        del waiting[user_id]

print("BOT STARTED")

bot.infinity_polling()
