import json

class ProcessMap: 
    def __init__(self):
        self._map_data = None 
        self._tile_map = None 
        
        self._waypoints_data_from_enemies_tilemap = []
        self._waypoints = [] 

        self.opendata() 
        self.enemies_tilemap() 

    def opendata(self):
        try:
            with open('ModuleComponent/levels/level.tmj') as file:
                self._map_data = json.load(file)
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

    def enemies_tilemap(self):
        for layer in self._map_data["layers"]:
            if layer["name"] == "tilemap":
                self._tile_map = layer["data"]
            
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    self._waypoints_data_from_enemies_tilemap = obj["polyline"]
                    self.process_waypoints(self._waypoints_data_from_enemies_tilemap)
    
    def process_waypoints(self, data): 
        for point in data:
            temp_x = point.get("x") 
            temp_y = point.get("y") 
            self._waypoints.append((temp_x, temp_y))


    