from components import *

class PlaygroundScreen(GameScreen):
    
    def __init__(self):
        pass

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("window_size", (0, 0))
    config.set_config_val("clock_rate", 30)
    model = GameModel()
    screen = GameScreen(config, model)
    loop_events = GameLoopEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
