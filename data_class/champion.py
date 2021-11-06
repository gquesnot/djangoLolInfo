import copy
from dataclasses import dataclass, field


@dataclass
class Champion:
    name: str
    hp: float
    hpPerLevel: float
    mp: float
    mpPerLevel: float
    armor: float
    armorPerLevel: float
    mr: float
    mrPerLevel: float
    attackSpeed: float
    attackSpeedPerLevel: float
    ad: float
    adPerLevel: float
    lvl: int = field(default=0)

    armorPen: float = field(init=False,default=0)
    armorPenPercent: float = field(init=False,default=0)
    magicPen: float = field(init=False,default=0)
    magicPenPercent: float = field(init=False,default=0)
    abilityHaste: int = field(init=False,default=0)
    ap: int = field(init=False,default=0)
    lifesteal: float = field(init=False,default=0)
    omnivamp: float = field(init=False,default=0)
    physicalVamp: float = field(init=False,default=0)
    ms: int = field(init=False,default=0)


    def byLevel(self, lvl):
        lvl = lvl - 1
        champCopy = copy.deepcopy(self)
        champCopy.hp += self.hpPerLevel * lvl
        champCopy.mp += self.mpPerLevel * lvl
        champCopy.armor += self.armorPerLevel * lvl
        champCopy.mr += self.mrPerLevel * lvl
        champCopy.attackSpeed = self.attackSpeed * (1 + (self.attackSpeedPerLevel / 100 * lvl))
        champCopy.ad += self.adPerLevel * lvl
        champCopy.lvl = lvl

        return champCopy

    def updateWithFrame(self, frameData):
        self.armor = frameData['armor']
        self.abilityHaste = frameData['abilityHaste']
        self.ap = frameData['abilityPower']
        self.armorPen = frameData['armorPen']
        self.armorPenPercent = frameData['armorPenPercent'] / 100
        self.ad = frameData['attackDamage']
        self.attackSpeed = frameData['attackSpeed'] / 100
        self.hp = frameData['healthMax']
        self.mp = frameData['powerMax']
        self.omnivamp = frameData['omnivamp']
        self.physicalVamp = frameData['physicalVamp']
        self.lifesteal = frameData['lifesteal']

        self.magicPen = frameData['magicPen']
        self.magicPenPercent = frameData['magicPenPercent'] / 100
        self.ms = frameData['movementSpeed']
