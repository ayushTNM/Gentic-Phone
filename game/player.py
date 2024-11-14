# game/player.py
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def provide_input(self, previous_output, phase, round):
        pass

    @abstractmethod
    def receive_output(self, output, phase):
        pass
