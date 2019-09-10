import os
import re
import json

from pythonwarrior.config import Config
from pythonwarrior.level import Level
from pythonwarrior.tower import Tower


class Profile(object):
    def __init__(self, player_profile=None):
        if not player_profile:
            self.epic = False
            self.tower_path = None
            self.warrior_name = None
            self.score = 0
            self.epic_score = 0
            self.current_epic_score = 0
            self.current_epic_grades = {}
            self.average_grade = None
            self.abilities = []
            self.level_number = 0
            self.last_level_number = None
            self._player_path = None
        else:
            self.__dict__=player_profile

    def save(self):
        self.update_epic_score()
        if self.epic:
            self.level_number = 0

        with open(self.player_path + '/profile.json','w') as fout:
            json.dump(self.__dict__, fout)

    @staticmethod
    def load(path):
        
        with open(path,'r') as fin:
            player = json.load(fin)
            
        print(type(player))
        return Profile(player)

    @property
    def player_path(self):
        if self._player_path is None:
            self._player_path = Config.path_prefix + \
                "/pythonwarrior/%s" % self.directory_name()
        return self._player_path

    def directory_name(self):
        return "-".join([re.sub("[^a-z0-9]", "-", self.warrior_name.lower()),
                        self.tower().name()])

    def __repr__(self):
        return " - ".join([self.warrior_name, self.tower().name(),
                           "level %s" % self.level_number,
                           "score %s" % self.score])

    def tower(self):
        return Tower(os.path.basename(self.tower_path))

    def current_level(self):
        return Level(self, self.level_number)

    def next_level(self):
        return Level(self, self.level_number+1)

    def add_abilities(self, *abilities):
        #self.abilities += list(set(abilities))
        self.abilities.append(abilities)

    def enable_epic_mode(self):
        self.epic = True
        if not hasattr(self, 'epic_score'):
            self.epic_score = 0
        if not hasattr(self, 'current_epic_score'):
            self.current_epic_score = 0
        self.current_epic_score = self.current_epic_score or 0
        if not hasattr(self, 'last_level_number'):
            self.last_level_number = self.level_number
        self.last_level_number = self.last_level_number or self.level_number

    def enable_normal_mode(self):
        self.epic = False
        self.epic_score = 0
        self.current_epic_score = 0
        self.current_epic_grades = {}
        self.average_grade = None
        self.level_number = self.last_level_number
        self.last_level_number = None

    def level_after_epic(self):
        if self.last_level_number:
            return Level(self, self.last_level_number + 1).exists()

    def update_epic_score(self):
        if self.current_epic_score > self.epic_score:
            self.epic_score = self.current_epic_score
            self.average_grade = self.calculate_average_grade()

    def calculate_average_grade(self):
        if len(self.current_epic_grades) > 0:
            summed_values = sum(self.current_epic_grades.values())
            return summed_values / len(self.current_epic_grades)
