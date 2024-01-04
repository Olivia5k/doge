"""
Words and static data

Please extend this file with more lvl=100 shibe wow.

"""

import datetime as dt
import random
from collections import deque

import dateutil.easter


class DogeDeque(deque):
    """
    A doge deque. A doqe, if you may.

    Because random is random, just using a random choice from the static lists
    below there will always be some repetition in the output. This collection
    will instead shuffle the list upon init, and act as a rotating deque
    whenever an item is gotten from it.

    """

    def __init__(self, *args, **kwargs):
        self.index = 0
        args = list(args)
        random.shuffle(args)
        super(DogeDeque, self).__init__(args)

    def get(self):
        """
        Get one item. This will rotate the deque one step. Repeated gets will
        return different items.

        """

        self.index += 1

        # If we've gone through the entire deque once, shuffle it again to
        # simulate ever-flowing random. self.shuffle() will run __init__(),
        # which will reset the index to 0.
        if self.index == len(self):
            self.shuffle()

        self.rotate(1)
        try:
            return self[0]
        except:
            return "wow"

    def extend(self, iterable):
        # Whenever we extend the list, make sure to shuffle in the new items!
        super(DogeDeque, self).extend(iterable)
        self.shuffle()

    def shuffle(self):
        """
        Shuffle the deque

        Deques themselves do not support this, so this will make all items into
        a list, shuffle that list, clear the deque, and then re-init the deque.

        """

        args = list(self)
        random.shuffle(args)

        self.clear()
        super(DogeDeque, self).__init__(args)


class FrequencyBasedDogeDeque(deque):
    def __init__(self, *args, **kwargs):
        self.index = 0
        if "step" in kwargs:
            self.step = kwargs["step"]
        else:
            self.step = 2
        args = list(args)
        # sort words by frequency
        args = (sorted(set(args), key=lambda x: args.count(x)))
        super(FrequencyBasedDogeDeque, self).__init__(args)

    def shuffle(self):
        pass

    def get(self):
        """
        Get one item and prepare to get an item with lower
        rank on the next call.

        """
        if len(self) < 1:
            return "wow"

        if self.index >= len(self):
            self.index = 0

        step = random.randint(1, min(self.step, len(self)))

        res = self[0]
        self.index += step
        self.rotate(step)
        return res

    def extend(self, iterable):

        existing = list(self)
        merged = existing + list(iterable)
        self.clear()
        self.index = 0
        new_to_add = (sorted(set(merged), key=lambda x: merged.count(x)))
        super(FrequencyBasedDogeDeque, self).__init__(new_to_add)


def easter_dates():
    """Calculate the start and stop dates of Easter."""
    this_year = dt.datetime.now().year
    easter_day = dateutil.easter.easter(this_year)
    start = easter_day - dt.timedelta(days=7)
    stop = easter_day + dt.timedelta(days=1)
    return ((start.month, start.day), (stop.month, stop.day))


PREFIXES = DogeDeque(
    'wow', 'such', 'very', 'so much', 'many', 'lol', 'beautiful',
    'all the', 'the', 'most', 'very much', 'pretty', 'so',
)

# Please keep in mind that this particular shibe is a terminal hax0r shibe,
# and the words added should be in that domain
WORD_LIST = ['computer', 'hax0r', 'code', 'data', 'internet', 'server',
             'hacker', 'terminal', 'doge', 'shibe', 'program', 'free software',
             'web scale', 'monads', 'git', 'daemon', 'loop', 'pretty',
             'uptime',
             'thread safe', 'posix']
WORDS = DogeDeque(*WORD_LIST)

SUFFIXES = DogeDeque(
    'wow', 'lol', 'hax', 'plz', 'lvl=100'
)

# A subset of the 255 color cube with the darkest colors removed. This is
# suited for use on dark terminals. Lighter colors are still present so some
# colors might be semi-unreadabe on lighter backgrounds.
#
# If you see this and use a light terminal, a pull request with a set that
# works well on a light terminal would be awesome.
COLORS = DogeDeque(
    23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 41, 42, 43,
    44, 45, 47, 48, 49, 50, 51, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71,
    72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 94,
    95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
    110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143,
    144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
    158, 159, 162, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
    177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
    191, 192, 193, 194, 195, 197, 202, 203, 204, 205, 206, 207, 208, 209,
    210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223,
    224, 225, 226, 227, 228
)

# Seasonal greetings by Shibe.
# Tuple for every single date is in (month, day) format (year is discarded).
# Doge checks if current date falls in between these dates and show wow
# congratulations, so do whatever complex math you need to make sure Shibe
# celebrates with you!
SEASONS = {
    'halloween': {
        'dates': ((10, 17), (10, 31)),
        'pic': 'doge-halloween.txt',
        'words': (
            'halloween', 'scary', 'ghosts', 'boo', 'candy', 'tricks or treats',
            'trick', 'treat', 'costume', 'dark', 'night'
        )
    },
    'thanksgiving': {
        'dates': ((11, 15), (11, 28)),
        'pic': 'doge-thanksgiving.txt',
        'words': (
            'thanksgiving', 'thanks', 'pilgrim', 'turkeys', 'stuffings',
            'cranberry', 'meshed potatoes'
        )
    },
    'xmas': {
        'dates': ((12, 14), (12, 26)),
        'pic': 'doge-xmas.txt',
        'words': (
            'christmas', 'xmas', 'candles', 'santa', 'merry', 'reindeers',
            'gifts', 'jul', 'vacation', 'carol'
        )
    },
    'easter': {
        'dates': easter_dates(),
        'pic': 'doge-easter.txt',
        'words': (
            'easter', 'bunni', 'playdoge bunni', 'pascha', 'passover', 'påsk',
            'life=100', 'crusify', 'fastings', 'eggs', 'lamb', 'candy',
            'easter bunni', 'easter eggs'
        )
    }

    # To be continued...
}

STOPWORDS = ["able", "about", "above", "abroad", "according", "accordingly",
             "across", "actually", "adj", "after",
             "afterwards", "again", "against", "ago", "ahead", "ain't", "all",
             "allow", "allows", "almost", "alone",
             "along", "alongside", "already", "also", "although", "always",
             "am", "amid", "amidst", "among", "amongst",
             "an", "and", "another", "any", "anybody", "anyhow", "anyone",
             "anything", "anyway", "anyways", "anywhere",
             "apart", "appear", "appreciate", "appropriate", "are", "aren't",
             "around", "as", "a's", "aside", "ask",
             "asking", "associated", "at", "available", "away", "awfully",
             "back", "backward", "backwards", "be",
             "became", "because", "become", "becomes", "becoming", "been",
             "before", "beforehand", "begin", "behind",
             "being", "believe", "below", "beside", "besides", "best",
             "better", "between", "beyond", "both", "brief",
             "but", "by", "came", "can", "cannot", "cant", "can't", "caption",
             "cause", "causes", "certain",
             "certainly", "changes", "clearly", "c'mon", "co", "co.", "com",
             "come", "comes", "concerning",
             "consequently", "consider", "considering", "contain",
             "containing", "contains", "corresponding", "could",
             "couldn't", "course", "c's", "currently", "dare", "daren't",
             "definitely", "described", "despite", "did",
             "didn't", "different", "directly", "do", "does", "doesn't",
             "doing", "done", "don't", "down", "downwards",
             "during", "each", "edu", "eg", "eight", "eighty", "either",
             "else", "elsewhere", "end", "ending", "enough",
             "entirely", "especially", "et", "etc", "even", "ever", "evermore",
             "every", "everybody", "everyone",
             "everything", "everywhere", "ex", "exactly", "example", "except",
             "fairly", "far", "farther", "few",
             "fewer", "fifth", "first", "five", "followed", "following",
             "follows", "for", "forever", "former",
             "formerly", "forth", "forward", "found", "four", "from",
             "further", "furthermore", "get", "gets",
             "getting", "given", "gives", "go", "goes", "going", "gone", "got",
             "gotten", "greetings", "had", "hadn't",
             "half", "happens", "hardly", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "hello",
             "help", "hence", "her", "here", "hereafter", "hereby", "herein",
             "here's", "hereupon", "hers", "herself",
             "he's", "hi", "him", "himself", "his", "hither", "hopefully",
             "how", "howbeit", "however", "hundred",
             "i'd", "ie", "if", "ignored", "i'll", "i'm", "immediate", "in",
             "inasmuch", "inc", "inc.", "indeed",
             "indicate", "indicated", "indicates", "inner", "inside",
             "insofar", "instead", "into", "inward", "is",
             "isn't", "it", "it'd", "it'll", "its", "it's", "itself", "i've",
             "just", "k", "keep", "keeps", "kept",
             "know", "known", "knows", "last", "lately", "later", "latter",
             "latterly", "least", "less", "lest", "let",
             "let's", "like", "liked", "likely", "likewise", "little", "look",
             "looking", "looks", "low", "lower",
             "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe",
             "mayn't", "me", "mean", "meantime",
             "meanwhile", "merely", "might", "mightn't", "mine", "minus",
             "miss", "more", "moreover", "most", "mostly",
             "mr", "mrs", "much", "must", "mustn't", "my", "myself", "name",
             "namely", "nd", "near", "nearly",
             "necessary", "need", "needn't", "needs", "neither", "never",
             "neverf", "neverless", "nevertheless", "new",
             "next", "nine", "ninety", "no", "nobody", "non", "none",
             "nonetheless", "noone", "no-one", "nor",
             "normally", "not", "nothing", "notwithstanding", "novel", "now",
             "nowhere", "obviously", "of", "off",
             "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones",
             "one's", "only", "onto", "opposite", "or",
             "other", "others", "otherwise", "ought", "oughtn't", "our",
             "ours", "ourselves", "out", "outside", "over",
             "overall", "own", "particular", "particularly", "past", "per",
             "perhaps", "placed", "please", "plus",
             "possible", "presumably", "probably", "provided", "provides",
             "que", "quite", "qv", "rather", "rd", "re",
             "really", "reasonably", "recent", "recently", "regarding",
             "regardless", "regards", "relatively",
             "respectively", "right", "round", "said", "same", "saw", "say",
             "saying", "says", "second", "secondly",
             "see", "seeing", "seem", "seemed", "seeming", "seems", "seen",
             "self", "selves", "sensible", "sent",
             "serious", "seriously", "seven", "several", "shall", "shan't",
             "she", "she'd", "she'll", "she's", "should",
             "shouldn't", "since", "six", "so", "some", "somebody", "someday",
             "somehow", "someone", "something",
             "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
             "specified", "specify", "specifying",
             "still", "sub", "such", "sup", "sure", "take", "taken", "taking",
             "tell", "tends", "th", "than", "thank",
             "thanks", "thanx", "that", "that'll", "thats", "that's",
             "that've", "the", "their", "theirs", "them",
             "themselves", "then", "thence", "there", "thereafter", "thereby",
             "there'd", "therefore", "therein",
             "there'll", "there're", "theres", "there's", "thereupon",
             "there've", "these", "they", "they'd", "they'll",
             "they're", "they've", "thing", "things", "think", "third",
             "thirty", "this", "thorough", "thoroughly",
             "those", "though", "three", "through", "throughout", "thru",
             "thus", "till", "to", "together", "too",
             "took", "toward", "towards", "tried", "tries", "truly", "try",
             "trying", "t's", "twice", "two", "un",
             "under", "underneath", "undoing", "unfortunately", "unless",
             "unlike", "unlikely", "until", "unto", "up",
             "upon", "upwards", "us", "use", "used", "useful", "uses", "using",
             "usually", "v", "value", "various",
             "versus", "very", "via", "viz", "vs", "want", "wants", "was",
             "wasn't", "way", "we", "we'd", "welcome",
             "well", "we'll", "went", "were", "we're", "weren't", "we've",
             "what", "whatever", "what'll", "what's",
             "what've", "when", "whence", "whenever", "where", "whereafter",
             "whereas", "whereby", "wherein", "where's",
             "whereupon", "wherever", "whether", "which", "whichever", "while",
             "whilst", "whither", "who", "who'd",
             "whoever", "whole", "who'll", "whom", "whomever", "who's",
             "whose", "why", "will", "willing", "wish",
             "with", "within", "without", "wonder", "won't", "would",
             "wouldn't", "yes", "yet", "you", "you'd",
             "you'll", "your", "you're", "yours", "yourself", "yourselves",
             "you've", "zero", "a", "about", "above",
             "after", "again", "against", "all", "am", "an", "and", "any",
             "are", "aren't", "as", "at", "be", "because",
             "been", "before", "being", "below", "between", "both", "but",
             "by", "can't", "cannot", "could", "couldn't",
             "did", "didn't", "do", "does", "doesn't", "doing", "don't",
             "down", "during", "each", "few", "for", "from",
             "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's",
             "her", "here", "here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll",
             "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more",
             "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
             "off", "on", "once", "only", "or", "other",
             "ought", "our", "ours", "", "ourselves", "out", "over", "own",
             "same", "shan't", "she", "she'd", "she'll",
             "she's", "should", "shouldn't", "so", "some", "such", "than",
             "that", "that's", "the", "their", "theirs",
             "them", "themselves", "then", "there", "there's", "these", "they",
             "they'd", "they'll", "they're",
             "they've", "this", "those", "through", "to", "too", "under",
             "until", "up", "very", "was", "wasn't", "we",
             "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
             "what's", "when", "when's", "where",
             "where's", "which", "while", "who", "who's", "whom", "why",
             "why's", "with", "won't", "would", "wouldn't",
             "you", "you'd", "you'll", "you're", "you've", "your", "yours",
             "yourself", "yourselves", "a", "a's",
             "able", "about", "above", "according", "accordingly", "across",
             "actually", "after", "afterwards", "again",
             "against", "ain't", "all", "allow", "allows", "almost", "alone",
             "along", "already", "also", "although",
             "always", "am", "among", "amongst", "an", "and", "another", "any",
             "anybody", "anyhow", "anyone",
             "anything", "anyway", "anyways", "anywhere", "apart", "appear",
             "appreciate", "appropriate", "are",
             "aren't", "around", "as", "aside", "ask", "asking", "associated",
             "at", "available", "away", "awfully",
             "b", "be", "became", "because", "become", "becomes", "becoming",
             "been", "before", "beforehand", "behind",
             "being", "believe", "below", "beside", "besides", "best",
             "better", "between", "beyond", "both", "brief",
             "but", "by", "c", "c'mon", "c's", "came", "can", "can't",
             "cannot", "cant", "cause", "causes", "certain",
             "certainly", "changes", "clearly", "co", "com", "come", "comes",
             "concerning", "consequently", "consider",
             "considering", "contain", "containing", "contains",
             "corresponding", "could", "couldn't", "course",
             "currently", "d", "definitely", "described", "despite", "did",
             "didn't", "different", "do", "does",
             "doesn't", "doing", "don't", "done", "down", "downwards",
             "during", "e", "each", "edu", "eg", "eight",
             "either", "else", "elsewhere", "enough", "entirely", "especially",
             "et", "etc", "even", "ever", "every",
             "everybody", "everyone", "everything", "everywhere", "ex",
             "exactly", "example", "except", "f", "far",
             "few", "fifth", "first", "five", "followed", "following",
             "follows", "for", "former", "formerly", "forth",
             "four", "from", "further", "furthermore", "g", "get", "gets",
             "getting", "given", "gives", "go", "goes",
             "going", "gone", "got", "gotten", "greetings", "h", "had",
             "hadn't", "happens", "hardly", "has", "hasn't",
             "have", "haven't", "having", "he", "he's", "hello", "help",
             "hence", "her", "here", "here's", "hereafter",
             "hereby", "herein", "hereupon", "hers", "herself", "hi", "him",
             "himself", "his", "hither", "hopefully",
             "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've",
             "ie", "if", "ignored", "immediate", "in",
             "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates",
             "inner", "insofar", "instead", "into",
             "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "its",
             "itself", "j", "just", "k", "keep", "keeps",
             "kept", "know", "knows", "known", "l", "last", "lately", "later",
             "latter", "latterly", "least", "less",
             "lest", "let", "let's", "like", "liked", "likely", "little",
             "look", "looking", "looks", "ltd", "m",
             "mainly", "many", "may", "maybe", "me", "mean", "meanwhile",
             "merely", "might", "more", "moreover", "most",
             "mostly", "much", "must", "my", "myself", "n", "name", "namely",
             "nd", "near", "nearly", "necessary",
             "need", "needs", "neither", "never", "nevertheless", "new",
             "next", "nine", "no", "nobody", "non", "none",
             "noone", "nor", "normally", "not", "nothing", "novel", "now",
             "nowhere", "o", "obviously", "of", "off",
             "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones",
             "only", "onto", "or", "other", "others",
             "otherwise", "ought", "our", "ours", "ourselves", "out",
             "outside", "over", "overall", "own", "p",
             "particular", "particularly", "per", "perhaps", "placed",
             "please", "plus", "possible", "presumably",
             "probably", "provides", "q", "que", "quite", "qv", "r", "rather",
             "rd", "re", "really", "reasonably",
             "regarding", "regardless", "regards", "relatively",
             "respectively", "right", "s", "said", "same", "saw",
             "say", "saying", "says", "second", "secondly", "see", "seeing",
             "seem", "seemed", "seeming", "seems",
             "seen", "self", "selves", "sensible", "sent", "serious",
             "seriously", "seven", "several", "shall", "she",
             "should", "shouldn't", "since", "six", "so", "some", "somebody",
             "somehow", "someone", "something",
             "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
             "specified", "specify", "specifying",
             "still", "sub", "such", "sup", "sure", "t", "t's", "take",
             "taken", "tell", "tends", "th", "than", "thank",
             "thanks", "thanx", "that", "that's", "thats", "the", "their",
             "theirs", "them", "themselves", "then",
             "thence", "there", "there's", "thereafter", "thereby",
             "therefore", "therein", "theres", "thereupon",
             "these", "they", "they'd", "they'll", "they're", "they've",
             "think", "third", "this", "thorough",
             "thoroughly", "those", "though", "three", "through", "throughout",
             "thru", "thus", "to", "together", "too",
             "took", "toward", "towards", "tried", "tries", "truly", "try",
             "trying", "twice", "two", "u", "un",
             "under", "unfortunately", "unless", "unlikely", "until", "unto",
             "up", "upon", "us", "use", "used",
             "useful", "uses", "using", "usually", "uucp", "v", "value",
             "various", "very", "via", "viz", "vs", "w",
             "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll",
             "we're", "we've", "welcome", "well",
             "went", "were", "weren't", "what", "what's", "whatever", "when",
             "whence", "whenever", "where", "where's",
             "whereafter", "whereas", "whereby", "wherein", "whereupon",
             "wherever", "whether", "which", "while",
             "whither", "who", "who's", "whoever", "whole", "whom", "whose",
             "why", "will", "willing", "wish", "with",
             "within", "without", "won't", "wonder", "would", "would",
             "wouldn't", "x", "y", "yes", "yet", "you",
             "you'd", "you'll", "you're", "you've", "your", "yours",
             "yourself", "yourselves", "z", "zero", "I", "a",
             "about", "an", "are", "as", "at", "be", "by", "com", "for",
             "from", "how", "in", "is", "it", "of", "on",
             "or", "that", "the", "this", "to", "was", "what", "when", "where",
             "who", "will", "with", "the", "www"]
