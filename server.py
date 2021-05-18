import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    next_next_move = ""
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Amy, Samuel, Arusha and Sunil",  
            "color": "#FFC72C",  # TODO: Personalize
            "head": "fang",  # TODO: Personalize
            "tail": "curled",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()  
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        #possible_moves = ["up", "down", "left", "right"]

        # Check corners
        #snake_body = data["you"]["body"]
        head = data["you"]["head"]
        second_entry = data["you"]["body"][1]
        health =data["you"]["health"]
        foods=data["board"]["food"]
        body = data["you"]["body"]
        all_snakes = []

        try: 
          all_snakes = data["snakes"]
        except:
          all_snakes = []

        
        max_x=data["board"]["width"]-1
        max_y=data["board"]["height"]-1

        next_moves = ["up","down","left","right"]
        head_x, head_y = head["x"], head["y"]
        second_entry_x, second_entry_y = second_entry["x"], second_entry["y"]

        #removing opposite move of to avoid backpedal
        if head_x > second_entry_x and head_y == second_entry_y: 
          last_move = "left" 
        elif head_x < second_entry_x and head_y == second_entry_y :
          last_move = "right" 
        elif head_y > second_entry_y and head_x == second_entry_x :
          last_move = "down"
        elif head_y < second_entry_y and head_x == second_entry_x :
          last_move = "up"
        else:
          pass
        
        try:
          next_moves.remove(last_move) 
        except:
          pass

         # wall check
        # if head_x <= testx and head_y <= testx:
        #   try:
        #    next_moves.remove("left")
        #    next_moves.remove("down")
        #   except:
        #    pass
        # elif head_x <= testx and head_y >= testy:
        #   try:
        #     next_moves.remove("left")
        #     next_moves.remove("up")
        #   except:
        #     pass
        # elif head_x <= testx:
        #   try:
        #     next_moves.remove("left")
        #   except:
        #     pass
        # else:
        #   pass
        # if head_x >= testy and head_y <= testx:
        #   try:
        #    next_moves.remove("right")
        #    next_moves.remove("down")
        #   except:
        #    pass
        # elif head_x >= testy and head_y >= testy:
        #   try:
        #     next_moves.remove("right")
        #     next_moves.remove("up")
        #   except:
        #     pass
        # elif head_x >= testy:
        #   try:
        #     next_moves.remove("right")
        #   except:
        #     pass
        # elif head_y <= testx:
        #   try:
        #     next_moves.remove("down")
        #   except:
        #     pass
        # elif head_y >= testy:
        #   try:
        #     next_moves.remove("up")
        #   except:
        #     pass
        # else:
        #   pass

        # expand movement out by one block
        possible_head_moves = [
          #original moves
          [head_x+1,head_y,["right"]],
          [head_x-1,head_y,["left"]],
          [head_x,head_y+1,["up"]],
          [head_x,head_y-1,["down"]],
          #moves after a right move
          [head_x+2,head_y,["right","right"]],
          [head_x+1,head_y+1,["right","up"]],
          [head_x+1,head_y-1,["right","down"]],
           #moves after a two right move
          [head_x+3,head_y,["right","right","right"]],
          [head_x+2,head_y+1,["right","right","up"]],
          [head_x+2,head_y-1,["right","right","down"]],
          [head_x+2,head_y+2,["right","right","up","up"]],
          [head_x+2,head_y-2,["right","right","down","down"]],
           #moves after a three right move
           #prev commented
          [head_x+4,head_y,["right"]],
          [head_x+3,head_y+1,["right"]],
          [head_x+3,head_y-1,["right"]],
          [head_x+3,head_y+2,["right"]],
          [head_x+3,head_y-2,["right"]],
          [head_x+3,head_y+3,["right"]],
          [head_x+3,head_y-3,["right"]],
          #moves after a left move
          [head_x-2,head_y,["left","left"]],
          [head_x-1,head_y+1,["left"]],
          [head_x-1,head_y-1,["left"]],
          #moves after two left move
          [head_x-3,head_y,["left","left","left"]],
          [head_x-2,head_y+1,["left","left","up"]],
          [head_x-2,head_y-1,["left","left","down"]],
          [head_x-2,head_y+2,["left","left","up","up"]],
          [head_x-2,head_y-2,["left","left","down"]],
           #moves after a three left move
           #previous commented
          [head_x-4,head_y,["left"]],
          [head_x-3,head_y+1,["left"]],
          [head_x-3,head_y-1,["left"]],
          [head_x-3,head_y+2,["left"]],
          [head_x-3,head_y-2,["left"]],
          [head_x-3,head_y+3,["left"]],
          [head_x-3,head_y-3,["left"]],
          #moves after an up move
          [head_x+1,head_y+1,["up","right"]],
          [head_x-1,head_y+1,["up","left"]],
          [head_x,head_y+2,["up","up"]],
          #moves after two up move
          [head_x+1,head_y+2,["up","up","right"]],
          [head_x-1,head_y+2,["up","up","left"]],
          [head_x,head_y+3,["up","up","up"]],
          #moves after three up move
          # previously commented
          [head_x+1,head_y+3,["up"]],
          [head_x-1,head_y+3,["up"]],
          [head_x+2,head_y+3,["up"]],
          [head_x-2,head_y+3,["up"]],
          [head_x,head_y+4,["up"]],
          #moves after a down move
          [head_x,head_y-2,["down","down"]],
          [head_x+1,head_y-1,["down","right"]],
          [head_x-1,head_y-1,["down","left"]],
          #moves after two down move
          [head_x,head_y-3,["down","down","down"]],
          [head_x+1,head_y-2,["down","down","right"]],
          [head_x-1,head_y-2,["down","down","left"]], 
          #moves after three down move
          # previously commented
          [head_x+1,head_y-3,["down"]],
          [head_x-1,head_y-3,["down"]],
          [head_x+2,head_y-3,["down"]],
          [head_x-2,head_y-3,["down"]],
          [head_x,head_y-4,["down"]],
        ]

        bad_paths = []

        body_blocking = []

        for block in body:
         body_blocking.append(block)

        # store all snake bodies on board
        if len(all_snakes) > 0:
          for snake in all_snakes:
           #body_blocking += snake["body"]
            for block in snake["body"]:
              body_blocking.append(block)
        
        # next gen self-body block
        #double loop == NOT GOOd
        
        for move in possible_head_moves:
          for block in body_blocking:
            if (move[0],move[1]) == (block["x"], block["y"]):
                 if len(move[2]) == 1:
                   try:
                      next_moves.remove(move[2][0])
                   except:
                      pass
                 bad_paths.append(move[2])
            elif move[0] <= -2 and move[1] >= 12:
                try:
                  next_moves.remove("left")
                  next_moves.remove("down")
                except:
                  pass
            elif move[0] <= -2 and move[1] <= -2:
                  try:
                    next_moves.remove("left")
                    next_moves.remove("up")
                  except:
                    pass
            elif move[0] <= -2:
                  try:
                    next_moves.remove("left")
                  except:
                    pass
            elif move[0] >= 12 and move[1] >= 12:
                try:
                  next_moves.remove("right")
                  next_moves.remove("down")
                except:
                  pass
            elif move[0] >= 12 and move[1] <= -2:
                  try:
                    next_moves.remove("right")
                    next_moves.remove("up")
                  except:
                    pass
            elif move[0] >= 12:
                  try:
                    next_moves.remove("right")
                  except:
                    pass
            elif move[1] >= 12:
                  try:
                    next_moves.remove("up")
                  except:
                    pass
            elif move[1] <= -2:
                  try:
                    next_moves.remove("down")
                  except:
                    pass
            else:
              pass
            
        move_1 = ""

        right1,left1,up1,down1 = 0,0,0,0

        if bad_paths is not None:
          for path in bad_paths:
              if path[0] == "right":
                right1 = 1 + right1
              elif path[0] == "left":
                left1 = 1 + left1
              elif path[0] == "down":
                down1 = 1 + down1
              elif path[0] == "up":
                up1 = 1 + up1
          
        if right1 <= left1 and right1 <= up1 and right1 <= down1:
            move_1 = "right"
        elif left1 <= right1 and left1 <= up1 and left1 <= down1:
            move_1 = "left"
        elif up1 <= right1 and up1 <= left1 and up1 <= down1:
            move_1 = "up"
        elif down1 <= right1 and down1 <= left1 and down1 <= up1:
            move_1 = "down"

        

        best_move = move_1
        
        move_right = True
        move_left = True
        move_up = True
        move_down = True

        if len(next_moves) == 0:
          for block in body_blocking:
            if block["x"] != head_x + 1 and block["y"] == head_y and head_x + 1 <= max_x:
              #final_move = "right"
              pass
            elif block["x"] != head_x - 1 and block["y"] == head_y and head_x - 1 >=0:
              move_right = False
              #final_move = "left"
            elif block["x"] == head_x and block["y"] != head_y + 1 and head_y + 1 <=max_y:
              move_left = False
              #final_move = "up"
            elif block["x"] == head_x and block["y"] != head_y - 1 and head_y - 1 >=0:
              move_up = False
              #final_move = "down"
          
          if move_right:
            if head_x  == max_x:
              move_right = False
          elif move_left:
            if head_x  == 0:
              move_left = False
          elif move_up:
            if head_y == max_y:
              move_up = False
          elif move_down:
            if head_y == max_y:
              move_down = False
          
          if move_right:
            final_move="right"
          elif move_left:
            final_move = "left"
          elif move_up:
            final_move = "up"
          else:
            final_move = "down"
                
            
          
        elif best_move in next_moves:
          final_move = best_move
        else:
          final_move = random.choice(next_moves)

          
        #removes move if body of snake is there
        
        

          # for block in body_blocking:
          #   if block["x"]+1 == head_x and block["y"] == head_y:
          #     try:
          #       next_moves.remove("left")
          #     except:
          #       pass
          #   if block["x"]-1 == head_x and block["y"] == head_y:
          #     try:
          #       next_moves.remove("right")
          #     except:
          #       pass
          #   if block["x"] == head_x and block["y"]+1 == head_y:
          #     try:
          #       next_moves.remove("down")
          #     except:
          #       pass
          #   if block["x"] == head_x and block["y"]-1 == head_y:
          #     try:
          #       next_moves.remove("up")
          #     except:
          #       pass

        #moves_before_food = next_moves
            #move toward food
        # food_moves = [] 
        # best_move = ""
        # if health <= 10:
          
        #   close_food = foods[0]
        #   smallest_distance = 22

        #   for food in foods:
        #     distance = ((((head_x - food["x"] )**2) + ((head_y-food["y"])**2) )**0.5)
        #     if distance < smallest_distance:
        #       close_food = food
          
        #   food_x, food_y = close_food["x"], close_food["y"]

        #   if food_x > head_x and food_y == head_y:
        #     try:
        #       if "right" in next_moves:
        #         best_move = "right"   
        #     except:
        #       pass
        #   elif food_x < head_x and food_y == head_y:
        #     try:
        #       if "left" in next_moves:
        #         best_move = "left"
        #     except:
        #       pass
        #   elif food_y > head_y and food_x == head_x:
        #     try:
        #       if "up" in next_moves:
        #         best_move = "up"
        #     except:
        #       pass
        #   elif food_y < head_y and food_x == head_x:
        #     try:
        #       if "down" in next_moves:
        #         best_move = "down"
        #     except:
        #       pass
        #   elif food_x > head_x and food_y >= head_y:
        #     try:
        #       if "right" in next_moves:
        #         best_move = "right"
        #       elif "up" in next_moves:
        #         best_move = "up"
        #     except:
        #       pass
        #   elif food_x > head_x and food_y <= head_y:
        #     try:
        #       if "right" in next_moves:
        #         best_move = "right"
        #       elif "down" in next_moves:
        #         best_move = "down"
        #     except:
        #       pass
        #   elif food_x < head_x and food_y >= head_y:
        #     try:
        #       if "left" in next_moves:
        #         best_move = "left"
        #       elif "up" in next_moves:
        #         best_move = "up"
        #     except:
        #       pass
        #   elif food_x < head_x and food_y <= head_y:
        #     try:
        #       if "left" in next_moves:
        #         best_move = "left"
        #       elif "down" in next_moves:
        #         best_move = "down"
        #     except:
        #       pass
        # best_move = ""
        # if best_move == "":
        #   final_move = random.choice(next_moves)
        # else:
        #   final_move = best_move
        
        return {"move": final_move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
