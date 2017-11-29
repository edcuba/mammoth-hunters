from .models import Hunter

def topHunters(context):
    hunters = Hunter.objects.all()

    maxKills = 1
    for hunter in hunters:
        kills = 0
        hunter.kills = kills  # TODO
        maxKills = max((kills, maxKills))

    for hunter in hunters:
        hunter.killPerc = 100 * (hunter.kills / maxKills)

    context['maxkills'] = maxKills
    tophunters = sorted(hunters, key=lambda x: x.kills)
    context['hunters'] = hunters[:5]
