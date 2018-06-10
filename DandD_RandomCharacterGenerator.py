from random import randint

#sets stats to numbers so accessing the array of stats is easier
STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

#lists of all possible values
races = ["Dwarf", "Elf", "Halfling", "Human", "Dragonborn", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
backgrounds = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"]
align1 = ["Lawful", "Neutral", "Chaotic"]
align2 = ["Good", "Neutral", "Evil"]
allLang = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc", "Abyssal", "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan", "Undercommon"]
statistics = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
skillNames = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]

#gets a random value from a list
def randList(list):
    return list[randint(0, len(list) - 1)]

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

class Char:
    def __init__(self, race, classe, background, level):
        self.race = race
        self.classe = classe
        self.background = background
        self.level = level
        self.alignment = randList(align1) + " " + randList(align2)
        if self.alignment == "Neutral Neutral":
            self.alignment = "True Neutral"
        #proficiency bonus = (1-4: +2, 5-8: +3, 9-12: +4, 13-16: +5, 17-20: +6)
        self.profic = (level-1)/4 + 2
        self.spellMod = "N/A"
        self.gold = 0
        self.features = []
        self.languages = ["Common"]
        self.inventory = []

        #Rolls for each stat in order (although in real life, after the six numbers are rolled, the player can assign them to whatever stats they want)
        self.stats = []
        for i in range(6):
            rolls = []
            for j in range(4):
                rolls.append(dieRoll(1, 6))
            self.stats.append(max(rolls[0], rolls[1]) + max(rolls[2], rolls[3]) + max(min(rolls[0], rolls[1]), min(rolls[2], rolls[3])))

        def abilMod(stat):
            return abilityScore(self.stats[stat])

        #sets saving throws and skill bonuses
        self.savingThrows = {}
        self.skills = {}
        class skill:
            def __init__(self, stat, prof):
                self.stat = stat
                self.prof = prof
        for stat in range(len(statistics)):
            self.savingThrows[statistics[stat]] = skill(stat, False)
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
            self.skills[skil] = skill(stat, False)

        def newLang():
            newLangs = allLang[:]
            for lang in self.languages:
                if lang != "Thieves' Cant" and lang != "Druidic":
                    newLangs.remove(lang)
            self.languages.append(randList(newLangs))

        def newSkill(skillz):
            list = skillz[:]
            for skil in skillz:
                if self.skills[skil].prof == True:
                    list.remove(skil)
            newSkil = randList(list)
            self.skills[newSkil].prof = True

        #Adds racial bonuses and features and sets speed
        self.subrace = ""
        if self.race == "Dwarf":
            self.stats[CON] += 2
            self.speed = 25
            self.features.append("Darkvision")
            self.languages.append("Dwarvish")
            self.features.append("Dwarven Resiliance: Advantage on saving throws against poison")
            self.features.append("Dwarven Resiliance: Resistance to poison damage")
            #Stonecunning
            self.subraces = ["Hill", "Mountain"]
            self.subrace = randList(self.subraces)
            if self.subrace == "Hill":
                self.stats[WIS] += 1
            elif self.subrace == "Mountain":
                self.stats[STR] += 2
        elif self.race == "Elf":
            self.stats[DEX] += 2
            self.speed = 30
            self.features.append("Darkvision")
            self.languages.append("Elvish")
            self.features.append("Fey Ancestry: Advantage on saving throws against being charmed")
            self.features.append("Fey Ancestry: Magic can't put you to sleep")
            #Trance
            self.skills["Perception"].prof = True
            self.subraces = ["High", "Wood", "Dark (Drow)"]
            self.subrace = randList(self.subraces)
            if self.subrace == "High":
                self.stats[INT] += 1
                newLang()
                #Wizard Cantrip
            elif self.subrace == "Wood":
                self.stats[WIS] += 1
                self.speed += 5
                self.features.append("Mask of the Wild: You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena")
            elif self.subrace == "Dark (Drow)":
                self.stats[CHA] += 1
                #Superior Darkvision
                #Drow magic
                #Sunlight sensitivity
        elif race == "Halfling":
            self.stats[DEX] += 2
            self.speed = 25
            self.languages.append("Halfling")
            self.features.append("Lucky: If a 1 is rolled on a d20, you can reroll and use the new roll")
            self.features.append("Brave: Advantage on saving throws against being frighted")
            self.features.append("Halfling Nimbleness: You can move through the space of any creature that is larger than you")
            self.subraces = ["Lightfoot", "Stout"]
            self.subrace = randList(self.subraces)
            if self.subrace == "Lightfoot":
                self.stats[CHA] += 1
                self.features.append("Naturally Stealthy: You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.")
            elif self.subrace == "Stout":
                self.stats[CON] += 1
                self.features.append("Stout Resiliance: Advantage on saving throws against poison")
                self.features.append("Stout Resiliance: Resistance against poison damage")
        elif self.race == "Human":
            for stat in self.stats:
                stat += 1
            self.speed = 30
            newLang()
        elif self.race == "Dragonborn":
            self.stats[STR] += 2
            self.stats[CHA] += 1
            self.speed = 30
            self.languages.append("Draconic")
            #Draconic Ancestry
            #Breath weapon
            #Damage Resistance
        elif self.race == "Gnome":
            self.stats[INT] += 2
            self.speed = 25
            self.features.append("Darkvision")
            self.languages.append("Gnomish")
            self.features.append("Gnome Cunning: Advantage on all Intelligence, Wisdom, and Charisma saving throws against magic")
            self.subraces = ["Forest", "Rock"]
            self.subrace = randList(self.subraces)
            if self.subrace == "Forest":
                self.stats[DEX] += 1
                #Natural Illusionist
                #Speak with small beasts
            elif self.subrace == "Rock":
                self.stats[CON] += 1
                #Artificer's lore
                #Tinker
        elif self.race == "Half-Elf":
            self.stats[CHA] += 2
            self.speed = 30
            self.features.append("Darkvision")
            self.languages.append("Elvish")
            newLang()
            self.features.append("Fey Ancestry: Advantage on saving throws against being charmed")
            self.features.append("Fey Ancestry: Magic can't put you to sleep")
            #proficiency in two skills
        elif self.race == "Half-Orc":
            self.stats[STR] += 2
            self.stats[CON] += 1
            self.speed = 30
            self.features.append("Darkvision")
            self.languages.append("Orc")
            self.skills["Intimidation"].prof = True
            self.features.append("Relentless Endurance: When you are dropped to 0 HP, but not killed, you can drop to 1 HP instead. Once per long rest")
            self.features.append("Savage Attacks: When you score a critical hit with a melee weapon attack, you can roll one of the weapon's damage dice one addition time and add it to the extra damage of the critical hit")
        elif self.race == "Tiefling":
            self.stats[CHA] += 2
            self.stats[INT] += 1
            self.speed = 30
            self.features.append("Darkvision")
            self.languages.append("Infernal")
            self.features.append("Hellish Resistance: Resistance to fire damage")
            #Infernal Legacy

        #Background features
        if self.background == "Acolyte":
            self.skills["Insight"].prof = True
            self.skills["Religion"].prof = True
            self.gold = 15
            newLang()
            newLang()
            self.inventory.extend(["holy symbol", "prayer book", "5 sticks of incense", "vestments", "a set of common clothes"])
            #Shelter of the faithful
        elif self.background == "Charlatan":
            self.skills["Deception"].prof = True
            self.skills["Sleight of Hand"].prof = True
            self.gold = 15
            self.inventory.extend(["set of fine clothes", "disguise kit", randList(["ten stopperd bottles fill with colored liquids", "set of weighted dice", "deck of marked cards", "signet ring of an imaginary duke"])])
            #False identity
        elif self.background == "Criminal":
            self.skills["Deception"].prof = True
            self.skills["Stealth"].prof = True
            self.gold = 15
            self.inventory.extend(["crowbar", "set of dark common clothes"])
            #criminal contact
        elif self.background == "Entertainer":
            self.skills["Acrobatics"].prof = True
            self.skills["Performance"].prof = True
            self.gold = 15
            self.inventory.extend(["favor of an admirer", "costume"])
            #musical instrument
            #by popular demand
        elif self.background == "Folk Hero":
            self.skills["Animal Handling"].prof = True
            self.skills["Survival"].prof = True
            self.gold = 10
            self.inventory.extend(["artisan's tools", "shovel", "iron pot", "set of common clothes"])
            #rustic hospitality
        elif self.background == "Guild Artisan":
            self.skills["Insight"].prof = True
            self.skills["Persuasion"].prof = True
            self.gold = 15
            newLang()
            self.inventory.extend(["artisan's tools", "letter of introduction from guild", "set of traveler's clothes"])
            #guild membership
        elif self.background == "Hermit":
            self.skills["Medicine"].prof = True
            self.skills["Religion"].prof = True
            self.gold = 5
            newLang()
            self.inventory.extend(["scroll case stuffed full of notes", "winter blanket", "set of common clothes", "herbalism kit"])
            #discovery
        elif self.background == "Noble":
            self.skills["History"].prof = True
            self.skills["Persuasion"].prof = True
            self.gold = 25
            newLang()
            self.inventory.extend(["set of fine clothes", "signet ring", "scroll of pedigree"])
            #position of privilege
        elif self.background == "Outlander":
            self.skills["Athletics"].prof = True
            self.skills["Survival"].prof = True
            self.gold = 10
            newLang()
            self.inventory.extend(["staff", "hunting trap", "trophy from animal", "set of traveler's clothes"])
            #wanderer
        elif self.background == "Sage":
            self.skills["Arcana"].prof = True
            self.skills["History"].prof = True
            self.gold = 10
            newLang()
            newLang()
            self.inventory.extend(["bottle of black ink", "quill", "small knife", "letter from a dead colleague posing a question you have not yet been able to answer", "set of common clothes"])
            #researcher
        elif self.background == "Sailor":
            self.skills["Athletics"].prof = True
            self.skills["Perception"].prof = True
            self.gold = 10
            self.inventory.extend(["belaying pin", "50 feet of silk rope", "a lucky charm", "a set of common clothes"])
            #Ship's passage
        elif self.background == "Soldier":
            self.skills["Athletics"].prof = True
            self.skills["Intimidation"].prof = True
            self.gold = 10
            self.inventory.extend(["insignia of rank", "trophy taken from fallen enemy", randList(["bone dice", "deck of cards"]), "common clothes"])
            #military rank
        elif self.background == "Urchin":
            self.skills["Sleight of Hand"].prof = True
            self.skills["Stealth"].prof = True
            self.gold = 10
            self.inventory.extend(["small knife", "map of home city", "pet mouse", "token to remember parents by", "set of common clothes"])
            #city secrets

        def abilImprove():
            for i in range(2):
                impr = []
                for j in range(len(self.stats)):
                    if self.stats[j] < 20:
                        impr.append(j)
                if len(impr) > 0:
                    stat = randList(impr)
                    self.stats[stat] += 1

        #Class Features
        #Implement subclass features and skill proficiencies and spells
        self.subclass = ""
        if self.classe == "Barbarian":
            for i in range(2):
                newSkill(["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"])
            self.hitdie = 12
            self.savingThrows["Strength"].prof = True
            self.savingThrows["Constitution"].prof = True
            #Rage
            if self.level >= 2:
                #Reckless attack
                #Danger sense
                if self.level >= 3:
                    self.subclasses = ["Berserker", "Totem"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Berserker":
                        ""
                        #frenzy
                    elif self.subclass == "Totem":
                        ""
                        #spirit seeker
                        #totem spirit
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 5:
                            self.features.append("Extra Attack")
                            self.speed += 10
                            if self.level >= 6:
                                if self.subclass == "Berserker":
                                    ""
                                    #mindless rage
                                elif self.subclass == "Totem":
                                    ""
                                    #aspect of the beast
                                if self.level >= 7:
                                    #feral instinct
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 9:
                                            #brutal critical
                                            if self.level >= 10:
                                                if self.subclass == "Berserker":
                                                    ""
                                                    #intimidating prescense
                                                elif self.subclass == "Totem":
                                                    ""
                                                    #spirit walker
                                                if self.level >= 11:
                                                    #relentless rage
                                                    if self.level >= 12:
                                                        abilImprove()
                                                        if self.level >= 13:
                                                            #brutal critical
                                                            if self.level >= 14:
                                                                if self.subclass == "Berserker":
                                                                    ""
                                                                    #retaliation
                                                                elif self.subclass == "Totem":
                                                                    ""
                                                                    #totemic attunement
                                                                if self.level >= 15:
                                                                    #persistent rage
                                                                    if self.level >= 16:
                                                                        abilImprove()
                                                                        if self.level >= 17:
                                                                            #brutal critical
                                                                            if self.level >= 18:
                                                                                #indomitable might
                                                                                if self.level >= 19:
                                                                                    abilImprove()
                                                                                    if self.level >= 20:
                                                                                        self.stats[STR] += 4
                                                                                        self.stats[CON] += 4
        elif self.classe == "Bard":
            for i in range(3):
                newSkill(skillNames)
            self.hitdie = 8
            self.savingThrows["Dexterity"].prof = True
            self.savingThrows["Charisma"].prof = True
            self.spellMod = self.profic + abilMod(CHA)
            #bardic inspiration
            #Jack of All Trades is added down when skills are being calculated
            #song of rest 1d6 (figure out equation)
            if self.level >= 3:
                self.subclasses = ["Lore", "Valor"]
                self.subclass = randList(self.subclasses)
                if self.subclass == "Lore":
                    for i in range(3):
                        newSkill(skillNames)
                    #cutting words
                elif self.subclass == "Valor":
                    ""
                    #combat inspiration
                #expertise
                if self.level >= 4:
                    abilImprove()
                    if self.level >= 5:
                        #font of inspiration
                        if self.level >= 6:
                            #countercharm
                            if self.subclass == "Lore":
                                ""
                                #magical secrets
                            elif self.subclass == "Valor":
                                ""
                                #extra attack
                        if self.level >= 8:
                            abilImprove()
                            if self.level >= 9:
                                #song of rest 1d8
                                if self.level >= 10:
                                    #expertise
                                    #magical secrets
                                    if self.level >= 12:
                                        abilImprove()
                                        if self.level >= 13:
                                            #song of rest 1d10
                                            if self.level >= 14:
                                                if self.subclass == "Lore":
                                                    ""
                                                    #peerless skill
                                                elif self.subclass == "Valor":
                                                    ""
                                                    #battle magic
                                                #magical secrets
                                                if self.level >= 15:
                                                    #
                                                    if self.level >= 16:
                                                        abilImprove()
                                                        if self.level >= 17:
                                                            #song of rest 1d12
                                                            if self.level >= 18:
                                                                #magical secrets
                                                                if self.level >= 19:
                                                                    abilImprove()
                                                                    if self.level >= 20:
                                                                        ""
                                                                        #superior inspiration
        elif self.classe == "Cleric":
            for i in range(2):
                newSkill(["History", "Insight", "Medicine", "Persuasion", "Religion"])
            self.hitdie = 8
            self.savingThrows["Wisdom"].prof = True
            self.savingThrows["Charisma"].prof = True
            self.spellMod = self.profic + abilMod(WIS)
            if self.level >= 2:
                if self.level >= 4:
                    abilImprove()
                    if self.level >= 5:
                        if self.level >= 6:
                            if self.level >= 8:
                                abilImprove()
                                if self.level >= 10:
                                    if self.level >= 11:
                                        if self.level >= 12:
                                            abilImprove()
                                            if self.level >= 14:
                                                if self.level >= 16:
                                                    abilImprove()
                                                    if self.level >= 17:
                                                        if self.level >= 18:
                                                            if self.level >= 19:
                                                                abilImprove()
                                                                if self.level >= 20:
                                                                    ""
        elif self.classe == "Druid":
            for i in range(2):
                newSkill(["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"])
            self.hitdie = 8
            self.savingThrows["Intelligence"].prof = True
            self.savingThrows["Wisdom"].prof = True
            self.spellMod = self.profic + abilMod(WIS)
            self.languages.append("Druidic")
            if self.level >= 2:
                if self.level >= 4:
                    abilImprove()
                    if self.level >= 6:
                        if self.level >= 8:
                            abilImprove()
                            if self.level >= 10:
                                if self.level >= 12:
                                    abilImprove()
                                    if self.level >= 14:
                                        if self.level >= 16:
                                            abilImprove()
                                            if self.level >= 18:
                                                if self.level >= 19:
                                                    abilImprove()
                                                    if self.level >= 20:
                                                        ""
        elif self.classe == "Fighter":
            for i in range(2):
                newSkill(["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"])
            self.hitdie = 10
            self.savingThrows["Strength"].prof = True
            self.savingThrows["Constitution"].prof = True
            #improve Fighting Style
            self.fightStyles = ["Archery", "Defense", "Dueling", "Great Weapon Fighting", "Protection", "Two-Weapon Fighting"]
            self.fistyle = {}
            self.fistyle["Archery"] = "You gain a +2 bonus to attack rolls you make with ranged weapons."
            self.fistyle["Defense"] = "While you are wearing armor, you gain a +1 bonus to AC."
            self.fistyle["Dueling"] = "When you are wielding a melee w eapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon."
            self.fistyle["Great Weapon Fighting"] = "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed or versatile property for you to gain this benefit."
            self.fistyle["Protection"] = "When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield."
            self.fistyle["Two-Weapon Fighting"] = "When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack."
            self.fightStyle = randList(self.fightStyles)
            self.fstl = "Fighting Style: " + self.fightStyle + ": " + self.fistyle[self.fightStyle]
            self.features.append(self.fstl)
            self.fightStyles.remove(self.fightStyle)
            secwind = "Second Wind: On your turn, you can use a bonus action to regain hit points equal to 1d10 + " + str(level) + ". Once you use this feature, you must finish a rest before you can use it again."
            self.features.append(secwind)
            if self.level >= 2:
                self.features.append("Action Surge: On your turn, you can take one additional action on top of your regular action and a possible bonus action. Once you use this feature, you must finish a rest before you can use it again.")
                if self.level >= 3:
                    self.subclasses = ["Champion", "Battle Master", "Eldritch Knight"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Champion":
                        self.features.append("Improved Critical: Beginning when you choose this archetype at 3rd level, your weapon attacks score a critical hit on a roll of 19 or 20.")
                    elif self.subclass == "Battle Master":
                        ""
                        #combat superiority
                    elif self.subclass == "Eldritch Knight":
                        self.spellMod = self.profic + abilMod(WIS)
                        ""
                        #weapon bond
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 5:
                            self.features.append("Extra Attack")
                            if self.level >= 6:
                                abilImprove()
                                if self.level >= 7:
                                    if self.subclass == "Champion":
                                        #proficiency bonus added down with throws
                                        self.features.append("Remarkable Athlete: When you make a running long jump, the distance you can cover increases by " + str(abilMod(STR)) + " (STR mod) feet")
                                    elif self.subclass == "Battle Master":
                                        ""
                                        #know your enemy
                                    elif self.subclass == "Eldritch Knight":
                                        ""
                                        #war magic
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 9:
                                            self.features.append("Indomitable: You can reroll a saving throw that you fail. If you do so, you must use the new roll, and you can't use this feature again until you finish a long rest.")
                                            if self.level >= 10:
                                                if self.subclass == "Champion":
                                                    self.fightStyle = randList(self.fightStyles)
                                                    self.fstl = "Fighting Style: " + self.fightStyle + ": " + self.fistyle[self.fightStyle]
                                                    self.features.append(self.fstl)
                                                    self.fightStyles.remove(self.fightStyle)
                                                elif self.subclass == "Battle Master":
                                                    ""
                                                    #improved combat superiority
                                                elif self.subclass == "Eldritch Knight":
                                                    ""
                                                    #eldritch strike
                                                if self.level >= 11:
                                                    self.features.remove("Extra Attack")
                                                    self.features.append("Extra Attack x 2")
                                                    if self.level >= 12:
                                                        abilImprove()
                                                        if self.level >= 13:
                                                            self.features.append("Indomitable x 2")
                                                            if self.level >= 14:
                                                                abilImprove()
                                                                if self.level >= 15:
                                                                    if self.subclass == "Champion":
                                                                        self.features.append("Superior Critical: Your weapon attacks score a critical hit on a roll of 18-20.")
                                                                    elif self.subclass == "Battle Master":
                                                                        ""
                                                                        #relerelentless
                                                                    elif self.subclass == "Eldritch Knight":
                                                                        ""
                                                                        #arcane charge
                                                                    if self.level >= 16:
                                                                        abilImprove()
                                                                        if self.level >= 17:
                                                                            self.features.append("You can use Action Surge twice before a rest, but only once on the same turn.")
                                                                            self.features.append("Indomitable x 3")
                                                                            if self.level >= 18:
                                                                                if self.subclass == "Champion":
                                                                                    self.features.append("Survivor: At the start of each of your turns, you regain hit points equal to 5 + " + str(abilMod(CON)) + " (CON mod) if you have less than or equal to half of your hit points left. You don't gain this benefit if you have 0 hit points.")
                                                                                    #if curHP <= maxHP/2 and cur > 0:
                                                                                        #curHP += 5 + abilMod(CON)
                                                                                elif self.subclass == "Battle Master":
                                                                                    ""
                                                                                    #improved combat superiority
                                                                                elif self.subclass == "Eldritch Knight":
                                                                                    ""
                                                                                    #improved war magic
                                                                                if self.level >= 19:
                                                                                    abilImprove()
                                                                                    if self.level >= 20:
                                                                                        self.features.remove("Extra Attack x 2")
                                                                                        self.features.append("Extra Attack x 3")
        elif self.classe == "Monk":
            for i in range(2):
                newSkill(["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"])
            self.hitdie = 8
            self.savingThrows["Strength"].prof = True
            self.savingThrows["Dexterity"].prof = True
            #martial arts
            if self.level >= 2:
                #ki
                #speed += (2-5: +10, 6-9: +15, 10-13: +20, 14-17: +25, 18-20: +30)
                self.speed += (level-2)/4 * 5 + 10
                if self.level >= 3:
                    #deflect missiles
                    self.subclasses = ["Open Hand", "Shadow", "Four Elements"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Open Hand":
                        ""
                        #open hand technique
                    elif self.subclass == "Shadow":
                        ""
                        #shadow arts
                    elif self.subclass == "Four Elements":
                        ""
                        #disciple of the elements
                    if self.level >= 4:
                        abilImprove()
                        #slow fall
                        if self.level >= 5:
                            self.features.append("Extra Attack")
                            #stunning strike
                            if self.level >= 6:
                                #ki-empowered strikes
                                if self.subclass == "Open Hand":
                                    ""
                                    #wholeness of body
                                elif self.subclass == "Shadow":
                                    ""
                                    #shadow step
                                elif self.subclass == "Four Elements":
                                    ""
                                    #elements
                                if self.level >= 7:
                                    #evasion
                                    #stillness of mind
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 9:
                                            #unarmored movement
                                            if self.level >= 10:
                                                self.features.append("Immune to disease and poison")
                                                if self.level >= 11:
                                                    if self.subclass == "Open Hand":
                                                        ""
                                                        #tranquility
                                                    elif self.subclass == "Shadow":
                                                        ""
                                                        #cloak of shadows
                                                    elif self.subclass == "Four Elements":
                                                        ""
                                                        #elements
                                                    if self.level >= 12:
                                                        abilImprove()
                                                        if self.level >= 13:
                                                            for lang in allLang:
                                                                if lang not in self.languages:
                                                                    self.languages.append(lang)
                                                            if self.level >= 14:
                                                                for throw in statistics:
                                                                    self.savingThrows[throw].prof = True
                                                                #diamond soul
                                                                if self.level >= 15:
                                                                    #timeless body
                                                                    if self.level >= 16:
                                                                        abilImprove()
                                                                        if self.level >= 17:
                                                                            if self.subclass == "Open Hand":
                                                                                ""
                                                                                #quivering palm
                                                                            elif self.subclass == "Shadow":
                                                                                ""
                                                                                #opportunist
                                                                            elif self.subclass == "Four Elements":
                                                                                ""
                                                                                #elements
                                                                            if self.level >= 18:
                                                                                #empty body
                                                                                if self.level >= 19:
                                                                                    abilImprove()
                                                                                    if self.level >= 20:
                                                                                        #perfect self
                                                                                        ""
        elif self.classe == "Paladin":
            for i in range(2):
                newSkill(["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"])
            self.hitdie = 10
            self.savingThrows["Wisdom"].prof = True
            self.savingThrows["Charisma"].prof = True
            if self.level >= 2:
                self.spellMod = self.profic + abilMod(CHA)
                if self.level >= 3:
                    self.subclasses = ["Devotion", "Ancients", "Vengeance"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Devotion":
                        ""
                    elif self.subclass == "Ancients":
                        ""
                    elif self.subclass == "Vengeance":
                        ""
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 5:
                            if self.level >= 6:
                                if self.level >= 7:
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 10:
                                            if self.level >= 11:
                                                if self.level >= 12:
                                                    abilImprove()
                                                    if self.level >= 14:
                                                        if self.level >= 15:
                                                            if self.level >= 16:
                                                                abilImprove()
                                                                if self.level >= 18:
                                                                    if self.level >= 19:
                                                                        abilImprove()
                                                                        if self.level >= 20:
                                                                            ""
        elif self.classe == "Ranger":
            for i in range(3):
                newSkill(["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"])
            self.hitdie = 10
            self.savingThrows["Strength"].prof = True
            self.savingThrows["Dexterity"].prof = True
            if self.level >= 2:
                self.spellMod = self.profic + abilMod(WIS)
                if self.level >= 3:
                    self.subclasses = ["Hunter", "Beast Master"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Hunter":
                        ""
                    elif self.subclass == "Beast Master":
                        ""
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 5:
                            if self.level >= 6:
                                if self.level >= 7:
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 10:
                                            if self.level >= 11:
                                                if self.level >= 12:
                                                    abilImprove()
                                                    if self.level >= 14:
                                                        if self.level >= 15:
                                                            if self.level >= 16:
                                                                abilImprove()
                                                                if self.level >= 18:
                                                                    if self.level >= 19:
                                                                        abilImprove()
                                                                        if self.level >= 20:
                                                                            ""
        elif self.classe == "Rogue":
            for i in range(4):
                newSkill(["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"])
            self.hitdie = 8
            self.savingThrows["Dexterity"].prof = True
            self.savingThrows["Intelligence"].prof = True
            self.languages.append("Thieves' Cant")
            #expertise
            #sneak attack
            #equation
            if self.level >= 2:
                #cunning action
                if self.level >= 3:
                    self.subclasses = ["Thief", "Assassin", "Arcane Trickster"]
                    self.subclass = randList(self.subclasses)
                    if self.subclass == "Thief":
                        ""
                        #fast hands
                        #second-story work
                    elif self.subclass == "Assassin":
                        ""
                        #assassinate
                    elif self.subclass == "Arcane Trickster":
                        ""
                        self.spellMod = self.profic + abilMod(INT)
                        #spells
                        #mage hand
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 5:
                            #uncanny dodge
                            if self.level >= 6:
                                #expertise
                                if self.level >= 7:
                                    #evasion
                                    if self.level >= 8:
                                        abilImprove()
                                        if self.level >= 9:
                                            if self.subclass == "Thief":
                                                ""
                                                #supreme sneak
                                            elif self.subclass == "Assassin":
                                                ""
                                                #infiltration expertise
                                            elif self.subclass == "Arcane Trickster":
                                                ""
                                                #magical ambush
                                            if self.level >= 10:
                                                abilImprove()
                                                if self.level >= 11:
                                                    #reliable talent
                                                    if self.level >= 12:
                                                        abilImprove()
                                                        if self.level >= 13:
                                                            if self.subclass == "Thief":
                                                                ""
                                                                #use magic device
                                                            elif self.subclass == "Assassin":
                                                                ""
                                                                #impostor
                                                            elif self.subclass == "Arcane Trickster":
                                                                ""
                                                                #versatile trickster
                                                            if self.level >= 14:
                                                                #blind sense
                                                                if self.level >= 15:
                                                                    self.savingThrows["Wisdom"].prof = True
                                                                    if self.level >= 16:
                                                                        abilImprove()
                                                                        if self.level >= 17:
                                                                            if self.subclass == "Thief":
                                                                                ""
                                                                                #thief's reflexes
                                                                            elif self.subclass == "Assassin":
                                                                                ""
                                                                                #death strike
                                                                            elif self.subclass == "Arcane Trickster":
                                                                                ""
                                                                                #spell thief
                                                                            if self.level >= 18:
                                                                                #elusive
                                                                                if self.level >= 19:
                                                                                    abilImprove()
                                                                                    if self.level >= 20:
                                                                                        ""
                                                                                        #stroke of luck
        elif self.classe == "Sorcerer":
            for i in range(2):
                newSkill(["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"])
            self.hitdie = 6
            self.savingThrows["Constitution"].prof = True
            self.savingThrows["Charisma"].prof = True
            #spells
            self.spellMod = self.profic + abilMod(CHA)
            self.subclasses = ["Draconic Bloodline", "Wild Magic"]
            self.subclass = randList(self.subclasses)
            if self.subclass == "Draconic Bloodline":
                ""
                #draconic ancestor
                if "Draconic" not in self.languages:
                    self.languages.append("Draconic")
            elif self.subclass == "Wild Magic":
                ""
                #wild magic surge
                #tides of chaos
            if self.level >= 2:
                #font of magic
                if self.level >= 3:
                    #metamagic
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 6:
                            if self.subclass == "Draconic Bloodline":
                                ""
                                #elemental affinity
                            elif self.subclass == "Wild Magic":
                                ""
                                #bend luck
                            if self.level >= 8:
                                abilImprove()
                                if self.level >= 10:
                                    #metamagic
                                    if self.level >= 12:
                                        abilImprove()
                                        if self.level >= 14:
                                            if self.subclass == "Draconic Bloodline":
                                                ""
                                                #dragon wings
                                            elif self.subclass == "Wild Magic":
                                                ""
                                                #controlled chaos
                                            if self.level >= 16:
                                                abilImprove()
                                                if self.level >= 17:
                                                    #metamagic
                                                    if self.level >= 18:
                                                        if self.subclass == "Draconic Bloodline":
                                                            ""
                                                            #draconic prescense
                                                        elif self.subclass == "Wild Magic":
                                                            ""
                                                            #spell bombardment
                                                        if self.level >= 19:
                                                            abilImprove()
                                                            if self.level >= 20:
                                                                #sorcerous restoration
                                                                ""
        elif self.classe == "Warlock":
            for i in range(2):
                newSkill(["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"])
            self.hitdie = 8
            self.savingThrows["Wisdom"].prof = True
            self.savingThrows["Charisma"].prof = True
            self.spellMod = self.profic + abilMod(CHA)
            if self.level >= 2:
                if self.level >= 3:
                    if self.level >= 4:
                        abilImprove()
                        if self.level >= 6:
                            if self.level >= 8:
                                abilImprove()
                                if self.level >= 10:
                                    if self.level >= 11:
                                        #Mystic Arcanum (6th-level)
                                        if self.level >= 12:
                                            abilImprove()
                                            if self.level >= 13:
                                                #Mystic Arcanum (7th-level)
                                                if self.level >= 14:
                                                    if self.level >= 15:
                                                        #Mystic Arcanum (8th-level)
                                                        if self.level >= 16:
                                                            abilImprove()
                                                            if self.level >= 17:
                                                                #Mystic Arcanum (9th-level)
                                                                if self.level >= 19:
                                                                    abilImprove()
                                                                    if self.level >= 20:
                                                                        ""
        elif self.classe == "Wizard":
            for i in range(2):
                newSkill(["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"])
            self.hitdie = 6
            self.savingThrows["Intelligence"].prof = True
            self.savingThrows["Wisdom"].prof = True
            self.spellMod = self.profic + abilMod(INT)
            if self.level >= 2:
                if self.level >= 4:
                    abilImprove()
                    if self.level >= 6:
                        if self.level >= 8:
                            abilImprove()
                            if self.level >= 10:
                                if self.level >= 12:
                                    abilImprove()
                                    if self.level >= 14:
                                        if self.level >= 16:
                                            abilImprove()
                                            if self.level >= 18:
                                                #Spell Mastery
                                                if self.level >= 19:
                                                    abilImprove()
                                                    if self.level >= 20:
                                                        #Signature Spells
                                                        ""

        self.maxHP = self.hitdie + abilMod(CON)*self.level + dieRoll(self.level - 1, self.hitdie)
        if (self.race == "Dwarf" and self.subrace == "Hill") or (self.classe == "Sorcerer" and self.subclass == "Draconic Bloodline"):
            self.maxHP += self.level
        self.curHP = self.maxHP

        #calculates other stats based on ability modifiers
        if self.classe == "Barbarian":
            self.AC = 10 + abilMod(DEX) + abilMod(CON)
        elif self.classe == "Monk":
            self.AC = 10 + abilMod(DEX) + abilMod(WIS)
        elif self.classe == "Sorcerer" and self.subclass == "Draconic Bloodline":
            self.AC = 13 + abilMod(DEX)
        else:
            #not the actual AC equation since there are multiple variables such as armor, but the actual AC values should be at least the AC values this outputs
            self.AC = 11 + abilMod(DEX)
        self.init = abilMod(DEX)
        self.passivePerception = 10 + abilMod(WIS)

    #prints out the character
    def toString(self):
        def abilMod(stat):
            return abilityScore(self.stats[stat])

        self.char = [self.background]
        if self.subrace != "":
            self.char.append(self.subrace)
        self.char.append(self.race)
        if self.subclass != "":
            self.char.append(self.subclass)
        self.char.append(self.classe)
        self.s = ""
        for att in self.char:
            self.s += att + " "
        print self.s[:-1]
        print "Level:", self.level
        print "Alignment:", self.alignment
        print "Proficiency Bonus: +" + str(self.profic)
        print
        for i in range (6):
            print str(statistics[i]) + ": \t", self.stats[i], "(" + str(abilMod(i)) + ")"
        print
        print "HP: \t\t", str(self.curHP) + "/" + str(self.maxHP)
        print "Armor Class: \t", self.AC
        print "Initiative: \t", self.init
        self.movement = self.speed/5
        print "Speed: \t\t", self.speed, "(" + str(self.movement) + ")"
        print "Hit Die: \t", self.hitdie
        print "Passive Perception:", self.passivePerception
        print
        print "Saving Throws:"
        for throw in statistics:
            save = self.savingThrows[throw]
            num = abilMod(save.stat)
            if save.prof == True:
                num += self.profic
                print throw + ": \t", num, "\tP"
            else:
                if self.classe == "Bard" and self.level >= 2:
                    num += self.profic/2
                elif self.classe == "Fighter" and self.subclass == "Champion" and self.level >= 7:
                    if throw in ["Strength", "Dexterity", "Constitution"]:
                        num += (self.profic + 1)/2
                print throw + ": \t", num
        print
        print "Skills:"
        for skil in skillNames:
            roll = self.skills[skil]
            num = abilMod(roll.stat)
            tabs = 1
            if skil == "Arcana" or skil == "Nature":
                tabs = 2
            if skil == "Animal Handling" or skil == "Sleight of Hand":
                tabs = 0
            if roll.prof == True:
                num += self.profic
                print skil, "\t"*tabs + "(" + statistics[roll.stat][:3].upper() + ")" + ": \t", num, "\tP"
            else:
                if self.classe == "Bard" and self.level >= 2:
                    num += self.profic/2
                print skil, "\t"*tabs + "(" + statistics[roll.stat][:3].upper() + ")" + ": \t", num
        print
        print "Features:"
        for feat in self.features:
            print " ", feat
        print
        print "Languages:"
        for lang in self.languages:
            print " ", lang
        print
        if self.spellMod != "N/A":
            print "Spell save DC:", 8 + self.spellMod
            print "Spell attack modifier:", self.spellMod
            print
        print "Gold:", self.gold
        print
        print "Inventory:"
        for inv in self.inventory:
            print " ", inv
        print

def randChar(rac = "-", clas = "-", backg = "-", lev = 0):
    race = randList(races)
    classe = randList(classes)
    background = randList(backgrounds)
    level = randint(1, 20)

    if rac in races:
        race = rac
    if clas in classes:
        clas = classe
    if backg in backgrounds:
        background = backg
    if lev > 0:
        level = lev

    return Char(race, classe, background, level)



rand = randChar()
#randChar(rac = "Human")
#randChar(clas = "Fighter")
#randChar(backg = "Soldier")
#randChar(lev = 1)
#randChar(rac = "Human", clas = "Fighter")
#randChar(rac = "Human", backg = "Soldier")
#randChar(rac = "Human", lev = 1)
#randChar(clas = "Fighter", backg = "Soldier")
#randChar(clas = "Fighter", lev = 1)
#randChar(backg = "Soldier", lev = 1)
#randChar(rac = "Human", clas = "Fighter", backg = "Soldier")
#randChar(rac = "Human", clas = "Fighter", lev = 1)
#randChar(rac = "Human", backg = "Soldier", lev = 1)
#randChar(clas = "Fighter", backg = "Soldier", lev = 1)
#randChar(rac = "Human", clas = "Fighter", backg = "Soldier", lev = 1)
rand.toString()

#testing every combination
'''for race in races:
    for classe in classes:
        for background in backgrounds:
            rand = randChar(rac = race, clas = classe, backg = background, lev = 20)
            rand.toString()'''
