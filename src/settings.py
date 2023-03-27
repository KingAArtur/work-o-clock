from __future__ import annotations

from abc import ABC
import datetime as dt
from enum import IntEnum, auto
import json
import os
from pathlib import Path
from typing import Any

import attr


__all__ = (
    'delete_preset',
    'edit_preset',
    'init_preset_storage',
    'load_and_validate_presets',
    'load_preset',
    'load_presets',
    'store_preset',

    'AppCategory',
    'FixedSchedule',
    'RegularSchedule',
    'SettingPreset',

    'DEFAULT_PRESETS',
)


class AppCategory(IntEnum):
    MESSENGER = auto()
    GAME = auto()
    VIDEO = auto()
    MUSIC = auto()
    STUDY = auto()

    @classmethod
    def list_all(cls) -> list[Any]:
        return [elem.value for elem in cls]


ALL_CATEGORIES = frozenset(AppCategory)


def datetime_to_json(date: dt.datetime) -> str:
    return date.isoformat()


def datetime_from_json(js: str) -> dt.datetime:
    return dt.datetime.fromisoformat(js)


class BlockSchedule(ABC):
    ...


def parse_datetime(value: dt.datetime | str) -> dt.datetime:
    if isinstance(value, str):
        return datetime_from_json(value)
    return value


@attr.s(slots=True, kw_only=True)
class FixedSchedule(BlockSchedule):
    start: dt.datetime = attr.ib(
        factory=dt.datetime.now,
        converter=parse_datetime,
    )
    end: dt.datetime = attr.ib(
        factory=lambda: dt.datetime.now() + dt.timedelta(days=1),
        converter=parse_datetime,
    )


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
    block_categories: frozenset[AppCategory] = attr.ib(
        default=ALL_CATEGORIES,
        converter=lambda data: frozenset(AppCategory(elem) for elem in data),
    )
    autodetect: bool = attr.ib(default=False)
    schedule: BlockSchedule = attr.ib(factory=FixedSchedule)
    enable: bool = attr.ib(default=False)

    def to_json(self) -> str:
        return json.dumps(attr.asdict(self), default=datetime_to_json)

    @staticmethod
    def from_json(data: str) -> SettingPreset:
        return SettingPreset(**json.loads(data))


# default presets:
# - all or nothing (block all and always)
# - zen (block messengers for a day / a week)
# - work-life balance (block all at weekdays at 8 a.m. - 6 p.m.)


DEFAULT_PRESETS = {
    'all-or-nothing': SettingPreset(
        name='all-or-nothing',
        block_categories=ALL_CATEGORIES,
        autodetect=True,
        schedule=FixedSchedule(end=dt.datetime.max),
    ),
}

MAX_PRESETS = 10
PRESET_STORAGE_DIR = Path(os.path.relpath(__file__)).parent / 'presets'
PRESET_STORAGE_PATH = PRESET_STORAGE_DIR / 'presets.json'


def dump_presets(presets: dict[str, str]) -> None:
    with open(PRESET_STORAGE_PATH, 'w', encoding='utf-8') as file:
        json.dump(presets, file)


def load_presets() -> dict[str, str]:
    with open(PRESET_STORAGE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_and_validate_presets() -> dict[str, str]:
    presets = load_presets()
    assert all(preset_name in presets for preset_name in DEFAULT_PRESETS), 'Default presets are missing.'
    return presets


def init_preset_storage() -> None:
    if not PRESET_STORAGE_PATH.exists():
        PRESET_STORAGE_DIR.mkdir(exist_ok=True)
        dump_presets({
            preset_name: preset.to_json()
            for preset_name, preset in DEFAULT_PRESETS.items()
        })
    else:
        load_and_validate_presets()


def load_preset(preset_name: str) -> SettingPreset:
    presets = load_and_validate_presets()
    if preset_name not in presets:
        raise ValueError(f'Cannot load preset: unknown preset name "{preset_name}".')
    return SettingPreset.from_json(presets[preset_name])


def store_preset(preset: SettingPreset, exist_ok: bool = False) -> None:
    presets = load_and_validate_presets()
    if len(presets) >= MAX_PRESETS:
        raise ValueError('Cannot store preset: too many presets in the file.')

    if not exist_ok and preset.name in presets:
        raise ValueError(f'Cannot store preset: preset "{preset.name}" already exists.')

    presets[preset.name] = preset.to_json()
    dump_presets(presets)


def delete_preset(preset_name: str, strict: bool = True) -> None:
    presets = load_and_validate_presets()
    if strict and preset_name not in presets:
        raise ValueError(f'Cannot delete preset: unknown preset name "{preset_name}".')

    presets.pop(preset_name)
    dump_presets(presets)


def edit_preset(old_preset_name: str, preset: SettingPreset) -> None:
    presets = load_and_validate_presets()
    if old_preset_name not in presets:
        raise ValueError(f'Cannot edit preset: unknown preset name "{old_preset_name}".')

    presets.pop(old_preset_name)
    presets[preset.name] = preset.to_json()
    dump_presets(presets)
