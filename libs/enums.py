import enum

class MutingTarget(enum.IntEnum):
    USER = enum.auto()
    GUILD = enum.auto()
    CATEGORY = enum.auto()
    CHANNEL = enum.auto()
    ROLE = enum.auto()


class SettingTarget(enum.IntEnum):
    USER = enum.auto()
    GUILD = enum.auto()
