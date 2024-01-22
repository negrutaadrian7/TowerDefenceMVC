from .Enemy import Enemy


class EnemyElite(Enemy):
    def __init__(self, _waypoints):
        super().__init__("elite", _waypoints)  

    