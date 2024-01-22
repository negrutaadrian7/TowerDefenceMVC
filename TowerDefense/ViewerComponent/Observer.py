from abc import ABC, abstractmethod

class Observer(ABC): # Will be the Viewer in our case
    @abstractmethod
    def update(self, message, game_state):
        pass