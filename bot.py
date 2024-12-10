import telebot
from telebot import types
from time import sleep
from ClassNameValidator import ClassNameValidator
from ReportLengthValidator import ReportLengthValidator
from CsvLogger import CsvLogger
import keys # .py file with confidential info


TOKEN = keys.TOKEN
FORWARD_CHAT_ID = keys.FORWARD_CHAT_ID  

user_class = ''
report_msg = ''

bot = telebot.TeleBot(token=TOKEN)

min_report_symbols = 20    # Minimum amount of symbols in a user input


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Sveiki! Es esmu report_bots.')
    bot.send_message(message.chat.id, 'Esmu gatavs izklausīties visas tavas sūdzības un komentārus par mūsu skolu.')
    bot.send_message(message.chat.id, 'Es pārsūtīšu tavu ziņojumu skolēnu paspārvaldei.\nJa gribi, varēsi norādīt savu klasi.')

    photo = 'https://cdn.discordapp.com/attachments/1058469027556626522/1081552888700096652/bot_message_sample.jpg'
    bot.send_photo(message.chat.id, photo, caption = 'Ko redz skolēnu pašpārvalde savā čatā:')

    sleep(2)
    hint_at_new_command(message)


@bot.message_handler(commands=['new'])
def new_report(message):
    markup = get_markup("Jā", "Nē")

    msg = bot.send_message(message.chat.id, 'Vai gribi norādīt savu klasi? (Jā/Nē)', reply_markup = markup)
    bot.register_next_step_handler(msg, check_user_consent_to_enter_class)


@bot.message_handler(commands=['cancel'])
def cancel_report(message):
    global report_msg, user_class

    report_msg = ''
    user_class = ''
    bot.send_message(message.chat.id, 'Ziņojums ir atcelts.')
    hint_at_new_command(message)


@bot.message_handler(content_types= ["photo"])
def send_text_on_photo(message):
    hint_at_new_command(message)


@bot.message_handler(content_types=["text"])
def send_text(message):
    hint_at_new_command(message)


def check_user_consent_to_enter_class(message):
    global min_report_symbols, user_class
    try:
        if message.text.lower() == 'jā':
            msg = bot.send_message(message.chat.id, 'Ievadi savu klasi\n(piemēram, "12A" vai "9")')
            bot.register_next_step_handler(msg, enter_class)
        else:
            user_class = ''
            ask_to_type_report(message)
    except Exception:
        ask_to_type_report(message)


def enter_class(message):
    global user_class
    try:
        user_class = message.text.upper()

        if ClassNameValidator.validate(user_class):
            show_typed_user_class(message)
            ask_to_type_report(message)
        elif message.text.lower() == '/cancel':
            cancel_report(message)
        else:
            incorrect_class_entered(message)
    except Exception:
        incorrect_class_entered(message)


def check_report_before_enter(message):
    # This function checks if report is >= min_report_symbols
    global min_report_symbols
    try:
        if not ReportLengthValidator.validate(message.text, min_report_symbols):
            bot.send_message(message.chat.id, 'Minimālais simbolu skaits: ' + str(min_report_symbols))
            msg = bot.send_message(message.chat.id, 'Uzraksti savu ziņojumu vēlreiz.')
            bot.register_next_step_handler(msg, check_report_before_enter)
        else:
            enter_report(message)

    except Exception:
        bot.send_message(message.chat.id, 'Ziņojumam jābūt tikai teksta formātā.')
        ask_to_type_report(message)


def enter_report(message):
    global user_class, report_msg
    raw_report_text = message.text
    if user_class == '':
        report_msg = bot.send_message(message.chat.id, 'Anonīms lietotājs: \n\n' + message.text)
    else:
        report_msg = bot.send_message(message.chat.id, 'Skolēns no klases ' + user_class + ':' + '\n\n' + message.text)

    markup = get_markup("Jā", "Nē")
    msg = bot.send_message(message.chat.id, 'Vai esi pārliecināts, ka vēlies nosūtīt šo ziņojumu? (Jā/Nē)', reply_markup=markup)
    bot.register_next_step_handler(msg, send_report, raw_report_text)


def send_report(message, raw_report_text):
    global user_class, report_msg
    try:
        if message.text.lower() == 'jā':
            bot.forward_message(FORWARD_CHAT_ID, message.chat.id, report_msg.message_id)
            bot.send_message(message.chat.id, 'Tavs ziņojums tika veiksmīgi nosūtīts, paldies!')
            CsvLogger.log(raw_report_text, user_class)
            hint_at_new_command(message)
        else:
            cancel_report(message)

    except Exception as e:
        bot.send_message(message.chat.id, 'Notika kāda tehniskā kļūme...')
        print(e)
        hint_at_new_command(message)


def get_markup(w1: str, w2: str) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(w1), types.KeyboardButton(w2))
    return markup


def show_typed_user_class(message):
    global user_class
    bot.reply_to(message, 'Tava klase: ' + user_class)


def incorrect_class_entered(message):
    msg = bot.send_message(message.chat.id, 'Nekorekta klase. Mēģini vēlreiz.\n\nJa gribi atcelt, lieto komandu /cancel')
    bot.register_next_step_handler(msg, enter_class)


def hint_at_new_command(message):
    bot.send_message(message.chat.id, 'Lai uzsāktu rakstīt savu ziņojumu, lieto komandu /new')


def ask_to_type_report(message):
    global min_report_symbols
    msg = bot.send_message(message.chat.id, 'Raksti savu ziņojumu.\n\nMinimālais simbolu skaits: ' + str(min_report_symbols))
    bot.register_next_step_handler(msg, check_report_before_enter)


if __name__ == '__main__':
    bot.polling(none_stop=True)
