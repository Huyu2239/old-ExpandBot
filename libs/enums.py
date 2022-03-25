import enum


class HelpTargetCommands(enum.IntEnum):
    MUTE = enum.auto()
    SET = enum.auto()


class MutingTargets(enum.IntEnum):
    USER = enum.auto()
    GUILD = enum.auto()
    CATEGORY = enum.auto()
    CHANNEL = enum.auto()
    ROLE = enum.auto()


class SettingTargets(enum.IntEnum):
    USER = enum.auto()
    MEMBER = enum.auto()
    GUILD = enum.auto()


class SettingArgs(enum.IntEnum):
    HIDDEN = enum.auto()
    ANONYMOUS = enum.auto()
    EMBED_TYPE = enum.auto()
    EMBED_COLOR = enum.auto()
    ALLOW = enum.auto()
