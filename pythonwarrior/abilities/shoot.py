from pythonwarrior.abilities.base import AbilityBase


class Shoot(AbilityBase):
    def description(self):
        return("Shoot your bow & arrows in given direction"
               "(forward by default)")

    def perform(self, direction='forward'):
        self.verify_direction(direction)
        units = self.multi_unit(direction, list(range(1, 4)))
        units = [unit for unit in units if unit]
        if len(units):
            receiver = units[0]
            self._unit.say("shoots %(direction)s and hits %(receiver)s" %
                           {'direction': direction, 'receiver': receiver})
            self.damage(receiver, self._unit.shoot_power)
        else:
            self._unit.say("shoots and hits nothing")

    def multi_unit(self, direction, range_list):
        return [self.unit(direction, n) for n in range_list]