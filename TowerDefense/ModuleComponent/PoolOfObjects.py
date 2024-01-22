

from .EnemyFactory import EnemyFactory

from .SingletonMeta import SingletonMeta

class PoolOfObjects(metaclass = SingletonMeta): 
    
    def __init__ (self, _waypoints):
        self._waypoints = _waypoints
        self._pool_of_enemies = [] 

        self._weak_enemies = 30 
        self._medium_enemies = 20
        self._strong_enemies = 15
        self._elite_enemies = 10

        self.initialization_of_pool()

    def initialization_of_pool(self):
        for _ in range(self._weak_enemies):
            enemy = EnemyFactory.create_enemy("weak", self._waypoints)
            self._pool_of_enemies.append(enemy)

        for _ in range(self._medium_enemies):
            enemy = EnemyFactory.create_enemy("medium", self._waypoints)
            self._pool_of_enemies.append(enemy)

        for _ in range(self._strong_enemies):
            enemy = EnemyFactory.create_enemy("strong", self._waypoints)
            self._pool_of_enemies.append(enemy)

        for _ in range(self._elite_enemies):
            enemy = EnemyFactory.create_enemy("elite", self._waypoints)
            self._pool_of_enemies.append(enemy)

    def get_enemy(self, enemy_type):
        for i, enemy in enumerate(self._pool_of_enemies):
            if enemy._enemy_type == enemy_type:
                print("SENT ENEMY FROM POOL ")
                return self._pool_of_enemies.pop(i)  
        print("SENT ENEMY")
        return self.create_function(enemy_type)    
    
    def create_function(self, enemy_type):
        return EnemyFactory.create_enemy(enemy_type, self._waypoints)

    def return_enemy(self, enemy):
        enemy.reset_enemy() 
        self._pool_of_enemies.append(enemy)
        print("RETURNED ENEMY")

    
