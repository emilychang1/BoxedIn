import cocos
import pyglet
from pyglet.gl import *
from cocos import scene
from cocos.layer import *
from cocos.director import director
from cocos.scenes import *
from cocos.sprite import Sprite
from cocos.actions import *
from cocos.menu import *
from cocos.scene import *
from pyglet.window.key import symbol_string

import time

class InputLayer(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(InputLayer, self).__init__(248, 248, 255, 1000)


        #add player
        self.sprite = Sprite('assets/happy.png')
        self.sprite.scale = 0.08
        self.sprite.position = 420, 240
        self.sprite.speed = 125
        self.sprite.opacity = 0
        self.add(self.sprite, z = 3)
        self.sprite.do(FadeIn(2))

        #add opponent
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
        self.game_over_sprite = cocos.sprite.Sprite('assets/nothappy.png')
        
        self.schedule_interval(self.movement, 0.001)
        self.schedule_interval(self.enemy_attack, 0.5)
        self.schedule_interval(self.add_mini, 2)
        self.schedule_interval(self.scoreboard, 0.001)
        self.left_move = False
        self.right_move = False
        self.up_move = False
        self.down_move = False 
        self.game_over = False


    """sets direction_move boolean variable to true as long as key is held"""
    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "LEFT":
            self.left_move = True

        elif symbol_string(key) == "RIGHT":
            self.right_move = True

        elif symbol_string(key) == "UP":
            self.up_move = True

        elif symbol_string(key) == "DOWN":
            self.down_move = True   

    """returns the distance from the player, given an x,y position"""
    def distance_from_sprite(self, pos):
        return ((self.sprite.position[0] - pos[0]) ** 2 + 
                    (self.sprite.position[1] - pos[1]) ** 2) ** 0.5

    """returns the blockade that is closest to the player"""
    def find_closest_sprite(self):
        smallest_distance = 500
        smallest_pos = (0, 0)
        for i in self.enemy_locations:
            i_dist_from_sprite = self.distance_from_sprite(i)
            if (i_dist_from_sprite < smallest_distance):
                smallest_distance = i_dist_from_sprite
                smallest_pos = i

        return smallest_pos


    """adds blockade dropped by the enemy sprite"""
    def add_mini(self, dt):
        self.mini = cocos.sprite.Sprite('assets/ball.png')
        self.mini.position = self.enemy.position
        self.mini.scale = 0.03
        self.add(self.mini, z = 1)

        self.enemy_locations.append(self.mini.position)
   


    """ move sprite in the appropriate direction as long as left/right key is held. 
    display game over message when player loses"""
    def movement(self, dt):

        move_left = MoveBy((-10, 0), .05)
        move_up = MoveBy((0, 10), .05)

        if self.left_move == True and self.sprite.position[0] > 45:
            self.sprite.do(move_left)

        elif self.right_move == True and self.sprite.position[0] < 600:
            self.sprite.do(Reverse(move_left)) 

        elif self.up_move == True and self.sprite.position[1] < 435:
            self.sprite.do(move_up) 

        elif self.down_move == True and self.sprite.position[1] > 45:
            self.sprite.do(Reverse(move_up))


        distanceFromDino = self.distance_from_sprite(self.enemy.position)
        fall = RotateBy(90, 2)

        closest_sprite = self.find_closest_sprite()

        if (self.game_over == False and (distanceFromDino <= 95 or self.distance_from_sprite(closest_sprite) < 60)):
            self.game_over_sprite.position = self.sprite.position
            self.game_over_sprite.scale = 0.7
            self.add(self.game_over_sprite, z = 3)
            self.remove(self.sprite)
            self.game_over_sprite.do(fall | MoveBy((0, -300), 3))
            msg1 = "GAME OVER"
            msg2 = "SCORE: " + str(self.score)
            self.msg1 = cocos.text.Label(msg1,
                                font_size=25,
                                font_name='Georgia',
                                anchor_y='center',
                                anchor_x='center',
                                color = (0,0,0,1000))
            self.msg2 = cocos.text.Label(msg2,
                                font_size=25,
                                font_name='Georgia',
                                anchor_y='center',
                                anchor_x='center',
                                color = (0,0,0,1000))

            self.msg1.position = 250, 250
            self.msg2.position = 250, 200

            self.add(self.msg1, z = 4)
            self.add(self.msg2, z = 5)
            self.game_over = True

    """sets boolean direction_move variable to false when key is no longer held"""
    def on_key_release(self, key, modifiers):
        if symbol_string(key) == "LEFT":
            self.left_move = False

        elif symbol_string(key) == "RIGHT":
            self.right_move = False

        elif symbol_string(key) == "UP":
            self.up_move = False

        elif symbol_string(key) == "DOWN":
            self.down_move = False   

    """moves enemy in the direction of player"""
    def enemy_attack(self, dt):
        if(self.game_over == False):
            distanceFromDino_x = self.sprite.position[0] - self.enemy.position[0]
            distanceFromDino_y = self.sprite.position[1] - self.enemy.position[1]
            
            move_toward_dino = MoveBy((distanceFromDino_x, distanceFromDino_y), 3)
            self.enemy.do(move_toward_dino)

    """increment scoreboard and display in top right corner"""
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



class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__("BOXED IN")
        pyglet.font.add_directory('.')

        self.font_title['font_name'] = 'Georgia'
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = 'Georgia'
        self.font_item['font_size'] = 35
        self.font_item_selected['font_name'] = 'Georgia'
        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []
        items.append(MenuItem('New Game', self.on_new_game))
        items.append(MenuItem('Quit', self.on_quit))

        self.create_menu(items)

    def on_new_game(self):
        director.run(scene.Scene(InputLayer()))


    def on_quit(self):
        director.pop()




if __name__ == '__main__':
    cocos.director.director.init(caption= 'Boxed In')
    menulayer = MultiplexLayer(MainMenu(), InputLayer())
    scenes = Scene(menulayer)
    director.run(scenes)
    
director.init() 