from typing import *
from toolz.curried import *

from mercylog.types import (
    MercylogInput,
    MercylogRule,
    Rule,
    Relation,
    InvertedRelationInstance,
    Term,
    Variable,
    BinaryUnifier,
    BinaryDisunifier,
    GreaterThanPredicate,
    Body,
    OrRelationGroup
)
from mercylog.abcdatalog.ast.variable import Variable as AVariable
from mercylog.abcdatalog.ast.term import Term as ATerm
from mercylog.abcdatalog.ast.constant import Constant as AConstant
from mercylog.abcdatalog.ast.positive_atom import (
    PositiveAtom as APositiveAtom,
    PositiveAtom,
)
from mercylog.abcdatalog.ast.predicate_sym import (
    PredicateSym as APredicateSym,
)
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom as ANegatedAtom
from mercylog.abcdatalog.ast.clause import Clause as AClause
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier as ABinaryUnifier
from mercylog.abcdatalog.ast.greater_than_predicate import GreaterThanPredicate as AGreaterThanPredicate
from mercylog.abcdatalog.ast.binary_disunifier import (
    BinaryDisunifier as ABinaryDisunifier,
)
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


def initEngine_engine(engine: DatalogEngine, program: List[MercylogInput]):
    converted = convert(program)
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

# def convert(program: List[Rule]) -> Set:
#     return pipe(program,
#                 map(_convert))

def convert(program: List[MercylogInput]) -> Set:
    return pipe(program,
                map(flatten),
                concat,
                map(_convert))

def flatten(clause: Union[MercylogRule, Relation]):
    if isinstance(clause, Relation):
        return [clause]
    elif isinstance(clause, MercylogRule):
        rule = clause
        body = rule.body
        if not isinstance(body, OrRelationGroup):
            if isinstance(body, list):
                _b = body
            else:
                _b = [body]
            return [Rule(rule.head, set(_b))]
        else:
            result = []
            for b in rule.body.relations:
                assert isinstance(b, Relation), "For now we don't allow nested relations. Just or_ at the highest level"
                result.append(Rule(rule.head, set([b])))
            return result
    else:
        raise ValueError(f"Invalid type: {clause}")


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




def convert_relation(relation: Union[Relation, InvertedRelationInstance]):
    if isinstance(relation, BinaryUnifier):
        return make_binary_unifier(relation)
    elif isinstance(relation, BinaryDisunifier):
        return make_binary_disunifier(relation)
    elif isinstance(relation, GreaterThanPredicate):
        return make_greater_than_predicate(relation)
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


def make_greater_than_predicate(relation):
    # TODO: Duplicate code
    terms = convert_terms(relation)
    return AGreaterThanPredicate(terms[0], terms[1])



def make_binary_unifier(relation):
    terms = convert_terms(relation)
    return ABinaryUnifier(terms[0], terms[1])


def make_positive_relation(relation):
    abc_vars = convert_terms(relation)

    return APositiveAtom.create(
        APredicateSym.create(relation.name, len(abc_vars)), abc_vars
    )


def convert_terms(relation):
    return pipe(relation.terms, map(convert_term), list)


def convert_term(term: Term) -> ATerm:
    if isinstance(term, Variable):
        if str(term) == "_":
            return AVariable.createFreshVariable()
        else:
            return AVariable.create(term.name)
    else:
        return AConstant.create(term)


def convert_query(a_query: MercylogRule):
    return pipe([a_query], convert, list, first, lambda x: x.getHead())


def q(engine, query):
    # TODO: There is a chance that users will input the relationcreator instead of the relation for no arity predicates e.g. q(). Give a helpful error message if it does
    return pipe(query, convert_query, engine.query, map(rconvert_patom))


def rconvert_patom(r: PositiveAtom) -> Relation:
    sym = r.getPred().getSym()
    return pipe(r.getArgs(), map(rconvert_term), tuple, lambda t: Relation(sym, t))


def rconvert_term(aterm: ATerm) -> Term:
    if isinstance(aterm, AVariable):
        return Variable(aterm.getName())
    elif isinstance(aterm, AConstant):
        return aterm.getName()
    else:
        assert f"Invalid Term:{type(aterm)}"
