from DAXXMUSIC import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " **➠ Good night 🌚** ",
           " **➠ Go to sleep, little one 🙊** ",
           " **➠ Keep your phone, go to sleep, you won't be up...👻** ",
           " **➠ Hey baby, you are going to sleep now...?? 🥲** ",
           " **➠ Mummy, look, I'm stuck in this, so I can't sleep 😜** ",
           " **➠ Papa, look, your son is using the phone at night 🤭** ",
           " **➠ Darling, what’s the scene tonight...?? 🌠** ",
           " **➠ Good night 🙂** ",
           " **➠ Good night, sweet dreams, take care...?? ✨** ",
           " **➠ It's night time, so sleep...🌌** ",
           " **➠ Mummy, see it's 11, but I'm still on my phone.. 🕦** ",
           " **➠ Will you go to school tomorrow? Hurry up! 🏫** ",
           " **➠ Good night, sweet dreams... 😊** ",
           " **➠ Have a beautiful night, my dear 🌄** ",
           " **➠ Good night, may all your dreams come true ❤️** ",
           " **➠ Close your eyes, snuggle up tight, and remember that angels are watching over you tonight... 💫** ",
        ]

VC_TAG = [ "**➠ Good morning, how are you? 🐱**",
         "**➠ Good morning, have you woken up yet? 🌤️**",
         "**➠ Good morning baby, ready to drink some tea? ☕**",
         "**➠ Hurry up, school is waiting 🏫**",
         "**➠ Good morning, let's get up and make some coffee 🧊**",
         "**➠ Wake up and get ready, we’ve got a fresh day ahead 🫕**",
         "**➠ Office work to do, get up now 🏣**",
         "**➠ Good morning friend, what do you want to drink today? ☕🍵**",
         "**➠ Baby, it's 8 am, and you're still sleeping... 🕖**",
         "**➠ Get up now! 🌞**",
         "**➠ Good morning, have a nice day! 🌄**",
         "**➠ Good morning, have a good day ahead 🌱**",
         "**➠ Good morning, how are you doing today? 😇**",
         "**➠ Mummy, look at this lazy bum... 😵‍💫**",
         "**➠ What's the scene? Wake up! 😏**",
         "**➠ Good morning, dear friend, let's do it... 🌟**",
         "**➠ Wake up and greet your friends in the group... 🌟**",
         "**➠ Papa, I haven't woken up yet, but I will soon 🥲**",
         "**➠ What’s up this morning? How are you? 😅**",
         "**➠ Good morning beastie, breakfast ready? 🍳**",
        ]

@app.on_message(filters.command(["gntag", "tagmember" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ This command is only for groups.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ You are not an admin to use this command.")
    
    users = await client.get_chat_members(chat_id)
    members = [user.user.mention for user in users if user.status == ChatMemberStatus.MEMBER]
    random.shuffle(members)
    
    text = f"{random.choice(EMOJI)}\n{random.choice(TAGMES)}\n{random.choice(VC_TAG)}\n" + "\n".join(members)
    await message.reply(text)
