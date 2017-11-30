from django.db.models import Model, CharField, BooleanField
from django.db.models import IntegerField, ForeignKey, ManyToManyField
from django.contrib.auth.models import User
from random import randint

ROLES = (
    (0, 'Hunter'),
    (1, 'Officer'),
    (2, 'Manager')
)

class Location(Model):
    """ World location """
    place = CharField(max_length=64)

    def __str__(self):
        return self.place


class Pit(Model):
    """Pit"""
    taken = BooleanField(default=False)
    location = ForeignKey(Location)

    def __str__(self):
        return 'Id: {0}, Loc: {1}, Taken: {2}'.format(self.id,
                                                      self.location.place,
                                                      self.taken)


class Mammoth(Model):
    """ Mammoth """
    age = IntegerField(default=0)
    health = IntegerField(default=100)
    hunted = BooleanField(default=False)
    behavior = CharField(max_length=128)
    symbol = CharField(max_length=128)
    killedIn = ForeignKey(Pit, null=True, blank=True)

    def __str__(self):
        """ Mammoth identification """
        return "{} {}".format(self.symbol, self.behavior)

    class Meta():
        """Meta"""
        verbose_name = 'Mammoth'
        verbose_name_plural = 'Mammoths'


class Hunter(User):
    """ Human being """
    role = IntegerField(choices=ROLES, default=0)
    age = IntegerField(default=0)
    health = IntegerField(default=100)
    available = BooleanField(default=True)
    killedBy = ForeignKey(Mammoth, null=True, blank=True)
    killedIn = ForeignKey('Hunt', null=True, blank=True)

    Stamina = IntegerField(default=randint(0, 100))
    Strength = IntegerField(default=randint(0, 100))
    Agility = IntegerField(default=randint(0, 100))
    Intellect = IntegerField(default=randint(0, 100))
    Speed = IntegerField(default=randint(0, 100))

    class Meta:
        permissions = (
            ('see_watches', 'See watches'),
        )
        verbose_name = 'Hunter'
        verbose_name_plural = 'Hunters'

    def __str__(self):
        """ Hunter identification """
        return self.username

class Abilities(Model):
    """ Abilities """
    ability = CharField(max_length=128)
    def __str__(self):
        return self.ability


class HunterAbilities(Model):
    """ Hunter abilities """
    hunter = ForeignKey(Hunter)
    ability = ForeignKey(Abilities)
    skill = IntegerField(default=0)

    class Meta():
        """" Meta """
        unique_together = (("hunter", "ability")),

    def __str__(self):
        return '{}: {}'.format(self.hunter.username, self.ability.ability)

class Watch(Model):
    """ Watch """
    location = ForeignKey(Location)
    hunters = ManyToManyField(Hunter)
    active = BooleanField(default=True)

    def __str__(self):
        return "Id: {0}, Loc: {1}, Active: {2}".format(self.id,
                                                       self.location.place,
                                                       self.active)


class Message(Model):
    """ Message """
    from_watch = ForeignKey(Watch)
    new_mammoths = IntegerField(default=0)
    mammoths = ManyToManyField(Mammoth)

class Hunt(Model):
    """ Hunt """
    finished = BooleanField(default=False)
    started_by = ForeignKey(Message)
    circumstances = CharField(max_length=128)
    hunters = ManyToManyField(Hunter)
    pits = ManyToManyField(Pit)
