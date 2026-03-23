# Made this to scratch a personal itch, just for fun

from dataclasses import dataclass
import random

VOWELS = ['a','i','e','o','u']
FINAL_SIBILANT = ['s', 'z', 'x'] # annoying cuz digraphs like <sh>, <ch> are a pain to implement. choosing not to deal with those

@dataclass
class Noun():
    word: str
    plural_form: str = None
    takes_article: bool = True
    is_pronoun: bool = False
    oblique: str = None
    person: int = 3

@dataclass
class Verb():
    word: str
    transitivity: int
    word_past: str = None


# Very very convoluted and ugly function thanks to english' horrendous spelling
def final_s(word):
    if word[-1] in FINAL_SIBILANT:
        if word[-1] == 'x' or word[-2] == word[-1]:
            return word + 'es'
        else:
            return word + word[-1] + 'es'
    return word + 's'

class DP:
    def __init__(self, det, noun: Noun, plural: bool=False, adjective=None) -> None:
        self.det = det
        self.plural = plural
        self.adjective = adjective
        self.noun = noun
    
    def make_plural(self):
        if self.noun.plural_form:
            return self.noun.plural_form
        else:
            return final_s(self.noun.word)

    def make_np(self):
        word = self.noun.word
        if self.plural:
            word = self.make_plural()
        if self.adjective:
            np = [self.adjective, word]
        else:
            np = [word]
        return np

    def make_dp(self):
        np = self.make_np()
        # Nested if statements 🫠
        if self.noun.takes_article:
            if self.det == "a":
                if self.plural:
                    self.det = None
                elif np[0][0] in VOWELS:
                    self.det += 'n'
            dp = [self.det] if self.det else []
        else:
            if self.adjective:
                dp = ["the"]
            else:
                dp = []
        dp += np
        # pronouns do weird syntactically, this implementation isn't fully accurate but works just fine
        if self.noun.is_pronoun:
            dp = [self.noun.word]
        return dp

    def give_oblique_form(self):
        return self.noun.oblique if self.noun.oblique else self.noun.word

    @property
    def is_plural(self):
        return self.plural
    
    @property
    def pronoun(self):
        return self.noun.is_pronoun

    @property
    def person(self):
        return self.noun.person


class VP:
    def __init__(self, verb: Verb, dp: list=None, past=False, *modifier) -> None:
        self.verb = verb
        self.dp = dp
        self.modifier = modifier
        self.past = past
    
    def make_past(self):
        if self.verb.word_past:
            return self.verb.word_past
        elif self.verb.word[-1] in VOWELS:
            return self.verb.word + 'd'
        else:
            return self.verb.word + 'ed'

    def make_vp(self):
        verb = ''
        if not self.past:
            verb = self.verb.word
        else:
            verb = self.make_past()

        vp = [verb]
        for i in range(self.verb.transitivity):
            dp = self.dp[i].make_dp()
            if self.dp[i].pronoun:
                dp = [self.dp[i].give_oblique_form()]
            vp += dp
        
        if self.modifier:
            vp += self.modifier
        return vp

    def third_person_conj(self):
        return final_s(self.verb.word)
    
    @property
    def is_past(self):
        return self.past


class S:
    def __init__(self, dp: DP, vp: VP) -> None:
        self.dp = dp
        self.vp = vp
    
    def make_s(self):
        dp_string = self.dp.make_dp()
        vp_string = self.vp.make_vp()

        if not self.vp.is_past:
            if self.dp.is_plural:
                pass
            elif self.dp.person != 3:
                pass
            else:
                vp_string[0] = self.vp.third_person_conj() # Verb is first element in VP cuz english has left-headedness there

        s = dp_string + vp_string
        return s
    
    def print_s(self):
        s = self.make_s()
        print(' '.join(s))


det = ["the", "a"]
nouns = [Noun("fox"),Noun("teacher"), Noun("assistant"), Noun("chemist"), Noun("Suzie", takes_article=False), Noun("child", "children"),
        Noun("ox", "oxen"), Noun("I", is_pronoun=True, oblique="me", person=1), Noun("you", is_pronoun=True, person=2)]
verbs = [Verb("walk", 0), Verb("hit", 1, "hit"), Verb("stand", 0, "stood"), Verb("call", 1), Verb("give", 2, "gave"), Verb("miss", 1)]
adj = ["cool", "remarkable", "great", "potent", "aristocratic", "enthusiastic", "well-meaning"]
modifiers = [["serendipitously", "quietly", "quickly"], # adverbs
            ["on monday", "in the evening"]] # prepositional phrases

def pick(a):
    return random.choice(a)


def random_dp():
    adjective = pick(adj) if random.random() < 0.2 else None
    plural = random.random() < 0.4
    return DP(pick(det), pick(nouns), plural, adjective)

def random_vp():
    args = []
    dp = []
    for x in modifiers:
        if random.random() < 0.2:
            args.append(pick(x))
    past_tense = random.random() < 0.4

    verb = pick(verbs)
    for i in range(verb.transitivity):
        dp.append(random_dp())

    return VP(verb, dp, past_tense, *args)

if __name__=="__main__":
    dp = random_dp()
    vp = random_vp()
    sentence = S(dp, vp)
    sentence.print_s()
