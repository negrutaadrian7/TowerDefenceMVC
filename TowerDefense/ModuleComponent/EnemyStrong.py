from .Enemy import Enemy


class EnemyStrong(Enemy):
    def __init__(self, _waypoints):
        super().__init__("strong", _waypoints)  

    