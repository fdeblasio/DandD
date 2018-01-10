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

    #gets a random value from each array
    race = races[randint(0, len(races) - 1)]
    classe = classes[randint(0, len(classes) - 1)]
    background = backgrounds[randint(0, len(backgrounds) - 1)]
    char = [background, race, classe]

    #Rolls for each stat in order (although in real life, after the six numbers are rolled, the player can assign them to whatever stats they want)
    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    statNums = []
    abilMod = []
    for i in range(6):
        rolls = []
        for j in range(4):
            rolls.append(dieRoll(1, 6))
        statNums.append(max(rolls[0], rolls[1]) + max(rolls[2], rolls[3]) + max(min(rolls[0], rolls[1]), min(rolls[2], rolls[3])))
        abilMod.append(abilityScore(statNums[i]))

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

    #calculates other stats
    movement = speed/5
    #not the actual AC equation since there are multiple variables, but the actual AC values should be at least the AC values this outputs
    AC = 10 + abilMod[DEX]
    init = abilMod[DEX]
    level = randint(1, 20)
    profic = (level-1)/4 + 2
    passivePerception = 10 + abilMod[WIS]

    #prints out the character
    s = ""
    for attribute in char:
        s += attribute + " "
    print s[:-1]
    print "Level:", level
    print "Proficiency Bonus: +" + str(profic)
    print
    for i in range (6):
        print str(stats[i]) + ": \t", statNums[i], "(" + str(abilMod[i]) + ")"
    print
    print "Armor Class: \t", AC
    print "Initiative: \t", init
    print "Speed: \t\t", speed, "(" + str(movement) + ")"
    print "Passive Perception:", passivePerception
    print

    #sets saving throws and skill bonuses
    saveThrows = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    skillNames = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
    savingThrows = {}
    skills = {}
    class skill:
        def __init__(self, stat, prof):
            self.stat = stat
            self.prof = prof
            self.num = 0

    for stat in range(len(saveThrows)):
        savingThrows[saveThrows[stat]] = skill(stat, False)
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
    print "Saving Throws:"
    for throw in saveThrows:
        save = savingThrows[throw]
        save.num = abilMod[save.stat]
        if save.prof == True:
            save.num += profic
        print throw + ": \t", save.num
    print

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
    print "Skills:"
    for skil in skillNames:
        roll = skills[skil]
        roll.num = abilMod[roll.stat]
        if roll.prof == True:
            roll.num += profic
        print skil + ": \t", roll.num

if __name__== "__main__":
    randChar()
