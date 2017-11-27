from django.db.models import Model, CharField, BooleanField
from django.db.models import IntegerField, ForeignKey, ManyToManyField
from django.contrib.auth.models import User

ROLES = (
    (0, 'Hunter'),
    (1, 'Officer'),
    (2, 'Manager')
)

class Location(Model):
    """ World location """
    place = CharField(max_length=64)


class Pit(Model):
    """Pit"""
    taken = BooleanField(default=False)
    location = ForeignKey(Location)


class Mammoth(Model):
    """ Mammoth """
    age = IntegerField(default=0)
    health = IntegerField(default=100)
    hunted = BooleanField(default=False)
    behavior = CharField(max_length=128)
    character = CharField(max_length=128)
    symbol = CharField(max_length=128)
    killedIn = ForeignKey(Pit, null=True, blank=True)

    def __str__(self):
        """ Mammoth identification """
        return self.symbol

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
    killedIn = ForeignKey(Hunt, null=True)

    class Meta:
        verbose_name = 'Hunter'
        verbose_name_plural = 'Hunters'

    def __str__(self):
        """ Hunter identification """
        return self.username

class Abilities(Model):
    """abilities"""
    ability = CharField(max_length=128)

class HunterAbilities(Model):
    """Hunter abilities"""
    hunter = ForeignKey(Hunter)
    ability = ForeignKey(Abilities)
    skill = IntegerField(default=0)

    class Meta():
        """"Meta"""
        unique_together = (("hunter", "ability")),

class Watch(Model):
    """Watch"""
    location = ForeignKey(Location)
    hunters = ManyToManyField(Hunter)

class Message(Model):
    """Message"""
    from_watch = ForeignKey(Watch)
    new_mammoths = IntegerField(default=0)
    mammoths = ManyToManyField(Mammoth)

class Hunt(Model):
    """Hunt"""
    finished = BooleanField(default=True)
    started_by = ForeignKey(Message)
    circumstances = CharField(max_length=128)
    hunters = ManyToManyField(Hunter)
    pits = ManyToManyField(Pit)
