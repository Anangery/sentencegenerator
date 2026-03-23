from dataclasses import dataclass
import random

VOWELS = ['a','i','u','e','o']

# I'm aware there's other ways to fix this issue, this seemed most fitting
@dataclass
class Noun:
    name: str
    plural: bool

@dataclass
class Verb:
    name: str
    transitive: bool


determiners = ['the', 'a']
nouns = [Noun("assistant", False), Noun("assistants", True), Noun('student', False), Noun("students", True)]
adjectives = ['friendly', 'mean', 'determined']
adverbs = ['quickly', 'amazingly', 'strenuously']
verbs = [Verb("walk", False), Verb("sleep", False), Verb("hit", True), Verb("call", True)]


def pick(x):
    return lambda : random.choice(x)

pick_determiner = pick(determiners)
pick_noun = pick(nouns)
pick_adjective = pick(adjectives)
pick_adverb = pick(adverbs)
pick_verb = pick(verbs)


def make_np():
    noun = pick_noun()
    noun_name = noun.name
    if random.random() < 0.2:
        noun_name = pick_adjective() + ' ' + noun_name
    return noun, noun_name
    
def make_dp():
    det = pick_determiner()
    np = make_np()
    noun = np[0]
    np_name = np[1]

    # Makes sure the determiner "a" isn't used in plural nouns
    if noun.plural:
        if det == 'a':
            return np_name, noun
    
    # Imperfect way to check for vowels because the rule for adding an n is phonological, not orthographical
    # Would't catch cases as "a uniform" or "an n"
    if det == 'a':
        if np_name[0] in VOWELS:
            det += 'n'

    return det + ' ' + np_name, noun

def make_vp():
    verb = pick_verb()
    adverb = pick_adverb()

    if verb.transitive:
        dp = make_dp()[0]
        vp = [verb.name, dp]
    else:
        vp = [verb.name]
    
    if random.random() < 0.2:
        vp.append(adverb)

    return vp

def make_s():
    dp = make_dp()
    dp_name = dp[0]
    noun = dp[1]

    vp = make_vp()

    if noun.plural:
        s = dp_name + ' ' + ' '.join(vp)
    else:
        vp[0] += 's'
        s = dp_name + ' ' + ' '.join(vp)
    return s