import os
from .data_game.turret_data import TURRET_DATA
from .data_game import constants as c
import pygame as pg 
import math 


class Turret (pg.sprite.Sprite): 

    def __init__(self, _tile_x, _tile_y, _enemy_group): # enemy_position, all the enemy objects 
        pg.sprite.Sprite.__init__(self)
        
        self._turret_level = 1 # upgrade system for the level of the turret 
        self._range = TURRET_DATA[self._turret_level - 1].get("range")
        self._cooldown = TURRET_DATA[self._turret_level - 1].get("cooldown")
        
        self._last_shoot = pg.time.get_ticks() # last shoot of a turret, in order to verify if the turret can shoot or not 
        self._selected = False # DISPLAY THE CIRCLE OF THE RANGE FOR THE TURRET
        self._target = None 

        self._tile_x = _tile_x
        self._tile_y = _tile_y

        self._x = (self._tile_x + 0.5) * c.TILE_SIZE
        self._y = (self._tile_y + 0.5) * c.TILE_SIZE

        self._frame_index = 0
        self._update_time = pg.time.get_ticks()

        self._angle = 90
        
        self._position = (self._x, self._y) # calculate the center of the point on a grid 
        self._enemy_group = _enemy_group
    

        ## MUSIC FOR SHOOTING
        current_dir = os.path.dirname(__file__)
        sound_path = os.path.join(current_dir, 'shooting.wav')
        self._shoot_sound = pg.mixer.Sound(sound_path)
        
        self._damage = None 
        self._damage = self.get_damage_rate(1) 
    
    def get_damage_rate(self, _turret_level):
        _damage = 0
        if _turret_level == 1:
            _damage = c.DAMAGE_TURRET_1
        elif _turret_level == 2:
            _damage = c.DAMAGE_TURRET_2
        elif _turret_level == 3:
            _damage = c.DAMAGE_TURRET_3
        elif _turret_level == 4:
            _damage = c.DAMAGE_TURRET_4  
        print(_damage) 
        return _damage
    
    def upgrade(self):

        if self._turret_level < len(TURRET_DATA):
            self._turret_level += 1
            self._range = TURRET_DATA[self._turret_level - 1]["range"]
            self._cooldown = TURRET_DATA[self._turret_level - 1]["cooldown"]
            self._damage = self.get_damage_rate(self._turret_level) 

    def pick_target (self, enemy_group): 
        x_dist = 0 
        y_dist = 0
        for enemy in enemy_group: 
            if enemy._health > 0:
                x_dist = enemy._actual_pos[0] - self._x
                y_dist = enemy._actual_pos[1] - self._y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self._range: 
                    self._target = enemy
                    self._angle = math.degrees(math.atan2(-y_dist, x_dist))

                    print("HERE IS DAMAGE")
                    print(self._damage)
                    self._target._health -= self._damage
                    break

    def play_animation(self):
        if pg.time.get_ticks() - self._update_time > c.ANIMATION_DELAY:
            self._update_time = pg.time.get_ticks()
            self._frame_index += 1
            if self._frame_index >= c.ANIMATION_STEPS:
                self._frame_index = 0
                self._last_shoot = pg.time.get_ticks()
                
                self._shoot_sound.play() 
                self._target = None
                # self._shoot_sound.play()     

    def update(self):
        if self._target:
            self.play_animation()

        else: 
            if pg.time.get_ticks() - self._last_shoot > self._cooldown:
                self.pick_target(self._enemy_group) 

    ########################################################################
    #                         INFO TO REND                                 #
    ########################################################################


    def get_info(self):
        
        return {
            "frame" : self._frame_index,
            "turret_level": self._turret_level,
            "turret_angle": self._angle,
            "position": self._position,
            "range": self._range,
            "target": self._target.get_info() if self._target else None,
            "selected": self._selected,
            "update_time" : self._update_time,
            "damage" : self._damage
        }