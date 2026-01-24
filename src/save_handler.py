import json
import os
import game

def write_save(game_state: game.gameState) -> None:
    dictionary = {"game_state": game_state.__dict__.copy()}
    if 'inventory' in dictionary["game_state"]:
        dictionary["game_state"].pop('inventory')
        dictionary.update(
            {"inventory": game_state.__dict__["inventory"].__dict__}
            )
    output = json.dumps(dictionary, indent=4)
    write_json(output)

def write_json(output: str) -> None:
  with open("game.sav", "wt") as f:
      f.write(output)

def read_json():
  if not os.path.exists('game.sav'):
      return({})
  else:
      with open("game.toml", "rb") as f:
          gamedata = json.loads(f).copy()
      return gamedata
