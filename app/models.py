from django.db.models import Model, CharField, BooleanField
from django.db.models import IntegerField, ForeignKey, ManyToManyField, TextField
from django.contrib.auth.models import AbstractUser
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
    """ Pit """
    taken = BooleanField(default=False)
    location = ForeignKey(Location)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.location)


class Mammoth(Model):
    """ Mammoth """
    health = IntegerField(default=100)
    behavior = CharField(max_length=128)
    symbol = CharField(max_length=128)
    killedIn = ForeignKey('Hunt', null=True, blank=True)

    def __str__(self):
        """ Mammoth identification """
        return "{} with {}".format(self.behavior, self.symbol)

    class Meta():
        """Meta"""
        verbose_name = 'Mammoth'
        verbose_name_plural = 'Mammoths'


class Hunter(AbstractUser):
    """ Human being """
    role = IntegerField(choices=ROLES, default=0)
    age = IntegerField(default=0)
    health = IntegerField(default=100)
    available = BooleanField(default=True)
    killedIn = ForeignKey('Hunt', null=True, blank=True)

    Stamina = IntegerField(default=0)
    Strength = IntegerField(default=0)
    Agility = IntegerField(default=0)
    Intellect = IntegerField(default=0)
    Speed = IntegerField(default=0)

    class Meta:
        verbose_name = 'Hunter'
        verbose_name_plural = 'Hunters'

    def __str__(self):
        """ Hunter identification """
        return self.username

    def __init__(self, *args, **kwargs):
        super(AbstractUser, self).__init__(*args, **kwargs)
        self.Stamina = randint(0, 100)
        self.Strength = randint(0, 100)
        self.Agility = randint(0, 100)
        self.Intellect = randint(0, 100)
        self.Speed = randint(0, 100)

    def isManager(self):
        return self.role == 2

    def isOfficer(self):
        return self.role == 1

    def isPrivileged(self):
        return self.role > 0


class Watch(Model):
    """ Watch """
    location = ForeignKey(Location)
    hunters = ManyToManyField(Hunter)
    active = BooleanField(default=True)

    class Meta:
        verbose_name = 'Watch'
        verbose_name_plural = 'Watches'

    def __str__(self):
        return "[{}] {}, Active: {}".format(self.id, self.location, self.active)


class Message(Model):
    """ Message """
    from_watch = ForeignKey(Watch)
    mammoths = ManyToManyField(Mammoth)
    text = TextField(default='', blank=True)
    title = CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return "[{0}] {1}".format(self.id, self.title)


class Hunt(Model):
    """ Hunt """
    target = ForeignKey(Mammoth)
    hunters = ManyToManyField(Hunter)
    pit = ForeignKey(Pit)
    finished = BooleanField(default=False)
    circumstances = CharField(max_length=128, blank=True)

    def __str__(self):
        return "[{}] Target: {} @ {}".format(self.id, self.target, self.pit.location)
