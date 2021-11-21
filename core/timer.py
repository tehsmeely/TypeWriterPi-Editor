import pygame


class Timer:
    ## An alarm style timer. Flag is set when `duration` elapsed and will not be
    ## retriggered until drained. Overshooting time between the end of `duration`
    ## and when drained is not considered
    def __init__(self, duration_ms):
        self._flag = False
        self._last_time = pygame.time.get_ticks()
        self._duration = duration_ms

    def update(self):
        if not self._flag:
            now = pygame.time.get_ticks()
            if now - self._last_time > self._duration:
                self._flag = True
                self._last_time = now
                return True

        return False

    def is_set(self):
        return self._flag

    def drain(self):
        self._flag = False
