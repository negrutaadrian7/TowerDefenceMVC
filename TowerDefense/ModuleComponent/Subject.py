# Will be the model that needs to notify about changes

class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message, game_state):
        for observer in self._observers:
            observer.update(message, game_state)
