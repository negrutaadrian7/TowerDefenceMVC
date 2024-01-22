import pygame as pg
from ModuleComponent.Module import Model
from ControllerComponent.Controller import Controller
from ViewerComponent.Viewer import Viewer
import pygame as pg
import ModuleComponent.data_game.constants as c

pg.init()
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT)) 
pg.display.set_caption("Tower Defense")

model = Model()   
controller = Controller(model)

view = Viewer(screen) 
model.register_observer(view)


clock = pg.time.Clock()
FPS = 60  
running = True
game_paused = False

while running:
    clock.tick(FPS)
    controller.handle_events()  
    model.update()  
    game_state = model.get_game_state()  
    view.render(game_state)  
    running = game_state['running']  
    game_paused = game_state['game_paused']  

pg.quit()  
