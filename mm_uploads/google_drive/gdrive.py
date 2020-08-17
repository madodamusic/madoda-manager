from pathlib import Path
import json
import os
import sys
class Gdive:
    def __init__(self):
        self.main_path = Path(__file__).parent.parent.parent.absolute()
        self.__conf = {}
        self.__init_conf()
        print("gdrive")

    
    def __init_conf(self):
        conf_path = Path(str(self.main_path)) / str("assets/google_drive/conf.json")
        if conf_path.exists():
            self.__conf = json.loads( conf_path.read_text() )
    
    @property
    def conf(self):
        return self.__conf

print(sys.path)
# Gdive()