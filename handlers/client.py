from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from config import bot
from db_handler import check_user_by_id, add_user_by_start, update_user_info
from settings import GROUP_ID

USER_STATES = {}


async def cmd_start(message: types.Message):
    """Start function"""

    await bot.send_message(message.from_user.id, 'Волшебное пространство "Why Not Manicure" приветствует новых гостей!')
    photo = FSInputFile('static/manicure_salon.jpg')

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption='Здесь вы можете забрать ✨подарок✨, если еще не были у нас.'
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Внутри у нас 💫очень красиво и уютно!💫Мы работаем с 2016 года.На Яндексе у нас стабильные 5⭐️.'
    )

    user_exist = check_user_by_id(telegram_id=message.from_user.id)
    if user_exist is None:
        USER_STATES[message.from_user.id] = {'state': 1, 'answer_1': '', 'answer_2': ''}
        add_user_by_start(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='А теперь помогите подобрать для Вас ✨подарок✨\n\nСейчас в нашем салоне можно сделать:\n'
                 '1. Маникюр\n'
                 '2. Педикюр\n'
                 '3. Оформить брови\n'
                 '4. Ламинирование ресниц\n\n'
                 'Напишите цифрами, какие услуги Вас заинтересовали?'
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Вы уже были у нас! Если у Вас есть вопросы, напишите нам сейчас и мы ответим в ближайшее время :) '
        )
        USER_STATES[message.from_user.id] = {'state': 3}


async def cmd_text(message: types.Message):
    """Text handler"""

    if message.chat.type in ['group', 'supergroup'] and message.chat.id == GROUP_ID:
        if message.reply_to_message:
            reply_text = message.reply_to_message.text  # то, на что ответили
            print(reply_text)
            try:
                reply_user_id = int(reply_text.split('\n')[1].split('Айди: ')[1])
            except IndexError as error:
                pass
            except Exception as error:
                print('ERROR!!', error)
            else:

                if message.text.lower().strip() == '/end':
                    await message.reply(text=f'☑️ Сессия с пользователем {reply_user_id} завершена..')
                    await bot.send_message(chat_id=reply_user_id, text='Текущая сессия завершена, используйте /start')
                    try:
                        del USER_STATES[reply_user_id]
                    except KeyError as error:
                        pass
                    return

                await bot.send_message(chat_id=reply_user_id, text=message.text)

        return

    if message.chat.type == 'private' and message.from_user.id not in USER_STATES:
        return

    state = USER_STATES[message.from_user.id]['state']

    if state == 1:
        USER_STATES[message.from_user.id]['answer_1'] = message.text
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Напишите ваше имя и номер телефона'.format(message.text)
        )
        USER_STATES[message.from_user.id]['state'] = 2
    elif state == 2:
        USER_STATES[message.from_user.id]['answer_2'] = message.text
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Сейчас к диалогу подключится администратор и оформит для Вас подарок по интересующей услуге. Уточните, пожалуйста, Вы новый гость и еще не были у нас, все верно?👌🏼'
        )
        await bot.send_message(GROUP_ID, f'✅ Сообщение от нового клиента:\n'
                                         f'Айди: {message.from_user.id}\n'
                                         f'Юзернейм: @{message.from_user.username}\n'
                                         f'Полное имя: {message.from_user.full_name}\n\n'
                                         f'Выбранная услуга: {USER_STATES[message.from_user.id]["answer_1"]}\n'
                                         f'Имя и номер телефона: {USER_STATES[message.from_user.id]["answer_2"]}')
        USER_STATES[message.from_user.id] = {'state': 3}
        update_user_info(telegram_id=message.from_user.id, info=message.text)
        return

    elif state == 3:
        await bot.send_message(chat_id=GROUP_ID,
                               text=f'💬 Сообщение от клиента:\n'
                                    f'Айди: {message.from_user.id}\n'
                                    f'Юзернейм: @{message.from_user.username}\n'
                                    f'Полное имя: {message.from_user.full_name}\n\n'
                                    f'Текст: {message.text}'
                               )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Спасибо за обращение! Ожидайте.'
        )


def client_register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_text, F.text)
