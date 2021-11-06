from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    id: int
    hp: float = field(default=0)
    gold: int = field(default=0)
    hpRegen: float = field(default=0)
    armor: float = field(default=0)
    ad: float = field(default=0)
    ap: float = field(default=0)
    mr: float = field(default=0)
    ms: float = field(default=0)
    msPercent: float = field(default=0)
    attackSpeedPercent: float = field(default=0)
    crit: float = field(default=0)
    lifeStealPercent: float = field(default=0)
    armorPenFlat: float = field(default=0)
    amorPenPercent: float = field(default=0)
    magicPenPercent: float = field(default=0)
    magicPenFlat: float = field(default=0)
    tags: list[str] = field(default_factory=list)