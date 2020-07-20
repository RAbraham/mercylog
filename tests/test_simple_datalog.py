import pytest
from mercylog.simple_datalog import *

RAJIV = Sym('Rajiv')
MIDHUN = Sym('Midhun')
X = Var('X')
Y = Var('Y')
Z = Var('Z')
W = Var('W')

MALE_PREDICATE = 'male'
BROTHER = 'brother'
MALE_ATOM = Atom(MALE_PREDICATE, [X])
BROTHER_ATOM = Atom(BROTHER, [X, Y])


def test_lookup():
    va = Var('a')
    sa = Sym('a')
    s = [(va, Sym('a')),
         (Var('b'), Sym('b'))]
    assert sa == lookup(s, va)
    assert lookup(s, Var('c')) == None


def test_substitute():
    s = [(X, RAJIV)]
    exp_a = Atom(MALE_PREDICATE, [RAJIV])
    assert substitute(MALE_ATOM, s) == exp_a

    # No Value
    s = []
    assert substitute(MALE_ATOM, s) == MALE_ATOM
    # Another Value
    s = [(Y, RAJIV)]
    assert substitute(MALE_ATOM, s) == MALE_ATOM

    # Multiple Values, substitute one
    s = [(X, RAJIV)]
    exp_aa = Atom(BROTHER, [RAJIV, Y])
    assert substitute(BROTHER_ATOM, s) == exp_aa

    # Multiple Values, substitute all
    s = [(X, RAJIV), (Y, MIDHUN)]
    exp_aa = Atom(BROTHER, [RAJIV, MIDHUN])
    assert exp_aa == substitute(BROTHER_ATOM, s)

    # Multiple Values, substitute none
    s = [(Z, RAJIV), (W, MIDHUN)]
    assert BROTHER_ATOM == substitute(BROTHER_ATOM, s)


def test_unify():
    # Var and Sym
    ground_atom = Atom(MALE_PREDICATE, [Sym('Rajiv')])
    assert unify(MALE_ATOM, ground_atom) == [(Var('X'), Sym('Rajiv'))]

    # Sym and Sym
    assert unify(ground_atom, ground_atom) == []

    # Var and Var
    # with pytest.raises(ValueError) as excinfo:
    #     unify(MALE_ATOM, MALE_ATOM)
    # assert "The second atom is assumed to be ground." in str(excinfo.value)
    assert unify(MALE_ATOM, MALE_ATOM) == []
    # Sym and Sym
    # excinfo = None
    # with pytest.raises(ValueError) as excinfo:
    #     unify(ground_atom, MALE_ATOM)
    # assert "The second atom is assumed to be ground." in str(excinfo.value)    with pytest.raises(ValueError) as excinfo:
    assert unify(ground_atom, MALE_ATOM) == []


def test_multiple_unify():
    # Multiple Vars. All Symbols
    grounded_brother_atom = Atom(BROTHER, [RAJIV, MIDHUN])
    print('\n')
    assert unify(BROTHER_ATOM, grounded_brother_atom) == [(X, RAJIV), (Y, MIDHUN)]


def test_person():
    # assert query("query1", person_query()) == [[(Var('X'), Sym('Rajiv'))]]
    # assert query("query1", simple_ancestor()) == [[Var('Intermediate'), Sym('Alan Mycroft')]]
    # ancestor() does not work. > query "query1" ancestor
    # [[(Intermediate,"Dominic Orchard")],[(Intermediate,"Alan Mycroft")]]
    # > query "query2" ancestor
    # []
    # > query "query3" ancestor
    # [[]]
    pass

def test_immediate_consequence():
    assert immediateConsequence(simple_ancestor(), []) == []
    # iteration0OutputKB = [adviser("Alan Mycroft", "Dominic Orchard"),
    #                       adviser("Robin Milner", "Alan Mycroft"),
    #                       academic_ancestor(X, Y),
    #                       academic_ancestor(X, Z)]

    pass

def test_evalRule():
    ancestorRuleBase = base_rule
    assert evalRule([], ancestorRuleBase) == []
    pass

def test_walk():
    #       walk [] [ Atom "adviser" [ Var "X", Var "Y" ] ] `shouldBe` []
    assert walk([], [adviser(X, Y)]) == []
    pass