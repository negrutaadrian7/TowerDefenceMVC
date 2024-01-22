from .data_game.enemy_data import ENEMY_SPAWN_DATA
import random

class ProcessEnemies:
    def __init__(self, _level_difficulty):
        self._level = _level_difficulty
        self._enemy_type_list = [] 
        self.process_enemies() 

    def process_enemies(self):
        print("Hello There")
        _enemies = ENEMY_SPAWN_DATA[self._level - 1] 
        for _enemy_type in _enemies: 
            _enemies_to_spawn = _enemies[_enemy_type] 
            for _enemy in range(_enemies_to_spawn):
                self._enemy_type_list.append(_enemy_type)
        random.shuffle(self._enemy_type_list)
    
    def set_level(self, _level):
        self._level = _level

    def next_level(self):
        self._enemy_type_list = []
        self._level += 1
        self.process_enemies() 
    

