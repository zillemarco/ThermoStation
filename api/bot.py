from telegram.ext import Updater
from telegram.ext import CommandHandler
from app.models.station import Station

stop_bot = False

updater = Updater(token="1032186620:AAGv99oOGBrxbzLij5NUjcOm5xfL6N4-La4", use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto nella stazione di controllo della caldaia")

def stop(update, context):
    global stop_bot
    stop_bot = True

def pumps_list(update, context):
    st = Station()
    pumps = st.get_pumps()

    message = ""

    for p in pumps:
        message = message + p.get_name() + " (" + ("on" if p.is_on() else "off") + ")\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def thermostats_list(update, context):
    st = Station()
    thermostats = st.get_thermostats()

    message = ""

    for t in thermostats:
        onOff = "on" if t.is_on() else "off"
        temp = ", {0:1} °C / {1:1} °C".format(t.get_current_temperature(), t.get_target_temperature()) if t.get_type() == 2 else ""

        message = message + t.get_name() + " (" + onOff + temp + ")\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))

dispatcher.add_handler(CommandHandler('pumps', pumps_list))
dispatcher.add_handler(CommandHandler('thermostats', thermostats_list))

updater.start_polling()