import discord
import logging
import re
import pymongo
import operator
import random, os, json

#Debug log setup
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Discord setup
client = discord.Client()

#MongoDB setup
dbClient = pymongo.MongoClient(
            "mongodb+srv://???:???@???.mongodb.net")
db = dbClient.neoninobot

COLORS = {"Red": 11740160,
          "Blue": 2133755,
          "Green": 109824,
          "Colorless": 12700886,
          "Bow": 12700886,
          "Breath": 12700886,
          "Dagger": 12700886,
          "4": 16775785,
          "3": 16766720,
          "2": 12632256,
          "1": 13467442,
          "Assist": 4454350,
          "Special": 16400592}
WEAPONS = {"Red Sword": "<:rsword:473280235136221195>",
           "Blue Lance": "<:blance:473280974810120214>",
           "Green Axe": "<:gaxe:473281036948602920>",
           "Colorless Bow": "<:ncbow:473281132214091779>",
           "Red Bow": "<:rbow:473281261671022592>",
           "Blue Bow": "<:bbow:473280951288594432>",
           "Green Bow": "<:gbow:473281065725984779>",
           "Bow": "<:rbow:473281261671022592><:bbow:473280951288594432>" + \
                  "<:gbow:473281065725984779><:ncbow:473281132214091779>",
           "Colorless Dagger": "<:ncdagger:473281155081306114>",
           "Red Dagger": "<:rdagger:476949815566008360>",
           "Blue Dagger": "<:bdagger:476949626113622037>",
           "Green Dagger": "<:gdagger:476949789661986836>",
           "Dagger": "<:rdagger:476949815566008360>"+ \
                     "<:bdagger:476949626113622037>"+ \
                     "<:gdagger:476949789661986836>"+ \
                     "<:ncdagger:473281155081306114>",
           "Colorless Staff": "<:ncstaff:473281222731366401>",
           "Red Tome": "<:rtome:473281324531318806>",
           "Blue Tome": "<:btome:473280998960922644>",
           "Green Tome": "<:gtome:473281101574438913>",
           "Red Breath": "<:rbreath:473281281589772299>",
           "Blue Breath": "<:bbreath:473280961539342337>",
           "Green Breath": "<:gbreath:473281083874607135>",
           "Colorless Breath": "<:ncbreath:473281179882225675>",
           "Breath": "<:rbreath:473281281589772299>"+ \
                     "<:bbreath:473280961539342337>"+ \
                     "<:gbreath:473281083874607135>"+ \
                     "<:ncbreath:473281179882225675>"}
MT = {"Infantry": "<:infantry:473279936677937153>",
      "Flying": "<:flying:473279830956179476>",
      "Cavalry": "<:cavalry:473279789088768000>",
      "Armored": "<:armored:473279769929056281>"}
LEGENDARY = {"Fire": "<:lfire:471580215655792661>",
             "Water": "<:lwater:471578904725815306>",
             "Wind": "<:lwind:471580315316518922>",
             "Earth": "<:learth:471580189013442563>",
             "Atk": "<:latk:471580178087149569>",
             "Spd": "<:lspd:471578972992307201>",
             "Def": "<:ldef:471580199113326593>",
             "Res": "<:lres:471580260090249216>"}
STARS = {5: "<:5Star:474433750718087189>",
         4: "<:4Star:466723465513140225>",
         3: "<:3Star:466723519414272000>",
         2: "<:2Star:466723367064698893>",
         1: "<:1Star:466723420567109653>",
        "S": "<:SStar:474437597511548939>",
        "5*+10": "<:510Star:474936158170775573>",
        "S10": "<:S10Star:474936382087757834>"}
PASSIVES = {"A": "<:IconAPassive:466723177763045387>",
            "B": "<:IconBPassive:466723323905310730>",
            "C": "<:IconCPassive:466723290140901397>",
            "Transparent": "<:ncbadge:468290716372828163>",
            "Scarlet": "<:rbadge:468290739286310922>",
            "Azure": "<:bbadge:468290757589991425>",
            "Verdant": "<:gbadge:468290690108096522>",
            "Weapon": "<:IconWeapon:466723674507182120>",
            "Special": "<:IconSpecial:466723251867877386>",
            "Assist": "<:IconAssist:466723225196560385>"}
SPECIAL_RESTRICTS = {"Melee Weapon Users Only":
                        ['Red Bow', 'Red Tome', 'Blue Bow', 'Blue Tome',
                         'Green Bow', 'Green Tome', 'Colorless Bow',
                         'Colorless Dagger', 'Colorless Staff'],
                     "Excludes Staff Users": ['Colorless Staff'],
                     "Sword, Lance, Axe Users Only":
                         ['Red Bow', 'Red Tome', 'Red Breath', 'Blue Bow',
                          'Blue Tome', 'Blue Breath', 'Green Bow', 'Green Tome',
                          'Green Breath', 'Colorless Bow', 'Colorless Dagger',
                          'Colorless Staff', 'Colorless Breath'],
                     "Staff Users Only": ['Red Sword', 'Red Bow', 'Red Tome',
                                          'Red Breath', 'Blue Lance',
                                          'Blue Bow', 'Blue Tome',
                                          'Blue Breath', 'Green Axe',
                                          'Green Bow', 'Green Tome',
                                          'Green Breath', 'Colorless Bow',
                                          'Colorless Dagger',
                                          'Colorless Breath']
                     }
ASSIST_RESTRICTS = {"Staff Users Only": ['Red Sword', 'Red Bow', 'Red Tome',
                                         'Red Breath', 'Blue Lance',
                                         'Blue Bow', 'Blue Tome',
                                         'Blue Breath', 'Green Axe',
                                         'Green Bow', 'Green Tome',
                                         'Green Breath', 'Colorless Bow',
                                         'Colorless Dagger',
                                         'Colorless Breath'],
                    "Excludes Staff Users": ['Colorless Staff']
                    }
EVERYONE_SKILLS = {"Iron Sword": "All 1" + STARS[1] + " Sword Users",
                    "Iron Axe":    "All 1" + STARS[1] + " Axe Users",
                    "Iron Lance":    "All 1" + STARS[1] + " Lance Users",
                    "Iron Dagger":    "All 1" + STARS[1] + " Dagger Users",
                    "Iron Bow":    "All 1" + STARS[1] + " Bow Users",
                    "Assault":    "All 1" + STARS[1] + " Staff Users",
                    "Heal":    "All 1" + STARS[1] + " Staff Users",
                    "Fire Breath":    "All 1" + STARS[1] + " Breath Users",

                    "Steel Sword":    "All 2" + STARS[2] + " Sword Users",
                    "Steel Axe":    "All 2" + STARS[2] + " Axe Users",
                    "Steel Lance":    "All 2" + STARS[2] + " Lance Users",
                    "Steel Dagger":    "All 2" + STARS[2] + " Dagger Users",
                    "Steel Bow":    "All 2" + STARS[2] + " Bow Users",
                    "Imbue":    "All 2" + STARS[2] + " Staff Users",
                    "Fire Breath+":    "All 2" + STARS[2] + " Breath Users"}

# Meme Consts
MEME_FILE = "memes.json"
MEME_IDS = "approved_ids"
MEME_ROLES = "approved_roles"
MEMES = "memes"
APPROVED_MEME_IDS = ["220546423265951745"]
APPROVED_MEME_ROLES = ["Black Fang"]

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Hero Stats command
    if re.search('^!h (5|4|3|2|1)\*', message.content):
        #collecting input
        hero_string = message.content.split("*")[1]
        nature = ""
        merge = 0
        hero_alias = ""

        if "~ss" in hero_string:
            if "/" in hero_string and hero_string.index("/") \
                                                    < hero_string.index("~ss") :
                hero_alias = hero_string.split("~ss")[0][:-3]
            else:
                hero_alias = hero_string.split("~ss")[0]
        elif "-ss" in hero_string:
            if "/" in hero_string and hero_string.index("/") \
                                                    < hero_string.index("-ss") :
                hero_alias = hero_string.split("-ss")[0][:-3]
            else:
                hero_alias = hero_string.split("-ss")[0]

        if "/" in hero_string:
            hero_alias, nature = check_nature(hero_alias, hero_string)

        if "+" in hero_string:
            hero_alias, merge = check_merge(hero_alias, hero_string)

        if hero_alias == "":
            hero_alias = hero_string

        r = int(message.content[3])

        #pulling relevant hero data
        heroes = db.heroes.find({"aliases":
                                  re.compile("^"+re.escape(hero_alias)+"$",
                                               re.IGNORECASE),
                                 "stats."+str(r)+"*1": {"$exists":True},
                                 "stats."+str(r)+"*40": {"$exists":True}},
                                {"wikiName", "displayName", "portraitUrl",
                                 "weaponType", "movementType", "stats",
                                 "growthPoints", "legendaryBonus"})
        for hero in heroes:
            #extracting relevant data
            base_stats = hero["stats"][str(r)+"*1"]

            if len(nature) != 0:
                hero["stats"][str(r)+"*1"], \
                hero["stats"][str(r)+"*40"] \
                = nature_mod(r, hero, nature)

            if merge != 0:
                hero["stats"][str(r)+"*1"], \
                hero["stats"][str(r)+"*40"] \
                = merge_mod(r, hero, merge)

            if "~ss" in hero_string or "-ss" in hero_string:
                for s in hero["stats"][str(r)+"*1"]:
                    hero["stats"][str(r)+"*1"][s]+=2

                for s in hero["stats"][str(r)+"*40"]:
                    hero["stats"][str(r)+"*40"][s]+=2

                hero["stats"][str(r)+"*1"]["HP"]+=3
                hero["stats"][str(r)+"*40"]["HP"]+=3

            base_stats = hero["stats"][str(r)+"*1"]

            if len(nature) == 0:
                max_stats = super_b_mod(str(r)+"*", hero, True, False)
            else:
                max_stats = [str(x) for x in \
                            list(hero["stats"][str(r)+"*40"].values())]

            legendary_bonus_text = ""

            if len(hero['legendaryBonus']) > 0:
                bonus_stats = hero["legendaryBonus"]["statBoost"][1:]

                stat_names = ['Atk', 'Spd', 'Def', 'Res']
                stat_emojis = [LEGENDARY['Atk'], LEGENDARY['Spd'],
                               LEGENDARY['Def'], LEGENDARY['Res']]

                bonus_index = [index for index, stat in enumerate(bonus_stats) \
                               if stat != 0][0]
                element_emoji = LEGENDARY[hero['legendaryBonus']['element']]

                legendary_bonus_text = ", " \
                   + "HP+3 " + stat_names[bonus_index] \
                   + "+" \
                   + str(hero['legendaryBonus']['statBoost'][bonus_index+1]) \
                   + element_emoji \
                   + stat_emojis[bonus_index]

            stat_string = "```    L1|40" + "\n    -- --" \
            + "\nHP :" + "{:>2}".format(base_stats["HP"]) + "|" +max_stats[0]  \
            + "\nATK:" + "{:>2}".format(base_stats["Atk"]) + "|" +max_stats[1] \
            + "\nSPD:" + "{:>2}".format(base_stats["Spd"]) + "|" +max_stats[2] \
            + "\nDEF:" + "{:>2}".format(base_stats["Def"]) + "|" +max_stats[3] \
            + "\nRES:" + "{:>2}".format(base_stats["Res"]) + "|" +max_stats[4] \
            + "```" + " BST: " + str(get_bst(str(r)+"*", hero, True)) \
            + legendary_bonus_text

            page = "https://feheroes.gamepedia.com/" + \
                   hero["wikiName"].replace(" ", "_")

            #building response embed
            embed = discord.Embed(color=COLORS[hero["weaponType"].split(" ")[0]])
            embed_name = hero["displayName"]
            embed_name += "" if merge == 0 else "+" + str(merge)
            embed_name += "" if len(nature)==0 else \
                          " (+" + nature["boon"] + ", -" + nature["bane"] + ")"
            embed.set_author(name=embed_name,
                             url=page)

            if "~ss" in hero_string or "-ss" in hero_string:
                if r == 5 and merge == 10:
                    embed_emotes = STARS["S10"]*5
                else:
                    embed_emotes = STARS["S"]*r
            else:
                if r == 5 and merge == 10:
                    embed_emotes = STARS["5*+10"]*5
                else:
                    embed_emotes = STARS[r]*r

            embed_emotes += WEAPONS[hero["weaponType"]] \
                            + MT[hero["movementType"]]

            embed.add_field(name=embed_emotes, value=stat_string, inline=True)
            embed.set_thumbnail(url=hero["portraitUrl"])

            #sending response
            await client.send_message(message.channel, embed=embed)

    #Hero Lv1 Default Stats command
    elif re.search('^!hw (5|4|3|2|1)\*', message.content):
        #collecting input
        hero_alias = message.content.split("*")[1]
        r = int(message.content[4])

        #pulling relevant hero data
        heroes = db.heroes.find({"aliases":
                                  re.compile("^"+re.escape(hero_alias)+"$",
                                               re.IGNORECASE),
                                 "stats."+str(r)+"*1": {"$exists":True}},
                                {"wikiName", "displayName", "portraitUrl",
                                 "weaponType", "movementType", "stats",
                                 "growthPoints", "weapons", "legendaryBonus"})

        for hero in heroes:
            #extracting relevant data
            if hero["weaponType"] != "Colorless Staff":
                if r == 4:
                    stat_mod = db.skills.find_one({"name":
                                                    hero["weapons"][2][0]},
                                                    {"stat_mod"})["stat_mod"]
                    weapon = hero["weapons"][2][0]
                elif r == 3:
                    stat_mod = db.skills.find_one({"name":
                                                    hero["weapons"][1][0]},
                                                    {"stat_mod"})["stat_mod"]
                    weapon = hero["weapons"][1][0]
                elif r == 5:
                    stat_mod = db.skills.find_one({"name":
                                                    hero["weapons"][3][0]},
                                                    {"stat_mod"})["stat_mod"]
                    weapon = hero["weapons"][3][0]
                elif r == 1 or r == 2:
                    stat_mod = db.skills.find_one({"name":
                                                    hero["weapons"][0][0]},
                                                    {"stat_mod"})["stat_mod"]
                    weapon = hero["weapons"][0][0]
            else:
                stat_mod = [0,0,0,0,0]
                weapon = "N/A"

            base_stats = [hero["stats"][str(r)+"*1"][s] \
                          for s in hero["stats"][str(r)+"*1"]]

            for s in range(5):
                base_stats[s]+=stat_mod[s]

                if base_stats[s] < 0:
                    base_stats[s] = 0

            supers = super_b_mod(str(r)+"*", hero, False, False)

            legendary_bonus_text = ""

            if len(hero['legendaryBonus']) > 0:
                bonus_stats = hero["legendaryBonus"]["statBoost"][1:]

                stat_names = ['Atk', 'Spd', 'Def', 'Res']
                stat_emojis = [LEGENDARY['Atk'], LEGENDARY['Spd'],
                               LEGENDARY['Def'], LEGENDARY['Res']]

                bonus_index = [index for index, stat in enumerate(bonus_stats) \
                               if stat != 0][0]
                element_emoji = LEGENDARY[hero['legendaryBonus']['element']]

                legendary_bonus_text = ", " \
                   + "HP+3 " + stat_names[bonus_index] \
                   + "+" \
                   + str(hero['legendaryBonus']['statBoost'][bonus_index+1]) \
                   + element_emoji \
                   + stat_emojis[bonus_index]

            stat_string = "**Weapon: **\n"+weapon+"```" \
                        + "\nHP :" + "{:>2}".format(base_stats[0]) + supers[0]\
                        + "\nATK:" + "{:>2}".format(base_stats[1]) + supers[1]\
                        + "\nSPD:" + "{:>2}".format(base_stats[2]) + supers[2]\
                        + "\nDEF:" + "{:>2}".format(base_stats[3]) + supers[3]\
                        + "\nRES:" + "{:>2}".format(base_stats[4]) + supers[4]\
                        + "```" + " BST: "+str(get_bst(str(r)+"*",hero,False))\
                        + legendary_bonus_text

            page = "https://feheroes.gamepedia.com/" + \
                   hero["wikiName"].replace(" ", "_")

            #building response embed
            embed = discord.Embed(color=COLORS[hero["weaponType"].split(" ")[0]])
            embed.set_author(name=hero["displayName"]+" Lv.1", url=page)
            embed.add_field(name=STARS[r]*r+ WEAPONS[hero["weaponType"]] + \
                                 MT[hero["movementType"]],
                            value=stat_string, inline=True)
            embed.set_thumbnail(url=hero["portraitUrl"])

            #sending response
            await client.send_message(message.channel, embed=embed)

    #Hero Skills command
    elif message.content.startswith('!h '):
        #collecting input
        hero_alias = message.content[3:]

        #pulling relevant hero data
        heroes = db.heroes.find({"aliases":
                                    re.compile("^"+re.escape(hero_alias)+"$",
                                               re.IGNORECASE)},
                                    {"aliases": False,
                                     "growthPoints": False})
        for hero in heroes:
            #extracting relevant data
            page = "https://feheroes.gamepedia.com/" + \
                   hero["wikiName"].replace(" ", "_")

            legendary_bonus_text = ""

            if len(hero['legendaryBonus']) > 0:
                bonus_stats = hero["legendaryBonus"]["statBoost"][1:]

                stat_names = ['Atk', 'Spd', 'Def', 'Res']
                stat_emojis = [LEGENDARY['Atk'], LEGENDARY['Spd'],
                               LEGENDARY['Def'], LEGENDARY['Res']]

                bonus_index = [index for index, stat in enumerate(bonus_stats) \
                               if stat != 0][0]
                element_emoji = LEGENDARY[hero['legendaryBonus']['element']]

                legendary_bonus_text = ", " \
                   + "HP+3 " + stat_names[bonus_index] \
                   + "+" \
                   + str(hero['legendaryBonus']['statBoost'][bonus_index+1]) \
                   + element_emoji \
                   + stat_emojis[bonus_index]

            #building response embed
            embed = discord.Embed(color=COLORS[hero["weaponType"].split(" ")[0]])
            embed.set_author(name=hero["displayName"],
                             url=page)
            embed.add_field(name= WEAPONS[hero["weaponType"]] + \
                                  MT[hero["movementType"]] + "\n" + \
                                  PASSIVES['Weapon']+" Weapon",
                            value="**" + hero["weapons"][-1][0] + "**" if \
                                  len(hero["weapons"]) != 5 else \
                                  "**" + hero["weapons"][-1][0] + "\n" + \
                                  hero["weapons"][-2][0] + "**",
                            inline=False)
            embed.add_field(name=PASSIVES['Assist']+" Assist",
                            value="**" + hero["assists"][-1][0] + "**" if \
                                  len(hero["assists"]) != 0 else "N/A",
                            inline=False)
            embed.add_field(name=PASSIVES['Special']+" Special",
                            value="**" + hero["specials"][-1][0] + "**" if \
                                  len(hero["specials"]) != 0 else "N/A",
                            inline=False)
            embed.add_field(name="\n\nPassives",
                            value=(PASSIVES['A']+"**:** " + \
                                  hero["a"][-1][0] + " (" + \
                                  str(hero["a"][-1][1]) + STARS[hero["a"][-1][1]] +\
                                  ")\n" if len(hero["a"]) != 0 else \
                                  PASSIVES['A']+"**:** N/A\n") \
                                  + \
                                  (PASSIVES['B']+"**:** " + \
                                  hero["b"][-1][0] + " (" + \
                                  str(hero["b"][-1][1]) + STARS[hero["b"][-1][1]] +\
                                  ")\n" if len(hero["b"]) != 0 else \
                                  PASSIVES['B']+"**:** N/A\n") \
                                  + \
                                  (PASSIVES['C']+"**:** " + \
                                  hero["c"][-1][0] + " (" + \
                                  str(hero["c"][-1][1]) + STARS[hero["c"][-1][1]] + \
                                  ")\nBST: " + str(get_bst("5*", hero, True)) \
                                  + legendary_bonus_text
                                  if len(hero["c"]) != 0 else \
                                  PASSIVES['C']+"**:** N/A" + \
                                  "\nBST: " + str(get_bst("5*", hero, True)) \
                                  + legendary_bonus_text),
                            inline=False)
            embed.set_thumbnail(url=hero["portraitUrl"])

            #sending response
            await client.send_message(message.channel, embed=embed)

    #Hero Alt command
    elif message.content.startswith('!a '):
        #collecting input
        hero_name = message.content[3:]

        #pulling relevant hero data
        heroes = db.heroes.find({"displayName":
                                    {"$regex": "^"+hero_name,
	                                 "$options": "im"}},
                                {"displayName"})

        alts = []
        alt_string = ""

        for h in heroes:
            alts.append(h["displayName"])

        for a in sorted(alts):
            if a != "Marth(Mask)":
                alt_string += a + "\n"

        exceptions = ["Black Knight", "Robin(M)", "Robin(F)", "Morgan(M)",
                      "Morgan(F)", "Corrin(M)", "Corrin(F)", "Kana(F)",
                      "Kana(M)", "Tiki(Y)", "Tiki(A)", "Charlotte(BB)",
                      "Noire(SA)", "Inigo(PA)", "Veronica(AB)"]

        if len(alt_string) != 0:
            if hero_name[0].upper()+hero_name[1:].lower() in alts:
                await client.send_message(message.channel,
                                          "```\n"+alt_string+"```")
            else:
                for a in alts:
                    if a in exceptions:
                        await client.send_message(message.channel,
                                                  "```\n"+alt_string+"```")
                        return

    #Compare command
    elif message.content.startswith('!c '):
        #collecting input
        try:
            hero_string_1 = message.content.split(" vs ")[0][3:]
            hero_string_2 = message.content.split(" vs ")[1]
        except IndexError:
            hero_string_1 = message.content[3:].split(" ")[0]
            hero_string_2 = message.content[3:].split(" ")[1]

        nature_1 = ""
        merge_1 = 0
        hero_alias_1 = ""
        rarity_1 = "5*"

        if hero_string_1[0] in ["1","2","3","4","5"]:
            rarity_1 = hero_string_1[0] + "*"
            hero_string_1 = hero_string_1[1:]

        if "~ss" in hero_string_1:
            if "/" in hero_string_1 and hero_string_1.index("/") \
                                                  < hero_string_1.index("~ss") :
                hero_alias_1 = hero_string_1.split("~ss")[0][:-3]
            else:
                hero_alias_1 = hero_string_1.split("~ss")[0]
        elif "-ss" in hero_string_1:
            if "/" in hero_string_1 and hero_string_1.index("/") \
                                                  < hero_string_1.index("-ss") :
                hero_alias_1 = hero_string_1.split("-ss")[0][:-3]
            else:
                hero_alias_1 = hero_string_1.split("-ss")[0]

        if "/" in hero_string_1:
            hero_alias_1, nature_1 = check_nature(hero_alias_1, hero_string_1)
        if "+" in hero_string_1:
            hero_alias_1, merge_1 = check_merge(hero_alias_1, hero_string_1)
        if hero_alias_1 == "":
            hero_alias_1 = hero_string_1

        nature_2 = ""
        merge_2 = 0
        hero_alias_2 = ""
        rarity_2 = "5*"

        if hero_string_2[0] in ["1","2","3","4","5"]:
            rarity_2 = hero_string_2[0] + "*"
            hero_string_2 = hero_string_2[1:]

        if "~ss" in hero_string_2:
            if "/" in hero_string_2 and hero_string_2.index("/") \
                                                  < hero_string_2.index("~ss") :
                hero_alias_2 = hero_string_2.split("~ss")[0][:-3]
            else:
                hero_alias_2 = hero_string_2.split("~ss")[0]
        elif "-ss" in hero_string_2:
            if "/" in hero_string_2 and hero_string_2.index("/") \
                                                  < hero_string_2.index("-ss") :
                hero_alias_2 = hero_string_2.split("-ss")[0][:-3]
            else:
                hero_alias_2 = hero_string_2.split("-ss")[0]

        if "/" in hero_string_2:
            hero_alias_2, nature_2 = check_nature(hero_alias_2, hero_string_2)
        if "+" in hero_string_2:
            hero_alias_2, merge_2 = check_merge(hero_alias_2, hero_string_2)
        if hero_alias_2 == "":
            hero_alias_2 = hero_string_2

        #pulling relevant hero data
        hero_1 = db.heroes.find_one({"aliases":
                                    re.compile("^"+re.escape(hero_alias_1)+"$",
                                               re.IGNORECASE)},
                                    {"displayName", "portraitUrl",
                                     "stats", "growthPoints", "movementType",
                                     "weaponType"})
        hero_2 = db.heroes.find_one({"aliases":
                                    re.compile("^"+re.escape(hero_alias_2)+"$",
                                               re.IGNORECASE)},
                                    {"displayName", "portraitUrl",
                                     "stats", "growthPoints", "movementType",
                                     "weaponType"})

        #setting up relevant data
        if len(nature_1) != 0:
            hero_1["stats"][rarity_1+"1"], \
            hero_1["stats"][rarity_1+"40"] \
            = nature_mod(int(rarity_1[0]), hero_1, nature_1)
        if merge_1 != 0:
            hero_1["stats"][rarity_1+"40"] = merge_mod(int(rarity_1[0]),
                                                       hero_1, merge_1)[1]

        if len(nature_2) != 0:
            hero_2["stats"][rarity_2+"1"], \
            hero_2["stats"][rarity_2+"40"] \
            = nature_mod(int(rarity_2[0]), hero_2, nature_2)
        if merge_2 != 0:
            hero_2["stats"][rarity_2+"40"] = merge_mod(int(rarity_2[0]),
                                                hero_2, merge_2)[1]

        if "~ss" in hero_string_1 or "-ss" in hero_string_1:
            for s in hero_1["stats"][rarity_1+"1"]:
                hero_1["stats"][rarity_1+"1"][s]+=2

            for s in hero_1["stats"][rarity_1+"40"]:
                hero_1["stats"][rarity_1+"40"][s]+=2

            hero_1["stats"][rarity_1+"1"]["HP"]+=3
            hero_1["stats"][rarity_1+"40"]["HP"]+=3

        if "~ss" in hero_string_2 or "-ss" in hero_string_2:
            for s in hero_2["stats"][rarity_2+"1"]:
                hero_2["stats"][rarity_2+"1"][s]+=2

            for s in hero_2["stats"][rarity_2+"40"]:
                hero_2["stats"][rarity_2+"40"][s]+=2

            hero_2["stats"][rarity_2+"1"]["HP"]+=3
            hero_2["stats"][rarity_2+"40"]["HP"]+=3

        if len(nature_1) != 0:
            max_stats_1 = hero_1["stats"][rarity_1+"40"]
            max_string_1 = "HP: " + str(max_stats_1["HP"]) + \
                "\nATK: " + str(max_stats_1["Atk"]) + \
                "\nSPD: " + str(max_stats_1["Spd"]) + \
                "\nDEF: " + str(max_stats_1["Def"]) + \
                "\nRES: " + str(max_stats_1["Res"])

        if len(nature_2) != 0:
            max_stats_2 = hero_2["stats"][rarity_2+"40"]
            max_string_2 = "HP: " + str(max_stats_2["HP"]) + \
                "\nATK: " + str(max_stats_2["Atk"]) + \
                "\nSPD: " + str(max_stats_2["Spd"]) + \
                "\nDEF: " + str(max_stats_2["Def"]) + \
                "\nRES: " + str(max_stats_2["Res"])

        stat_dict = {0: "HP", 1: "Atk", 2: "Spd", 3: "Def", 4: "Res"}
        results = []
        result_string = ""
        hero_stats = [list(hero_1["stats"][rarity_1+"40"].values()),
                      list(hero_2["stats"][rarity_2+"40"].values())]
        bst1 = get_bst(rarity_1, hero_1, True)
        bst2 = get_bst(rarity_2, hero_2, True)

        if hero_alias_1 == hero_alias_2:
            result_name_1 = hero_1["displayName"]+" 1"
            result_name_2 = hero_2["displayName"]+" 2"
        else:
            result_name_1 = hero_1["displayName"]
            result_name_2 = hero_2["displayName"]

        for i in range(5):
            results.append(hero_stats[0][i] - hero_stats[1][i])

        for i in range(5):
            if results[i] < 0:
                result_string += result_name_2 + " has **" + \
                                 str(abs(results[i])) + "** more " + \
                                 stat_dict[i] + "\n"
            elif results[i] > 0:
                result_string += result_name_1 + " has **" + \
                                 str(abs(results[i])) + "** more " + \
                                 stat_dict[i] + "\n"
            else:
                result_string += "Equal " + stat_dict[i] + "\n"

        if bst1 > bst2:
            result_string += result_name_1 + " has **" + str(bst1-bst2)\
                             + "** more BST"
        elif bst2 > bst1:
            result_string += result_name_2 + " has **" + str(bst2-bst1)\
                             + "** more BST"
        else:
            result_string += "Equal BST"

        #building response embed
        embed = discord.Embed(color=COLORS["Colorless"])
        embed.set_image(url="https://cdn.discordapp.com/attachments/" + \
                        "458338281667428355/468202446724792330/ninowhut.png")
        embed_name_1 = hero_1["displayName"]
        embed_name_1 += "-SS" \
                        if "~ss" in hero_string_1 or "-ss" in hero_string_1 \
                        else ""
        embed_name_1 += " 1" if hero_alias_1 == hero_alias_2 else ""
        embed_name_1 += "" if merge_1 == 0 else "+" + str(merge_1)
        embed_name_1 += "" if len(nature_1)==0 else \
                      "\n (+" + nature_1["boon"] + ", -" + nature_1["bane"] + ")"
        embed_value_1 = super_b_mod(rarity_1, hero_1, True, True) \
                        if len(nature_1) == 0 \
                        else max_string_1
        embed_value_1 += "\nBST: " + str(get_bst(rarity_1, hero_1, True))+ "\n" + \
                         WEAPONS[hero_1["weaponType"]] + \
                         MT[hero_1["movementType"]]
        embed.add_field(name=rarity_1+" "+embed_name_1,
                        value=embed_value_1,
                        inline=True)
        embed_name_2 = hero_2["displayName"]
        embed_name_2 += "-SS" \
                        if "~ss" in hero_string_2 or "-ss" in hero_string_2 \
                        else ""
        embed_name_2 += " 2" if hero_alias_1 == hero_alias_2 else ""
        embed_name_2 += "" if merge_2 == 0 else "+" + str(merge_2)
        embed_name_2 += "" if len(nature_2)==0 else \
                      "\n (+" + nature_2["boon"] + ", -" + nature_2["bane"] + ")"
        embed_value_2 = super_b_mod(rarity_2, hero_2, True, True) \
                        if len(nature_2) == 0 \
                        else max_string_2
        embed_value_2 += "\nBST: " + str(get_bst(rarity_2, hero_2, True)) + "\n" + \
                         WEAPONS[hero_2["weaponType"]] + \
                         MT[hero_2["movementType"]]
        embed.add_field(name=rarity_2+" "+embed_name_2,
                        value=embed_value_2,
                        inline=True)
        embed.add_field(name="Results", value=result_string, inline=True)

        #sending response
        await client.send_message(message.channel, embed=embed)

    #Skill command
    elif message.content.startswith('!s '):
        #collecting input
        skill_alias = message.content[3:]

        #pulling relevant skill data
        skills = db.skills.find({"aliases":
                                 re.compile("^"+re.escape(skill_alias)+"$",
                                               re.IGNORECASE)} ,
                                 {"aliases": False})

        for skill in skills:
            #creating response
            response_string = ""

            #non-weapons
            if skill["type"] in ("A","B","C","S","Special","Assist"):
                #skill type
                response_string += "\n**Type:** "
                response_string += PASSIVES[skill["type"]] if skill["type"] != "S" \
                                   else PASSIVES[skill["sealColor"]] \
                                   if skill["sealColor"]!="" else "Sacred Seal"
                response_string += ", " + PASSIVES[skill["sealColor"]] \
                                   if skill["type"] not in ("S","Special","Assist")\
                                   and skill["seal"] == True \
                                   else ""
                #skill sp cost
                response_string += "\n**Cost:** "
                response_string += str(skill["spCost"]) \
                                   if skill["spCost"] != 0 else "N/A"
                response_string += ", " + str(int(skill["spCost"]*1.5)) + \
                                   " (Inherited)" \
                                   if skill["prf"]!=True \
                                   else ""

                #special/assist exclusive fields
                if skill["type"] not in ("A","B","C","S"):
                    if skill["type"] == "Special":
                        response_string += "\n**Cooldown:** "+str(skill["cooldown"])
                    elif skill["type"] == "Assist":
                        response_string += "\n**Range:** "+str(skill["range"])
                #prereqs
                if len(skill["prereq"]) > 0:
                    response_string += "\n**Prereq:** "+ str(skill["prereq"][0])
                    response_string += " or " + str(skill["prereq"][1]) \
                                       if len(skill["prereq"]) > 1 \
                                       else ""
                #skill effect
                response_string += "\n**Effect:** " + skill["effect"]

                #clarification note
                try:
                    response_string += "\n**Note:** " + skill["note"]
                except KeyError:
                    pass

                #skill source
                response_string += "\n**Heroes:** "
                if skill["name"] not in EVERYONE_SKILLS:
                    for r in skill["source"]:
                        if len(skill["source"][r]) > 0:
                            response_string += "\n" + r + STARS[int(r)] + ": "
                        for h in skill["source"][r]:
                            response_string += h + ", "
                        response_string = response_string[0:-2] \
                                          if len(skill["source"][r])!=0 \
                                          else response_string
                    response_string += "N/A" \
                                       if skill["type"] == "S" \
                                       else ""
                else:
                    response_string += EVERYONE_SKILLS[skill["name"]]

                #inherit restrictions
                response_string += "\n**Can be Inherited?** " \
                                   if skill["type"] != "S" \
                                   else "\n**Can be Equipped?** "

                if skill["type"] in ("A","B","C","S"):
                    response_string += "Yes" \
                                       if skill["inheritRestrict"] == "" \
                                       else skill["inheritRestrict"] \
                                       if skill["inheritRestrict"]!="Is exclusive" \
                                       else "No"
                else:
                    if len(skill["weaponRestrict"]) == 0:
                        if skill["prf"] == True:
                            response_string += "No"
                        else:
                            response_string += "Yes"
                    elif skill["type"] == "Special":
                        restrict = skill["weaponRestrict"]
                        for r in SPECIAL_RESTRICTS:
                            if set(restrict) == set(SPECIAL_RESTRICTS[r]):
                               response_string += r
                               break
                    elif skill["type"] == "Assist":
                        restrict = skill["weaponRestrict"]
                        for r in ASSIST_RESTRICTS:
                            if set(restrict) == set(ASSIST_RESTRICTS[r]):
                               response_string += r
                               break
            else: #weapons
                #weapon type
                response_string += "\n**Type:** " + WEAPONS[skill["type"]]

                #weapon Mt(s)
                response_string += "\n**Mt:** " + str(skill["Mt"])
                response_string += ", " + str(skill["Mt2"]) + " (Refined)" \
                                   if skill["Mt2"] != 0 else "" \
                                   if skill["name"] != "Cherche's Axe" else \
                                   ", 12 (Atk Refine)"

                #weapon sp cost(s)
                response_string += "\n**Cost:** " + str(skill["spCost"])
                response_string += ", " + str(int(skill["spCost"]*1.5)) + \
                                   " (Inherited)" if skill["prf"]==False \
                                   else ""
                response_string += " | " + str(skill["spCost2"]) + " (Refine)"\
                                   + ", " + str(int(skill["spCost2"]*1.5)) + \
                                                      " (Inherited Refine)" \
                                   if skill["spCost2"] != 0 else ""

                #prereqs
                if len(skill["prereq"]) > 0:
                    response_string += "\n**Prereq:** "+ str(skill["prereq"][0])
                    response_string += " or " + str(skill["prereq"][1]) \
                                       if len(skill["prereq"]) > 1 \
                                       else ""
                #weapon effect(s)
                response_string += "\n**Effect:** " + skill["effect"]
                response_string += "\n\n**Refined Effect:** " + skill["refinedEffect"]+"\n" \
                                   if skill["refinedEffect"] != "" else ""
                response_string += "\n" if skill["refinedEffect"] == "" and \
                                   skill["specialEffect"] != "" else ""
                if skill["prf"]==False:
                    response_string += "\n**Special Refine:** " + skill["specialEffect"]+"\n" \
                                   if skill["specialEffect"] != "" else ""
                else:
                    response_string += "\n**Special Refine - " + \
                                       skill["specialEffect"].split("***")[0]+":** "\
                                       +skill["specialEffect"].split("***")[1]+"\n"\
                                       if skill["specialEffect"] != "" else ""

                #clarification note
                try:
                    response_string += "\n**Note:** " + skill["note"]
                except KeyError:
                    pass

                #weapon sources
                response_string += "\n**Heroes:** "
                if skill["name"] not in EVERYONE_SKILLS:
                    for r in skill["source"]:
                        if len(skill["source"][r]) > 0:
                            response_string += "\n" + r + STARS[int(r)] + ": "
                        for h in skill["source"][r]:
                            response_string += h + ", "
                        response_string = response_string[0:-2] \
                                          if len(skill["source"][r])!=0 \
                                          else response_string
                    response_string += "N/A" \
                                       if len(skill["source"]) == 0 \
                                       else ""
                else:
                    response_string += EVERYONE_SKILLS[skill["name"]]

                #inherit restrictions/refine info
                response_string += "\n**Can be Inherited?** "
                response_string += "Yes" if skill["prf"] == False else "No"

                response_string += " (Unrefined)" if skill["spCost2"]==350 else ""
                response_string += " (Can refine from "+skill["refinesFrom"][0]+")"\
                                   if len(skill["refinesFrom"]) != 0 else ""
                                   #change if there's ever multiple paths
                response_string += " (Can refine to "+skill["refinesTo"][0] + ")" \
                                   if len(skill["refinesTo"]) != 0 else ""
                                   #change if there's ever multiple paths

            #embed build
            if skill["type"] not in ["A","B","C","S"]:
                embed = discord.Embed(color=COLORS[skill["type"].split()[0]])
            else:
                if skill["name"][-1] in ["1","2","3","4"]:
                    if skill["name"][-1] == "1":
                        if skill["spCost"] >= 80:
                            embed = discord.Embed(color=COLORS["2"])
                        else:
                            embed = discord.Embed(color=COLORS["1"])
                    elif skill["name"][-1] == "2":
                        if skill["spCost"] >= 160:
                            embed = discord.Embed(color=COLORS["3"])
                        else:
                            embed = discord.Embed(color=COLORS["2"])
                    elif skill["name"][-1] == "3":
                        embed = discord.Embed(color=COLORS["3"])
                    else:
                        embed = discord.Embed(color=COLORS["4"])
                else:
                    embed = discord.Embed(color=COLORS["Colorless"])

            embed.add_field(name=skill["name"], value=response_string,
                            inline=False)
            try:
                embed.set_thumbnail(url=skill["icon"])
            except KeyError:
                try:
                    embed.set_thumbnail(url=skill["image"])
                except KeyError:
                    pass

            #sending response
            await client.send_message(message.channel, embed=embed)

    #Help command
    elif message.content == "!help":
        # Build db querying string
        db_cmds = ""
        db_cmds += "!h [5|4|3|2|1]\*[alias] - Gets hero stats for a certain rarity.\n"
        db_cmds += "- - Optionally append the alias with [~ss] for S-rank Summoner Support\n"
        db_cmds += "- - [/[boon][bane]] for nature, with each stat represented by its initial\n"
        db_cmds += "- - [+n] for merge, where n is the desired merge level\n"
        db_cmds += "- - You can also combine any of these so long as merge is listed last\n"
        db_cmds += "- - For example, 5\*Ayra/sr~ss+10\n\n"
        db_cmds += "!hw [5|4|3|2|1]\*[alias] - Gets hero Lv.1 stats for a certain rarity\n"
        db_cmds += "- - This is with their default weapon at that rarity equipped and does not support the additional parameters\n\n"
        db_cmds += "!h [alias] - Gets hero skills\n\n"
        db_cmds += "!a [original name] - Gets names of hero alts\n\n"
        db_cmds += "!c [alias1] vs [alias2] - Compare two hero 5\* statlines.\n"
        db_cmds += "- - Each alias can also be appended with the above support, nature, and merge parameters\n\n"
        db_cmds += "!s [alias] - Gets skill info\n"

        # Build general help string
        help_cmds = ""
        help_cmds += "!help - displays this prompt\n"
        #help_cmds += "!memes - Gets a random FEH meme\n"

        embed = discord.Embed(title="Ninobot Ultra")

        embed.add_field(name="Help Commands", value=help_cmds, inline=True)
        embed.add_field(name="Query Commands", value=db_cmds, inline=True)

        await client.send_message(message.author, embed=embed)

    #Memes commands
    elif message.content == '!memes':
        success, meme = get_meme()

        if success:
            await client.send_message(message.channel, meme)
        else:
            await client.send_message(message.channel, "No memes found :wrathful:")
    elif message.content.startswith('!add '):
        if validate_meme_permissions(message.author):
            if add_meme(message.content[5:]):
                await client.send_message(message.channel, "Added: " + message.content[5:])
            else:
                await client.send_message(message.channel, "Error adding meme: meme already exists ")
    elif message.content.startswith('!remove '):
        if validate_meme_permissions(message.author):
            if remove_meme(message.content[8:]):
                await client.send_message(message.channel, "Removed: " + message.content[8:])
            else:
                await client.send_message(message.channel, "Error removing meme: meme not found")


def super_b_mod(r, h, lv40, compare):
    gp = h["growthPoints"]
    stats = h["stats"][r+"40"] if lv40 else h["stats"][r+"1"]

    if not compare:
        if r == "5*":
            super_hp = "" if gp["HP"] not in (1,5,10,2,6,11) else "-" \
                      if gp["HP"] in (2,6,11) else "+"
            super_atk = "" if gp["Atk"] not in (1,5,10,2,6,11) else "-" \
                      if gp["Atk"] in (2,6,11) else "+"
            super_spd = "" if gp["Spd"] not in (1,5,10,2,6,11) else "-" \
                      if gp["Spd"] in (2,6,11) else "+"
            super_def = "" if gp["Def"] not in (1,5,10,2,6,11) else "-" \
                      if gp["Def"] in (2,6,11) else "+"
            super_res = "" if gp["Res"] not in (1,5,10,2,6,11) else "-" \
                      if gp["Res"] in (2,6,11) else "+"
        elif r == "4*":
            super_hp = "" if gp["HP"] not in (10,11) else "-" \
                      if gp["HP"] == 11 else "+"
            super_atk = "" if gp["Atk"] not in (10,11) else "-" \
                      if gp["Atk"] == 11 else "+"
            super_spd = "" if gp["Spd"] not in (10,11) else "-" \
                      if gp["Spd"] == 11 else "+"
            super_def = "" if gp["Def"] not in (10,11) else "-" \
                      if gp["Def"] == 11 else "+"
            super_res = "" if gp["Res"] not in (10,11) else "-" \
                      if gp["Res"] == 11 else "+"
        else:
            super_hp, super_atk, super_spd, super_def, super_res = "","","","",""
    else:
        if r == "5*":
            super_hp = "" if gp["HP"] not in (1,5,10,2,6,11) else " (-)" \
                      if gp["HP"] in (2,6,11) else " (+)"
            super_atk = "" if gp["Atk"] not in (1,5,10,2,6,11) else " (-)" \
                      if gp["Atk"] in (2,6,11) else " (+)"
            super_spd = "" if gp["Spd"] not in (1,5,10,2,6,11) else " (-)" \
                      if gp["Spd"] in (2,6,11) else " (+)"
            super_def = "" if gp["Def"] not in (1,5,10,2,6,11) else " (-)" \
                      if gp["Def"] in (2,6,11) else " (+)"
            super_res = "" if gp["Res"] not in (1,5,10,2,6,11) else " (-)" \
                      if gp["Res"] in (2,6,11) else " (+)"
        elif r == "4*":
            super_hp = "" if gp["HP"] not in (10,11) else " (-)" \
                      if gp["HP"] == 11 else " (+)"
            super_atk = "" if gp["Atk"] not in (10,11) else " (-)" \
                      if gp["Atk"] == 11 else " (+)"
            super_spd = "" if gp["Spd"] not in (10,11) else " (-)" \
                      if gp["Spd"] == 11 else " (+)"
            super_def = "" if gp["Def"] not in (10,11) else " (-)" \
                      if gp["Def"] == 11 else " (+)"
            super_res = "" if gp["Res"] not in (10,11) else " (-)" \
                      if gp["Res"] == 11 else " (+)"
        else:
            super_hp, super_atk, super_spd, super_def, super_res = "","","","",""

    if not lv40:
        response = [super_hp, super_atk, super_spd, super_def, super_res]
    elif not compare:
        response = [str(stats["HP"]) + super_hp,
                     str(stats["Atk"]) + super_atk,
                     str(stats["Spd"]) + super_spd,
                     str(stats["Def"]) + super_def,
                     str(stats["Res"]) + super_res]
    else:
        response = "HP: " + str(stats["HP"])  + super_hp  + \
                 "\nATK: " + str(stats["Atk"]) + super_atk + \
                 "\nSPD: " + str(stats["Spd"]) + super_spd + \
                 "\nDEF: " + str(stats["Def"]) + super_def + \
                 "\nRES: " + str(stats["Res"]) + super_res


    return response

def get_bst(r, h, forty):
    if forty:
        return sum(h["stats"][r+"40"].values())
    else:
        return sum(h["stats"][r+"1"].values())

def nature_mod(r, h, n):
    h["stats"][str(r)+"*1"][n["boon"]]+=1
    h["stats"][str(r)+"*1"][n["bane"]]-=1

    if r == 5:
        h["stats"]["5*40"][n["boon"]]+=3 \
           if h["growthPoints"][n["boon"]] not in [1,5,10] \
           else 4
        h["stats"]["5*40"][n["bane"]]-=3 \
           if h["growthPoints"][n["bane"]] not in [2,6,11] \
           else 4
    elif r == 4:
        h["stats"]["4*40"][n["boon"]]+=3 \
           if h["growthPoints"][n["boon"]] not in [10] \
           else 4
        h["stats"]["4*40"][n["bane"]]-=3 \
           if h["growthPoints"][n["bane"]] not in [11] \
           else 4
    else:
        h["stats"][str(r)+"*40"][n["boon"]]+=3
        h["stats"][str(r)+"*40"][n["bane"]]-=3

    return h["stats"][str(r)+"*1"], h["stats"][str(r)+"*40"]

def merge_mod(r, h, m):
    sorted_base = sorted(h["stats"][str(r)+"*1"].items(),
                         key=operator.itemgetter(1),
                         reverse=True)
    merge_order = [sb[0] for sb in sorted_base]

    first = 0
    second = 1

    for lv in range(m):
        h["stats"][str(r)+"*1"][merge_order[first]]+=1
        h["stats"][str(r)+"*40"][merge_order[first]]+=1

        h["stats"][str(r)+"*1"][merge_order[second]]+=1
        h["stats"][str(r)+"*40"][merge_order[second]]+=1

        first+=2 if first < 3 else -3
        second+=2 if second < 3 else -3

    return h["stats"][str(r)+"*1"], h["stats"][str(r)+"*40"]

def check_nature(alias, input):
    nat = ""

    try:
        if alias == "":
            alias = input.split("/")[0]
        nat = input.split("/")[1][:2].lower()

        if nat[0] not in "hasdr" or nat[1] not in "hasdr" or \
           nat[0] == nat[1]:
           nat = ""
        else:
            nat = [nat[0], nat[1]]
            for n in range(2):
                if nat[n] == "h":
                    nat[n] = "HP"
                elif nat[n] == "a":
                    nat[n] = "Atk"
                elif nat[n] == "s":
                    nat[n] = "Spd"
                elif nat[n] == "d":
                    nat[n] = "Def"
                elif nat[n] == "r":
                    nat[n] = "Res"
            nat = {"boon": nat[0], "bane": nat[1]}
    except IndexError:
        pass

    return alias, nat

def check_merge(alias, input):
    try:
        if alias == "":
            alias = input.split("+")[0]

        m = int(input.split("+")[1][:2])

        if m > 11 or m < 0:
           m = 0
    except ValueError:
        pass

    return alias, m

########################
# Meme Functions
########################

def get_meme():
    """
    Get a meme

    @return: if successful, ret is True and meme contains a random meme
             if false, ret is False and meme is an empty string
    """
    ret = False
    meme = ""
    try:
        data = {}
        with open(MEME_FILE, 'r') as file:
            data = json.load(file)

        # Check that we actually have memes to get
        if len(data[MEMES]) > 0:
            meme_index = random.randint(0, len(data[MEMES])-1)
            meme = data[MEMES][meme_index]
            ret = True

    except FileNotFoundError as e:
        # File not found, create the default file and log the issue
        logger.log(logging.WARNING, e)
        create_meme_file()

    return ret, meme

def validate_meme_permissions(requesting_user):
    """
    Validate the permissions of a user for certain meme commands

    @param requesting_user: user object requesting to do a meme requiring
                            certain permissions
    @return: True if user authorized, False otherwise
    """
    ret = False
    user_id = requesting_user.id
    data = {}

    try:
        with open(MEME_FILE, 'r') as f:
            data = json.load(f)

        # Check if the user is a special pre-approved user
        if user_id in data[MEME_IDS]:
            ret = True
        else:
            # Check if the user has a role assigned for meme commands
            for role in data[MEME_ROLES]:
                if role in [r.name for r in requesting_user.roles]:
                    ret = True
    except FileNotFoundError as e:
        logger.log(logging.WARNING, e)

    return ret

def add_meme(meme_url):
    """
    Add a meme to the memes.json file

    @param meme_url: meme to add to the json file
    @return: True if meme is added to the json file, false otherwise.
    """
    ret = False
    try:
        data = {}
        with open(MEME_FILE, 'r') as file:
            data = json.load(file)

        # Check that the meme doesn't already exist in the file
        if meme_url not in data[MEMES]:
            data[MEMES].append(meme_url)

            with open(MEME_FILE, 'w') as file:
                json.dump(data, file)

            ret = True

    except FileNotFoundError as e:
        # File doesn't exist, create the file and add the meme
        logger.log(logging.WARNING, e)
        create_meme_file()

        with open(MEME_FILE, 'w') as file:
            json.dump(data, file)

        ret = True

    except KeyError as e:
        # File exists, but doesn't contain the memes key we expected
        # Log the error and do nothing
        logger.log(logging.WARNING, e)

    return ret

def remove_meme(meme_url):
    """
    remove a meme from the memes.json file

    @param meme_url: meme to remove from the json file
    @return: True if meme existed and is removed, false otherwise
    """
    ret = False
    try:
        data = {}
        with open(MEME_FILE, 'r') as file:
            data = json.load(file)

        # Check that the meme is in the file
        if meme_url in data[MEMES]:
            data[MEMES].remove(meme_url)

            with open(MEME_FILE, 'w') as file:
                json.dump(data, file)

            ret = True

    except FileNotFoundError as e:
        # File doesn't exist, create the file and log the error
        logger.log(logging.WARNING, e)
        create_meme_file()

    except KeyError as e:
        # File exists, but doesn't contain the memes key we expected
        # Log the error and do nothing
        logger.log(logging.WARNING, e)

    return ret

def create_meme_file():
    """
    Get the meme file data

    @return: if successful, ret is True and data contains file data as a dict
             if false, ret is False and data is an empty dict
    """
    ret = True
    try:
        #Check if memes.json already exists
        if MEME_FILE in os.listdir():
            raise FileExistsError
        else:
            #File doesn't exist, we need to create the default file
            #Prepare default file data
            data = {}
            data[MEME_IDS] = [id for id in APPROVED_MEME_IDS]
            data[MEME_ROLES] = [role for role in APPROVED_MEME_ROLES]
            data[MEMES] = []

            #Create the default file
            with open(MEME_FILE, 'w') as file:
                json.dump(data, file)

    except FileExistsError as e:
        logger.log(logging.INFO, e)
        ret = False

    return ret

client.run('') 
