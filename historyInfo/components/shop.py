import copy
from typing import List, Dict

from django.template.defaultfilters import register
from django_unicorn.components import UnicornView

from data_class.datacontroller import DataController
from data_class.item import Item
from data_class.participant import Participant
from util.jsonfunction import listMatchList


class ShopView(UnicornView):
    dc: DataController
    items: dict[str:Item]
    catItems: dict[str:Item]
    version: str
    activeParticipant: Participant
    selectedCategory: int = 0


