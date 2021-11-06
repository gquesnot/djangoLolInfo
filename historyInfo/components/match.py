import copy

import dacite
from django_unicorn.components import UnicornView

from data_class.datacontroller import DataController
from data_class.item import Item
from data_class.participant import Participant, participantParser, rebuildPartcipant
from util.init_lol_watcher import initLolWatcher
from util.jsonfunction import listMatchList


class MatchView(UnicornView):
    matchId: str
    frameId: int = 0
    durationM: int = 0
    version: str = ""
    participants: list[Participant] = []
    enemyParticipants: list[Participant] = []
    activeParticipant: Participant = None
    activeId: int
    dataFull: dict
    dataLight: dict
    modItems: dict[str:Item]
    items: dict[str:Item]
    dc: DataController
    selectedCategory: int = 0
    itemCategory: list
    modalIsOpen: bool
    changeItems: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matchId = kwargs.get('matchId')
        lolWatcher = initLolWatcher()
        self.dc = DataController()
        self.version = self.dc.version
        self.itemCategory = [
            {
                "name": "All Items",
                "tags": [],
            },
            {
                "name": "Attack Damage",
                "tags": ["Damage"],
            },
            {
                "name": "Critical Strike",
                "tags": ["CriticalStrike"],
            },
            {
                "name": "Attack Speed",
                "tags": ["AttackSpeed"],
            },
            {
                "name": "On-Hit Effects",
                "tags": ["OnHit"],
            },
            {
                "name": "Armor Penetration",
                "tags": ["ArmorPenetration"],
            },
            {
                "name": "Ability Power",
                "tags": ["SpellDamage"],
            },
            {
                "name": "Mana & Regeneration",
                "tags": ["Mana", "ManaRegeneration"],
            },
            {
                "name": "Magic Penetration",
                "tags": ["MagicPenetration"],
            },
            {
                "name": "Health & Regeneration",
                "tags": ["Health", "HealthRegen"],
            },
            {
                "name": "Armor",
                "tags": ["Armor"],
            },
            {
                "name": "Magic Resistance",
                "tags": ["SpellBlock"],
            },
            {
                "name": "Ability Haste",
                "tags": ["AbilityHaste"],
            },
            {
                "name": "Movement",
                "tags": ["Boots"],
            },
            {
                "name": "Life Steal & Vamp",
                "tags": ["LifeSteal", "SpellVamp"],
            },
        ]

        self.badItemTags = [
            "Consumable",
            "Vision",
            "Trinket",
            "Jungle",


        ]
        self.frameId = 0
        self.dataLight = lolWatcher.match.by_id("EUROPE", self.matchId)
        self.dataFull = lolWatcher.match.timeline_by_match("EUROPE", self.matchId)
        self.frames = self.dataFull['info']['frames']
        self.durationS = self.dataLight['info']['gameDuration']
        self.durationM = int(self.durationS / 60)
        self.items = dict()
        for k ,v in self.dc.items.items():
            if not listMatchList(self.badItemTags, v.tags) and len(v.tags):
                self.items[k] = v
        self.modItems = copy.deepcopy(self.items)
        for itemdId, item in self.modItems.items():
            print(item.name, item.tags)
        self.participants = [participantParser(participant, self.getMatchInfoByPuuid(participant['puuid']), self.dc) for
                             participant in self.dataFull['info']['participants']]

        self.summonerUpdated(1)
        self.frameUpdated(0)
        # print(self.activeParticipant.items)

    def getActiveParticipant(self):
        self.activeParticipant = self.participants[self.activeId]
        return self.activeParticipant

    def toggleChangeItems(self):
        self.changeItems = not self.changeItems

    def openModal(self):
        self.modalIsOpen = True

    def closeModal(self):
        self.modalIsOpen = False

    def selectCategory(self, id_):
        self.selectedCategory = id_
        res = dict()
        tagToFind = self.itemCategory[id_]['tags']

        for itemId, item in self.items.items():
            if listMatchList(tagToFind, item.tags):
                res[itemId] = item
        self.modItems = res

    def removeItem(self, idx):
        self.rebuildParticipant()
        print("remove item", self.participants[self.activeId].modItems[idx])
        del self.participants[self.activeId].modItems[idx]
        self.participants[self.activeId].updateGold()
        self.getActiveParticipant()

    def addItem(self, itemId):
        self.rebuildParticipant()
        if len(self.getActiveParticipant().modItems) < 6:
            print("ADD ITEM", self.dc.items[str(itemId)])

            self.participants[self.activeId].modItems.append(copy.deepcopy(self.dc.items[str(itemId)]))
        else:
            print("TO MUCH ITEM")
        self.participants[self.activeId].updateGold()
        self.getActiveParticipant()

    def summonerUpdated(self, summonerId):
        self.activeId = int(summonerId) - 1
        self.rebuildParticipant()
        self.getActiveParticipant()

    def rebuildParticipant(self):
        for idx, participant in enumerate(self.participants):
            if not isinstance(participant, Participant):
                self.participants[idx] = rebuildPartcipant(participant)



    def getMatchInfoByPuuid(self, puuid):
        for participant in self.dataLight['info']['participants']:
            if participant['puuid'] == puuid:
                return participant
        return None

    def frameUpdated(self, newFrame):
        newFrame = int(newFrame)
        self.rebuildParticipant()
        print("rebuild ok ")
        self.updateToFrame(newFrame)
        print("update frame ok")
        self.frameId = newFrame
        self.getActiveParticipant()

    def updateToFrame(self, newFrame):

        if newFrame < self.frameId:
            for participant in self.participants:
                participant.reset()
            frameList = self.frames[:newFrame]
        else:
            frameList = self.frames[self.frameId:newFrame]
        for participantId, participantFrame in self.frames[newFrame]['participantFrames'].items():
            participant = self.participants[int(participantId) - 1]
            participant.newFrame(participantFrame)

        for participantId, participantFrame in self.frames[newFrame]['participantFrames'].items():
            participant = self.participants[int(participantId) - 1]
            participant.generateDps(self.participants[self.activeId])
