import pygame as pg 
from .data_game.enemy_data import ENEMY_DATA
import math
from pygame.math import Vector2
from abc import ABC, abstractmethod

class Enemy(pg.sprite.Sprite): 
    def __init__(self, _enemy_type, _waypoints):
        pg.sprite.Sprite.__init__(self) 
        ABC().__init__()

        self._enemy_type = _enemy_type
        self._waypoints = _waypoints 
        self._actual_pos = Vector2(self._waypoints[0]) 
        self._next_point = 1 
        self._health = ENEMY_DATA.get(self._enemy_type)["health"] 
        self._speed = ENEMY_DATA.get(self._enemy_type)["speed"]
        
        self._enemy_reached_end = False 
        self._enemy_killed = False

        self._angle = 0 

    
    ##################################################################
    #                       POOL OF OBJECTS                          #
    ##################################################################   

    def reset_enemy(self):
        self._actual_pos = Vector2(self._waypoints[0])
        self._next_point = 1
        self._health = ENEMY_DATA.get(self._enemy_type)["health"] 
        self._speed = ENEMY_DATA.get(self._enemy_type)["speed"]
        self._enemy_reached_end = False 
        self._enemy_killed = False
        self._angle = 0 


    def update(self):
        self.move() 
        self.rotate() 
        self.check_enemy_alive() 


    def get_enemy_reached_end(self):
        return self._enemy_reached_end 

    def get_enemy_killed(self):
        return self._enemy_killed
    
    def move(self):
        if self._next_point < len(self._waypoints):
            self.target = Vector2(self._waypoints[self._next_point])
            self.movement = self.target - self._actual_pos
        else:
            self._enemy_reached_end = True
            self.kill()

        dist = self.movement.length()

        if dist >= self._speed:
            self._actual_pos += self.movement.normalize() * self._speed
        else:
            if dist != 0:
                self._actual_pos += self.movement.normalize() * dist 
            self._next_point += 1
        
    def rotate(self):
        if self._next_point < len(self._waypoints):
            target_waypoint = Vector2(self._waypoints[self._next_point])
            dist = target_waypoint - self._actual_pos
            self._angle = math.degrees(math.atan2(-dist[1], dist[0]))  # Calculate the angle for rotation

    def check_enemy_alive(self):
        if self._health <= 0:
            self._enemy_killed = True 
            self.kill() 
    
    ################################################################
        #           RENDER INFORMATION ABOUT ENEMY         #
    ################################################################

    def get_info(self):
       
        return {
            "type": self._enemy_type,
            "angle" : self._angle,
            "position": self._actual_pos,
            "health": self._health,
            "reached_end": self._enemy_reached_end,
        }