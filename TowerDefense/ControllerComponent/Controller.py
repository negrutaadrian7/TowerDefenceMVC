import pygame as pg
from ModuleComponent.SingletonMeta import SingletonMeta
from ModuleComponent.data_game import constants as c

# SINGLETON

class Controller(metaclass = SingletonMeta):
    
    def __init__(self, model):
        self.model = model 
        self._is_placing_turret = False 
        
        self._selected_turret = None
        self._upgrade_turret = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.model.handle_quit_game()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            
            elif event.type == pg.MOUSEMOTION: # hover 
                if self._is_placing_turret:
                    self.model.update_turret_placement_position(event.pos)
    
    def handle_mouse_click(self, mouse_pos):
        
        if self.is_click_on_ui(mouse_pos):
            print("UI Click")
            self.handle_ui_interaction(mouse_pos)

        elif self._is_placing_turret:
            if self.model.is_within_playable_area(mouse_pos):
                self.model.create_turret(mouse_pos) 
                self._is_placing_turret = False 
            

        # SELECT A TURRET BY CLICKING ON IT
        elif self.model.get_turret_at_mouse_position(mouse_pos) != None:
            self._selected_turret = self.model.get_turret_at_mouse_position(mouse_pos) # update the selected turret in controller
            self.model._selected_turret = self._selected_turret # update the selected turret in the model
            self.model.update_selected_turret()
            self._upgrade_turret = True # The button is displayed 
        
        elif self.is_click_on_ui(mouse_pos):
            print("UI Click")
            self.handle_ui_interaction(mouse_pos)

        else:
            self.handle_neutral_zone_click()
    
    # WHEN THE USER WILL CLICK THE UPGRADE THEN WE APPLY THE MODEL UPGRADE METHOD ON TURRET.
    def is_click_on_ui(self, mouse_pos):
        for button in self.model.get_buttons_list():
            if button._rect.collidepoint(mouse_pos):
                return True 
        return False 

    def handle_ui_interaction(self, mouse_pos):
        for button in self.model.get_buttons_list():
            if button._rect.collidepoint(mouse_pos):
                if button._id == "buy_turret":
                    print("Hello from buy flow")
                    self._is_placing_turret = True 
                    self.model.handle_turret_button_click() 
                
                if button._id == "cancel":
                    print("Hello from cancel flow")
                    self.model.handle_cancel_button_click() 

                if button._id == "upgrade_turret" and self._selected_turret != None and self._upgrade_turret:
                    self.model.upgrade_turret(self._selected_turret) # we pass the turret for updating
                    self._selected_turret = None
                
                if button._id == "begin": 
                    print("begin button clicked...")
                    self.model.start_next_level() 

                if button._id == "restart":
                    print("restart the game ")
                    self.model.handle_restart_button_click() 

    # ZONE NOT HANDLED, JUST THROW THE TURRET CLICKED
    def handle_neutral_zone_click(self):
        self._selected_turret = None 
        self._upgrade_turret = False
        self.model.handle_cancel_button_click()
