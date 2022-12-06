from __future__ import annotations

import typing
import unittest

from uuid25 import Uuid25, ParseError


class TestUuid25(unittest.TestCase):
    def test_eq(self) -> None:
        """Tests `__eq__()` implementation."""
        for e in TEST_CASES:
            x = Uuid25.parse(e.uuid25)
            self.assertEqual(x, x)
            self.assertIs(x, x)

            self.assertEqual(x, Uuid25.parse(e.uuid25))
            self.assertEqual(Uuid25.parse(e.uuid25), x)
            self.assertIsNot(x, Uuid25.parse(e.uuid25))
            self.assertIsNot(Uuid25.parse(e.uuid25), x)

            self.assertEqual(x, e.uuid25)
            self.assertEqual(e.uuid25, x)
            self.assertEqual(x.value, e.uuid25)
            self.assertEqual(e.uuid25, x.value)

    def test_hash(self) -> None:
        """Tests `__hash__()` implementation."""
        A = "e56ib2nq5r4xc5s1m3ra7tgn5"
        B = "021dqro063u0taj7l442f625s"
        C = "39yf1dk3bobxkselkuibw01dv"
        D = "co6p485732iprk9ih1x208hvo"
        E = "bd5lnb5mncp14mpqhah063zi9"
        F = "7hoo4kemx18f7628fieegto0l"
        G = "375850bf-c24a-b932-09e8-bb3e5b3bd303"  # C == G

        s = set()
        s.add(Uuid25.parse(A))
        s.add(Uuid25.parse(B))
        s.add(Uuid25.parse(C))
        self.assertEqual(len(s), 3)

        self.assertIn(A, s)
        self.assertIn(B, s)
        self.assertIn(C, s)
        self.assertNotIn(D, s)
        self.assertNotIn(E, s)
        self.assertNotIn(F, s)

        self.assertIn(Uuid25.parse(A), s)
        self.assertIn(Uuid25.parse(B), s)
        self.assertIn(Uuid25.parse(C), s)
        self.assertNotIn(Uuid25.parse(D), s)
        self.assertNotIn(Uuid25.parse(E), s)
        self.assertNotIn(Uuid25.parse(F), s)

        self.assertNotIn(G, s)
        self.assertIn(Uuid25.parse(G), s)

    def test_from_to_bytes(self) -> None:
        """Tests conversions from/to byte arrays using manually prepared cases."""
        for e in TEST_CASES:
            x = Uuid25.parse(e.uuid25)
            self.assertEqual(x.value, Uuid25.from_bytes(e.bytes).value)

            bs = x.to_bytes()
            self.assertEqual(len(bs), len(e.bytes))
            for i in range(len(bs)):
                self.assertEqual(bs[i], e.bytes[i])

    def test_parse(self) -> None:
        """Examines parsing results against manually prepared cases."""
        for e in TEST_CASES:
            x = e.uuid25
            self.assertEqual(x, Uuid25.parse(e.uuid25).value)
            self.assertEqual(x, Uuid25.parse(e.hex).value)
            self.assertEqual(x, Uuid25.parse(e.hyphenated).value)
            self.assertEqual(x, Uuid25.parse(e.braced).value)
            self.assertEqual(x, Uuid25.parse(e.urn).value)

            self.assertEqual(x, Uuid25.parse_uuid25(e.uuid25).value)
            self.assertEqual(x, Uuid25.parse_hex(e.hex).value)
            self.assertEqual(x, Uuid25.parse_hyphenated(e.hyphenated).value)
            self.assertEqual(x, Uuid25.parse_braced(e.braced).value)
            self.assertEqual(x, Uuid25.parse_urn(e.urn).value)

            self.assertRaises(ParseError, lambda: Uuid25.parse_uuid25(e.hex))
            self.assertRaises(ParseError, lambda: Uuid25.parse_uuid25(e.hyphenated))
            self.assertRaises(ParseError, lambda: Uuid25.parse_uuid25(e.braced))
            self.assertRaises(ParseError, lambda: Uuid25.parse_uuid25(e.urn))

            self.assertRaises(ParseError, lambda: Uuid25.parse_hex(e.uuid25))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hex(e.hyphenated))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hex(e.braced))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hex(e.urn))

            self.assertRaises(ParseError, lambda: Uuid25.parse_hyphenated(e.uuid25))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hyphenated(e.hex))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hyphenated(e.braced))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hyphenated(e.urn))

            self.assertRaises(ParseError, lambda: Uuid25.parse_braced(e.uuid25))
            self.assertRaises(ParseError, lambda: Uuid25.parse_braced(e.hex))
            self.assertRaises(ParseError, lambda: Uuid25.parse_braced(e.hyphenated))
            self.assertRaises(ParseError, lambda: Uuid25.parse_braced(e.urn))

            self.assertRaises(ParseError, lambda: Uuid25.parse_urn(e.uuid25))
            self.assertRaises(ParseError, lambda: Uuid25.parse_urn(e.hex))
            self.assertRaises(ParseError, lambda: Uuid25.parse_urn(e.hyphenated))
            self.assertRaises(ParseError, lambda: Uuid25.parse_urn(e.braced))

            self.assertEqual(x, Uuid25.parse(e.uuid25.upper()).value)
            self.assertEqual(x, Uuid25.parse(e.hex.upper()).value)
            self.assertEqual(x, Uuid25.parse(e.hyphenated.upper()).value)
            self.assertEqual(x, Uuid25.parse(e.braced.upper()).value)
            self.assertEqual(x, Uuid25.parse(e.urn.upper()).value)

    def test_to_other_formats(self) -> None:
        """Examines "conversion-to" results against manually prepared cases."""
        for e in TEST_CASES:
            x = Uuid25.parse(e.uuid25)
            self.assertEqual(str(x), e.uuid25)
            self.assertEqual(x.value, e.uuid25)
            self.assertEqual(x.to_hex(), e.hex)
            self.assertEqual(x.to_hyphenated(), e.hyphenated)
            self.assertEqual(x.to_braced(), e.braced)
            self.assertEqual(x.to_urn(), e.urn)

    def test_parse_error(self) -> None:
        """Tests if parsing methods raise error on invalid inputs."""
        cases = [
            "",
            "0",
            "f5lxx1zz5pnorynqglhzmsp34",
            "zzzzzzzzzzzzzzzzzzzzzzzzz",
            " 65xe2jcp3zjc704bvftqjzbiw",
            "65xe2jcp3zjc704bvftqjzbiw ",
            " 65xe2jcp3zjc704bvftqjzbiw ",
            "{65xe2jcp3zjc704bvftqjzbiw}",
            "-65xe2jcp3zjc704bvftqjzbiw",
            "65xe2jcp-3zjc704bvftqjzbiw",
            "5xe2jcp3zjc704bvftqjzbiw",
            " 82f1dd3c-de95-075b-93ff-a240f135f8fd",
            "82f1dd3c-de95-075b-93ff-a240f135f8fd ",
            " 82f1dd3c-de95-075b-93ff-a240f135f8fd ",
            "82f1dd3cd-e95-075b-93ff-a240f135f8fd",
            "82f1dd3c-de95075b-93ff-a240f135f8fd",
            "82f1dd3c-de95-075b93ff-a240-f135f8fd",
            "{8273b64c5ed0a88b10dad09a6a2b963c}",
            "urn:uuid:8273b64c5ed0a88b10dad09a6a2b963c",
        ]

        for e in cases:
            self.assertRaises(ParseError, lambda: Uuid25.parse(e))
            self.assertRaises(ParseError, lambda: Uuid25.parse_uuid25(e))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hex(e))
            self.assertRaises(ParseError, lambda: Uuid25.parse_hyphenated(e))
            self.assertRaises(ParseError, lambda: Uuid25.parse_braced(e))
            self.assertRaises(ParseError, lambda: Uuid25.parse_urn(e))

    def test_from_to_uuid(self) -> None:
        """Tests conversions from/to standard uuid module's UUID values."""
        import uuid

        for e in TEST_CASES:
            x = uuid.UUID(hex=e.hyphenated)
            self.assertEqual(str(x), e.hyphenated)

            y = Uuid25.parse(e.uuid25).to_uuid()
            self.assertEqual(x, y)
            self.assertEqual(Uuid25.from_uuid(x).value, e.uuid25)


class PreparedCase(typing.NamedTuple):
    uuid25: str
    hex: str
    hyphenated: str
    braced: str
    urn: str
    bytes: bytes


TEST_CASES: list[PreparedCase] = [
    PreparedCase(
        uuid25="0000000000000000000000000",
        hex="00000000000000000000000000000000",
        hyphenated="00000000-0000-0000-0000-000000000000",
        braced="{00000000-0000-0000-0000-000000000000}",
        urn="urn:uuid:00000000-0000-0000-0000-000000000000",
        bytes=bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ),
    PreparedCase(
        uuid25="f5lxx1zz5pnorynqglhzmsp33",
        hex="ffffffffffffffffffffffffffffffff",
        hyphenated="ffffffff-ffff-ffff-ffff-ffffffffffff",
        braced="{ffffffff-ffff-ffff-ffff-ffffffffffff}",
        urn="urn:uuid:ffffffff-ffff-ffff-ffff-ffffffffffff",
        bytes=bytes(
            [
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
                255,
            ]
        ),
    ),
    PreparedCase(
        uuid25="8j7qcpk2yebp9ouobnujfc312",
        hex="90252ae1bdeeb5e6454983a13e69d556",
        hyphenated="90252ae1-bdee-b5e6-4549-83a13e69d556",
        braced="{90252ae1-bdee-b5e6-4549-83a13e69d556}",
        urn="urn:uuid:90252ae1-bdee-b5e6-4549-83a13e69d556",
        bytes=bytes(
            [144, 37, 42, 225, 189, 238, 181, 230, 69, 73, 131, 161, 62, 105, 213, 86]
        ),
    ),
    PreparedCase(
        uuid25="1ixkdgkqeu8wln1vfrw6csla3",
        hex="19c63717dd78907f153dc2d12a357ebb",
        hyphenated="19c63717-dd78-907f-153d-c2d12a357ebb",
        braced="{19c63717-dd78-907f-153d-c2d12a357ebb}",
        urn="urn:uuid:19c63717-dd78-907f-153d-c2d12a357ebb",
        bytes=bytes(
            [25, 198, 55, 23, 221, 120, 144, 127, 21, 61, 194, 209, 42, 53, 126, 187]
        ),
    ),
    PreparedCase(
        uuid25="1rt96u8g5mehk7anquaf5v0yd",
        hex="1df0de923543c9886d446b0ef75df795",
        hyphenated="1df0de92-3543-c988-6d44-6b0ef75df795",
        braced="{1df0de92-3543-c988-6d44-6b0ef75df795}",
        urn="urn:uuid:1df0de92-3543-c988-6d44-6b0ef75df795",
        bytes=bytes(
            [29, 240, 222, 146, 53, 67, 201, 136, 109, 68, 107, 14, 247, 93, 247, 149]
        ),
    ),
    PreparedCase(
        uuid25="18hye57ickp5c2mg8x9w4o1ji",
        hex="14e0fa5629c70c0d663f5d326e51f1ce",
        hyphenated="14e0fa56-29c7-0c0d-663f-5d326e51f1ce",
        braced="{14e0fa56-29c7-0c0d-663f-5d326e51f1ce}",
        urn="urn:uuid:14e0fa56-29c7-0c0d-663f-5d326e51f1ce",
        bytes=bytes(
            [20, 224, 250, 86, 41, 199, 12, 13, 102, 63, 93, 50, 110, 81, 241, 206]
        ),
    ),
    PreparedCase(
        uuid25="b7b5eir8qxbgpe8ofpfx0jmk4",
        hex="bd3ba1d1ed924804b9004b6f96124cf4",
        hyphenated="bd3ba1d1-ed92-4804-b900-4b6f96124cf4",
        braced="{bd3ba1d1-ed92-4804-b900-4b6f96124cf4}",
        urn="urn:uuid:bd3ba1d1-ed92-4804-b900-4b6f96124cf4",
        bytes=bytes(
            [189, 59, 161, 209, 237, 146, 72, 4, 185, 0, 75, 111, 150, 18, 76, 244]
        ),
    ),
    PreparedCase(
        uuid25="dsc6tknluzhcyoh0wbdhtfm91",
        hex="e8e1d087617c3a88e8f4789ab4a7cf65",
        hyphenated="e8e1d087-617c-3a88-e8f4-789ab4a7cf65",
        braced="{e8e1d087-617c-3a88-e8f4-789ab4a7cf65}",
        urn="urn:uuid:e8e1d087-617c-3a88-e8f4-789ab4a7cf65",
        bytes=bytes(
            [
                232,
                225,
                208,
                135,
                97,
                124,
                58,
                136,
                232,
                244,
                120,
                154,
                180,
                167,
                207,
                101,
            ]
        ),
    ),
    PreparedCase(
        uuid25="edzg3t2pm0tzkjolrcmvlyhtx",
        hex="f309d5b02bf3a736740075948ad1ffc5",
        hyphenated="f309d5b0-2bf3-a736-7400-75948ad1ffc5",
        braced="{f309d5b0-2bf3-a736-7400-75948ad1ffc5}",
        urn="urn:uuid:f309d5b0-2bf3-a736-7400-75948ad1ffc5",
        bytes=bytes(
            [243, 9, 213, 176, 43, 243, 167, 54, 116, 0, 117, 148, 138, 209, 255, 197]
        ),
    ),
    PreparedCase(
        uuid25="1da9001w3ld329fiyf574wuk2",
        hex="171fd840f315e7322796dea092d372b2",
        hyphenated="171fd840-f315-e732-2796-dea092d372b2",
        braced="{171fd840-f315-e732-2796-dea092d372b2}",
        urn="urn:uuid:171fd840-f315-e732-2796-dea092d372b2",
        bytes=bytes(
            [23, 31, 216, 64, 243, 21, 231, 50, 39, 150, 222, 160, 146, 211, 114, 178]
        ),
    ),
    PreparedCase(
        uuid25="bvdc0zy20yoipgda8sb65tczv",
        hex="c885af254a61954a1687c08e41f9940b",
        hyphenated="c885af25-4a61-954a-1687-c08e41f9940b",
        braced="{c885af25-4a61-954a-1687-c08e41f9940b}",
        urn="urn:uuid:c885af25-4a61-954a-1687-c08e41f9940b",
        bytes=bytes(
            [200, 133, 175, 37, 74, 97, 149, 74, 22, 135, 192, 142, 65, 249, 148, 11]
        ),
    ),
    PreparedCase(
        uuid25="3mll19wjhi37qe68vtgobt04h",
        hex="3d46fe7978287d4ff1e57bdf80ab30e1",
        hyphenated="3d46fe79-7828-7d4f-f1e5-7bdf80ab30e1",
        braced="{3d46fe79-7828-7d4f-f1e5-7bdf80ab30e1}",
        urn="urn:uuid:3d46fe79-7828-7d4f-f1e5-7bdf80ab30e1",
        bytes=bytes(
            [61, 70, 254, 121, 120, 40, 125, 79, 241, 229, 123, 223, 128, 171, 48, 225]
        ),
    ),
    PreparedCase(
        uuid25="dlut3j4j5hudfwua508w8h25v",
        hex="e5d7215d6e2c32991506498b84b32d33",
        hyphenated="e5d7215d-6e2c-3299-1506-498b84b32d33",
        braced="{e5d7215d-6e2c-3299-1506-498b84b32d33}",
        urn="urn:uuid:e5d7215d-6e2c-3299-1506-498b84b32d33",
        bytes=bytes(
            [229, 215, 33, 93, 110, 44, 50, 153, 21, 6, 73, 139, 132, 179, 45, 51]
        ),
    ),
    PreparedCase(
        uuid25="bi0ifb9jmm2tig1hsdb9uol2v",
        hex="c2416789944cb584e886ac162d9112b7",
        hyphenated="c2416789-944c-b584-e886-ac162d9112b7",
        braced="{c2416789-944c-b584-e886-ac162d9112b7}",
        urn="urn:uuid:c2416789-944c-b584-e886-ac162d9112b7",
        bytes=bytes(
            [194, 65, 103, 137, 148, 76, 181, 132, 232, 134, 172, 22, 45, 145, 18, 183]
        ),
    ),
    PreparedCase(
        uuid25="0js3yf434vbqa069pkebbly89",
        hex="0947fa843806088a77aa1b1ed69b7789",
        hyphenated="0947fa84-3806-088a-77aa-1b1ed69b7789",
        braced="{0947fa84-3806-088a-77aa-1b1ed69b7789}",
        urn="urn:uuid:0947fa84-3806-088a-77aa-1b1ed69b7789",
        bytes=bytes(
            [9, 71, 250, 132, 56, 6, 8, 138, 119, 170, 27, 30, 214, 155, 119, 137]
        ),
    ),
    PreparedCase(
        uuid25="42ur2gf0i7xgtnlislvutk5fq",
        hex="44e76ce21f2e77bdbadb64850026fd86",
        hyphenated="44e76ce2-1f2e-77bd-badb-64850026fd86",
        braced="{44e76ce2-1f2e-77bd-badb-64850026fd86}",
        urn="urn:uuid:44e76ce2-1f2e-77bd-badb-64850026fd86",
        bytes=bytes(
            [68, 231, 108, 226, 31, 46, 119, 189, 186, 219, 100, 133, 0, 38, 253, 134]
        ),
    ),
    PreparedCase(
        uuid25="6ry55bbvow6mllk9nvfsd4w5f",
        hex="7275ea4776280fa82afb0c4b47f148c3",
        hyphenated="7275ea47-7628-0fa8-2afb-0c4b47f148c3",
        braced="{7275ea47-7628-0fa8-2afb-0c4b47f148c3}",
        urn="urn:uuid:7275ea47-7628-0fa8-2afb-0c4b47f148c3",
        bytes=bytes(
            [114, 117, 234, 71, 118, 40, 15, 168, 42, 251, 12, 75, 71, 241, 72, 195]
        ),
    ),
    PreparedCase(
        uuid25="1xl7tld67nekvdlrp0pkvsut5",
        hex="20a6bddafff4faa14e8fc0eb75a169f9",
        hyphenated="20a6bdda-fff4-faa1-4e8f-c0eb75a169f9",
        braced="{20a6bdda-fff4-faa1-4e8f-c0eb75a169f9}",
        urn="urn:uuid:20a6bdda-fff4-faa1-4e8f-c0eb75a169f9",
        bytes=bytes(
            [
                32,
                166,
                189,
                218,
                255,
                244,
                250,
                161,
                78,
                143,
                192,
                235,
                117,
                161,
                105,
                249,
            ]
        ),
    ),
]
