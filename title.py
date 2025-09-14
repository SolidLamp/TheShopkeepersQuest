from shm import gameLoop
from shm import print2
from shm import option

print(
        "\033[36m\033[40m"
        + r"""
___ _  _ ____ 
 |  |__| |___ 
 |  |  | |___ 

____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ 
[__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__  
___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___] 

____ _  _ ____ ____ ___ 
|  | |  | |___ [__   |  
|_\| |__| |___ ___]  |  
                        """
        + "\033[0m"
)
print2("Use the numbers to choose options, or press 'Q' to quit at any time")
query = option(["Begin", "Skip Intro", "Quit"], Inventory=False)
if query == "1":
    print2(
        "You are a travelling merchant, approaching a new village to sell your wares in another region.\nAs you approach the village, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just outside the limits of our little village.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them..\nAny that resided within the village limits have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the village with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?'\033[0m he continues, \033[33m'There's an old legend that if all seems to disappear overnight, then it marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a golden idol.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the main limits of the village.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m"
    )
    print()
    gameLoop(1)
if query == "2":
    gameLoop(2)
else:
    exit()

while True:
    gameLoop()