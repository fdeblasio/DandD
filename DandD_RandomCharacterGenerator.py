from random import randint

#sets stats to numbers so accessing the array of stats is easier
STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

#Rolls a die with or without a modifier
def dieRoll(*args):
    numRolls = args[0]
    sidedDie = args[1]
    sum = 0
    for i in range(numRolls):
        sum += randint(1, sidedDie)
    if len(args) >= 3:
        modifier = args[2]
        sum += modifier
    return sum

#Returns a stat's corresponding abilityScore
def abilityScore(stat):
    return (stat-10)/2

def randChar():
    #arrays of all possible values
    races = ["Dwarf", "Elf", "Halfling", "Human", "Dragonborn", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
    backgrounds = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"]
    align1 = ["Lawful", "Neutral", "Chaotic"]
    align2 = ["Good", "Neutral", "Evil"]
    allLang = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc", "Abyssal", "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan", "Undercommon"]

    #gets a random value from a list
    def randList(list):
        return list[randint(0, len(list) - 1)]

    race = randList(races)
    classe = randList(classes)
    background = randList(backgrounds)
    alignment = randList(align1) + " " + randList(align2)
    if alignment == "Neutral Neutral":
        alignment = "True Neutral"
    level = randint(1, 20)
    #proficiency bonus = (1-4: +2, 5-8: +3, 9-12: +4, 13-16: +5, 17-20: +6)
    profic = (level-1)/4 + 2
    spellMod = "N/A"
    gold = 0
    features = []
    languages = ["Common"]
    inventory = []

    #Rolls for each stat in order (although in real life, after the six numbers are rolled, the player can assign them to whatever stats they want)
    statistics = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    stats = []
    def abilMod(stat):
        return abilityScore(stats[stat])
    for i in range(6):
        rolls = []
        for j in range(4):
            rolls.append(dieRoll(1, 6))
        stats.append(max(rolls[0], rolls[1]) + max(rolls[2], rolls[3]) + max(min(rolls[0], rolls[1]), min(rolls[2], rolls[3])))

    #sets saving throws and skill bonuses
    skillNames = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
    savingThrows = {}
    skills = {}
    class skill:
        def __init__(self, stat, prof):
            self.stat = stat
            self.prof = prof
    for stat in range(len(statistics)):
        savingThrows[statistics[stat]] = skill(stat, False)
    for skil in skillNames:
        if skil == "Athletics":
            stat = STR
        elif skil == "Acrobatics" or skil == "Sleight of Hand" or skil == "Stealth":
            stat = DEX
        elif skil == "Arcana" or skil == "History" or skil == "Investigation" or skil == "Nature" or skil == "Religion":
            stat = INT
        elif skil == "Animal Handling" or skil == "Insight" or skil == "Medicine" or skil == "Perception" or skil == "Survival":
            stat = WIS
        elif skil == "Deception" or skil == "Intimidation" or skil == "Performance" or skil == "Persuasion":
            stat = CHA
        skills[skil] = skill(stat, False)

    def newLang():
        newLangs = allLang[:]
        for lang in languages:
            if lang != "Thieves' Cant" and lang != "Druidic":
                newLangs.remove(lang)
        languages.append(randList(newLangs))

    def newSkill(skillz):
        list = skillz
        for skil in skillz:
            if skills[skil].prof == True:
                list.remove(skil)
        newSkil = randList(list)
        skills[newSkil].prof = True

    #Adds racial bonuses and features and sets speed
    subrace = ""
    if race == "Dwarf":
        stats[CON] += 2
        speed = 25
        features.append("Darkvision")
        languages.append("Dwarvish")
        features.append("Dwarven Resiliance: Advantage on saving throws against poison")
        features.append("Dwarven Resiliance: Resistance to poison damage")
        #Stonecunning
        subraces = ["Hill", "Mountain"]
        subrace = randList(subraces)
        if subrace == "Hill":
            stats[WIS] += 1
        elif subrace == "Mountain":
            stats[STR] += 2
    elif race == "Elf":
        stats[DEX] += 2
        speed = 30
        features.append("Darkvision")
        languages.append("Elvish")
        features.append("Fey Ancestry: Advantage on saving throws against being charmed")
        features.append("Fey Ancestry: Magic can't put you to sleep")
        #Trance
        skills["Perception"].prof = True
        subraces = ["High", "Wood", "Dark (Drow)"]
        subrace = randList(subraces)
        if subrace == "High":
            stats[INT] += 1
            newLang()
            #Wizard Cantrip
        elif subrace == "Wood":
            stats[WIS] += 1
            speed += 5
            features.append("Mask of the Wild: You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena")
        elif subrace == "Dark (Drow)":
            stats[CHA] += 1
            #Superior Darkvision
            #Drow magic
            #Sunlight sensitivity
    elif race == "Halfling":
        stats[DEX] += 2
        speed = 25
        languages.append("Halfling")
        features.append("Lucky: If a 1 is rolled on a d20, you can reroll and use the new roll")
        features.append("Brave: Advantage on saving throws against being frighted")
        features.append("Halfling Nimbleness: You can move through the space of any creature that is larger than you")
        subraces = ["Lightfoot", "Stout"]
        subrace = randList(subraces)
        if subrace == "Lightfoot":
            stats[CHA] += 1
            features.append("Naturally Stealthy: You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.")
        elif subrace == "Stout":
            stats[CON] += 1
            features.append("Stout Resiliance: Advantage on saving throws against poison")
            features.append("Stout Resiliance: Resistance against poison damage")
    elif race == "Human":
        for stat in stats:
            stat += 1
        speed = 30
        newLang()
    elif race == "Dragonborn":
        stats[STR] += 2
        stats[CHA] += 1
        speed = 30
        languages.append("Draconic")
        #Draconic Ancestry
        #Breath weapon
        #Damage Resistance
    elif race == "Gnome":
        stats[INT] += 2
        speed = 25
        features.append("Darkvision")
        languages.append("Gnomish")
        features.append("Gnome Cunning: Advantage on all Intelligence, Wisdom, and Charisma saving throws against magic")
        subraces = ["Forest", "Rock"]
        subrace = randList(subraces)
        if subrace == "Forest":
            stats[DEX] += 1
            #Natural Illusionist
            #Speak with small beasts
        elif subrace == "Rock":
            stats[CON] += 1
            #Artificer's lore
            #Tinker
    elif race == "Half-Elf":
        stats[CHA] += 2
        speed = 30
        features.append("Darkvision")
        languages.append("Elvish")
        newLang()
        features.append("Fey Ancestry: Advantage on saving throws against being charmed")
        features.append("Fey Ancestry: Magic can't put you to sleep")
        #proficiency in two skills
    elif race == "Half-Orc":
        stats[STR] += 2
        stats[CON] += 1
        speed = 30
        features.append("Darkvision")
        languages.append("Orc")
        skills["Intimidation"].prof = True
        features.append("Relentless Endurance: When you are dropped to 0 HP, but not killed, you can drop to 1 HP instead. Once per long rest")
        features.append("Savage Attacks: When you score a critical hit with a melee weapon attack, you can roll one of the weapon's damage dice one addition time and add it to the extra damage of the critical hit")
    elif race == "Tiefling":
        stats[CHA] += 2
        stats[INT] += 1
        speed = 30
        features.append("Darkvision")
        languages.append("Infernal")
        features.append("Hellish Resistance: Resistance to fire damage")
        #Infernal Legacy

    #Background features
    if background == "Acolyte":
        skills["Insight"].prof = True
        skills["Religion"].prof = True
        gold = 15
        newLang()
        newLang()
        inventory.extend(["holy symbol", "prayer book", "5 sticks of incense", "vestments", "a set of common clothes"])
        #Shelter of the faithful
    elif background == "Charlatan":
        skills["Deception"].prof = True
        skills["Sleight of Hand"].prof = True
        gold = 15
        inventory.extend(["set of fine clothes", "disguise kit", randList(["ten stopperd bottles fill with colored liquids", "set of weighted dice", "deck of marked cards", "signet ring of an imaginary duke"])])
        #False identity
    elif background == "Criminal":
        skills["Deception"].prof = True
        skills["Stealth"].prof = True
        gold = 15
        inventory.extend(["crowbar", "set of dark common clothes"])
        #criminal contact
    elif background == "Entertainer":
        skills["Acrobatics"].prof = True
        skills["Performance"].prof = True
        gold = 15
        inventory.extend(["favor of an admirer", "costume"])
        #musical instrument
        #by popular demand
    elif background == "Folk Hero":
        skills["Animal Handling"].prof = True
        skills["Survival"].prof = True
        gold = 10
        inventory.extend(["artisan's tools", "shovel", "iron pot", "set of common clothes"])
        #rustic hospitality
    elif background == "Guild Artisan":
        skills["Insight"].prof = True
        skills["Persuasion"].prof = True
        gold = 15
        newLang()
        inventory.extend(["artisan's tools", "letter of introduction from guild", "set of traveler's clothes"])
        #guild membership
    elif background == "Hermit":
        skills["Medicine"].prof = True
        skills["Religion"].prof = True
        gold = 5
        newLang()
        inventory.extend(["scroll case stuffed full of notes", "winter blanket", "set of common clothes", "herbalism kit"])
        #discovery
    elif background == "Noble":
        skills["History"].prof = True
        skills["Persuasion"].prof = True
        gold = 25
        newLang()
        inventory.extend(["set of fine clothes", "signet ring", "scroll of pedigree"])
        #position of privilege
    elif background == "Outlander":
        skills["Athletics"].prof = True
        skills["Survival"].prof = True
        gold = 10
        newLang()
        inventory.extend(["staff", "hunting trap", "trophy from animal", "set of traveler's clothes"])
        #wanderer
    elif background == "Sage":
        skills["Arcana"].prof = True
        skills["History"].prof = True
        gold = 10
        newLang()
        newLang()
        inventory.extend(["bottle of black ink", "quill", "small knife", "letter from a dead colleague posing a question you have not yet been able to answer", "set of common clothes"])
        #researcher
    elif background == "Sailor":
        skills["Athletics"].prof = True
        skills["Perception"].prof = True
        gold = 10
        inventory.extend(["belaying pin", "50 feet of silk rope", "a lucky charm", "a set of common clothes"])
        #Ship's passage
    elif background == "Soldier":
        skills["Athletics"].prof = True
        skills["Intimidation"].prof = True
        gold = 10
        inventory.extend(["insignia of rank", "trophy taken from fallen enemy", randList(["bone dice", "deck of cards"]), "common clothes"])
        #military rank
    elif background == "Urchin":
        skills["Sleight of Hand"].prof = True
        skills["Stealth"].prof = True
        gold = 10
        inventory.extend(["small knife", "map of home city", "pet mouse", "token to remember parents by", "set of common clothes"])
        #city secrets

    def abilImprove():
        for i in range(2):
            impr = []
            for j in range(len(stats)):
                if stats[j] < 20:
                    impr.append(j)
            if len(impr) > 0:
                stat = randList(impr)
                stats[stat] += 1

    #Class Features
    #Implement subclass features and skill proficiencies and spells
    subclass = ""
    if classe == "Barbarian":
        for i in range(2):
            newSkill(["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"])
        hitdie = 12
        savingThrows["Strength"].prof = True
        savingThrows["Constitution"].prof = True
        #Rage
        if level >= 2:
            #Reckless attack
            #Danger sense
            if level >= 3:
                subclasses = ["Berserker", "Totem"]
                subclass = randList(subclasses)
                if subclass == "Berserker":
                    ""
                    #frenzy
                elif subclass == "Totem":
                    ""
                    #spirit seeker
                    #totem spirit
                if level >= 4:
                    abilImprove()
                    if level >= 5:
                        feat.append("Extra Attack")
                        speed += 10
                        if level >= 6:
                            if subclass == "Berserker":
                                ""
                                #mindless rage
                            elif subclass == "Totem":
                                ""
                                #aspect of the beast
                            if level >= 7:
                                #feral instinct
                                if level >= 8:
                                    abilImprove()
                                    if level >= 9:
                                        #brutal critical
                                        if level >= 10:
                                            if subclass == "Berserker":
                                                ""
                                                #intimidating prescense
                                            elif subclass == "Totem":
                                                ""
                                                #spirit walker
                                            if level >= 11:
                                                #relentless rage
                                                if level >= 12:
                                                    abilImprove()
                                                    if level >= 13:
                                                        #brutal critical
                                                        if level >= 14:
                                                            if subclass == "Berserker":
                                                                ""
                                                                #retaliation
                                                            elif subclass == "Totem":
                                                                ""
                                                                #totemic attunement
                                                            if level >= 15:
                                                                #persistent rage
                                                                if level >= 16:
                                                                    abilImprove()
                                                                    if level >= 17:
                                                                        #brutal critical
                                                                        if level >= 18:
                                                                            #indomitable might
                                                                            if level >= 19:
                                                                                abilImprove()
                                                                                if level >= 20:
                                                                                    stats[STR] += 4
                                                                                    stats[CON] += 4
    elif classe == "Bard":
        for i in range(3):
            newSkill(skillNames)
        hitdie = 8
        savingThrows["Dexterity"].prof = True
        savingThrows["Charisma"].prof = True
        spellMod = profic + abilMod(CHA)
        #bardic inspiration
        #Jack of All Trades is added down when skills are being calculated
        #song of rest 1d6 (figure out equation)
        if level >= 3:
            subclasses = ["Lore", "Valor"]
            subclass = randList(subclasses)
            if subclass == "Lore":
                ""
                for i in range(3):
                    newSkill(skillNames)
                #cutting words
            elif subclass == "Valor":
                ""
                #combat inspiration
            #expertise
            if level >= 4:
                abilImprove()
                if level >= 5:
                    #font of inspiration
                    if level >= 6:
                        #countercharm
                        if subclass == "Lore":
                            ""
                            #magical secrets
                        elif subclass == "Valor":
                            ""
                            #extra attack
                    if level >= 8:
                        abilImprove()
                        if level >= 9:
                            #song of rest 1d8
                            if level >= 10:
                                #expertise
                                #magical secrets
                                if level >= 12:
                                    abilImprove()
                                    if level >= 13:
                                        #song of rest 1d10
                                        if level >= 14:
                                            if subclass == "Lore":
                                                ""
                                                #peerless skill
                                            elif subclass == "Valor":
                                                ""
                                                #battle magic
                                            #magical secrets
                                            if level >= 15:
                                                #
                                                if level >= 16:
                                                    abilImprove()
                                                    if level >= 17:
                                                        #song of rest 1d12
                                                        if level >= 18:
                                                            #magical secrets
                                                            if level >= 19:
                                                                abilImprove()
                                                                if level >= 20:
                                                                    #superior inspiration
    elif classe == "Cleric":
        for i in range(2):
            newSkill(["History", "Insight", "Medicine", "Persuasion", "Religion"])
        hitdie = 8
        savingThrows["Wisdom"].prof = True
        savingThrows["Charisma"].prof = True
        spellMod = profic + abilMod(WIS)
    elif classe == "Druid":
        for i in range(2):
            newSkill(["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"])
        hitdie = 8
        savingThrows["Intelligence"].prof = True
        savingThrows["Wisdom"].prof = True
        spellMod = profic + abilMod(WIS)
        languages.append("Druidic")
    elif classe == "Fighter":
        for i in range(2):
            newSkill(["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"])
        hitdie = 10
        savingThrows["Strength"].prof = True
        savingThrows["Constitution"].prof = True
        #improve Fighting Style
        fightStyles = ["Archery", "Defense", "Dueling", "Great Weapon Fighting", "Protection", "Two-Weapon Fighting"]
        fistyle = {}
        fistyle["Archery"] = "You gain a +2 bonus to attack rolls you make with ranged weapons."
        fistyle["Defense"] = "While you are wearing armor, you gain a +1 bonus to AC."
        fistyle["Dueling"] = "When you are wielding a melee w eapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon."
        fistyle["Great Weapon Fighting"] = "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed or versatile property for you to gain this benefit."
        fistyle["Protection"] = "When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield."
        fistyle["Two-Weapon Fighting"] = "When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack."
        fightStyle = randList(fightStyles)
        fstl = "Fighting Style: " + fightStyle + ": " + fistyle[fightStyle]
        features.append(fstl)
        fightStyles.remove(fightStyle)
        secwind = "Second Wind: On your turn, you can use a bonus action to regain hit points equal to 1d10 + " + str(level) + ". Once you use this feature, you must finish a rest before you can use it again."
        features.append(secwind)
        if level >= 2:
            features.append("Action Surge: On your turn, you can take one additional action on top of your regular action and a possible bonus action. Once you use this feature, you must finish a rest before you can use it again.")
            if level >= 3:
                subclasses = ["Champion", "Battle Master", "Eldritch Knight"]
                subclass = randList(subclasses)
                if subclass == "Champion":
                    features.append("Improved Critical: Beginning when you choose this archetype at 3rd level, your weapon attacks score a critical hit on a roll of 19 or 20.")
                elif subclass == "Battle Master":
                    ""
                elif subclass == "Eldritch Knight":
                    spellMod = profic + abilMod(WIS)
                    ""
                if level >= 4:
                    abilImprove()
                    if level >= 5:
                        features.append("Extra Attack")
                        if level >= 6:
                            abilImprove()
                            if level >= 7:
                                if subclass == "Champion":
                                    #proficiency bonus added down with throws
                                    features.append("Remarkable Athlete: When you make a running long jump, the distance you can cover increases by " + str(abilMod(STR)) + " (STR mod) feet")
                                elif subclass == "Battle Master":
                                    ""
                                elif subclass == "Eldritch Knight":
                                    ""
                                if level >= 8:
                                    abilImprove()
                                    if level >= 9:
                                        features.append("Indomitable: You can reroll a saving throw that you fail. If you do so, you must use the new roll, and you can't use this feature again until you finish a long rest.")
                                        if level >= 10:
                                            if subclass == "Champion":
                                                fightStyle = randList(fightStyles)
                                                fstl = "Fighting Style: " + fightStyle + ": " + fistyle[fightStyle]
                                                features.append(fstl)
                                                fightStyles.remove(fightStyle)
                                            elif subclass == "Battle Master":
                                                ""
                                            elif subclass == "Eldritch Knight":
                                                ""
                                            if level >= 11:
                                                features.remove("Extra Attack")
                                                features.append("Extra Attack x 2")
                                                if level >= 12:
                                                    abilImprove()
                                                    if level >= 13:
                                                        features.append("Indomitable x 2")
                                                        if level >= 14:
                                                            abilImprove()
                                                            if level >= 15:
                                                                if subclass == "Champion":
                                                                    features.append("Superior Critical: Your weapon attacks score a critical hit on a roll of 18-20.")
                                                                elif subclass == "Battle Master":
                                                                    ""
                                                                elif subclass == "Eldritch Knight":
                                                                    ""
                                                                if level >= 16:
                                                                    abilImprove()
                                                                    if level >= 17:
                                                                        features.append("You can use Action Surge twice before a rest, but only once on the same turn.")
                                                                        features.append("Indomitable x 3")
                                                                        if level >= 18:
                                                                            if subclass == "Champion":
                                                                                features.append("Survivor: At the start of each of your turns, you regain hit points equal to 5 + " + str(abilMod(CON)) + " (CON mod) if you have less than or equal to half of your hit points left. You don't gain this benefit if you have 0 hit points.")
                                                                                #if curHP <= maxHP/2 and cur > 0:
                                                                                    #curHP += 5 + abilMod(CON)
                                                                            elif subclass == "Battle Master":
                                                                                ""
                                                                            elif subclass == "Eldritch Knight":
                                                                                ""
                                                                            if level >= 19:
                                                                                abilImprove()
                                                                                if level >= 20:
                                                                                    features.remove("Extra Attack x 2")
                                                                                    features.append("Extra Attack x 3")
    elif classe == "Monk":
        for i in range(2):
            newSkill(["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"])
        hitdie = 8
        savingThrows["Strength"].prof = True
        savingThrows["Dexterity"].prof = True
        if level >= 2:
            #speed += (2-5: +10, 6-9: +15, 10-13: +20, 14-17: +25, 18-20: +30)
            speed += (level-2)/4 * 5 + 10
            if level >= 3:
                subclasses = ["Open Hand", "Shadow", "Four Elements"]
                subclass = randList(subclasses)
                if subclass == "Open Hand":
                    ""
                elif subclass == "Shadow":
                    ""
                elif subclass == "Four Elements":
                    ""
                if level >= 13:
                    for lang in allLang:
                        if lang not in languages:
                            languages.append(lang)
    elif classe == "Paladin":
        for i in range(2):
            newSkill(["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"])
        hitdie = 10
        savingThrows["Wisdom"].prof = True
        savingThrows["Charisma"].prof = True
        if level >= 2:
            spellMod = profic + abilMod(CHA)
            if level >= 3:
                subclasses = ["Devotion", "Ancients", "Vengeance"]
                subclass = randList(subclasses)
                if subclass == "Devotion":
                    ""
                elif subclass == "Ancients":
                    ""
                elif subclass == "Vengeance":
                    ""
    elif classe == "Ranger":
        for i in range(3):
            newSkill(["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"])
        hitdie = 10
        savingThrows["Strength"].prof = True
        savingThrows["Dexterity"].prof = True
        if level >= 2:
            spellMod = profic + abilMod(WIS)
            if level >= 3:
                subclasses = ["Hunter", "Beast Master"]
                subclass = randList(subclasses)
                if subclass == "Hunter":
                    ""
                elif subclass == "Beast Master":
                    ""
    elif classe == "Rogue":
        for i in range(4):
            newSkill(["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"])
        hitdie = 8
        savingThrows["Dexterity"].prof = True
        savingThrows["Intelligence"].prof = True
        languages.append("Thieves' Cant")
        if level >= 3:
            subclasses = ["Thief", "Assassin", "Arcane Trickster"]
            subclass = randList(subclasses)
            if subclass == "Thief":
                ""
            elif subclass == "Assassin":
                ""
            elif subclass == "Arcane Trickster":
                ""
            if level >= 15:
                savingThrows["Wisdom"].prof = True
    elif classe == "Sorcerer":
        for i in range(2):
            newSkill(["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"])
        hitdie = 6
        savingThrows["Constitution"].prof = True
        savingThrows["Charisma"].prof = True
        #spells
        spellMod = profic + abilMod(CHA)
        subclasses = ["Draconic Bloodline", "Wild Magic"]
        subclass = randList(subclasses)
        if subclass == "Draconic Bloodline":
            ""
            #draconic ancestor
            if "Draconic" not in languages:
                languages.append("Draconic")
        elif subclass == "Wild Magic":
            ""
            #wild magic surge
            #tides of chaos
        if level >= 2:
            #font of magic
            if level >= 3:
                #metamagic
                if level >= 4:
                    abilImprove()
                    if level >= 6:
                        if subclass == "Draconic Bloodline":
                            ""
                            #elemental affinity
                        elif subclass == "Wild Magic":
                            ""
                            #bend luck
                        if level >= 8:
                            abilImprove()
                            if level >= 10:
                                #metamagic
                                if level >= 12:
                                    abilImprove()
                                    if level >= 14:
                                        if subclass == "Draconic Bloodline":
                                            ""
                                            #dragon wings
                                        elif subclass == "Wild Magic":
                                            ""
                                            #controlled chaos
                                        if level >= 16:
                                            abilImprove()
                                            if level >= 17:
                                                #metamagic
                                                if level >= 18:
                                                    if subclass == "Draconic Bloodline":
                                                        ""
                                                        #draconic prescense
                                                    elif subclass == "Wild Magic":
                                                        ""
                                                        #spell bombardment
                                                    if level >= 19:
                                                        abilImprove()
                                                        if level >= 20:
                                                            #sorcerous restoration
    elif classe == "Warlock":
        for i in range(2):
            newSkill(["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"])
        hitdie = 8
        savingThrows["Wisdom"].prof = True
        savingThrows["Charisma"].prof = True
        spellMod = profic + abilMod(CHA)
    elif classe == "Wizard":
        for i in range(2):
            newSkill(["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"])
        hitdie = 6
        savingThrows["Intelligence"].prof = True
        savingThrows["Wisdom"].prof = True
        spellMod = profic + abilMod(INT)

    maxHP = hitdie + abilMod(CON)*level + dieRoll(level - 1, hitdie)
    if (race == "Dwarf" and subrace == "Hill") or (classe == "Sorcerer" and subclass == "Draconic Bloodline"):
        maxHP += level
    curHP = maxHP

    #calculates other stats based on ability modifiers
    if classe == "Barbarian":
        AC = 10 + abilMod(DEX) + abilMod(CON)
    elif classe == "Monk":
        AC = 10 + abilMod(DEX) + abilMod(WIS)
    elif classe == "Sorcerer" and subclass == "Draconic Bloodline":
        AC = 13 + abilMod(DEX)
    else:
        #not the actual AC equation since there are multiple variables such as armor, but the actual AC values should be at least the AC values this outputs
        AC = 11 + abilMod(DEX)
    init = abilMod(DEX)
    passivePerception = 10 + abilMod(WIS)

    #prints out the character
    char = [background]
    if subrace != "":
        char.append(subrace)
    char.append(race)
    if subclass != "":
        char.append(subclass)
    char.append(classe)
    s = ""
    for att in char:
        s += att + " "
    print s[:-1]
    print "Level:", level
    print "Alignment:", alignment
    print "Proficiency Bonus: +" + str(profic)
    print
    for i in range (6):
        print str(statistics[i]) + ": \t", stats[i], "(" + str(abilMod(i)) + ")"
    print
    print "HP: \t\t", str(curHP) + "/" + str(maxHP)
    print "Armor Class: \t", AC
    print "Initiative: \t", init
    movement = speed/5
    print "Speed: \t\t", speed, "(" + str(movement) + ")"
    print "Hit Die: \t", hitdie
    print "Passive Perception:", passivePerception
    print
    print "Saving Throws:"
    for throw in statistics:
        save = savingThrows[throw]
        num = abilMod(save.stat)
        if save.prof == True:
            num += profic
            print throw + ": \t", num, "\tP"
        else:
            if classe == "Bard" and level >= 2:
                num += profic/2
            elif classe == "Fighter" and subclass == "Champion" and level >= 7:
                if throw in ["Strength", "Dexterity", "Constitution"]:
                    num += (profic + 1)/2
            print throw + ": \t", num
    print
    print "Skills:"
    for skil in skillNames:
        roll = skills[skil]
        num = abilMod(roll.stat)
        tabs = 1
        if skil == "Arcana" or skil == "Nature":
            tabs = 2
        if skil == "Animal Handling" or skil == "Sleight of Hand":
            tabs = 0
        if roll.prof == True:
            num += profic
            print skil, "\t"*tabs + "(" + statistics[roll.stat][:3].upper() + ")" + ": \t", num, "\tP"
        else:
            if classe == "Bard" and level >= 2:
                num += profic/2
            print skil, "\t"*tabs + "(" + statistics[roll.stat][:3].upper() + ")" + ": \t", num
    print
    print "Features:"
    for feat in features:
        print " ", feat
    print
    print "Languages:"
    for lang in languages:
        print " ", lang
    print
    if spellMod != "N/A":
        print "Spell save DC:", 8 + spellMod
        print "Spell attack modifier:", spellMod
        print
    print "Gold:", gold
    print
    print "Inventory:"
    for inv in inventory:
        print " ", inv
    print

if __name__== "__main__":
    randChar()
