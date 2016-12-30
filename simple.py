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

    def __init__(self, x=320, y=240, is_trippy=False):
        super(InputLayer, self).__init__(46, 204, 113, 1000)


        self.sprite = Sprite('assets/85857.png')
        self.sprite.position = x, y
        self.sprite.opacity = 0
        self.add(self.sprite)
        self.sprite.do(FadeIn(2))

        self.enemy = Sprite('assets/enemy.png')
        self.enemy.position = x, y
        self.enemy.opacity = 0
        self.add(self.enemy)
        self.enemy.do(FadeIn(2))

        self.schedule_interval(self.movement, 0.05)
        self.schedule_interval(self.enemy_attack, 3)
        self.left_move = False
        self.right_move = False
        self.up_move = False


    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "LEFT":
            self.left_move = True

        elif symbol_string(key) == "RIGHT":
            self.right_move = True

        elif symbol_string(key) == "SPACE":
            self.up_move = True

    
    def movement(self, dt):

        """ move sprite in the appropriate direction as long as left/right key is held"""

        move_left = MoveBy((-20, 0), .1)
        move_up = MoveBy((0, 15), .1) + MoveBy((0, -15), .1)

        if self.left_move == True:
            self.sprite.do(move_left)

        elif self.right_move == True:
            self.sprite.do(Reverse(move_left)) 

        elif self.up_move == True:
            self.sprite.do(move_up) 


    def on_key_release(self, key, modifiers):

        self.left_move = False
        self.right_move = False
        self.up_move = False
        default_y = MoveBy((0, -(self.sprite.position[1] - 240)), 0.5)
        self.sprite.do(default_y)

    def enemy_attack(self, dt):
        distanceFromDino_x = self.sprite.position[0] - self.enemy.position[0]
        move_toward_dino = MoveBy((distanceFromDino_x, 0), 5)
        self.enemy.do(move_toward_dino)


director.init()
director.run(scene.Scene(InputLayer()))
