from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import codecs

BOT_TOKEN: str = 'BOT_TOKEN'
f = codecs.open("text.txt", "r", "utf-8")
main_text = f.read() 
f.close()
print(main_text)

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()
admins = ['DmirtyB', 'bdosha06']
chanels = ['aboutmma_ru', 'UFCMMA00']

chan_1 =  InlineKeyboardButton(
    text='1',
    url=f'https://t.me/{chanels[0]}')


chan_2 =  InlineKeyboardButton(
    text='2',
    url=f'https://t.me/{chanels[1]}')

get_url = InlineKeyboardButton(
    text='🤗Трансляция тут!',
    callback_data='get')

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[chan_1], 
                     [chan_2],
                     [get_url]])


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    
    await message.answer(text=main_text, 
                         reply_markup=keyboard)

@dp.callback_query(Text(text='get'))
async def notif_turn_on(callback: CallbackQuery):
    print(callback.from_user.username, end = ' ')
    for chanel in chanels:
        try:
            temp = await bot.get_chat_member(chat_id=f'@{chanel}', user_id=callback.from_user.id)
            print(temp.status, end = ' ')
            if temp.status == 'left':
                await callback.answer(text='Вы еще не подписались на все каналы')
                return 

        except:
            await callback.answer(text='Вы еще не подписались на все каналы')
            return
    print()
    await callback.message.edit_text(text=f'Вот ссылка на трансляцию! https://t.me/UFCMMA0000')

@dp.message()
async def message(message: Message):  #
    if message.from_user.username in admins:
        global main_text
        main_text = message.text
        await message.answer(text='Текст успешно изменен')
        with codecs.open("text.txt") as temp:
            temp.write(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)  # Запуск бота
