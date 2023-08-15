"""Uuid25: 25-digit case-insensitive UUID encoding

Uuid25 is an alternative UUID representation that shortens a UUID string to just
25 digits using the case-insensitive Base36 encoding. This library provides
functionality to convert from the conventional UUID formats to Uuid25 and vice
versa.

```python
from uuid25 import Uuid25

# convert from/to string
a = Uuid25.parse("8da942a4-1fbe-4ca6-852c-95c473229c7d")
assert a.value == "8dx554y5rzerz1syhqsvsdw8t"
assert a.to_hyphenated() == "8da942a4-1fbe-4ca6-852c-95c473229c7d"

# convert from/to 128-bit byte array
b = Uuid25.from_bytes(bytes([0xFF] * 16))
assert b.value == "f5lxx1zz5pnorynqglhzmsp33"
assert all([x == 0xFF for x in b.to_bytes()])

# convert from/to other popular textual representations
c = [
    Uuid25.parse("e7a1d63b711744238988afcf12161878"),
    Uuid25.parse("e7a1d63b-7117-4423-8988-afcf12161878"),
    Uuid25.parse("{e7a1d63b-7117-4423-8988-afcf12161878}"),
    Uuid25.parse("urn:uuid:e7a1d63b-7117-4423-8988-afcf12161878"),
]
assert all([x.value == "dpoadk8izg9y4tte7vy1xt94o" for x in c])

d = Uuid25.parse("dpoadk8izg9y4tte7vy1xt94o")
assert d.to_hex() == "e7a1d63b711744238988afcf12161878"
assert d.to_hyphenated() == "e7a1d63b-7117-4423-8988-afcf12161878"
assert d.to_braced() == "{e7a1d63b-7117-4423-8988-afcf12161878}"
assert d.to_urn() == "urn:uuid:e7a1d63b-7117-4423-8988-afcf12161878"

# convert from/to standard uuid module's UUID value
import uuid

uuid_module = uuid.UUID("f38a6b1f-576f-4c22-8d4a-5f72613483f6")
e = Uuid25.from_uuid(uuid_module)
assert e.value == "ef1zh7jc64vprqez41vbwe9km"
assert e.to_uuid() == uuid_module

# generate UUIDv4 in Uuid25 format (backed by uuid module)
import uuid25

print(uuid25.gen_v4())  # e.g., "99wfqtl0z0yevxzpl4hv2dm5p"
```
"""

from __future__ import annotations

__all__ = ["Uuid25", "ParseError", "gen_v4"]

import re
import uuid


class Uuid25:
    """The primary value type containing the Uuid25 representation of a UUID.

    This class wraps a string value to provide conversion methods from/to other popular
    UUID textual representations.

    Create an instance of this class using one of "conversion-from" class methods. It is
    strongly discouraged to create an instance directly with the constructor.

    Attributes:
        value:
            (Read only) The underlying string value of the object in the 25-digit Base36
            textual representation.
    """

    value: str

    __slots__ = "value"

    def __init__(self, uuid25_string: str) -> None:
        self.value = uuid25_string

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}("{self.value}")'

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if type(other) is str:
            return self.value == other
        elif isinstance(other, self.__class__):
            return self.value == other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other: object) -> bool:
        if type(other) is str:
            return self.value < other
        elif isinstance(other, self.__class__):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if type(other) is str:
            return self.value <= other
        elif isinstance(other, self.__class__):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if type(other) is str:
            return self.value > other
        elif isinstance(other, self.__class__):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if type(other) is str:
            return self.value >= other
        elif isinstance(other, self.__class__):
            return self.value >= other.value
        return NotImplemented

    @classmethod
    def _from_int(cls, uint128: int) -> Uuid25:
        """Creates an instance from a 128-bit unsigned integer."""
        if not 0 <= uint128 < 1 << 128:
            raise AssertionError("invalid int value")

        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        buffer = ["0"] * 25
        for i in reversed(range(25)):
            (uint128, rem) = divmod(uint128, 36)
            buffer[i] = digits[rem]
        return cls("".join(buffer))

    @classmethod
    def from_bytes(cls, uuid_bytes: bytes) -> Uuid25:
        """Creates an instance from a 16-byte UUID binary representation.

        Raises:
            `ValueError` if the length of the argument is not 16.
        """
        if len(uuid_bytes) != 16:
            raise ValueError("the length of byte array must be 16")
        return cls._from_int(int.from_bytes(uuid_bytes, "big"))

    def to_bytes(self) -> bytes:
        """Converts `self` into the 16-byte binary representation of a UUID."""
        return int(self.value, 36).to_bytes(16, "big")

    @classmethod
    def parse(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from a UUID string representation.

        This method accepts the following formats:

        - 25-digit Base36 Uuid25 format: `3ud3gtvgolimgu9lah6aie99o`
        - 32-digit hexadecimal format without hyphens:
          `40eb9860cf3e45e2a90eb82236ac806c`
        - 8-4-4-4-12 hyphenated format: `40eb9860-cf3e-45e2-a90e-b82236ac806c`
        - Hyphenated format with surrounding braces:
          `{40eb9860-cf3e-45e2-a90e-b82236ac806c}`
        - RFC 4122 URN format: `urn:uuid:40eb9860-cf3e-45e2-a90e-b82236ac806c`

        Raises:
            `ParseError` if the argument is not a valid UUID string.
        """
        length = len(uuid_string)
        if length == 25:
            return cls.parse_uuid25(uuid_string)
        elif length == 32:
            return cls.parse_hex(uuid_string)
        elif length == 36:
            return cls.parse_hyphenated(uuid_string)
        elif length == 38:
            return cls.parse_braced(uuid_string)
        elif length == 45:
            return cls.parse_urn(uuid_string)
        raise ParseError._with_default_message()

    @classmethod
    def parse_uuid25(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from the 25-digit Base36 Uuid25 format:
        `3ud3gtvgolimgu9lah6aie99o`.

        Raises:
            `ParseError` if the argument is not in the specified format.
        """
        if re.fullmatch(r"[0-9a-z]{25}", uuid_string, flags=re.I):
            value = uuid_string.lower()
            if value <= "f5lxx1zz5pnorynqglhzmsp33":  # 2^128 - 1
                return cls(value)
        raise ParseError._with_default_message()

    @classmethod
    def parse_hex(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from the 32-digit hexadecimal format without hyphens:
        `40eb9860cf3e45e2a90eb82236ac806c`.

        Raises:
            `ParseError` if the argument is not in the specified format.
        """
        if re.fullmatch(r"[0-9a-f]{32}", uuid_string, flags=re.I):
            return cls._from_int(int(uuid_string, 16))
        raise ParseError._with_default_message()

    @classmethod
    def parse_hyphenated(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from the 8-4-4-4-12 hyphenated format:
        `40eb9860-cf3e-45e2-a90e-b82236ac806c`.

        Raises:
            `ParseError` if the argument is not in the specified format.
        """
        m = re.fullmatch(
            r"([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})",
            uuid_string,
            flags=re.I,
        )
        if m:
            return cls._from_int(int("".join(m.groups()), 16))
        raise ParseError._with_default_message()

    @classmethod
    def parse_braced(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from the hyphenated format with surrounding braces:
        `{40eb9860-cf3e-45e2-a90e-b82236ac806c}`.

        Raises:
            `ParseError` if the argument is not in the specified format.
        """
        m = re.fullmatch(
            r"\{([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})\}",
            uuid_string,
            flags=re.I,
        )
        if m:
            return cls._from_int(int("".join(m.groups()), 16))
        raise ParseError._with_default_message()

    @classmethod
    def parse_urn(cls, uuid_string: str) -> Uuid25:
        """Creates an instance from the RFC 4122 URN format:
        `urn:uuid:40eb9860-cf3e-45e2-a90e-b82236ac806c`.

        Raises:
            `ParseError` if the argument is not in the specified format.
        """
        m = re.fullmatch(
            r"urn:uuid:([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})",
            uuid_string,
            flags=re.I,
        )
        if m:
            return cls._from_int(int("".join(m.groups()), 16))
        raise ParseError._with_default_message()

    def to_hex(self) -> str:
        """Formats `self` in the 32-digit hexadecimal format without hyphens:
        `40eb9860cf3e45e2a90eb82236ac806c`.
        """
        return f"{int(self.value, 36):032x}"

    def to_hyphenated(self) -> str:
        """Formats `self` in the 8-4-4-4-12 hyphenated format:
        `40eb9860-cf3e-45e2-a90e-b82236ac806c`.
        """
        uint128 = int(self.value, 36)
        return "{:08x}-{:04x}-{:04x}-{:04x}-{:012x}".format(
            uint128 >> 96,
            (uint128 >> 80) & 0xFFFF,
            (uint128 >> 64) & 0xFFFF,
            (uint128 >> 48) & 0xFFFF,
            uint128 & 0xFFFF_FFFF_FFFF,
        )

    def to_braced(self) -> str:
        """Formats `self` in the hyphenated format with surrounding braces:
        `{40eb9860-cf3e-45e2-a90e-b82236ac806c}`.
        """
        return "{" + self.to_hyphenated() + "}"

    def to_urn(self) -> str:
        """Formats `self` in the RFC 4122 URN format:
        `urn:uuid:40eb9860-cf3e-45e2-a90e-b82236ac806c`.
        """
        return "urn:uuid:" + self.to_hyphenated()

    @classmethod
    def from_uuid(cls, uuid_object: uuid.UUID) -> Uuid25:
        """Creates an instance from the standard `uuid` module's UUID object."""
        return cls._from_int(uuid_object.int)

    def to_uuid(self) -> uuid.UUID:
        """Converts `self` into the standard `uuid` module's UUID object."""
        return uuid.UUID(int=int(self.value, 36))


class ParseError(ValueError):
    """An error parsing a UUID string representation."""

    @classmethod
    def _with_default_message(cls) -> ParseError:
        """Creates an instance with the default error message."""
        return cls("could not parse a UUID string")


def gen_v4() -> Uuid25:
    """Generates a random UUID (UUIDv4) value encoded in the Uuid25 format.

    This function calls the standard `uuid` module's `uuid4()` function and converts the
    result into a Uuid25 instance.
    """
    return Uuid25.from_uuid(uuid.uuid4())
