import copy

import json
from dataclasses import dataclass, field

import dacite

from data_class.champion import Champion
from data_class.item import Item
from util.jsonfunction import getValue


def fixChamp(champ):
    if isinstance(champ['armorPerLevel'], str):
        champ['armorPerLevel'] = float(champ['armorPerLevel'])
    if isinstance(champ['mrPerLevel'], str):
        champ['mrPerLevel'] = float(champ['mrPerLevel'])
    if isinstance(champ['attackSpeed'], str):
        champ['attackSpeed'] = float(champ['attackSpeed'])
    if isinstance(champ['attackSpeedPerLevel'], str):
        champ['attackSpeedPerLevel'] = float(champ['attackSpeedPerLevel'])
    if isinstance(champ['adPerLevel'], str):
        champ['adPerLevel'] = float(champ['adPerLevel'])
    if isinstance(champ['mp'], str):
        champ['mp'] = float(champ['mp'])
    if isinstance(champ['mr'], str):
        champ['mr'] = float(champ['mr'])
    if isinstance(champ['mpPerLevel'], str):
        champ['mpPerLevel'] = float(champ['mpPerLevel'])
    if isinstance(champ['armorPenPercent'], str):
        champ['armorPenPercent'] = float(champ['armorPenPercent'])
    if isinstance(champ['magicPenPercent'], str):
        champ['magicPenPercent'] = float(champ['magicPenPercent'])

    return champ


def fixItems(items):
    for idx, item in enumerate(items):
        if isinstance(item['msPercent'], str):
            items[idx]["msPercent"] = float(items[idx]["msPercent"])
        if isinstance(item['crit'], str):
            items[idx]["crit"] = float(items[idx]["crit"])
        if isinstance(item['attackSpeedPercent'], str):
            items[idx]["attackSpeedPercent"] = float(
                items[idx]["attackSpeedPercent"])
        if isinstance(item['lifeStealPercent'], str):
            items[idx]["lifeStealPercent"] = float(items[idx]["lifeStealPercent"])
    return items


def rebuildPartcipant(participantDict):
    participantDict['dps'] = float(participantDict['dps'])
    participantDict['dpsFrom'] = float(participantDict['dpsFrom'])
    participantDict['adReductionFrom'] = float(participantDict['adReductionFrom'])
    participantDict['items'] = fixItems(participantDict['items'])
    participantDict['modItems'] = fixItems(participantDict['modItems'])

    participantDict['champion'] = fixChamp(participantDict['champion'])
    participantDict['calculatedChamp'] = fixChamp(participantDict['calculatedChamp'])
    participant = dacite.from_dict(Participant, data=participantDict)
    return participant


def participantParser(dataFrame, dataInit, dc):
    res = dict()
    res['id'] = int(dataFrame['participantId'])
    res['puuid'] = dataFrame['puuid']
    res['summonerName'] = dataInit['summonerName']
    res['win'] = dataInit['win']
    res['maxGold'] = dataInit['goldEarned']
    res['gold'] = 0
    res['teamId'] = int(dataInit['teamId'])
    itemsJson = [f"item{i}" for i in range(0, 7)]
    res['items'] = []
    for itemName in itemsJson:
        itemId = str(dataInit[itemName])
        if itemId != "0":
            item = dc.items[itemId]
            if "Trinket" not in item.tags:
                res['items'].append(copy.deepcopy(copy.deepcopy(item)))
    res['modItems'] = res['modItems'] if 'modItems' in res else res['items']
    res['champion'] = copy.deepcopy(dc.champions[dataInit['championName']])
    res['calculatedChamp'] = copy.deepcopy(dc.champions[dataInit['championName']])
    participant = dacite.from_dict(Participant, data=res)
    return participant


@dataclass
class Participant:
    id: int
    puuid: str
    summonerName: str
    win: bool
    teamId: int
    items: list[Item]
    modItems: list[Item]
    champion: Champion
    calculatedChamp: Champion = field(default=None)
    gold: int = field(default=0)
    goldDiff: int = field(default=0)
    maxGold: int = field(default=0)
    dpsFrom: float = field(default=0)
    adReductionFrom: float = field(default=0)
    dps: float = field(default=0)

    def reset(self):
        pass

    def newFrame(self, participantFrame):
        if self.calculatedChamp is None:
            self.calculatedChamp = copy.deepcopy(self.champion)
        elif isinstance(self.calculatedChamp, dict):
            self.calculatedChamp = dacite.from_dict(Champion, data=fixChamp(self.calculatedChamp))
        self.calculatedChamp.updateWithFrame(participantFrame['championStats'])
        self.gold = participantFrame["totalGold"]

        self.updateGold()
        print(self.summonerName, len(self.modItems), self.goldDiff)
        myAs = self.calculatedChamp.attackSpeed if self.calculatedChamp.attackSpeed <= 2.5 else 2.5
        self.dps = myAs * self.calculatedChamp.ad

    def updateGold(self):
        self.goldDiff = self.gold
        for item in self.modItems:
            if isinstance(item, Item):
                gold = item.gold
            else:
                gold = item['gold']
            self.goldDiff -= gold

    def generateDps(self, me):

        armor = (self.calculatedChamp.armor * (1 - me.calculatedChamp.armorPenPercent)) - me.calculatedChamp.armorPen
        self.adReductionFrom = round(100 / (100 + armor), 2) * 100

        self.dpsFrom = round(me.dps * (self.adReductionFrom / 100), 2)
        print(self.summonerName, me.summonerName, self.dpsFrom)
