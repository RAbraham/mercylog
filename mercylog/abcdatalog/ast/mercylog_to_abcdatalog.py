from typing import *
from mercylog.types import Rule, Relation, InvertedRelationInstance, Term, Variable, BinaryUnifier, BinaryDisunifier
from mercylog.abcdatalog.ast.variable import Variable as AVariable
from mercylog.abcdatalog.ast.term import Term as ATerm
from mercylog.abcdatalog.ast.constant import Constant as AConstant
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom as APositiveAtom, PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym as APredicateSym, PredicateSym
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom as ANegatedAtom
from mercylog.abcdatalog.ast.clause import Clause as AClause
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier as ABinaryUnifier
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier as ABinaryDisunifier
from mercylog.abcdatalog.engine.bottomup.bottom_up_engine_frame import (
    BottomUpEngineFrame,
)
from mercylog.abcdatalog.engine.bottomup.sequential.semi_naive_eval_manager import (
    SemiNaiveEvalManager,
)

from functools import partial
from mercylog.abcdatalog.engine.datalog_engine import DatalogEngine
def seminaive_engine():
    return BottomUpEngineFrame(SemiNaiveEvalManager())


def initEngine_engine(engine: DatalogEngine, program: List[Rule]):
    converted = convert(list(program))
    engine.init(converted)
    return engine

def run_abcdatalog(database, rules, head):
    semi_engine = seminaive_engine()
    initEngine = partial(initEngine_engine, semi_engine)
    program = database + rules
    engine = initEngine(program)
    do_query = q
    rs = do_query(engine, head)
    return rs

def convert(program: List[Rule]) -> Set:
    converts = list(map(_convert, program))
    return set(converts)

# def _convert(r: Rule):
#     if isinstance(r, Rule):
#         abc_head = convert_relation(r.head)
#         abc_body = tuple([convert_relation(b) for b in r.body])
#         return AClause(abc_head, abc_body)
#     else:
#
#         raise ValueError(f"Unexpected Argument:{r} of type: {type(r)}")
#     pass


def _convert(r):

    if isinstance(r, Rule):
        abc_head = convert_relation(r.head)
        abc_body = tuple([convert_relation(b) for b in r.body])
        return AClause(abc_head, abc_body)
    elif isinstance(r, Relation):
        abc_head = convert_relation(r)
        abc_body = tuple([])
        return AClause(abc_head, abc_body)
    else:
        raise ValueError(f"Unexpected Argument:{r} of type: {type(r)}")
    pass

def convert_relation(relation: Union[Relation, InvertedRelationInstance]):
    if isinstance(relation, BinaryUnifier):
        return make_binary_unifier(relation)
    elif isinstance(relation, BinaryDisunifier):
        return make_binary_disunifier(relation)
    elif isinstance(relation, Relation):
        return make_positive_relation(relation)
    elif isinstance(relation, InvertedRelationInstance):
        positive_relation = relation.relation_instance
        return ANegatedAtom(make_positive_relation(positive_relation))
    else:
        raise ValueError(f"Unexpected argument: {relation} of type: {type(relation)}")

def make_binary_disunifier(relation):
    terms = convert_terms(relation)
    return ABinaryDisunifier(terms[0], terms[1])

def make_binary_unifier(relation):
    terms = convert_terms(relation)
    return ABinaryUnifier(terms[0], terms[1])

def make_positive_relation(relation):
    abc_vars = convert_terms(relation)

    return APositiveAtom.create(APredicateSym.create(relation.name, len(abc_vars)), abc_vars)


def convert_terms(relation):
    return list(map(convert_term, relation.terms))


# def convert_term(term: Term) -> ATerm:
#
#     if isinstance(term, Variable):
#         if str(term) == "_":
#             return AVariable.createFreshVariable()
#         else:
#             return AVariable.create(term.name)
#     else:
#         return AConstant.create(str(term))

def convert_term(term: Term) -> ATerm:

    if isinstance(term, Variable):
        if str(term) == "_":
            return AVariable.createFreshVariable()
        else:
            return AVariable.create(term.name)
    else:
        return AConstant.create(term)

# def convert_query(q: Relation):
#     predSym = q.name
#     args = q.terms
#     array = [convert_term(term) for term in args]
#     return PositiveAtom.create(PredicateSym.create(predSym, len(args)), array)

def convert_query(q: Rule):
    return list(convert([q]))[0].getHead()

def q(engine, query):
    # TODO: There is a chance that users will input the relationcreator instead of the relation for no arity predicates e.g. q(). Give a helpful error message if it does
    rs: Set[PositiveAtom] = engine.query(convert_query(query))
    # return [dict(name=r.getPred().getSym(), terms=r.getArgs()) for r in rs]
    return [rconvert_patom(r) for r in rs]

def rconvert_patom(r: PositiveAtom) -> Relation:
    return Relation(r.getPred().getSym(), tuple(rconvert_terms(r.getArgs())))

def rconvert_terms(aterms: Iterable[ATerm]) -> Iterable[Term]:
    result = []
    for aterm in aterms:
        if isinstance(aterm, AVariable):
            result.append(Variable(aterm.getName()))
        elif isinstance(aterm, AConstant):
            result.append(aterm.getName())
        else:
            assert f"Invalid Term:{type(aterm)}"
    return result

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