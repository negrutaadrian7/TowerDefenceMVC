import pygame as pg 
import sys, os

class Button:
    def __init__ (self, x, y, id, visibility):
        self._id = id
        self._x = x 
        self._y = y
        self._position = (self._x, self._y)
        self._visible = visibility


        _image_dir = sys.path[0] 
        _image_path = os.path.join(_image_dir, 'ViewerComponent/images/buttons/{}.png'.format(self._id))
        self._image = pg.image.load(_image_path).convert_alpha() 
        self._rect = self._image.get_rect() 
        self._rect.topleft = (self._x, self._y)
    
    def update_visibility(self, visibility):
        self._visible = visibility


    def is_clicked(self, mouse_pos):
        if self._rect.collidepoint(mouse_pos):
            print(f"Button {self._id} clicked!") 
            return True 
        return False 

    def get_button_info(self):
        return {
            "image" : self._image, 
            "rect" : self._rect,
            "id": self._id,
            "visible" : self._visible
        }
    

        