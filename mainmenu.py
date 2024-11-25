from ursina import *
app = Ursina()
class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.player = None

        def start():
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.time_running = True

        title = Entity(model="quad", texture="assets/mainmenu", parent=self.main_menu, y=0, scale_x=1.8)
        start_button = Button(text="S t a r t  G a m e", color=color.hsv(0, 0, 0, .8), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=-0.3)
        quit_button = Button(text="Q u i t", color=color.hsv(0, 0, 0, .8), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=0.3)
        quit_button.on_click = application.quit

m = MainMenu()
app.run()