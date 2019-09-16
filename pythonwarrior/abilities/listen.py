from pythonwarrior.abilities.base import AbilityBase


class Listen(AbilityBase):
    def description(self):
        return "Returns an array of all spaces which have units in them."

    def perform(self):
        def _collect_non_warrior_spaces(unit):
            if unit and unit != self._unit:
                return unit.position.space()

        units = list(map(_collect_non_warrior_spaces,
                    self._unit.position.floor.units))
        units = [x for x in units if x]

        return units