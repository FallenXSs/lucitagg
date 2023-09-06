import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(name)

api_id = int(os.environ.get("9839833"))
api_hash = os.environ.get("23818dbf65e7d370cc0adb900f32d16c")
bot_token = os.environ.get("6347172241:AAE5pVT6ASZuE9Kd4gicFGF4ZeayPrR1EGY")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = [5638708289]

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("LuciTagger Bot, Grup veya kanaldaki neredeyse tüm üyelerden bahsedebilirim ★\nDaha fazla bilgi için /help'i tıklayın.",
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/LuciTaggerBot?startgroup=a'),
                      Button.url('📣 Support', 'https://t.me/MajesteTr'),
                      Button.url('🚀 Sahibim', 'https://t.me/BenYakup')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "Lucitagger bot'un Yardım Menüsü\n\nKomut: /all \n  Bu komutu, başkalarına bahsetmek istediğiniz metinle birlikte kullanabilirsiniz. \nÖrnek: /all Günaydın!  \nBu komutu yanıt olarak kullanabilirsiniz. herhangi bir mesaj Bot, yanıtlanan iletiye kullanıcıları etiketleyecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/LuciTaggerBot?startgroup=a'),
                       Button.url('📣 Support', 'https://t.me/MajesteTr'),
                      Button.url('🚀 Sahibim', 'https://t.me/BenYakup')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("Bu komut gruplarda ve kanallarda kullanılabilir.!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Yalnızca yöneticiler hepsinden bahsedebilir!")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Bana bir argüman ver!")
  else:
    return await event.respond("Bir mesajı yanıtlayın veya başkalarından bahsetmem için bana bir metin verin!")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"{usr.first_name} "
      if event.chat_id not in anlik_calisan:
        await event.respond("İşlem Başarılı Bir Şekilde Durduruldu ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"{usr.first_name} "
      if event.chat_id not in anlik_calisan:
        await event.respond("İşlem Başarılı Bir Şekilde Durduruldu ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot çalıyor merak etme 🚀 @BenYakup @MajesteTr bilgi alabilirsin <<")
client.run_until_disconnected()