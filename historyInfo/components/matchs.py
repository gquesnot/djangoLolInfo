import json

from django_unicorn.components import UnicornView
from riotwatcher import LolWatcher

from util.init_lol_watcher import initLolWatcher


class Match:
    def __init__(self, id_):
        self.id = id_

    def __str__(self):
        return f"MatchId: {self.id}"

class MatchsView(UnicornView):
    search: str = ""
    summoner: LolWatcher.summoner = ""
    matchList: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lolWatcher = initLolWatcher()

    def doSearch(self):

        self.summoner = self.lolWatcher.summoner.by_name("EUW1", self.search)
        matches = self.lolWatcher.match.matchlist_by_puuid("EUROPE", self.summoner['puuid'])
        print(matches)
        self.matchList = matches
