import pygame.time


class Blinker:
    def __init__(self, interval_ms=500):
        self.last_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.interval_ms = interval_ms
        self.state = True
        self.enabled = True

    def update(self, disable):
        now = pygame.time.get_ticks()
        time_since_last_tick = now - self.last_time
        self.elapsed_time += time_since_last_tick
        if self.elapsed_time > self.interval_ms:
            self.state = not self.state
            self.elapsed_time -= self.interval_ms
        self.last_time = now
        self.enabled = not disable

    def is_on(self):
        return self.enabled and self.state
