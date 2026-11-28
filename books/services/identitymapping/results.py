from enum import StrEnum, auto

from ninja import Schema


class IdentifyResults(Schema):
    new_to_existing: int = 0
    new_to_new: int = 0
    existing_to_existing: int = 0
    existing_to_new: int = 0
    existing_manual_override: int = 0


class IdentifyResult(StrEnum):
    new_to_existing = auto()
    new_to_new = auto()
    existing_to_existing = auto()
    existing_to_new = auto()
    existing_manual_override = auto()
