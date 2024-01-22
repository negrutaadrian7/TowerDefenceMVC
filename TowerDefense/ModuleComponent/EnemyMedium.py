from .Enemy import Enemy


class EnemyMedium(Enemy):
    def __init__(self, _waypoints):
        super().__init__("medium", _waypoints)  

    