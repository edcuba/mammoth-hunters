from .models import Hunter, Hunt
from .models import Hunt, Mammoth

def getKills(hunter):
    hunts = Hunt.objects.filter(hunters=hunter.id)
    kills = 0
    mammoths = Mammoth.objects.exclude(killedIn=None)
    for mammoth in mammoths:
        if mammoth.killedIn in hunts:
            kills += 1

    return kills


def topHunters(context):
    hunters = Hunter.objects.all()

    maxKills = 1
    for hunter in hunters:
        kills = getKills(hunter)
        hunter.kills = kills
        maxKills = max((kills, maxKills))

    for hunter in hunters:
        hunter.killPerc = 100 * (hunter.kills / maxKills)

    context['maxkills'] = maxKills
    tophunters = sorted(hunters, key=lambda x: x.kills, reverse=True)
    context['hunters'] = tophunters[:5]

def activeHunts(context):
    hunts = Hunt.objects.filter(finished=False)

    if not hunts:
        return

    context['hunts'] = hunts
