from display.app import App
from core.cube import Cube

app = App(objects=[Cube(5, 0, 0, 1)])
app.run()
