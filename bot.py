# Telegram Temp Group Access Bot
# Users ko sirf 10 minute ke liye group join karne deta hai
# 10 minute ke baad unhe remove kar deta hai

from pyrogram import Client, filters
import asyncio, time

API_ID = 26741021       # apna API_ID daalo (my.telegram.org se milega)
API_HASH = "7c5af0b88c33d2f5cce8df5d82eb2a94"   # apna API_HASH daalo
BOT_TOKEN = "your_bot_token" # BotFather se mila token
GROUP_ID = -1002988067946    # apne supergroup ka ID daalo (jaise: -100xxxxxx)

app = Client("temp_access_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start command
@app.on_message(filters.command("start"))
async def start(_, m):
    link = await app.create_chat_invite_link(
        chat_id=GROUP_ID,
        expire_date=int(time.time()) + 60,   # link 1 minute me expire hoga
        member_limit=1
    )
    await m.reply_text(
        "👋 Aapko 10 minute ke liye group access mil raha hai.\n\n"
        f"👉 Jaldi join karo: {link.invite_link}"
    )

# Jab user group join kare to 10 min timer start
@app.on_chat_member_updated()
async def member_join(client, event):
    if event.chat.id != GROUP_ID:
        return

    if event.new_chat_member and event.new_chat_member.user and not event.new_chat_member.user.is_bot:
        user = event.new_chat_member.user
        await client.send_message(user.id, "✅ Aap group me join ho gaye ho. 10 minute baad aapko remove kar diya jayega.")

        # 10 minute wait
        await asyncio.sleep(600)

        try:
            await client.ban_chat_member(GROUP_ID, user.id)
            await asyncio.sleep(1)
            await client.unban_chat_member(GROUP_ID, user.id)
            await client.send_message(user.id, "⏳ Aapka 10 minute ka access khatam ho gaya. Aapko group se remove kar diya gaya hai.")
        except Exception as e:
            print("Error:", e)

app.run()
  
