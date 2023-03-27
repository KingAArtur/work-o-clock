from __future__ import annotations

from abc import ABC, abstractmethod
import datetime as dt
from enum import Enum, auto
import json

import attr


class AppCategory(Enum):
    MESSENGER = auto()
    GAME = auto()
    VIDEO = auto()
    MUSIC = auto()
    STUDY = auto()


class BlockSchedule(ABC):
    ...


@attr.s(slots=True, kw_only=True)
class FixedSchedule(BlockSchedule):
    start: dt.datetime = attr.ib(factory=dt.datetime.now)
    end: dt.datetime = attr.ib(factory=lambda: dt.datetime.now() + dt.timedelta(days=1))


@attr.s(slots=True, kw_only=True)
class RegularSchedule(BlockSchedule):
    ...


# default schedules & factories:
# - fixed hours everyday
# - for N days every M days (M free, N block, M free...)
# - all weekdays
# - all weekends


@attr.s(slots=True, kw_only=True)
class SettingPreset:
    name: str = attr.ib(default='MyLovelyPreset')
    block_categories: frozenset[AppCategory] = attr.ib(factory=frozenset)
    autodetect: bool = attr.ib(default=False)
    # custom_blacklist?
    schedule: BlockSchedule = attr.ib(factory=FixedSchedule)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data: str) -> SettingPreset:
        return SettingPreset(**json.loads(data))


# default presets:
# - all or nothing (block all and always)
# - zen (block messengers for a day / a week)
# - work-life balance (block all at weekdays at 8 a.m. - 6 p.m.)
