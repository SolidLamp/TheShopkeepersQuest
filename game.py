import time
from dataclasses import dataclass
import random

def print2(text, newline=True, pauseAtNewline=0.0, endingChar=False):
    for char in text:
        if char == "\n":
            time.sleep(pauseAtNewline)
        print(char, end="", flush=True)
        time.sleep(0.01)
    if newline: print()

def option(a):
    print()
    for i, options in enumerate(a, start=1):
        print2(f"{i}. {options}")
    print2("i. Inventory")
    if True == True:
      print2("d. debug")
    query=input(">>> ")
    if query == "i":
      print(game_state.inventory)
    if query == "d":
      print(game_state)
      debug()
    if query == "q":
        exit()
    print()
    return(query)



def ending(end):
    if end in endingsWithCustomText:
      index = endingsWithCustomText.index(end)
      print2(endingCustomText[index].replace("|",end), pauseAtNewline=0.65)
    print("\n\n")
    print2(defaultEndingText.replace("|",end), pauseAtNewline=0.65)

    print()
    print()
    print()
    time.sleep(0.25)
    print("You achieved the:")
    time.sleep(0.25)
    print()
    print("\033[1m" + end + "\033[0m")
    time.sleep(0.25)
    print()
    print("Ending.")
    time.sleep(0.5)
    print()
    print()
    print()
    print("Try again?")

def lose(text):
    print("\n\n")
    time.sleep(0.25)
    print("\033[31m\033[1mYou died!\033[0m")
    print("'" + text + "'")
    time.sleep(0.5)
    print("\n\n\nTry again?")

ShopkeeperQuotesExit = [
  "Remember, tomorrow is another day.",
  "Be seeing you.",
  "I wish you the best of luck.",
  "I give you my grace.",
  "I wish you luck on your quest.",
  "I'll get started on my tea.",
  "May all the spirits be with you."
  ]

ShopkeeperQuotes = [
  "Welcome!",
  "Sit down, my friend. Stay a while.",
  "You'll always be welcome here in my shop.",
  "Have a look at my wares. They could prove to be useful.",
  "Sorry I can't give discounts - I have a business to run, and I must make my money somehow.",
  "I don't blame you for coming inside in this winter.",
  "Sit down a while. I don't want you too stressed, my friend.",
  "I always believe that everyone has a tale worth telling - maybe talk to more people.",
  "Have you checked out the bazaar? There's a fisherman there who sells excellent-quality rods.",
  "Have you heard the news about the King? It's said that he's fallen ill. He's a good man - I hope he fully recovers.",
  "Have you seen the nearby forest? There's been some monkey sightings there."
  ]
  
endingsWithCustomText = ["Good","Secret","SHM"]
endingCustomText = [
  "And so, overnight, all the people returned to the town, as if they had never left.\nSoon after, the town was lifted into high spirits as the harvest had been the best in almost thirty years.\nDespite, the prospering town, you decided to leave.\nYou had no desire to stay after the events you just experienced, and you would rather leave than stay to make some money.",
  "And so, overnight, you became the new shopkeeper, but nothing really changed in the end.\nThe townspeople never returned, but many travellers came, hearing about what happened.\nMany decided te stay after a plentiful harvest brought good omens to the town.\nThis, however, would not be the last of it...\n...and you knew that.",
  "You achieved the\n|\nEnding.\nTry Again?",
  ]
defaultEndingText = "\033[1mThe Shopkeeper's Quest\033[0m\n\nSchool Project Edition\n\nWith inspiration from:\nColossal Cave Adventure, by Will Crowther and Don Woods;\nKing's Quest, by Sierra On-Line;\nHenry Stickmin, by Puffballs United;\nMinecraft: Story Mode, by Telltale Games;\n and RTX Morshu: The Game, by koshkamatew\nWith special thanks to\n\033[1m\033[33mYOU\033[0m\nfor playing the game,\nfor if a tree falls and no one hears it, does it make a noise?"


@dataclass
class Inventory:
    items: list[str] = None
    keyItems: list[str] = None
    def __post_init__(self):
        self.items = [] if self.items is None else self.items
        self.keyItems = [] if self.keyItems is None else self.keyItems
    def getItem(self, item: str):
        print2("\nYou got \033[1m" + str(item) + "\033[0m!")
        self.items.append(item)
    def getKeyItem(self, item: str):
        print2("\nYou got \033[1m" + str(item) + "\033[0m!")
        self.keyItems.append(item)
    def __str__(self):
        if not self.items and not self.keyItems:
            return "Your inventory is empty"
        output = []
        if self.items:
            output.append("Items:\n" + "\n".join(f"- {item}" for item in self.items))
        if self.keyItems:
            output.append("Key Items:\n" + "\n".join(f"- {item}" for item in self.keyItems))
        return "\n".join(output)
#Rusted Sword (Forest), Amber Necklace (Town), AncientKey (Fountain) and Golden Idol (Cave)
@dataclass
class gameState:
    inventory: Inventory
    rubies: int = 0
    shopkeeperName: str = "The Shopkeeper"
    position: float = 0.0
    beatenGame: bool = False
    caveOpened: bool = False
    def getRuby(self, num: int):
        print2("\nYou got \033[1m" + str(num) + "\033[0m Rubies!")
        self.rubies=self.rubies+num
        print2("\033[0m You currently have \033[1m" + str(self.rubies) + "\033[0m Rubies.\n")

game_state = gameState(
    inventory=Inventory(items=[])
)


##


def intro():
    print("\033[36m\033[40m" + r"""___ _  _ ____ 
 |  |__| |___ 
 |  |  | |___ 
              
____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ 
[__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__  
___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___] 
                                                       
____ _  _ ____ ____ ___ 
|  | |  | |___ [__   |  
|_\| |__| |___ ___]  |  
                        """ + "\033[0m")
    print2("Use the numbers to choose options")
    query = option(["Begin","Quit"])
    if query == "1":
        #print2("You are a travelling merchant, approaching a new town to sell your wares in another region.\nAs you approach the town, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just outside the limits of our little town of Llanerchwyrd.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them all.\nAny that resided within the town limits have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the town with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?' he continues, 'There's an old legend that if all seems to disappear overnight, then this marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic, however.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a silver _.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the limits of the main town.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m")
        print()
        gameLoop()
    else:
        exit()

#altar uuddlrlrba

def gameLoop():
    print2("You are standing in a field. There is a road to the north, leading to a town, a forest to the east, a cave to the south, a shop and bazaar to the west, and there are some bushes nearby.")
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to " + game_state.shopkeeperName + "'s shop","Go to the bazaar"])
    if query == "1":
        forest()
    elif query == "2":
        road()
    elif query == "3":
        cave()
    elif query == "4":
        shop()
    elif query == "5":
        bazaar()
    else:
        field()
    query = option(["Yes","No"])
    if query == "1":
        gameLoop()
    elif query == "2":
        exit()
    else:
        exit()

def field():
    print2("You are standing in a field.")
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to " + game_state.shopkeeperName + "'s shop","Go to the bazaar"])
    if query == "1":
        forest()
    elif query == "2":
        road()
    elif query == "3":
        cave()
    elif query == "4":
        shop()
    elif query == "5":
        bazaar()
    else:
        field()

def forest():
    print2("You come to the opening of the forest. The forest is vast and the trees tower over you.")
    query = option(["Go further in","Leave"])
    if query == "1":
        forest2()
    elif query == "2":
        field()
    else:
        forest()

def forest2():
    print2("You are deep in the forest. It is dim, and difficult to see.")
    if "Rusted Sword" in game_state.inventory.keyItems: 
        query = option(["Leave"])
    else:
        query = option(["Leave","Go further in"])
    if query == "2":
        if "Rusted Sword" in game_state.inventory.keyItems: forest3()
    elif query == "1":
        forest()
    else:
        forest2()

def forest3():
    print2("You come to a clearing, deep in the forest. There is a bonobo sitting, facing you")
    query = option(["Fight the bonobo","Leave"])
    if query == "1":
        if 1 == 1:
            print2("You manage to defeat the bonobo, using your weapon.")
            print2("You manage to find a chest, containing 15 rubies!")
            game_state.getRuby(15)
            print2("Underneath all the rubies, you find the rusted sword.")
            game_state.inventory.getKeyItem("Rusted Sword")
            forest2()
        else:
            print2("You attempt to fight the bonobo, but it easily overpowers you. You are killed.")
            lose("What did you think was going to happen?")
    elif query == "2":
        print2("You attempt to leave, but the bonobo catches you. You are killed.")
        lose("Bonobos are quite agressive.")
    else:
        forest3()
        


def road():
    print2("You follow the road, but although it looks like a short distance, it feels like a long journey, as if it were a mile long. You wish for a mule to travel on.")
    query = option(["Go to the town","Go to the field"])
    if query == "1":
        townArrival()
    elif query == "2":
        field()
    else:
        action1()

def townArrival():
    print2("You follow the road to town. It seems barren and no one is there.")
    query = option(["Follow the High Street further","Go Back"])
    if query == "1":
        door()
    elif query == "2":
        road()
    else:
        town()

def town():
    print2("You are in the town. It seems barren and no one is there.")
    query = option(["Follow the High Street further","Go Back"])
    if query == "1":
        town2()
    elif query == "2":
        road()
    else:
        town()

def town2():
    print2("You are in the high street of the town. The town centre is to your north.")
    query = option(["Go to the town centre","Go South"])
    if query == "1":
        town3()
    elif query == "2":
        town()
    else:
        town2()

def town3():
    print2("You are in the centre of town. There are paths each direction, with a fountain in the middle.")
    query = option(["Go North","Go East","Go South","Go West","Go to the Fountain"])
    if query == "1":
        townNorth()
    elif query == "2":
        townEast()
    elif query == "3":
        town2()
    elif query == "4":
        townWest()
    elif query == "5":
        fountain()
    else:
        town3()

def fountain():
    print2("You are at the fountain in the town centre.")
    query = option(["Admire it","Throw a ruby in for good luck","Go back"])
    if query == "1":
        print2("You admire the fountain.")
        fountain()
    elif query == "2":
        print2("You throw a ruby in")
        fountain() #TODO
    elif query == "3":
        town3()
    else:
        fountain()

def townEast():
    print2("There is a note on the floor.")
    query = option(["Read the note","Return"])
    if query == "1":
        note()
    elif query == "2":
        town3()
    else:
        townEast()

def note():
    print2("You read the note. It reads, 'None can stop me now. At 38, they will know. North, North, South, South, West, East, West, East.'")
    query = option(["Read the note again","Place it back down"])
    if query == "1":
        note()
    elif query == "2":
        townEast()
    else:
        note()

def townNorth():
    print2("You enter an empty street of market stalls. A northern route leads to a smaller street.")
    query = option(["Go down the smaller street","Go to the Town Centre."])
    if query == "1":
        door()
    elif query == "2":
        town3()
    else:
        townNorth()

def door():
    print("You come to a dead-end on the street, where you see a mysterious door that doesn't seem to lead anywhere. Its lock seems rusted. There is a keyhole. What will you do?")
    query = option(["Attempt to turn the handle","Unlock the door with the Ancient Key","Go back"])
    if query == "1":
        lock()
    elif query == "2":
        unlock()
    elif query == "3":
        town3()
    else:
        door()

def lock():
    print2("You attempt to turn the handle, but it does not budge.")
    query = option(["Try Again","Go Back"])
    if query == "1":
        lock()
    elif query == "2":
        door()
    else:
        lock()
  
def unlock():
    print2("You unlock the mysterious door with the Ancient Key.")
    query = option(["Continue"])
    if query == "1":
        secret()
    else:
        print2("You cannot go back now.")
        secret()

def secret():
    print2("You go through the door. It is pitch-black.")
    query = option(["Continue"])
    if query == "1":
        secret2()
    else:
        print2("You cannot go back now.")
        secret2()

def secret2():
    print2("As you continue, everything goes pitch-black.")
    query = option(["Continue"])
    if query == "1":
        secret3()
    else:
        print2("You cannot go back now.")
        secret3()

def secret3():
    print2("As you continue, you see a light at the end.")
    query = option(["Continue"])
    if query == "1":
        secret4()
    else:
        print2("You cannot go back now.")
        secret4()

def secret4():
    print2("Eventually, you get to the end, and can go through the illuminated exit.")
    query = option(["Continue"])
    if query == "1":
        secret5()
    else:
        print2("You cannot go back now.")
        secret5()

def secret5():
    print2("It is the back room of " + game_state.shopkeeperName + "'s shop. It is full of rubies and products. There is a letter on a nearby desk.")
    query = option(["Take some rubies","Take some lamp oil","Take some rope","Take some bombs","Go through to the front","Inspect the letter"])
    if query == "1":
        print2("You take some rubies.")
        getRuby(9000)
        secret5()
    elif query == "2":
        print2("You take some lamp oil.")
        secret5()
    elif query == "3":
        print2("You take some rope.")
        secret5()
    elif query == "4":
        print2("You take some bombs.")
        secret5()
    elif query == "5":
        secret6()
    elif query == "6":
        print2("The envelope is sealed with a luxurious seal. The letter is addressed to 'The Overseer', and has the number 38 written on it. There is no letter inside the envelope.")
        secret5()
    else:
        print2("You cannot go back now.")
        secret5()

def secret6():
    print2("You are in the front room of " + game_state.shopkeeperName + "'s shop.")
    query = option(["Become " + game_state.shopkeeperName])
    if query == "1":
        print2("You become " + game_state.shopkeeperName + ". The people eventually return. You begin selling your wares again, and you finally understand the full circumstances of these events.")
        ending("Secret")
    else:
        print2("You cannot go back now.")
        secret6()

def townWest():
    print2("There is a large square, with houses all around. There is an alley.")
    query = option(["Go down the alley","Go to the Town Centre"])
    if query == "1":
        maze1()
    elif query == "2":
        town3()
    else:
        townWest() 

def maze1():
    print2("You are in a maze of twisty little alleys, all alike. Something about this seems familiar. You believe the alley you entered from is to the South.")
    query = option(["Go north","Go east","Go south","Go west"])
    if query == "1":
        maze1()
    elif query == "2":
        town3()
    else:
        townWest() 


def shop():
    print2("\033[33m'" + random.choice(ShopkeeperQuotes) + "'\033[0m")
    print2("Current Rubies:" + str(game_state.rubies) + "\nLamp Oil - 15 Rubies\nRope - 20 Rubies\nBomb - 30 Rubies")
    query = option(["Purchase lamp oil","Purchase rope","Purchase bomb","Ask about quest","Leave"])
    if query == "1":
        if game_state.rubies >= 15:
          game_state.rubies = game_state.rubies - 15
          game_state.inventory.getItem("Lamp Oil")
        else:
          print2("\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m")
        shop()
    elif query == "2":
        if game_state.rubies >= 20:
          game_state.rubies = game_state.rubies - 20
          game_state.inventory.getItem("Rope")
        else:
          print2("\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m")
        shop()
    elif query == "3":
        if game_state.rubies >= 30:
          game_state.rubies = game_state.rubies - 30
          game_state.inventory.getItem("Bomb")
        else:
          print2("\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m")
        shop()
    elif query == "4":
        cursedItems = len({"Rusted Sword","Amber Necklace","Golden Idol"}) & set(game_state.inventory.keyItems)
        if cursedItems == 3:
          print2("\033[33m'Well, I'll be. That's all of them. Honestly, I kind of doubted you could do it - now I see that my doubt was misplaced! You will go down in legend for your heroism!'")
          time.sleep(0.25)
          print2("\033[33m'Oh, and just one more thing: thank you.'\033[0m")
          ending("Good")
        elif cursedItems > 0:
          print2(f"\033[33m'Great! You managed to get {cursedItems} of the items - now we just need {3 - cursedItems} more!'\033[0m")
        print2("\033[33m'Sorry, I can't help you much. I do know, however, that one of the items is somewhere in the town and another is in the nearby forest. That's all I know.'\033[0m")
        shop()
    elif query == "5":
        print2("\033[33m'" + random.choice(ShopkeeperQuotesExit) + "'\033[0m")
        field()
    else:
        shop() 


def action1():
    print2("")
    query = option(["",""])
    if query == "1":
        action2()
    elif query == "2":
        action3()
    else:
        print2("WHAT?")
        action1()


def action2():
    print2("")

def action3():
    print2("")


##

def debug():
    query = option(["ShopkeeperQuote","ShopkeeperQuoteExit","Rusted Sword","Win the game","Secret ending","Get all items","Debug ending code","SHM Ending"])
    if query == "1": print(random.choice(ShopkeeperQuotes))
    elif query == "2": print(random.choice(ShopkeeperQuotesExit))
    elif query == "3": game_state.inventory.getKeyItem("Rusted Sword")
    elif query == "4": ending("Good")
    elif query == "5": ending("Secret")
    elif query == "6": 
        game_state.inventory.getKeyItem("Rusted Sword")
        game_state.inventory.getKeyItem("Amber Necklace")
        game_state.inventory.getKeyItem("Golden Idol")
        game_state.inventory.getKeyItem("Ancient Key")
        game_state.inventory.getItem("Fishing Rod")
        game_state.inventory.getItem("Lamp Oil") #Forest
        game_state.inventory.getItem("Lamp Oil") #Cave
        game_state.inventory.getItem("Rope") #Cave
        game_state.inventory.getItem("Bombs") #Cave
        game_state.inventory.getItem("Bombs") #Cave
        game_state.getRuby(9001)
    elif query == "7":
        print("Good")
        if "Good" in endingsWithCustomText:
            print("Good is in there")
        else: print("Not this time")
        index = endingsWithCustomText.index("Good")
        print(index)
        print2(endingCustomText[index], pauseAtNewline=0.65)
        print(defaultEndingText)
    elif query == "8":
        ending("SHM")


##

while True:
    intro()
exit