from .EnemyWeak import EnemyWeak
from .EnemyMedium import EnemyMedium
from .EnemyStrong import EnemyStrong
from .EnemyElite import EnemyElite

class EnemyFactory:

    @staticmethod
    def create_enemy(enemy_type, _waypoints):
        if enemy_type == "weak":
            return EnemyWeak(_waypoints)
        elif enemy_type == "medium":
            return EnemyMedium(_waypoints) 
        
        elif enemy_type == "strong":
            return EnemyStrong(_waypoints) 
        
        elif enemy_type == "elite":
            return EnemyElite(_waypoints) 

