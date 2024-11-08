from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


number_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="☎️ Telefon raqamni yuborish", request_contact=True)],
],
                resize_keyboard=True, 
                input_field_placeholder="Pastdagi tugma orqali raqamingizni yuboring!")


none_kb = ReplyKeyboardRemove(remove_keyboard=True)



