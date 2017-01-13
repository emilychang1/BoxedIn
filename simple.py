import cocos
from cocos import scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.scenes import *
from cocos.sprite import Sprite
from cocos.actions import *
from pyglet.window.key import symbol_string

import time

class InputLayer(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(InputLayer, self).__init__(248, 248, 255, 1000)

        self.sprite = Sprite('assets/happy.png')
        self.sprite.scale = 0.08
        self.sprite.position = 320, 240
        self.sprite.speed = 125
        self.sprite.opacity = 0
        self.add(self.sprite, z = 3)
        self.sprite.do(FadeIn(2))

        self.enemy = Sprite('assets/ball.png')
        self.enemy.scale = 0.08
        self.enemy.position = 220, 240
        self.enemy.speed = 125
        self.enemy.opacity = 0
        self.add(self.enemy, z = 2)
        self.enemy.do(FadeIn(2))

        self.enemy_locations = []
        self.message = [0]

        self.score = 0
        

        self.schedule_interval(self.movement, 0.05)
        self.schedule_interval(self.enemy_attack, 0.5)
        self.schedule_interval(self.add_mini, 2)
        self.schedule_interval(self.scoreboard, 0.001)
        self.left_move = False
        self.right_move = False
        self.up_move = False
        self.down_move = False 
        self.game_over = False






    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "LEFT":
            self.left_move = True

        elif symbol_string(key) == "RIGHT":
            self.right_move = True

        elif symbol_string(key) == "UP":
            self.up_move = True

        elif symbol_string(key) == "DOWN":
            self.down_move = True   


    def myround(self, x, base = 30):
        return int(base * round(float(x)/base))

    def add_mini(self, dt):
        mini_position = self.enemy.position
        self.mini = cocos.sprite.Sprite('assets/ball.png')
        self.mini.position = mini_position
        self.mini.scale = 0.03
        self.add(self.mini, z = 1)
        mini_position = self.myround(mini_position[0]), self.myround(mini_position[1])
        self.enemy_locations.append(mini_position)
        

    

    def movement(self, dt):

        """ move sprite in the appropriate direction as long as left/right key is held"""

        move_left = MoveBy((-20, 0), .1)
        move_up = MoveBy((0, 20), .1)

        if self.left_move == True and self.sprite.position[0] > 50:
            self.sprite.do(move_left)

        elif self.right_move == True and self.sprite.position[0] < 590:
            self.sprite.do(Reverse(move_left)) 

        elif self.up_move == True and self.sprite.position[1] < 430:
            self.sprite.do(move_up) 

        elif self.down_move == True and self.sprite.position[1] > 50:
            self.sprite.do(Reverse(move_up))


        distanceFromDino = ((self.sprite.position[0] - self.enemy.position[0]) ** 2 + 
                    (self.sprite.position[1] - self.enemy.position[1]) ** 2) ** 0.5
        fall = RotateBy(90, 2)

        rounded_sprite_position = self.myround(self.sprite.position[0]), self.myround(self.sprite.position[1])
        if (distanceFromDino <= 80 or rounded_sprite_position in self.enemy_locations):
            self.sprite.do(fall | MoveBy((0, -300), 3))
            msg1 = "GAME OVER"
            msg2 = "SCORE: " + str(self.score)
            self.msg1 = cocos.text.Label(msg1,
                                font_size=25,
                                font_name='Verdana',
                                anchor_y='center',
                                anchor_x='center',
                                color = (0,0,0,1000))
            self.msg2 = cocos.text.Label(msg2,
                                font_size=25,
                                font_name='Verdana',
                                anchor_y='center',
                                anchor_x='center',
                                color = (0,0,0,1000))

            self.msg1.position = 250, 250
            self.msg2.position = 250, 200

            self.add(self.msg1, z = 4)
            self.add(self.msg2, z = 5)
            self.game_over = True


            


    def on_key_release(self, key, modifiers):

        self.left_move = False
        self.right_move = False
        self.up_move = False
        self.down_move = False 
        #default_y = MoveBy((0, -(self.sprite.position[1] - 240)), 0.5)
        #self.sprite.do(default_y)

    def enemy_attack(self, dt):
        if(self.game_over == False):
            distanceFromDino_x = self.sprite.position[0] - self.enemy.position[0]
            distanceFromDino_y = self.sprite.position[1] - self.enemy.position[1]
            
            move_toward_dino = MoveBy((distanceFromDino_x, distanceFromDino_y), 3)
            self.enemy.do(move_toward_dino)

    def scoreboard(self, dt):
        if (self.game_over == False):
            self.score += 1
            
            msg = "Score: " + str(self.score)
            self.msg = cocos.text.Label(msg,
                                    font_size=15,
                                    font_name='Verdana',
                                    anchor_y='center',
                                    anchor_x='center',
                                    color = (0,0,0,1000))
            self.msg.position = 520, 450

            self.message.append(self.msg)

            self.add(self.message[1])
            if(self.message[0]):
                self.remove(self.message[0])
            del self.message[0]

if __name__ == '__main__':
    cocos.director.director.init(caption= 'Boxed In')
    
    director.run(scene.Scene(InputLayer()))
    
director.init()   




