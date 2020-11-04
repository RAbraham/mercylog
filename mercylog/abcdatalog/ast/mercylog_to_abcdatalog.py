from typing import *
from mercylog.types import Rule, Relation, InvertedRelationInstance, Term, Variable
from mercylog.abcdatalog.ast.variable import Variable as AVariable
from mercylog.abcdatalog.ast.term import Term as ATerm
from mercylog.abcdatalog.ast.constant import Constant as AConstant
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom as APositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym as APredicateSym
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom as ANegatedAtom
from mercylog.abcdatalog.ast.clause import Clause as AClause

def convert(program: List[Rule]) -> Set:
    converts = list(map(_convert, program))
    from pprint import pprint
    pprint("\n")
    pprint(converts[0:1])

    return set(converts)

def _convert(r: Rule):
    if isinstance(r, Rule):
        abc_head = convert_relation(r.head)
        abc_body = [convert_relation(b) for b in r.body]
        return AClause(abc_head, abc_body)
    pass


def convert_relation(relation: Union[Relation, InvertedRelationInstance]):
    if isinstance(relation, Relation):
        return make_positive_relation(relation)
    elif isinstance(relation, InvertedRelationInstance):
        positive_relation = relation.relation()
        return ANegatedAtom(make_positive_relation(positive_relation))


def make_positive_relation(relation):
    abc_vars = list(map(convert_term, relation.terms))
    return APositiveAtom.create(APredicateSym.create(relation.name, len(abc_vars)), abc_vars)


def convert_term(term: Term) -> ATerm:

    if isinstance(term, Variable):
        if str(term) == "_":
            return AVariable.createFreshVariable()
        else:
            return AVariable.create(term.name)
    else:
        AConstant.create(str(term))


'''

class Relation:
    """
    A relation is a like a table in a SQL database. An instance of a relation is called a record

    Also called Atom in Datalog terminology
    Note also that in the context of logic-based languages, a relation's name is also called it's _predicate_
    """

    name: str
    terms: Tuple[Term]
'''


'''
class InvertedRelationInstance(object):
    def __init__(self, relation_instance):
        self.relation_instance = relation_instance
        pass

'''