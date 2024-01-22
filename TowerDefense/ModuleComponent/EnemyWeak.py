from .Enemy import Enemy


class EnemyWeak(Enemy):
    def __init__(self, _waypoints):
        super().__init__("weak", _waypoints)  

