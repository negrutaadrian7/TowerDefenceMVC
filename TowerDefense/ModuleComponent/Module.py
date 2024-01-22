from .data_game import constants as c 
from .ProcessMap import ProcessMap
from .ProcessEnemies import ProcessEnemies
from .Turret import Turret
from .Button import Button
from .Subject import Subject
from .SingletonMeta import SingletonMeta
from .PoolOfObjects import PoolOfObjects


import pygame as pg 

    #############################################
    #                 SINGLETON                 # 
    #############################################

class Model (Subject, metaclass = SingletonMeta):
    
    def __init__(self):
        
        super().__init__()  
         
        self._maximum_lvl = c.TOTAL_LEVELS
        self._running = True 

       
        self.enemies_path = ProcessMap()  
        self._map_data = self.enemies_path._map_data
        self._tile_map = self.enemies_path._tile_map 
        self._waypoints = self.enemies_path._waypoints
        self._pool_of_enemies = PoolOfObjects(self._waypoints)

        # ENEMIES PROCESSING
        
        self._level = 1 
        self.enemy_treatement = ProcessEnemies(self._level)
        self._enemy_list = self.enemy_treatement._enemy_type_list
        self._enemy_group = pg.sprite.Group() 
        self._last_enemy_spawn = pg.time.get_ticks() 
        self._spawned_enemies = 0

        # GAME PROCESS
        
        self._spawned_enemies = 0
        
        # PlAYER DETAILS: HEALTH AND MONEY
        self._health = c.HEALTH
        self._money = c.MONEY

        # TURRETS PROCESSING
        self._selected_turret = None 
        self._turret_group = pg.sprite.Group() 

        # NEXT LEVEL
        self._killed_enemies = 0 
        self._missed_enemies = 0

        # GAME INCOME
        self._wave_in_progress = True
        self._game_status = False 
        self._game_outcome = 0 
        self._level_passed = False
        self._game_paused = False

        # BUTTONS 
        # need to stock the position of the buttons in the model 
        self.turret_button = Button(c.SCREEN_WIDTH + 70, 120, "buy_turret", True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 100 , 180, "cancel", False)
        self.upgrade_button = Button(c.SCREEN_WIDTH + 50, 620, "upgrade_turret", False)
        self.begin_button = Button(c.SCREEN_WIDTH + 70, 300, "begin", False)
        self.restart_button = Button(c.SCREEN_WIDTH + 60, 350, "restart", False) # rematch
        
        self._buttons_list = []
        self.append_buttons() 

        self._placing_turret = False  
        self._turret_placement_pos = None 
        self._is_valid_placement = False

        self._upgrade_button = False 
        self._begin_button = False 
        self._restart_button = False 

        self._playable_area = (0, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        
    def update(self):
        # Update game logic
        self.update_game_status()
        self.spawn_enemies()
        self.update_enemies()
        self.update_turrets()
    

    def update_turret_placement_position(self, pos):
        self._turret_placement_pos = pos
        self._is_valid_placement = self.is_within_playable_area(pos) and self.is_space_free(pos)
        self.notify_observers("turret_placement_update", self.get_game_state())
        

    def is_space_free(self, pos):
        space_is_free = False
        if self._placing_turret:
            _mouse_tile_x = pos[0] // c.TILE_SIZE
            _mouse_tile_y = pos[1] // c.TILE_SIZE
            _mouse_tile_num = (_mouse_tile_y * c.COLS) + _mouse_tile_x 
            
            if (self._tile_map[_mouse_tile_num] == 7): 
                space_is_free = True 
                for turret in self._turret_group:
                    if (_mouse_tile_x, _mouse_tile_y) == (turret._tile_x, turret._tile_y):
                        space_is_free = False 
        
        else:
            space_is_free = False 
        return space_is_free 

    def update_turrets (self):
        for turret in self._turret_group:
            turret.update()

    def update_selected_turret (self):
        self.notify_observers("turret_selected", self.get_game_state())
        if self._selected_turret != None:
            self._selected_turret._selected = True
            self.cancel_button.update_visibility(True)
            self.upgrade_button.update_visibility(True)
    
    def clear_selection (self):
        for turret in self._turret_group: 
            turret._selected = False 

    def update_enemies(self):
        # Update each enemy
        if self._wave_in_progress:
            for enemy in self._enemy_group:
                enemy.update()
                if enemy.get_enemy_reached_end():
                    self._missed_enemies += 1
                    self.update_health(5, False)
                    self.retrieve_money(c.MISSED_ENEMY_COST)
                    self._pool_of_enemies.return_enemy(enemy) 
                    
                
                if enemy.get_enemy_killed():
                    self._killed_enemies += 1
                    self.reward_money_system(enemy._enemy_type) 
                    self.reward_health_system(enemy._enemy_type)
                    self._pool_of_enemies.return_enemy(enemy)
                
    def update_game_status(self):
        
        self.prepare_next_level() 
        self.game_finished()

    #################################################
    #               HANDLE BUTTONS                  #
    #################################################
           
    def is_placing_turret(self):
        return self._placing_turret
    
    def handle_turret_button_click(self):
        print("Turret button clicked, changing state...")  # Debug print
        self._placing_turret = True
        
    def handle_cancel_button_click(self):
        self.notify_observers("cancel_clicked", self.get_game_state())
        self.clear_selection()
        self._buttons_list[1].update_visibility(False)  
        self._buttons_list[2].update_visibility(False) 

    def handle_upgrade_button_click(self):
        self._upgrade_button = True
    
    def handle_restart_button_click(self):
        self._restart_button = True
        
    def append_buttons(self):
        self._buttons_list.append(self.turret_button)
        self._buttons_list.append(self.cancel_button)
        self._buttons_list.append(self.upgrade_button)
        self._buttons_list.append(self.begin_button)
        self._buttons_list.append(self.restart_button)
        print(self._buttons_list)

    def handle_quit_game(self):
        self._running = False 

    def upgrade_turret(self, turret):
        _turret_level = turret._turret_level
        _money_for_upgrade = self.get_upgrade_cost(_turret_level) 
        if (self._money >= _money_for_upgrade):
            turret.upgrade()
            self.retrieve_money(_money_for_upgrade)
        else:
            print("Sorry, can't update the turret for instance")

    def get_upgrade_cost(self, _level):
        if _level == 1:
            return c.UPGRADE_COST_1
        elif _level == 2:
            return c.UPGRADE_COST_2
        elif _level == 3:
            return c.UPGRADE_COST_3
        elif _level == 4:
            return c.UPGRADE_COST_4

    def restart_game(self):
        
        self._level = 1
        self.enemy_treatement.set_level(1)
        self.enemy_treatement._enemy_type_list = []
        self.enemy_treatement.process_enemies() 
        self._enemy_list = self.enemy_treatement._enemy_type_list
        self._enemy_group.empty() 
        self._turret_group.empty() 

        self._health = c.HEALTH
        self._money = c.MONEY
        self._killed_enemies = 0
        self._missed_enemies = 0
        self._spawned_enemies = 0

        self._wave_in_progress = True
        self._game_status = False 
        self._game_outcome = 0 
        self._level_passed = False
        self._game_paused = False
        self._restart_button = False
        self._selected_turret = None 

        self.cancel_button.update_visibility(False) 
        self.begin_button.update_visibility(False)
        self.restart_button.update_visibility(False)
        self.upgrade_button.update_visibility(False)
        
        self.notify_observers("restart_game", self.get_game_state())

    #################################################
    #               GET INFORMATIONS                #
    #################################################

    def get_health(self):
        return self._health

    def get_money(self):
        return self._money
    
    def get_level(self):
        return self._level
    
    def get_enemies_group(self):
        return self._enemy_group
    
    def get_turrets_group(self):
        return self._turret_group

    def get_buttons_list(self):
        return self._buttons_list

    #################################################
    #              GAME LOGIC                       #
    #################################################
    
    def start_next_level(self):
        print("Starting next level...")
        self._killed_enemies = 0 # may be saved
        self._missed_enemies = 0 # may be saved
        self._spawned_enemies = 0
        
        self._game_paused = False
        self._level_passed = False
        self._wave_in_progress = True 

        self._level += 1
        self.enemy_treatement._level = self._level 
        self.enemy_treatement._enemy_type_list = []
        self.enemy_treatement.process_enemies() 
        self._enemy_list = self.enemy_treatement._enemy_type_list
        
        self._enemy_group.empty() 
       
        self.begin_button.update_visibility(False)

    def wave_finished(self):
        if (self._killed_enemies + self._missed_enemies) == len(self._enemy_list):
            self._wave_in_progress = False 

    def prepare_next_level(self):
        self.wave_finished() 
    
        if (self._wave_in_progress):
            self._level_passed = False 
            self._game_paused = False 
        
        elif (self._wave_in_progress == False): 
            self._level_passed = True 
            self._game_paused = True 
            self.begin_button.update_visibility(True) 

    def game_finished(self):
        if (self._game_status == False and self._health <= 0): 
            self._game_status = True  
            self._game_outcome = -1  
            self.notify_observers("game_lost", self.get_game_state())
            self._game_paused = True 
            self._wave_in_progress = False
            self.restart_button.update_visibility(True)

        if (self._level == self._maximum_lvl and  self._wave_in_progress == False and self._health > 0):
            self._game_status = True  
            self._game_outcome = 1
            
            self.restart_button.update_visibility(True)
            self.begin_button.update_visibility(False)
            self.upgrade_button.update_visibility(False)
            self.cancel_button.update_visibility(False)
            self._selected_turret = None 
            
            self._game_paused = True 
            self._wave_in_progress = False 
            self.notify_observers("game_win", self.get_game_state())


        if (self._level == self._maximum_lvl and self._wave_in_progress == False and self._health <= 0):
            self._game_status = True  
            self._game_outcome = -1 
            
            self.restart_button.update_visibility(True)
            self.begin_button.update_visibility(False) 
            self.upgrade_button.update_visibility(False)
            self.cancel_button.update_visibility(False)
            self._selected_turret = None 
            
            self._game_paused = True
            self._wave_in_progress = False 
            self.notify_observers("game_lost", self.get_game_state())

        if (self._restart_button == True):
            self.restart_game() 

    def reward_money_system(self, enemy_type):
        if enemy_type == 'weak':
            self.add_money(c.KILL_REWARD_WEAK)
        elif enemy_type == "medium":
            self.add_money(c.KILL_REWARD_MED)
        elif enemy_type == "strong":
            self.add_money(c.KILL_REWARD_STR)
        elif enemy_type == "elite":
            self.add_money(c.KILL_REWARD_ELI)
            
    def reward_health_system(self, enemy_type):
        if enemy_type == 'weak':
            self.update_health(c.KIlL_HEALTH_REWARD_WEAK, True)
        elif enemy_type == "medium":
            self.update_health(c.KIlL_HEALTH_REWARD_MEDIUM, True)
        elif enemy_type == "strong":
            self.update_health(c.KIlL_HEALTH_REWARD_STRONG, True)
        elif enemy_type == "elite":
            self.update_health(c.KIlL_HEALTH_REWARD_ELITE, True)

    ##########################################################
    #                   ENEMIES                              #
    #                      +                                 #
    #                POOL OF OBJECTS                         #
    ##########################################################

    def spawn_enemies(self):
        if self._wave_in_progress:
            if pg.time.get_ticks() - self._last_enemy_spawn > c.SPAWN_COOLDOWN:
                if self._spawned_enemies < len(self._enemy_list):   
                    _enemy_type = self._enemy_list[self._spawned_enemies]
                    _enemy = self._pool_of_enemies.get_enemy(_enemy_type)
                    self._enemy_group.add(_enemy)
                    self._spawned_enemies += 1
                    self._last_enemy_spawn = pg.time.get_ticks()
                    self.notify_observers("enemy_spawned", self.get_game_state())

    ##########################################################
    #                   TURRETS                              # 
    ##########################################################

    def is_within_playable_area(self, pos):
        x, y = pos  
        return x <= c.SCREEN_WIDTH and y <= c.SCREEN_HEIGHT
    
    def create_turret(self, _mouse_pos): 
        print("create turret called")

        space_is_free = False
        if self._placing_turret:
            _mouse_tile_x = _mouse_pos[0] // c.TILE_SIZE
            _mouse_tile_y = _mouse_pos[1] // c.TILE_SIZE
            _mouse_tile_num = (_mouse_tile_y * c.COLS) + _mouse_tile_x 
            
            if (self._tile_map[_mouse_tile_num] == 7): 
                space_is_free = True 
                for turret in self._turret_group:
                    if (_mouse_tile_x, _mouse_tile_y) == (turret._tile_x, turret._tile_y):
                        space_is_free = False 
                
                if (space_is_free == True and self._money > c.BUY_COST):
                    self.retrieve_money(c.BUY_COST)
                    _new_turret = Turret(_mouse_tile_x, _mouse_tile_y, self._enemy_group) 
                    self._turret_group.add(_new_turret)
                        
        else:
            print("Chose in the game area to place a turret, select one more time the button and execute the same process correctly")
            space_is_free = False 
            self._placing_turret = False
        return space_is_free          

    def get_turret_at_mouse_position(self, mouse_pos): 
        _mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        _mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

        for turret in self._turret_group:
            if (_mouse_tile_x, _mouse_tile_y) == (turret._tile_x, turret._tile_y):
                print("HELLO THERE")
                return turret

    ##########################################################
    #                    PLAYER                              # 
    ##########################################################

    def update_health(self, _amount_of_health, _positive):
            if _positive:
                self._health = max(self._health + _amount_of_health, 0) 
            else:
                self._health = max(self._health - _amount_of_health, 0)

    def retrieve_money (self, _cost): 
        self._money = max(self._money - _cost, 0)
    
    def add_money (self, _cost):
        self._money += _cost 
    
    ###########################################################################
    #                    ELEMENTS FOR THE VIEWER                              # 
    ###########################################################################

    def get_game_state(self):
        return {
            'generalInfo': {
                "level": self._level, # level of the player at the moment 
                "health": self._health, # health of the player
                "money": self._money, # amount of money
                "spawned_enemies" : self._spawned_enemies, 
                "killed_enemies" : self._killed_enemies,
                "missed_enemies" : self._missed_enemies
            },
            "enemies": [enemy.get_info() for enemy in self._enemy_group] if self._wave_in_progress else [], # for each enemy return his list of necessary elements 
            "turrets": [turret.get_info() for turret in self._turret_group], # the same for turrets 
            "buttons": [button.get_button_info() for button in self._buttons_list], # a list of dictionaries containing information about the buttons
            "game_outcome": self._game_outcome, # who is the winner
            "running": self._running,
            "level_passed": self._level_passed,
            "selected_turret": self._selected_turret, # need to be handled
            "game_paused" : self._game_paused,
            
            "is_placing_turret" : self.is_placing_turret,
            "turret_placement_pos" : self._turret_placement_pos,
            "is_valid_placement": self._is_valid_placement,

        }
