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

## License

Licensed under the Apache License, Version 2.0.
