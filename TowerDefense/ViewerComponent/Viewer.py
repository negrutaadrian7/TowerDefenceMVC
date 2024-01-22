import pygame as pg
from ModuleComponent.data_game import constants as c
from ModuleComponent.SingletonMeta import SingletonMeta
from .Observer import Observer

# SINGLETON

class Viewer(Observer):
    __metaclass__ = SingletonMeta
    
    def __init__(self, screen):
        self._game_state = None
        self.screen = screen
        self.map_image = pg.image.load("ViewerComponent/map.png").convert_alpha()
        
        self._game_lost = False
        self._game_win = False 

        self._enemy_images = { 
            "weak": pg.image.load('ViewerComponent/images/enemies/enemy_1.png').convert_alpha(),
            "medium": pg.image.load('ViewerComponent/images/enemies/enemy_2.png').convert_alpha(),
            "strong": pg.image.load('ViewerComponent/images/enemies/enemy_3.png').convert_alpha(),
            "elite": pg.image.load('ViewerComponent/images/enemies/enemy_4.png').convert_alpha()
        } 
        self._turret_sprites = [
            pg.image.load('ViewerComponent/images/turrets/turret_1.png').convert_alpha(),
            pg.image.load('ViewerComponent/images/turrets/turret_2.png').convert_alpha(),
            pg.image.load('ViewerComponent/images/turrets/turret_3.png').convert_alpha(),
            pg.image.load('ViewerComponent/images/turrets/turret_4.png').convert_alpha(),
        ]
        self.draw_range_of_turret = False
        self.display_damage = False

        self._is_placing_turret = False 
        self._turret_placement_pos = None 
        self._is_valid_placement = False 





    def update(self, message, game_state):
        self._game_state = game_state # each time it will receive a message, will update its state
        
        if message == "turret_selected":
            self.draw_range_of_turret = True
            self.display_damage = True 

        elif message == "cancel_clicked":
            self.draw_range_of_turret = False
            self.display_damage = False
        
        elif message == "game_lost":
            self._game_lost = True 
        
        elif message == "game_win":
            self._game_win = True 

        elif message == "restart_game":
            self._game_state = game_state
            self.draw_range_of_turret = False
            self.display_damage = False
            self._game_lost = False 
            self._game_win = False 
        
        elif message == "turret_placement_update":
            self._is_placing_turret = self._game_state['is_placing_turret']
            self._is_valid_placement = self._game_state['is_valid_placement']
            self._turret_placement_pos = self._game_state['turret_placement_pos']

            self.draw_turret_placement_range()

    
    def draw_turret_placement_range(self):
        print("drawing turret placement range CHECK")
        if self._is_placing_turret:
            print("IS PLACING TURRET")
            print(self._is_placing_turret)
            turret_pos = self._turret_placement_pos
            is_valid_placement = self._is_valid_placement
            print("IS VALID PLACEMEENTT ", is_valid_placement)
            color = (0, 255, 0) if is_valid_placement else (255, 0, 0)
            range_radius = 50  
            print("TURRET POS")
            print(turret_pos)
            range_image = pg.Surface((range_radius * 2, range_radius * 2), pg.SRCALPHA)
            range_image.fill((0, 0, 0, 0))
            pg.draw.circle(range_image, color, (range_radius, range_radius), range_radius)
            blit_position = (turret_pos[0] - range_radius, turret_pos[1] - range_radius)
            self.screen.blit(range_image, blit_position)
            pg.display.flip()


    def render(self, game_state): 
        self.screen.fill((204, 200, 122))
        self.screen.blit(self.map_image, (0, 0))  
        self.render_enemies(game_state['enemies'])
        self.render_turrets(game_state['turrets'])
        
        if self.draw_range_of_turret:
            self.draw_turret_range()
        
        self.render_buttons(game_state['buttons'])
        self.render_game_info(game_state['generalInfo'])
        
        if self._game_win: 
            self.render_game_winner()
        if self._game_lost:
            self.render_game_loser() 

        pg.display.flip()

    def render_enemies(self, enemies):
        for enemy_info in enemies:
            _type = enemy_info['type']
            _image = self._enemy_images.get(_type) 
            
            _angle = enemy_info['angle']
            _pos = enemy_info['position']
            _image = pg.transform.rotate(_image, _angle)
            _rect = _image.get_rect() 
            _rect.center = _pos
            self.screen.blit(_image, _rect)
    
    def render_turrets(self, turrets):
        for turret_info in turrets:
            
            turret_level = turret_info['turret_level']
            animation_list = self.load_images(self._turret_sprites[turret_level - 1])
            

            turret_frame_index = turret_info['frame']
            original_image = animation_list[turret_frame_index]

            turret_angle = turret_info['turret_angle']
            image = pg.transform.rotate(original_image, turret_angle - 90)
            rect = image.get_rect() 

            turret_pos = turret_info['position']
            rect.center = turret_pos

            self.screen.blit(image, rect)


    def draw_turret_range(self):
        _selected_turret = self._game_state['selected_turret']
        _selected_turret_info = _selected_turret.get_info() 
        _selected_turret_range = _selected_turret_info['range']
        _selected_turret_position = _selected_turret_info['position']
        

        if (_selected_turret != None):
            range_image = pg.Surface((_selected_turret_range * 2, _selected_turret_range * 2), pg.SRCALPHA)
            range_image.fill((0, 0, 0, 0))
            pg.draw.circle(range_image, (0, 255, 0, 100), (_selected_turret_range, _selected_turret_range), _selected_turret_range)
            blit_position = (_selected_turret_position[0] - _selected_turret_range, _selected_turret_position[1] - _selected_turret_range)
            self.screen.blit(range_image, blit_position)

    def load_images(self, sprite_sheet):
        #extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def render_buttons(self, buttons):
        for button in buttons: 
            _image = button['image']
            _rect = button['rect']
            _visibility = button['visible']
            if (_visibility):
                self.screen.blit(_image, _rect)
            
    def render_game_info(self, game_state):
        
        _health = game_state['health']
        font1 = pg.font.SysFont('Calibri', 24, bold=True)
        # HEALTH
        text = "Health : {}".format(_health)
        text_surface = font1.render(str(text), True, (122, 120, 83))
        _x = c.SCREEN_WIDTH + 150
        _y = 15
        text_rect = text_surface.get_rect() 
        text_rect.center = (_x, _y) 
        
        # MONEY 
        _money = game_state['money']
        font2 = pg.font.SysFont('Calibri', 24, bold=True)
        text2 = "Money : {}".format(_money)
        text_surface2 = font2.render(str(text2), True, (122, 120, 83))
        _x2 = c.SCREEN_WIDTH + 150
        _y2 = 35
        text_rect2 = text_surface2.get_rect() 
        text_rect2.center = (_x2, _y2) 
        
        # ENEMIES 
        _spawned_enemies = game_state['spawned_enemies']
        font3 = pg.font.SysFont('Calibri', 24, bold=True)
        text3 = "Spawned Enemies : {}".format(_spawned_enemies)
        text_surface3 = font3.render(str(text3), True, (122, 120, 83))
        _x3 = c.SCREEN_WIDTH + 150
        _y3 = 55
        text_rect3 = text_surface3.get_rect() 
        text_rect3.center = (_x3, _y3) 
        
        
        # KILLED ENEMIES
        _killed_enemies = game_state['killed_enemies']
        font4 = pg.font.SysFont('Calibri', 24, bold=True)
        text4 = "Killed enemies : {}".format(_killed_enemies)
        text_surface4 = font4.render(str(text4), True, (122, 120, 83))
        _x4 = c.SCREEN_WIDTH + 150
        _y4 = 80
        text_rect4 = text_surface4.get_rect() 
        text_rect4.center = (_x4, _y4) 
        
        # MISSED ENEMIES
        _missed_enemies = game_state['missed_enemies']
        font5 = pg.font.SysFont('Calibri', 24, bold=True)
        text5 = "Missed enemies : {}".format(_missed_enemies)
        text_surface5 = font5.render(str(text5), True, (122, 120, 83))
        _x5 = c.SCREEN_WIDTH + 150
        _y5 = 105
        text_rect5 = text_surface5.get_rect() 
        text_rect5.center = (_x5, _y5) 
        
        if self.display_damage == True :
            _selected = self._game_state["selected_turret"]
            _turret_info = _selected.get_info() 
            _damage = _turret_info['damage']
            font6 = pg.font.SysFont('Calibri', 24, bold=True)
            text6 = "Turret damage : {}".format(_damage)
            text_surface6 = font6.render(str(text6), True, (122, 120, 83))
            _x6 = c.SCREEN_WIDTH + 150
            _y6 = 705
            text_rect6 = text_surface6.get_rect() 
            text_rect6.center = (_x6, _y6) 
            self.screen.blit(text_surface6, text_rect6)


        
        self.screen.blit(text_surface, text_rect)        
        self.screen.blit(text_surface2, text_rect2) 
        self.screen.blit(text_surface3, text_rect3) 
        self.screen.blit(text_surface4, text_rect4) 
        self.screen.blit(text_surface5, text_rect5) 

    def render_game_winner(self):
        self.draw_text("You are the WINNER !", pg.font.SysFont("Consolas", 36), "red", 200, 230)
        # self.screen.blit(self._congrats_image, (200, 300))
    
    def render_game_loser(self):
        self.draw_text("Game OVER !", pg.font.SysFont("Consolas", 36), "red", 200, 230)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
