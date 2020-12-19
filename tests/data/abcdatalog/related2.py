## BEGIN ANSWER
# Define your rules here for the predicates siblings, related, same_generation, and unrelated. Hint, you may find it helpful to define additional relations, such as ancestor, etc.

# We will only grade your code between the "BEGIN ANSWER" and "END ANSWER" comments.
from mercylog.types import not_eq
from tests.data.abcdatalog.related import (
    adria,
    ancestor,
    barrett,
    carson,
    check,
    deidra,
    eldon,
    fern,
    gonzalo,
    harley,
    ignacia,
    kati,
    lauretta,
    mayra,
    noe,
    odell,
    parent_of,
    person,
    reanna,
    related,
    same_generation,
    siblings,
    sona,
    terra,
    unrelated,
    ursula,
    virgilio,
)

related_data_raw = """
siblings(X,Y) :- X != Y, person(X), person(Y), parent_of(Z, X), parent_of(Z, Y).

ancestor(X,Y) :- person(X), person(Y), parent_of(X, Y).

ancestor(X,Z) :- person(X), person(Y), parent_of(X, Y), ancestor(Y,Z).

related(X,Y) :- ancestor(X, Y).
related(X,Y) :- ancestor(Y, X).
related(X,Y) :- siblings(X, Y).
related(X,Y) :- ancestor(Z, X), X != Y, ancestor(Z, Y).
same_generation(X,Y) :- parent_of(Z, X), parent_of(Z, Y), X != Y.
same_generation(X,Y) :- X != Y, same_generation(U,V), parent_of(U, X), parent_of(V, Y).
unrelated(X,Y) :- not related(X,Y), person(X), X != Y, person(Y).
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

from tests.abcdatalog.helper import U, V, X, Y, Z, parse

related_data = [
    siblings(X, Y)
    <= [not_eq(X, Y), person(X), person(Y), parent_of(Z, X), parent_of(Z, Y)],
    ancestor(X, Y) <= [person(X), person(Y), parent_of(X, Y)],
    ancestor(X, Z) <= [person(X), person(Y), parent_of(X, Y), ancestor(Y, Z)],
    related(X, Y) <= ancestor(X, Y),
    related(X, Y) <= ancestor(Y, X),
    related(X, Y) <= siblings(X, Y),
    related(X, Y) <= [ancestor(Z, X), not_eq(X, Y), ancestor(Z, Y)],
    same_generation(X, Y) <= [parent_of(Z, X), parent_of(Z, Y), not_eq(X, Y)],
    same_generation(X, Y)
    <= [not_eq(X, Y), same_generation(U, V), parent_of(U, X), parent_of(V, Y)],
    unrelated(X, Y) <= [~related(X, Y), person(X), not_eq(X, Y), person(Y)],
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

_exp_ancestors = [
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
    ancestor(ursula, virgilio)
]
