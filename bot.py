import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
owner_id = os.environ.get("OWNER_İD")
database_url = os.environ.get("DATABASE_URL)
client = TelegramClient('client', api_id, api_hash, owner_id, database_url).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Ali Tagger Bot**, Grup veya kanaldaki neredeyse tüm üyelerden bahsedebilirim ★\nDaha fazla bilgi için **/help**'i tıklayın.",
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/alitaggerBot?startgroup=a'),
                      Button.url('📣 Destek', 'https://t.me/mmagneto3'),
                      Button.url('🚀 Sahibim', 'https://t.me/mmagneto')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Ali Tagger Bot'un Komutları**\n\nKomut: /all \n  Bu komutu, Tag İşlemini Başlatmak için Kullan Komutu Yazdıktan Sonra Yazmak İstediğin Cümleyi Veya Kelimeyi Girebilirsin. \n`Örnek: /all Günaydın!`  \nBu komutu yanıt olarak kullanabilirsiniz. herhangi bir mesaja yanıt verirseniz Bot yanıtlanan mesaja kullanıcıları etiketleyecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/alitaggerBot?startgroup=a'),
                       Button.url('📣 Destek', 'https://t.me/mmagneto3'),
                      Button.url('🚀 Sahibim', 'https://t.me/mmagneto')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca yöneticiler herkesten bahsedebilir!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver!__")
  else:
    return await event.respond("__Bir mesajı yanıtlayın veya başkalarından bahsetmem için bana bir metin verin!__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
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
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("İşlem Başarılı Bir Şekilde Durduruldu ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot çalıyor merak etme 🚀 @mmagneto3 bilgi alabilirsin <<")
client.run_until_disconnected()
