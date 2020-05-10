import os
from pathlib import Path

class App:
    def __init__(self):
        self.main_path =  os.path.dirname(Path(__file__).absolute())


app = App()
print(app.main_path)