import time
from dataclasses import dataclass

def print2(a):
    for i in a:
        print(i, end="", flush=True)
        time.sleep(0.01)
    print()

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
    print()
    return(query)



def ending(a):
    print()
    print()
    print()
    time.sleep(0.25)
    print("You achieved the:")
    time.sleep(0.25)
    print()
    print("\033[1m" + a + "\033[0m")
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

ShopkeeperQuotes = [
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
@dataclass
class Inventory:
    items: list[str]
    def __str__(self):
        if not self.items:
            return "Your inventory is empty"
        return "Inventory items:\n" + "\n".join(f"- {item}" for item in self.items)


@dataclass
class gameState:
    inventory: Inventory
    rubies: int = 0
    shopkeeperName: str = "The Shopkeeper"
    position: float = 0.0
    beatenGame: bool = False

def getRuby(num):
    print()
    print2("You got \033[1m" + str(num) + "\033[0m Rubies!")
    gameState.rubies=gameState.rubies+num
    print("\033[0m")
    print2("You currently have \033[1m" + str(gameState.rubies) + "\033[0m Rubies.")
    print()

game_state = gameState(
    inventory=Inventory(items=[])
)

print("DEBUG: Initial game state")
print(game_state)
print("Initial inventory:")
print(game_state.inventory)


# The Game

def intro():
    print("\033[1m" + "The Shopkeeper's Quest" + "\033[0m\n" + "or" + "\n\033[1m" + "The Merchant's Quest" + "\033[0m\n" + "[Working title]\n\033[0m")
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
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to the shop","Go to the bazaar"])
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
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to the shop","Go to the bazaar"])
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
    query = option(["Go further in","Leave"])
    if query == "1":
        forest3()
    elif query == "2":
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
            getRuby(15)
            print2("Underneath all the rubies, you find the rusted sword.")
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
    query = option(["Continue","Go Back"])
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
        door()
    elif query == "2":
        road()
    else:
        town()

def door():
    print("You come to a dead-end on the street, where you see a mysterious door that doesn't seem to lead anywhere. Its lock seems rusted. There is a keyhole. What will you do?")
    query = option(["Attempt to turn the handle","Unlock the door with the Ancient Key","Go back"])
    if query == "1":
        lock()
    elif query == "2":
        unlock()
    elif query == "3":
        town()
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
    print2("It is the back room of " + game_state.shopkeeperName + "'s shop. It is full of rubies and products.")
    query = option(["Take some rubies","Take some lamp oil","Take some rope","Take some bombs","Go through to the front"])
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

intro()
exit