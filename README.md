# Uuid25: 25-digit case-insensitive UUID encoding

[![PyPI](https://img.shields.io/pypi/v/uuid25)](https://pypi.org/project/uuid25/)
[![License](https://img.shields.io/pypi/l/uuid25)](https://github.com/uuid25/python/blob/main/LICENSE)

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
b = Uuid25.from_bytes([0xFF] * 16)
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
```

## License

Licensed under the Apache License, Version 2.0.
