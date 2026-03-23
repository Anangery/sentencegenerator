# Made this to scratch a personal itch, fun to make

from dataclasses import dataclass
import random

VOWELS = ['a','i','e','o','u']

@dataclass
class Noun():
    word: str
    plural: bool

@dataclass
class Verb():
    word: str
    transitive: bool


class DP:
    def __init__(self, det, noun: Noun, adjective=None) -> None:
        self.det = det
        self.adjective = adjective
        self.noun = noun
    
    def make_np(self):
        if self.adjective:
            np = [self.adjective, self.noun.word]
        else:
            np = [self.noun.word]
        return np

    def make_dp(self):
        np = self.make_np()
        if self.det == "a":
            if self.noun.plural:
                self.det = None
            elif np[0][0] in VOWELS:
                self.det += 'n'
        dp = [self.det] if self.det != None else []
        dp += np
        return dp

    @property
    def is_plural(self):
        return self.noun.plural


class VP:
    def __init__(self, verb: Verb, dp: DP=None, *modifier) -> None:
        self.verb = verb
        self.dp = dp
        self.modifier = modifier
    
    def make_vp(self):
        verb = self.verb.word
        if self.verb.transitive:
            dp = self.dp.make_dp()
            vp = [verb]
            vp += dp
        else:
            vp = [verb]
        
        if self.modifier:
            vp += self.modifier
        return vp


class S:
    def __init__(self, dp: DP, vp: VP) -> None:
        self.dp = dp
        self.vp = vp
    
    def make_s(self):
        dp_string = self.dp.make_dp()
        vp_string = self.vp.make_vp()

        if self.dp.is_plural:
            pass
        else:
            vp_string[0]+='s'
        s = dp_string + vp_string
        return s
    
    def print_s(self):
        s = self.make_s()
        print(' '.join(s))


det = ["the", "a"]
nouns = [Noun("students", True), Noun("teacher", False), Noun("assistant", False), Noun("chemist", False)]
verbs = [Verb("walk", False), Verb("hit", True), Verb("stand", False), Verb("call", True)]
adj = ["cool", "remarkable", "great", "potent", "aristocratic"]
adv = ["serendipitously", "quietly", "quickly"]
pp = ["on monday", "in the evening"]

def pick(a):
    return random.choice(a)


def random_dp():
    if random.random() < 0.2:
        adjective = pick(adj)
    else:
        adjective = None
    return DP(pick(det), pick(nouns), adjective)

def random_vp():
    adverb = pick(adv) if random.random() < 0.2 else None
    prep_phrase = pick(pp) if random.random() < 0.2 else None

    args = [x for x in [adverb, prep_phrase] if x != None]

    verb = pick(verbs)
    if verb.transitive:
        dp = random_dp()
    else:
        dp = None
    return VP(verb, dp, *args)

if __name__=="__main__":
    dp = random_dp()
    vp = random_vp()
    sentence = S(dp, vp)
    sentence.print_s()
