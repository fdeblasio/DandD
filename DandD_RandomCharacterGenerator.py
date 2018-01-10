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
    if len(args) == 3:
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

    #gets a random value from each array
    def randList(list):
        return list[randint(0, len(list) - 1)]

    race = randList(races)
    classe = randList(classes)
    background = randList(backgrounds)
    char = [race, classe, background]
    alignment = randList(align1) + " " + randList(align2)
    if alignment == "Neutral Neutral":
        alignment = "True Neutral"

    #Rolls for each stat in order (although in real life, after the six numbers are rolled, the player can assign them to whatever stats they want)
    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    statNums = []
    def abilMod(stat):
        return abilityScore(statNums[stat])

    for i in range(6):
        rolls = []
        for j in range(4):
            rolls.append(dieRoll(1, 6))
        statNums.append(max(rolls[0], rolls[1]) + max(rolls[2], rolls[3]) + max(min(rolls[0], rolls[1]), min(rolls[2], rolls[3])))

    #Adds racial bonuses and sets speed
    speed = 0
    if race == "Dwarf":
        statNums[CON] += 2
        speed = 25
    elif race == "Elf":
        statNums[DEX] += 2
        speed = 30
    elif race == "Halfling":
        statNums[DEX] += 2
        speed = 25
    elif race == "Human":
        for stat in statNums:
            stat += 1
        speed = 30
    elif race == "Dragonborn":
        statNums[STR] += 2
        statNums[CHA] += 1
        speed = 30
    elif race == "Gnome":
        statNums[INT] += 2
        speed = 25
    elif race == "Half-Elf":
        statNums[CHA] += 2
        speed = 30
    elif race == "Half-Orc":
        statNums[STR] += 2
        statNums[CON] += 1
        speed = 30
    elif race == "Tiefling":
        statNums[CHA] += 2
        statNums[INT] += 1
        speed = 30

    #hit die for HP
    if classe == "Sorcerer" or classe == "Wizard":
        hitdie = 6
    elif classe == "Bard" or classe == "Cleric" or classe == "Druid" or classe == "Monk" or classe == "Rogue" or classe == "Warlock":
        hitdie = 8
    elif classe == "Fighter" or classe == "Paladin" or classe == "Ranger":
        hitdie = 10
    elif classe == "Barbarian":
        hitdie = 12

    #calculates other stats
    #not the actual AC equation since there are multiple variables, but the actual AC values should be at least the AC values this outputs
    level = randint(1, 20)
    #proficieny bonus = (1-4: +2, 5-8: +3, 9-12: +4, 13-16: +5, 17-20: +6)
    profic = (level-1)/4 + 2
    spellMod = "N/A"
    gold = 0
    features = []
    languages = ["Common"]
    inventory = []

    #sets saving throws and skill bonuses
    skillNames = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
    savingThrows = {}
    skills = {}
    class skill:
        def __init__(self, stat, prof):
            self.stat = stat
            self.prof = prof

    for stat in range(len(stats)):
        savingThrows[stats[stat]] = skill(stat, False)
    #checks for the class in order to set its corresponding saving throws as proficient
    if classe == "Barbarian" or classe == "Fighter":
        savingThrows["Strength"].prof = True
        savingThrows["Constitution"].prof = True
    elif classe == "Bard":
        savingThrows["Dexterity"].prof = True
        savingThrows["Charisma"].prof = True
    elif classe == "Cleric" or classe == "Paladin" or classe == "Warlock":
        savingThrows["Wisdom"].prof = True
        savingThrows["Charisma"].prof = True
    elif classe == "Druid" or classe == "Wizard":
        savingThrows["Intelligence"].prof = True
        savingThrows["Wisdom"].prof = True
    elif classe == "Monk" or classe == "Ranger":
        savingThrows["Strength"].prof = True
        savingThrows["Dexterity"].prof = True
    elif classe == "Rogue":
        savingThrows["Dexterity"].prof = True
        savingThrows["Intelligence"].prof = True
    elif classe == "Sorcerer":
        savingThrows["Constitution"].prof = True
        savingThrows["Charisma"].prof = True

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
    #checks for the background in order to set its corresponding skills as proficient
    if background == "Acolyte":
        skills["Insight"].prof = True
        skills["Religion"].prof = True
    elif background == "Charlatan":
        skills["Deception"].prof = True
        skills["Sleight of Hand"].prof = True
    elif background == "Criminal":
        skills["Deception"].prof = True
        skills["Stealth"].prof = True
    elif background == "Entertainer":
        skills["Acrobatics"].prof = True
        skills["Performance"].prof = True
    elif background == "Folk Hero":
        skills["Animal Handling"].prof = True
        skills["Survival"].prof = True
    elif background == "Guild Artisan":
        skills["Insight"].prof = True
        skills["Persuasion"].prof = True
    elif background == "Hermit":
        skills["Medicine"].prof = True
        skills["Religion"].prof = True
    elif background == "Noble":
        skills["History"].prof = True
        skills["Persuasion"].prof = True
    elif background == "Outlander":
        skills["Athletics"].prof = True
        skills["Survival"].prof = True
    elif background == "Sage":
        skills["Arcana"].prof = True
        skills["History"].prof = True
    elif background == "Sailor":
        skills["Athletics"].prof = True
        skills["Perception"].prof = True
    elif background == "Soldier":
        skills["Athletics"].prof = True
        skills["Intimidation"].prof = True
    elif background == "Urchin":
        skills["Sleight of Hand"].prof = True
        skills["Stealth"].prof = True

    #Race features
    if race == "Dwarf":
        features.append("Darkvision")
        languages.append("Dwarvish")
    elif race == "Elf":
        features.append("Darkvision")
        languages.append("Elvish")
        skills["Perception"].prof = True
    elif race == "Halfling":
        languages.append("Halfling")
    elif race == "Human":
        noCommon = allLang
        noCommon.remove("Common")
        languages.append(randList(noCommon))
    elif race == "Dragonborn":
        languages.append("Draconic")
    elif race == "Gnome":
        features.append("Darkvision")
        languages.append("Gnomish")
    elif race == "Half-Elf":
        features.append("Darkvision")
        languages.append("Elvish")
        noComElf = allLang
        noComElf.remove("Common")
        noComElf.remove("Elvish")
        languages.append(randList(noComElf))
    elif race == "Half-Orc":
        features.append("Darkvision")
        languages.append("Orc")
        skills["Intimidation"].prof = True
    elif race == "Tiefling":
        features.append("Darkvision")
        languages.append("Infernal")

    #Class Features
    #Implement Path/School/etc features
    if classe == "Barbarian":
        if level >= 5:
            speed += 10
            if level >= 20:
                statNums[STR] += 4
                statNums[CON] += 4
        AC = 10 + abilMod(DEX) + abilMod(CON)
    elif classe == "Bard":
        stats = stats
        #proficieny bonus is added down when skills are being calculated
    elif classe == "Cleric":
        spellMod = profic + abilMod(WIS)
    elif classe == "Druid":
        spellMod = profic + abilMod(WIS)
        languages.append("Druidic")
    elif classe == "Fighter":
        stats = stats
    elif classe == "Monk":
        AC = 10 + abilMod(DEX) + abilMod(WIS)
        if level >= 2:
            #speed += (2-5: +10, 6-9: +15, 10-13: +20, 14-17: +25, 18-20: +30)
            speed += (level-2)/4 * 5 + 10
            if level >= 13:
                for lang in allLang:
                    if lang not in languages:
                        languages.append(lang)
    elif classe == "Paladin":
        if level >= 2:
            spellMod = profic + abilMod(CHA)
    elif classe == "Ranger":
        if level >= 2:
            spellMod = profic + abilMod(WIS)
    elif classe == "Rogue":
        languages.append("Thieves' Cant")
        if level >= 15:
            savingThrows["Wisdom"].prof = True
    elif classe == "Sorcerer":
        spellMod = profic + abilMod(CHA)
    elif classe == "Warlock":
        spellMod = profic + abilMod(CHA)
    elif classe == "Wizard":
        spellMod = profic + abilMod(INT)

    #These stats are based off of ability modifiers so they're put at the end since all modifiers should be final by now
    HP = hitdie + abilMod(CON)*level + dieRoll(level - 1, hitdie)
    AC = 10 + abilMod(DEX)
    init = abilMod(DEX)
    passivePerception = 10 + abilMod(WIS)

    #prints out the character
    s = ""
    for attribute in char:
        s += attribute + " "
    print s[:-1]
    print "Level:", level
    print "Alignment:", alignment
    print "Proficiency Bonus: +" + str(profic)
    print
    for i in range (6):
        print str(stats[i]) + ": \t", statNums[i], "(" + str(abilMod(i)) + ")"
    print
    print "HP: \t\t", HP
    print "Armor Class: \t", AC
    print "Initiative: \t", init
    movement = speed/5
    print "Speed: \t\t", speed, "(" + str(movement) + ")"
    print "Hit Die: \t", hitdie
    print "Passive Perception:", passivePerception
    print
    print "Saving Throws:"
    for throw in stats:
        save = savingThrows[throw]
        num = abilMod(save.stat)
        if save.prof == True:
            num += profic
        elif classe == "Bard" and level >= 2:
            num += profic/2
        print throw + ": \t", num
    print
    print "Skills:"
    for skil in skillNames:
        roll = skills[skil]
        num = abilMod(roll.stat)
        if roll.prof == True:
            num += profic
        elif classe == "Bard" and level >= 2:
            num += profic/2
        print skil, "\t(" + stats[roll.stat][:3].upper() + ")" + ": \t", num
    print
    print "Features:"
    for feat in features:
        print feat
    print
    print "Languages:"
    for lang in languages:
        print lang
    print
    if spellMod != "N/A":
        print "Spell save DC:", 8 + spellMod
        print "Spell attack modifier:", spellMod
        print
    print "Gold:", gold
    print
    print "Inventory:"
    for inv in inventory:
        print inv
    print

if __name__== "__main__":
    randChar()
