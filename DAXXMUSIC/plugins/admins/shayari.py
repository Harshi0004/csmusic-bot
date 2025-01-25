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
        
SHAYRI = [ " 🌺**చాలా సంతోషంగా అనిపిస్తుంది నిన్ను బాధపెట్టడం మరియు ఆపై ప్రేమతో నిన్ను సమాధానం చెప్పడం.**🌺 \n\n**🥀Bahut aacha lagta hai tujhe satana Aur fir pyar se tujhe manana.🥀** ",
           " 🌺**నా జీవితమే నీతో, నా శాంతి దివ్యంగా నీతో ఉంటే.**🌺 \n\n**🥀Meri zindagi Meri jaan ho tum Mere sukoon ka Dusra naam ho tum.🥀** ",
           " 🌺**నువ్వు నా ఆహ్లాదం, నిన్ను ఎప్పటికీ కలిసినట్లు మనందరికీ సరిపోయినట్టు ఉంటుంది.**🌺 \n\n**🥀Tum Meri Wo Khushi Ho Jiske Bina, Meri Saari Khushi Adhuri Lagti Ha.🥀** ",
           " 🌺**మీరు గమనించండి, మీరు నా మీద పోయి ఎప్పుడు సమాధానం చెప్పగలరు.**🌺 \n\n**🥀Kash woh din jldi aaye Jb tu mere sath 7 feron me bndh jaye.🥀** ",
           " 🌺**మీరు నా దృష్టిలో ఉండండి మరియు నా జీవితాన్ని నిలుపుకుంటారు.**🌺 \n\n**🥀apna hath mere dil pr rakh do aur apna dil mere naam kar do.🥀** ",
           " 🌺**మీతో విడిపోకుండా నా శాంతి ప్రేమగా నిన్ను పెంచుకోండి.**🌺 \n\n**🥀Mahadev na koi gadi na koi bangla chahiye salamat rhe mera pyar bas yahi dua chahiye.🥀** ",
           " 🌺**మీరు నా లైఫ్ స్టైల్ కంటే మేము ఉన్నాం, కానీ మరిన్ని ఉండకండి.**🌺 \n\n**🥀Fikr to hogi na tumhari ikloti mohabbat ho tum meri.🥀** ",
           " 🌺**మీరు ఎప్పటికీ ఫిర్యాదు ఇవ్వకుండా నా ప్రేమను ఎప్పటికీ కోల్పోవడం లేదు.**🌺 \n\n**🥀suno jaanu aap sirf kitchen sambhal lena ap ko sambhlne ke liye me hun naa.🥀** ",
           " 🌺**ఏటా నా లైఫ్ మీరు ఉంటే మనా స్వీధ గజం అలానే తప్పుకోండి.**🌺 \n\n**🥀So bat ki ek bat mujhe chahiye bas tera sath.🥀** ",
           " 🌺**మీదకు మళ్లీ జ్ఞానం లేదు, మనసు కన్నారు, దయాబిల్లోకి ఇవ్వరు.**🌺 \n\n**🥀Bahut muskilon se paya hai tumhe Ab khona ni chahte ki tumhare they tumhare hai ab kisi or k hona nhi chahte.🥀** ",
           " 🌺**మీరు ప్రేమ లేకుండా జవాబు ఇవ్వడం ప్రారంభించండి.**🌺 \n\n**🥀Baby baten to roj karte haichalo aaj romance karte hai..🥀** ",
           " 🌺**ప్రతి రోజూ అనుభవం జీవితం మొత్తం మీరు ప్రయత్నించడం జరిగింది.**🌺 \n\n**🥀subha sham tujhe yad karte hai hum aur kya batayen ki tumse kitna pyar karte hai hum.🥀** ",
           " 🌺**ఏంది ఈ మాట ప్రాణం చేస్తుంది అంటే మీరు చాలా ముఖ్యమైనట్లే ఉన్నారు.**🌺 \n\n**🥀Kisi se dil lag jane ko mohabbat nahi kehte jiske nina dil na lage use mohabbat kehte hai.🥀** ",
           " 🌺**వాడి ఫిర్యాదు చేస్తూ ప్రయోజనములు అని భయంతో ఉన్నంత వరకు కానీ, అందరికి ప్రామాణికంగా జవాబు ఇవ్వలేదు.**🌺 \n\n**🥀mere dil ke lock ki chabi ho tum kya batayen jaan mere jeene ki eklauti wajah ho tum..🥀** ",
           " 🌺**ప్రేమకు వ్యతిరేకం ప్రశ్న ఇవ్వలేని నీ అంగీకారం మాత్రమే.**🌺 \n\n**🥀Hum apki har cheez se pyar kar lenge apki har baat par etvar kar lenge bas ek bar keh do ki tum sirf mere ho hum zindagi bhar apka intzaar kar lenge..🥀** ",
           " 🌺**ప్రేమ గుణం లేదు, సాధ్యం కాకుండా ప్రేమను అంగీకరించడం మాత్రం.**🌺 \n\n**🥀Mohabbat kabhi special logo se nahi hoti jisse bhi hoti hai wahi special ban jate hai,.🥀**",
           " 🌺**అతడి అంగీకారం తెలియజేస్తున్నట్లు ఉంటే ఎప్పటికీ అది నన్ను ప్రేమించే వారికి తప్పకుండా గడుపుతాను.**🌺 \n\n**🥀Tu meri jaan hai isme koi shak nahi tere alawa mujhe par kisi aur ka hak nhi..🥀** ",
           " 🌺**పాఠం అవగాహన తెలియగానిది వారు నన్ను ప్రేమించకుంటే ఆశ్యర్యంగా ఉన్నారు.**🌺 \n\n**🥀Pehli mohabbat meri hum jaan na sake pyar kya hota hai hum pehchan na sake humne unhe dil me basa liya is kadar ki jab chaha unhe dil se nikal na sake.🥀** ",
           " 🌺**పుడిపోలని ప్రేరణతో మీరు లేకుండా నేను ఉంటాను, మీరు ప్రగతితో కలిసి ఉత్తమంగా ఉంటారు.**🌺 \n\n**🥀khud nahi janti vo kitni pyari hai jan hai hamari par jan se jyda payari hai duriya ke hone se frak nahi pdta vo kal bhe hamari the or aaj bhe hamari hai.🥀** ",
           " 🌺**ఇష్కు మీరు నా తో పరిచయం చూపించారు, మీరు ఎదురుగా అంగీకరించడం ప్రారంభించండి.**🌺 \n\n**🥀Chupke Se Aakar Iss Dil Mein Utar Jate Ho, Saanso Mein Meri Khushbu BanKe Bikhar Jate Ho,Kuchh Yun Chala Hai Tere Ishq Ka Jadoo, Sote-Jagte Tum Hi Tum Najar Aate Ho..🥀** ",
           " 🌺**ప్రేమ విపరీతములు ఉన్నారు, ఎప్పటికీ రాహితీ ప్రేరణను చూపిస్తూ ఉండండి.**🌺 \n\n**🥀Dil ki khamoshiyan bhi tumse pyaar karti hai is liye har pal tumhare saath rehne ka man karata hai.🥀** "
        ]

# Command
    


@app.on_message(filters.command(["shayari" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐎𝐧𝐥𝐲 𝐅𝐨𝐫 𝐆𝐫𝐨𝐮𝐩𝐬.")

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
        return await message.reply("𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐁𝐚𝐛𝐲, 𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 . ")

    if message.reply_to_message and message.text:
        return await message.reply("/shayaril  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/shayari  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ...")
    else:
        return await message.reply("/shayari  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ..")
    if chat_id in spam_chats:
        return await message.reply("𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐭 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐨𝐩 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 ...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(SHAYRI)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


#

@app.on_message(filters.command(["shstop", "shayarioff"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐈'𝐦 𝐍𝐨𝐭 ..")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐁𝐚𝐛𝐲, 𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 𝐓𝐚𝐠 𝐌𝐞𝐦𝐛𝐞𝐫𝐬.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♦ OFFFFFFFFF♦")
