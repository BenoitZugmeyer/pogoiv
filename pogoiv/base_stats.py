from pogoiv.data import get_csv

from pogoiv.poke_data_error import PokeDataError

if "basestring" in dir(__builtins__):
    def is_string(s):
        return isinstance(s, basestring)
else:
    def is_string(s):
        return isinstance(s, str)


class BaseStats:
    BASE_ATTACK = 'base_attack'
    BASE_DEFENSE = 'base_defense'
    BASE_STAMINA = 'base_stamina'

    def __init__(self):
        self._stats, self._names = self._load_stats()

    def _load_stats(self):
        reader = get_csv('base_stats.tsv')

        names = {}
        stats = []
        for index, row in enumerate(reader):
            if index == 0:
                continue
            name, attack, defense, stamina = row
            names[name.lower()] = index - 1
            stats.append({
                self.BASE_ATTACK: int(attack),
                self.BASE_DEFENSE: int(defense),
                self.BASE_STAMINA: int(stamina)
            })
        return stats, names

    def get_base_stats(self, pokemon):
        if is_string(pokemon):

            if pokemon.isdigit():
                index = int(pokemon) - 1
            elif pokemon.lower() in self._names:
                index = self._names[pokemon.lower()]
            else:
                raise PokeDataError("Could not find Pokemon matching: {}".format(pokemon))

        elif isinstance(pokemon, int):
            index = pokemon - 1

        else:
            raise PokeDataError("Invalid pokemon argument type")

        if not 0 <= index < len(self._stats):
            raise PokeDataError("Invalid pokemon id: {}".format(index + 1))

        return self._stats[index]

    def validate_pokemon(self, pokemon):
        self.get_base_stats(pokemon)
