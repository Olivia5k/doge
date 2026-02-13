"""Define words and static data.

Please extend this file with more lvl=100 shibe wow.
"""

# Copyright (C) 2013-2024 Olivia Thiderman

from __future__ import annotations

import datetime as dt
import random
from collections import deque
from typing import TYPE_CHECKING, NamedTuple, TypedDict, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

import dateutil.easter
import dateutil.tz
import fullmoon


class MonthDay(NamedTuple):
    """A (month, day) pair for seasonal date ranges."""

    month: int
    day: int


DateRange = tuple[MonthDay, MonthDay]


class Season(TypedDict):
    """A seasonal holiday definition."""

    dates: DateRange
    pic: str
    words: tuple[str, ...]


T = TypeVar("T")


class DogeDeque(deque[T]):
    """A doge deque. A doqe, if you may.

    Because random is random, just using a random choice from the static lists
    below there will always be some repetition in the output. This collection
    will instead shuffle the list upon init, and act as a rotating deque
    whenever an item is gotten from it.
    """

    def __init__(self, *args: T) -> None:
        self.doge_index = 0
        items = list(args)
        random.shuffle(items)
        super().__init__(items)

    def get(self) -> T:
        """Get one item and prepare the next.

        This will rotate the deque one step. Repeated gets will
        return different items.
        """
        self.doge_index += 1

        # If we've gone through the entire deque once, shuffle it again to
        # simulate ever-flowing random. self.shuffle() will run __init__(),
        # which will reset the index to 0.
        if self.doge_index == len(self):
            self.shuffle()

        self.rotate(1)
        return self[0]

    def extend(self, iterable: Iterable[T]) -> None:
        """Extend and shuffle."""
        # Whenever we extend the list, make sure to shuffle in the new items!
        super().extend(iterable)
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deque.

        Deques themselves do not support this, so this will make all items into
        a list, shuffle that list, clear the deque, and then re-init the deque.
        """
        items = list(self)
        random.shuffle(items)

        self.clear()
        self.doge_index = 0
        super().__init__(items)


class FrequencyBasedDogeDeque(deque[T]):
    """A doge deque based on word frequencies.

    Interchangeable with DogeDeque (same get/extend/clear/append interface).
    """

    def __init__(self, *args: T, step: int = 2) -> None:
        self.doge_index = 0
        self.step = step
        items = sorted(set(args), key=list(args).count)
        super().__init__(items)

    def shuffle(self) -> None:
        """Shuffle the deque."""

    def get(self) -> T:
        """Get one item and prepare the next.

        Prepare to get an item with lower rank on the next call.
        """
        if self.doge_index >= len(self):
            self.doge_index = 0

        step = random.randint(1, min(self.step, len(self)))

        res = self[0]
        self.doge_index += step
        self.rotate(step)
        return res

    def extend(self, iterable: Iterable[T]) -> None:
        """Extend and recalculate."""
        existing = list(self)
        merged = existing + list(iterable)
        self.clear()
        self.doge_index = 0
        new_to_add = sorted(set(merged), key=merged.count)
        super().__init__(new_to_add)


def easter_dates() -> DateRange:
    """Calculate the start and stop dates of Easter."""
    this_year = dt.datetime.now(tz=dateutil.tz.tzlocal()).year
    easter_day = dateutil.easter.easter(this_year)
    start = easter_day - dt.timedelta(days=7)
    stop = easter_day + dt.timedelta(days=1)
    return (MonthDay(start.month, start.day), MonthDay(stop.month, stop.day))


def moon_dates(look_back_days: int = 14, margin_time_hours: int = 12) -> DateRange:
    """Calculate the nearest full moon date."""
    now = dt.datetime.now(tz=dateutil.tz.tzlocal())
    moon_calculation_start = now - dt.timedelta(days=look_back_days)
    full_moon_finder = fullmoon.NextFullMoon()
    full_moon_finder.set_origin_datetime(moon_calculation_start)
    calculated_full_moon = full_moon_finder.next_full_moon()
    start = calculated_full_moon - dt.timedelta(hours=margin_time_hours)
    stop = calculated_full_moon + dt.timedelta(hours=margin_time_hours)
    return (MonthDay(start.month, start.day), MonthDay(stop.month, stop.day))


PREFIXES = DogeDeque(
    "wow",
    "such",
    "very",
    "so much",
    "many",
    "lol",
    "beautiful",
    "all the",
    "the",
    "most",
    "very much",
    "pretty",
    "so",
)

# Please keep in mind that this particular shibe is a terminal hax0r shibe,
# and the words added should be in that domain
WORD_LIST = [
    "computer",
    "hax0r",
    "code",
    "data",
    "internet",
    "server",
    "hacker",
    "terminal",
    "doge",
    "shibe",
    "program",
    "free software",
    "web scale",
    "monads",
    "git",
    "daemon",
    "loop",
    "pretty",
    "uptime",
    "thread safe",
    "posix",
]
SUFFIXES = DogeDeque("wow", "lol", "hax", "plz", "lvl=100")

# A subset of the 255 color cube with the darkest colors removed. This is
# suited for use on dark terminals. Lighter colors are still present so some
# colors might be semi-unreadable on lighter backgrounds.
#
# If you see this and use a light terminal, a pull request with a set that
# works well on a light terminal would be awesome.
#
# The "1 2 3".split() trick keeps the line count low, even with ruff auto-formatting.
COLORS = DogeDeque(
    *(
        int(x)
        for x in """
        23 24 25 26 27 29 30 31 32 33 35 36 37 38 39 41 42 43 44 45 47 48 49 50
        51 58 59 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83
        84 85 86 87 88 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109
        110 111 112 113 114 115 116 117 118 119 120 121 122 123 130 131 132 133
        134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151
        152 153 154 155 156 157 158 159 162 166 167 168 169 170 171 172 173 174
        175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192
        193 194 195 197 202 203 204 205 206 207 208 209 210 211 212 213 214 215
        216 217 218 219 220 221 222 223 224 225 226 227 228""".split()
    )
)

# Seasonal greetings by Shibe.
# Tuple for every single date is in (month, day) format (year is discarded).
# Doge checks if current date falls in between these dates and show wow
# congratulations, so do whatever complex math you need to make sure Shibe
# celebrates with you!
SEASONS: dict[str, Season] = {
    "valentine": {
        "dates": (MonthDay(2, 12), MonthDay(2, 15)),
        "pic": "doge-valentine.txt",
        "words": (
            "valentine",
            "love",
            "romantic",
            "chocolate",
            "heart",
            "flower",
            "date night",
            "kiss",
            "cuddle",
            "hugs",
            "sweet",
            "affection",
            "roses",
            "sweetheart",
        ),
    },
    "halloween": {
        "dates": (MonthDay(10, 17), MonthDay(10, 31)),
        "pic": "doge-halloween.txt",
        "words": (
            "halloween",
            "scary",
            "ghosts",
            "boo",
            "candy",
            "tricks or treats",
            "trick",
            "treat",
            "costume",
            "dark",
            "night",
        ),
    },
    "thanksgiving": {
        "dates": (MonthDay(11, 15), MonthDay(11, 28)),
        "pic": "doge-thanksgiving.txt",
        "words": (
            "thanksgiving",
            "thanks",
            "pilgrim",
            "turkeys",
            "stuffings",
            "cranberry",
            "meshed potatoes",
        ),
    },
    "xmas": {
        "dates": (MonthDay(12, 14), MonthDay(12, 26)),
        "pic": "doge-xmas.txt",
        "words": (
            "christmas",
            "xmas",
            "candles",
            "santa",
            "merry",
            "reindeers",
            "gifts",
            "jul",
            "vacation",
            "carol",
        ),
    },
    "easter": {
        "dates": easter_dates(),
        "pic": "doge-easter.txt",
        "words": (
            "easter",
            "bunni",
            "playdoge bunni",
            "pascha",
            "passover",
            "påsk",
            "life=100",
            "crusify",
            "fastings",
            "eggs",
            "lamb",
            "candy",
            "easter bunni",
            "easter eggs",
        ),
    },
    "earth": {
        "dates": (MonthDay(4, 16), MonthDay(4, 22)),
        "pic": "doge-earth.txt",
        "words": (
            "earth day",
            "earth",
            "planet",
            "trees",
            "eco friend",
            "green",
            "reduce",
            "reuse",
            "recycle",
            "renew",
            "energy",
            "conservate",
            "nature",
            "sustain",
            "planet love",
            "climate",
            "environment",
            "aware",
            "carbon",
            "sun power",
        ),
    },
    "kabosu": {
        "dates": (MonthDay(5, 24), MonthDay(5, 26)),
        "pic": "doge-kabosu.txt",
        "words": (
            "sweet kabosu",
            "missed",
            "love",
            "memory",
            "cheer",
            "none forget",
            "eternal doge",
            "brightest doge",
            "smiles",
            "star in sky",
            "puppy",
        ),
    },
    "moon": {
        "dates": moon_dates(),
        "pic": "doge-moon.txt",
        "words": (
            "hi-res 4K moon",
            "glow",
            "night lamp",
            "lunar",
            "orbit",
            "werewolf",
            "awoooo",
            "big cheese",
            "sky donut",
            "space boop",
            "NASA",
            "eclipse",
            "crater",
            "moon.exe",
        ),
    },
    # To be continued...
}

# Using "1 2 3".split() keeps the line count low, even with ruff auto-formatting.
STOPWORDS = frozenset(
    """a a's able about above abroad according accordingly across actually adj
    after afterwards again against ago ahead ain't all allow allows almost
    alone along alongside already also although always am amid amidst among
    amongst an and another any anybody anyhow anyone anything anyway anyways
    anywhere apart appear appreciate appropriate are aren't around as aside ask
    asking associated at available away awfully b back backward backwards be
    became because become becomes becoming been before beforehand begin behind
    being believe below beside besides best better between beyond both brief
    but by c c'mon c's came can can't cannot cant caption cause causes certain
    certainly changes clearly co co. com come comes concerning consequently
    consider considering contain containing contains corresponding could
    couldn't course currently d dare daren't definitely described despite did
    didn't different directly do does doesn't doing don't done down downwards
    during e each edu eg eight eighty either else elsewhere end ending enough
    entirely especially et etc even ever evermore every everybody everyone
    everything everywhere ex exactly example except f fairly far farther few
    fewer fifth first five followed following follows for forever former
    formerly forth forward found four from further furthermore g get gets
    getting given gives go goes going gone got gotten greetings h had hadn't
    half happens hardly has hasn't have haven't having he he'd he'll he's hello
    help hence her here here's hereafter hereby herein hereupon hers herself hi
    him himself his hither hopefully how how's howbeit however hundred I I'd
    I'll I'm I've ie if ignored immediate in inasmuch inc inc. indeed indicate
    indicated indicates inner inside insofar instead into inward is isn't it
    it'd it'll it's its itself j just k keep keeps kept know known knows l last
    lately later latter latterly least less lest let let's like liked likely
    likewise little look looking looks low lower ltd m made mainly make makes
    many may maybe mayn't me mean meantime meanwhile merely might mightn't mine
    minus miss more moreover most mostly mr mrs much must mustn't my myself n
    name namely nd near nearly necessary need needn't needs neither never
    neverf neverless nevertheless new next nine ninety no no-one nobody non
    none nonetheless noone nor normally not nothing notwithstanding novel now
    nowhere o obviously of off often oh ok okay old on once one one's ones only
    onto opposite or other others otherwise ought oughtn't our ours ourselves
    out outside over overall own p particular particularly past per perhaps
    placed please plus possible presumably probably provided provides q que
    quite qv r rather rd re really reasonably recent recently regarding
    regardless regards relatively respectively right round s said same saw say
    saying says second secondly see seeing seem seemed seeming seems seen self
    selves sensible sent serious seriously seven several shall shan't she she'd
    she'll she's should shouldn't since six so some somebody someday somehow
    someone something sometime sometimes somewhat somewhere soon sorry
    specified specify specifying still sub such sup sure t t's take taken
    taking tell tends th than thank thanks thanx that that'll that's that've
    thats the their theirs them themselves then thence there there'd there'll
    there're there's there've thereafter thereby therefore therein theres
    thereupon these they they'd they'll they're they've thing things think
    third thirty this thorough thoroughly those though three through throughout
    thru thus till to together too took toward towards tried tries truly try
    trying twice two u un under underneath undoing unfortunately unless unlike
    unlikely until unto up upon upwards us use used useful uses using usually
    uucp v value various versus very via viz vs w want wants was wasn't way we
    we'd we'll we're we've welcome well went were weren't what what'll what's
    what've whatever when when's whence whenever where where's whereafter
    whereas whereby wherein whereupon wherever whether which whichever while
    whilst whither who who'd who'll who's whoever whole whom whomever whose why
    why's will willing wish with within without won't wonder would wouldn't www
    x y yes yet you you'd you'll you're you've your yours yourself yourselves z
    zero
""".split()
)
