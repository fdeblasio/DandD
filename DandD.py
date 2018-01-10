from random import randint

def dieRoll(numRolls, sidedDie, modifier):
    sum = 0
    for i in range(numRolls):
        sum += randint(1, sidedDie)
    sum += modifier
    return sum

def dieRoll(numRolls, sidedDie):
    return dieRoll(numRolls, sidedDie, 0)

def abilityScore(a):
    return (a-10)/2

def randChar():
    races = ["Dwarf", "Elf", "Halfling", "Human", "Dragonborn", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
    classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
    backgrounds = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"]
    char = [backgrounds, races, classes]

    stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    statNums = []
    for i in range(6):
        rolls = []
        for j in range(4):
            rolls.append(randint(1, 6))
        statNums.append(max(rolls[0], rolls[1]) + max(rolls[2], rolls[3]) + max(min(rolls[0], rolls[1]), min(rolls[2], rolls[3])))

    s = ""
    for attribute in char:
        s += attribute[randint(0, len(attribute) - 1)] + " "
    print s[:-1]
    for i in range (6):
        print stats[i], statNums[i], "(" + str(abilityScore(statNums[i])) + ")"

if __name__== "__main__":
    randChar()
