# At the end of the file are definitions of the predicates person(name) and parent_of(parent, child).


## BEGIN ANSWER
# Define your rules here for the predicates siblings, related, same_generation, and unrelated. Hint, you may find it helpful to define additional relations, such as ancestor, etc.

# We will only grade your code between the "BEGIN ANSWER" and "END ANSWER" comments.

related_data_raw = """
siblings(X,Y) :- person(X), person(Y), parent_of(Z, X), parent_of(Z, Y), not_eq(X, Y). ancestor(X,Y) :- person(X), person(Y), parent_of(X, Y).
ancestor(X,Z) :- person(X), person(Y), parent_of(X, Y), ancestor(Y,Z).


related(X,Y) :- ancestor(X, Y).
related(X,Y) :- ancestor(Y, X).
related(X,Y) :- siblings(X, Y).
related(X,Y) :- ancestor(Z, X), ancestor(Z, Y), not_eq(X, Y).

same_generation(X,Y) :- parent_of(Z, X), parent_of(Z, Y), not_eq(X, Y).
same_generation(X,Y) :- same_generation(U,V), parent_of(U, X), parent_of(V, Y), not_eq(X, Y).

unrelated(X,Y) :- person(X), person(Y), not_eq(X, Y), not related(X,Y).

check(X, Y) :- related(X, Y), unrelated(X, Y).


person(adria).
person(barrett).
person(carson).
person(deidra).
person(eldon).
person(fern).
person(gonzalo).
person(harley).
person(ignacia).
person(kati).
person(lauretta).
person(mayra).
person(noe).
person(odell).
person(reanna).
person(sona).
person(terra).
person(ursula).
person(virgilio).

parent_of(adria, carson).
parent_of(barrett, carson).
parent_of(adria, deidra).
parent_of(barrett, deidra).
parent_of(deidra, eldon).
parent_of(deidra, fern).
parent_of(carson, gonzalo).
parent_of(carson, harley).

parent_of(ignacia, lauretta).
parent_of(kati, lauretta).
parent_of(lauretta, mayra).
parent_of(mayra, noe).
parent_of(mayra, odell).
parent_of(noe, reanna).
parent_of(noe, sona).
parent_of(odell, terra).
parent_of(odell, ursula).
parent_of(ursula, virgilio).
"""

from tests.abcdatalog.helper import parse, U, V, W, X, Y, Z
from mercylog.types import relation, variables, not_eq

siblings = relation("siblings")
ancestor = relation("ancestor")
related = relation("related")
person = relation("person")
parent_of = relation("parent_of")
same_generation = relation("same_generation")
unrelated = relation("unrelated")
check = relation("check")
adria = "adria"
barrett = "barrett"
carson = "carson"
deidra = "deidra"
eldon = "eldon"
fern = "fern"
gonzalo = "gonzalo"
harley = "harley"
ignacia = "ignacia"
kati = "kati"
lauretta = "lauretta"
mayra = "mayra"
noe = "noe"
odell = "odell"
reanna = "reanna"
sona = "sona"
terra = "terra"
ursula = "ursula"
virgilio = "virgilio"

related_data = [
    siblings(X, Y)
    <= [person(X), person(Y), parent_of(Z, X), parent_of(Z, Y), not_eq(X, Y)],
    ancestor(X, Y) <= [person(X), person(Y), parent_of(X, Y)],
    ancestor(X, Z) <= [person(X), person(Y), parent_of(X, Y), ancestor(Y, Z)],
    related(X, Y) <= ancestor(X, Y),
    related(X, Y) <= ancestor(Y, X),
    related(X, Y) <= siblings(X, Y),
    related(X, Y) <= [ancestor(Z, X), ancestor(Z, Y), not_eq(X, Y)],
    same_generation(X, Y) <= [parent_of(Z, X), parent_of(Z, Y), not_eq(X, Y)],
    same_generation(X, Y)
    <= [same_generation(U, V), parent_of(U, X), parent_of(V, Y), not_eq(X, Y)],
    unrelated(X, Y) <= [person(X), person(Y), not_eq(X, Y), ~related(X, Y)],
    check(X, Y) <= [related(X, Y), unrelated(X, Y)],
    person(adria),
    person(barrett),
    person(carson),
    person(deidra),
    person(eldon),
    person(fern),
    person(gonzalo),
    person(harley),
    person(ignacia),
    person(kati),
    person(lauretta),
    person(mayra),
    person(noe),
    person(odell),
    person(reanna),
    person(sona),
    person(terra),
    person(ursula),
    person(virgilio),
    parent_of(adria, carson),
    parent_of(barrett, carson),
    parent_of(adria, deidra),
    parent_of(barrett, deidra),
    parent_of(deidra, eldon),
    parent_of(deidra, fern),
    parent_of(carson, gonzalo),
    parent_of(carson, harley),
    parent_of(ignacia, lauretta),
    parent_of(kati, lauretta),
    parent_of(lauretta, mayra),
    parent_of(mayra, noe),
    parent_of(mayra, odell),
    parent_of(noe, reanna),
    parent_of(noe, sona),
    parent_of(odell, terra),
    parent_of(odell, ursula),
    parent_of(ursula, virgilio),
]

_exp_data_siblings = [
    siblings(carson, deidra),
    siblings(deidra, carson),
    siblings(harley, gonzalo),
    siblings(gonzalo, harley),
    siblings(eldon, fern),
    siblings(fern, eldon),
    siblings(noe, odell),
    siblings(odell, noe),
    siblings(reanna, sona),
    siblings(sona, reanna),
    siblings(terra, ursula),
    siblings(ursula, terra),
]
_exp_data_ancestors_raw = """
            ancestor(adria, carson). ancestor(adria, harley). ancestor(adria, gonzalo).
            ancestor(adria, deidra). ancestor(adria, eldon). ancestor(adria, fern).
            ancestor(barrett, carson). ancestor(barrett, harley). ancestor(barrett, gonzalo).
            ancestor(barrett, deidra). ancestor(barrett, eldon). ancestor(barrett, fern).
            ancestor(carson, harley). ancestor(carson, gonzalo).
            ancestor(deidra, eldon). ancestor(deidra, fern).
            ancestor(ignacia, lauretta). ancestor(ignacia, mayra).
            ancestor(ignacia, noe). ancestor(ignacia, reanna). ancestor(ignacia, sona).
            ancestor(ignacia, odell). ancestor(ignacia, terra). ancestor(ignacia, ursula).
            ancestor(ignacia, ursula).
            ancestor(ignacia, virgilio).
            ancestor(kati, lauretta). ancestor(kati, mayra).
            ancestor(kati, noe). ancestor(kati, reanna). ancestor(kati, sona).
            ancestor(kati, odell). ancestor(kati, terra). ancestor(kati, ursula).
            ancestor(kati, ursula).
            ancestor(kati, virgilio).
            ancestor(lauretta, mayra).
            ancestor(lauretta, noe). ancestor(lauretta, reanna). ancestor(lauretta, sona).
            ancestor(lauretta, odell). ancestor(lauretta, terra). ancestor(lauretta, ursula).
            ancestor(lauretta, ursula).
            ancestor(lauretta, virgilio).
            ancestor(mayra, noe). ancestor(mayra, reanna). ancestor(mayra, sona).
            ancestor(mayra, odell). ancestor(mayra, terra). ancestor(mayra, ursula).
            ancestor(mayra, ursula).
            ancestor(mayra, virgilio).
            ancestor(noe, reanna). ancestor(noe, sona).
            ancestor(odell, terra). ancestor(odell, ursula).
            ancestor(odell, ursula).
            ancestor(odell, virgilio).
            ancestor(ursula, virgilio).
    """
# parse(_exp_data_ancestors_raw)
_exp_data_ancestors = [
    ancestor(adria, carson),
    ancestor(adria, harley),
    ancestor(adria, gonzalo),
    ancestor(adria, deidra),
    ancestor(adria, eldon),
    ancestor(adria, fern),
    ancestor(barrett, carson),
    ancestor(barrett, harley),
    ancestor(barrett, gonzalo),
    ancestor(barrett, deidra),
    ancestor(barrett, eldon),
    ancestor(barrett, fern),
    ancestor(carson, harley),
    ancestor(carson, gonzalo),
    ancestor(deidra, eldon),
    ancestor(deidra, fern),
    ancestor(ignacia, lauretta),
    ancestor(ignacia, mayra),
    ancestor(ignacia, noe),
    ancestor(ignacia, reanna),
    ancestor(ignacia, sona),
    ancestor(ignacia, odell),
    ancestor(ignacia, terra),
    ancestor(ignacia, ursula),
    ancestor(ignacia, ursula),
    ancestor(ignacia, virgilio),
    ancestor(kati, lauretta),
    ancestor(kati, mayra),
    ancestor(kati, noe),
    ancestor(kati, reanna),
    ancestor(kati, sona),
    ancestor(kati, odell),
    ancestor(kati, terra),
    ancestor(kati, ursula),
    ancestor(kati, ursula),
    ancestor(kati, virgilio),
    ancestor(lauretta, mayra),
    ancestor(lauretta, noe),
    ancestor(lauretta, reanna),
    ancestor(lauretta, sona),
    ancestor(lauretta, odell),
    ancestor(lauretta, terra),
    ancestor(lauretta, ursula),
    ancestor(lauretta, ursula),
    ancestor(lauretta, virgilio),
    ancestor(mayra, noe),
    ancestor(mayra, reanna),
    ancestor(mayra, sona),
    ancestor(mayra, odell),
    ancestor(mayra, terra),
    ancestor(mayra, ursula),
    ancestor(mayra, ursula),
    ancestor(mayra, virgilio),
    ancestor(noe, reanna),
    ancestor(noe, sona),
    ancestor(odell, terra),
    ancestor(odell, ursula),
    ancestor(odell, ursula),
    ancestor(odell, virgilio),
    ancestor(ursula, virgilio),
]
