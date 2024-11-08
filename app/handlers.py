from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext


from app.generators import generate
from app.states import Work
from app.states import Login
from app.kb import number_kb
from app.kb import none_kb


root = Router()


@root.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    file = open("app/db/db.txt", "r", encoding='utf-8')
    lines = [line.replace("\n", "").split("|")[1] for line in file.readlines()]
    file.close
    check_id = str(message.from_user.id) 
    if check_id in lines:
        await message.answer(f"Salom {message.from_user.full_name}, xush kelibsiz! men Nexus AI — sizning sun'iy intellekt yordamchingizman. Sizga kerakli ma'lumotlarni taqdim etishga tayyorman. Qanday yordam bera olishimni ayting!", reply_markup=none_kb)
    else:
        await state.set_state(Login.number)
        await message.answer(f"Salom {message.from_user.full_name}, Iltimos, telefon raqamingizni yuboring.", reply_markup=number_kb )

            
@root.message(Work.process)
async def stop_ai(message: types.Message):
    await message.answer("Iltimos, biroz kutib turing. Hozircha oldingi savolingiz ustida o'ylayapman, tez orada javobim tayyor bo'ladi!")


@root.message(F.photo)
async def stop_img(message: types.Message):
    await message.reply("Iltimos, rasm yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.video)
async def stop_video(message: types.Message):
    await message.reply("Iltimos, video yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.voice)
async def stop_voice(message: types.Message):
    await message.reply("Iltimos, ovozli xabar yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.audio)
async def stop_music(message: types.Message):
    await message.reply("Iltimos, ovozli xabar yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.document)
async def stop_file(message: types.Message):
    await message.reply("Iltimos, fayl yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.location)
async def stop_location(message: types.Message):
    await message.reply("Iltimos, lokatsiya yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message(F.caption)
async def stop_caption(message: types.Message):
    await message.reply("Iltimos, caption yubormang, men faqat matnli savollarga javob bera olaman.")
    

@root.message(Login.number)
async def num_handler(message: types.Message, state: FSMContext):
    
    try:
        message.contact is not None
        await state.update_data(name=message.from_user.full_name, id=message.from_user.id, user=message.from_user.username, utc=message.date, num=message.contact.phone_number, etc=message.contact)
        data = await state.get_data()
        file = open("app/db/db.txt", "a", encoding='utf-8')
        file.write(f"{data["name"]}|{data["id"]}|{data["user"]}|{data["num"]}|{data["utc"]}|{data["etc"]}\n")
        await state.clear()
        file.close()
        await message.answer(f"Salom {message.from_user.full_name}, xush kelibsiz! men Nexus AI — sizning sun'iy intellekt yordamchingizman. Sizga kerakli ma'lumotlarni taqdim etishga tayyorman. Qanday yordam bera olishimni ayting!", reply_markup=none_kb)
    except:
        await message.answer("Iltimos pasdagi ☎️ Telefon raqamni yuborish tugmasi orqali yuboring", reply_markup=number_kb)
        await state.set_state(Login.number)


@root.message(F.contact)
async def stop_img(message: types.Message):
    await message.reply("Iltimos, telefon raqamini yubormang, men faqat matnli savollarga javob bera olaman.")


@root.message()
async def ai(message: types.Message, state: FSMContext):    
    try:
       await state.set_state(Work.process)
       await state.update_data(name=message.from_user.full_name, id=message.from_user.id, user=message.from_user.username, inf=message.text, utc=message.date)
       data = await state.get_data()
       file = open("app/db/information.txt", "a", encoding='utf-8')
       file.write(f"{data["name"]}|{data["id"]}|{data["user"]}|{data["inf"]}|{data["utc"]}\n")
       file.close()
       res = await generate(message.text)
       await message.answer(res.choices[0].message.content)
       await state.clear()
    except: 
        await message.answer("Qandaydur hatolik yuz berdi /start buyrug'i orqali botni qayta ishga tushiring")
        await state.clear()