from typing import *
from dataclasses import dataclass
from pprint import pprint

"""
Given, rules + facts + query
Given:
Male('Rajiv')
Person(X) <= Male(X)
query1(X) <= Person(X)

-- 
first the kb is empty. we take Male('Rajiv'), it's a fact so we put it in the knowledge base.
next: Person(X) <= Male(X). It's a rule. Take the previous kb  and body(i.e. Male(X)) and see if it matches with any fact in the kb. it will match with Male('Rajiv'), so if matched, return Person('Rajiv') and add it to the kb
next: query1(X) <= Person(X). It's a rule. previous kb = [Male('Rajiv'), Person('Rajiv')]. Take body(i.e. Person(X)). 
   take Male('Rajiv') and Person('X'), no match(simple predicate check)
   take Person('Rajiv') and Person(X), there is match, return query1('Rajiv') and add it to kb 

"""


class SimpleDatalog:
    pass


# abstract
class Term:
    pass


@dataclass(eq=True, frozen=True)
class Var(Term):
    _str: str

    def __str__(self):
        return self._str

    def __repr__(self):
        return self.__str__()


@dataclass(eq=True, frozen=True)
class Sym(Term):
    _str: str

    def __str__(self):
        return '"' + self._str + '"'

    def __repr__(self):
        return self.__str__()


@dataclass(eq=True, frozen=True)
class Atom:
    _predSym: str
    _terms: List[Term]

    def __str__(self):
        return self._predSym + "(" + ",".join(map(str, self._terms)) + ")"

    def __repr__(self):
        return self.__str__()

    pass


@dataclass(eq=True, frozen=True)
class Rule:
    _head: Atom
    _body: List[Atom]

    def __str__(self):
        result = str(self._head)
        if self._body:
            result += " <= " + ",".join(map(str, self._body))
        return result

    def __repr__(self):
        return self.__str__()


Program = List[Rule]
KnowledgeBase = List[Atom]
Substitution = List[Tuple[Term, Term]]

"""

emptySubstitution :: Substitution
emptySubstitution = []
"""
# TODO: Is this a constant
emptySubstitution: Substitution = []

"""
isRangeRestricted :: Rule -> Bool
isRangeRestricted Rule{..} =
  vars _head `isSubsetOf` concatMap vars _body
  where
  isSubsetOf as bs = all (`elem` bs) as
  vars Atom{..} = nub $ filter (\case {Var{} -> True; _ -> False}) _terms
"""

elem = lambda element, a_list: element in a_list


def isSubsetOf(ass, bs) -> bool:
    mapped = map(lambda a: elem(a, bs), ass)
    return all(mapped)


def isRangeRestricted(rule: Rule) -> bool:
    _head = rule._head
    _body = rule._body
    is_var = lambda term: isinstance(term, Var)
    vars = lambda atom: nub(filter(is_var, atom._terms))
    return isSubsetOf(vars(_head), concatMap(vars, _body))
    pass


"""
solve :: Program -> KnowledgeBase
solve rules =
  if all isRangeRestricted rules
    then fix step []
    else error "The input program is not range-restricted."
  where
  step :: (KnowledgeBase -> KnowledgeBase)
       -> (KnowledgeBase -> KnowledgeBase)
  step f currentKB | nextKB <- immediateConsequence rules currentKB =
    if nextKB == currentKB
      then currentKB
      else f nextKB

"""
KnowledgeBaseTransformer = Callable[[KnowledgeBase], KnowledgeBase]

"""
  step :: (KnowledgeBase -> KnowledgeBase)
       -> (KnowledgeBase -> KnowledgeBase)
  step f currentKB | nextKB <- immediateConsequence rules currentKB =
    if nextKB == currentKB
      then currentKB
      else f nextKB

"""


def fix(rules: Program):
    current_kb = []
    fix_point = False
    while not fix_point:
        new_kb = immediateConsequence(rules, current_kb)
        if new_kb == current_kb:
            fix_point = True
        else:
            current_kb = new_kb

    return current_kb
    pass


def solve(rules: Program) -> KnowledgeBase:
    if all(map(isRangeRestricted, rules)):
        return fix(rules)
    else:
        raise ValueError("The input program is not range-restricted.")
    pass


def lookup(substitution: Substitution, term: Term) -> Optional[Term]:
    result_list = [x for x in substitution if x[0] == term]
    if result_list:
        return result_list[0][1]
    else:
        return None
    pass


def go_substitute(term: Term, substitution) -> Term:
    if isinstance(term, Sym):
        return term
    else:
        return lookup(substitution, term) or term
    pass


def substitute(atom: Atom, substitution: Substitution) -> Atom:
    go = lambda term: go_substitute(term, substitution)
    new_terms = list(map(go, atom._terms))
    return Atom(_predSym=atom._predSym, _terms=new_terms)


def go_unify(substitution: Substitution) -> Optional[Substitution]:
    # print(f'Input:{substitution}')
    if not substitution:
        return emptySubstitution
    left, right = substitution[0]
    rest = substitution[1:]
    # TODO: use all or use Python MultiMethods?
    if isinstance(left, Sym) and isinstance(right, Sym):
        if left == right:
            result = go_unify(rest)
        else:
            result = None
        pass

    v = left
    s = right
    if isinstance(v, Var) and isinstance(s, Sym):
        # print('Left Var, Right Sym')
        incompleteSubstitution = go_unify(rest)
        if incompleteSubstitution:
            s_dash = lookup(incompleteSubstitution, v)
            if s_dash and s != s_dash:
                result = None
            else:
                result = [(v, s)] + incompleteSubstitution
        else:
            result = [(v, s)] + incompleteSubstitution

    if isinstance(right, Var):
        raise ValueError("The second atom is assumed to be ground.")

    # print(f"Output:{result}")
    return result


# def go_unify(substitution: Substitution) -> Optional[Substitution]:
#     # print(f'Input:{substitution}')
#     if not substitution:
#         return emptySubstitution
#     left, right = substitution[0]
#     rest = substitution[1:]
#     # TODO: use all or use Python MultiMethods?
#     if isinstance(left, Sym) and isinstance(right, Sym):
#         if left == right:
#             result = go_unify(rest)
#         else:
#             result = []
#         pass
#
#     v = left
#     s = right
#     if isinstance(v, Var) and isinstance(s, Sym):
#         # print('Left Var, Right Sym')
#         incompleteSubstitution = go_unify(rest)
#         if incompleteSubstitution:
#             s_dash = lookup(incompleteSubstitution, v)
#             if s_dash and s != s_dash:
#                 result = []
#             else:
#                 result = [(v, s)] + incompleteSubstitution
#         else:
#             result = [(v, s)] + incompleteSubstitution
#             # result = []
#
#     if isinstance(right, Var):
#         print('WRONG RAJ:')
#         print(right)
#         raise ValueError('The second atom is assumed to be ground.')
#     # if isinstance(right, Var):
#     #     result = []
#     # print(f"Output:{result}")
#     return result


def unify(atom1: Atom, atom2: Atom) -> Optional[Substitution]:
    predSym = atom1._predSym
    ts = atom1._terms
    predSym_dash = atom2._predSym
    ts_dash = atom2._terms
    if predSym == predSym_dash:
        zipped = list(zip(ts, ts_dash))
        return go_unify(zipped)
    else:
        return None
    pass


"""
evalAtom :: KnowledgeBase -> Atom -> [ Substitution ] -> [ Substitution ]
evalAtom kb atom substitutions = do
  substitution <- substitutions
  let downToEarthAtom = substitute atom substitution
  extension <- mapMaybe (unify downToEarthAtom) kb
  return $ substitution <> extension
"""


def evalAtom(
    kb: KnowledgeBase, atom: Atom, substitutions: List[Substitution]
) -> List[Substitution]:
    final_result = []
    # print('----------')
    # pprint(f'KnowledgeBase:{kb}')
    # pprint(f'Substitutions:{substitutions}')
    for substitution in substitutions:
        downToEarthAtom = substitute(atom, substitution)
        # print(f"Eval Atom, Before Unify:{atom}")
        # print(f'Eval Atom, downToEarthAtom:{downToEarthAtom}')

        unified = [unify(downToEarthAtom, atom) for atom in kb]
        # print(f"Eval Atom, Unified:{unified}")

        extension = [s for s in unified if s]
        # print(f'Extension:{extension}')

        result = [substitution] + extension
        final_result.extend(result)

    return final_result

    pass


"""
walk :: KnowledgeBase -> [ Atom ] -> [ Substitution ]
walk kb = foldr (evalAtom kb) [ emptySubstitution ]
"""
import functools

foldr = lambda func, acc, xs: functools.reduce(lambda x, y: func(y, x), xs[::-1], acc)


def empty_walk(walk_list) -> bool:
    return len(walk_list) == 1 and not walk_list[0]
    pass


def walk(kb: KnowledgeBase, atoms: List[Atom]) -> List[Substitution]:
    reduce_func = lambda atom, substitutions: evalAtom(kb, atom, substitutions)
    # result = foldr(reduce_func, [emptySubstitution], atoms)
    result = foldr(reduce_func, emptySubstitution, atoms)
    # return result if not empty_walk(result) else []
    return result


"""
evalRule :: KnowledgeBase -> Rule -> KnowledgeBase
evalRule kb (Rule head body) = map (substitute head) (walk kb body)
"""


def evalRule(kb: KnowledgeBase, rule: Rule) -> KnowledgeBase:
    # -----------------------------------------
    # print('>>>>>>>')
    # print('Eval Rule')
    # print(rule)
    # print('Eval Rule KB')
    # print(kb)
    head = rule._head
    body = rule._body
    sub_func = lambda substitution: substitute(head, substitution)

    walk_list = walk(kb, body)
    # print('Walk List')
    # print(walk_list)

    rule_evaluation = list(map(sub_func, walk_list))
    # print('Rule Evaluation')
    # print(rule_evaluation)
    # print('<<<<<<<<<')
    return rule_evaluation


"""
immediateConsequence :: Program -> KnowledgeBase -> KnowledgeBase
immediateConsequence rules kb =
  nub . (kb <>) . concatMap (evalRule kb) $ rules
"""
from itertools import chain


# nub = lambda x: list(dict.fromkeys(x))
def nub(xn: List) -> List:
    dedup = []
    for x in xn:
        if x not in dedup:
            dedup.append(x)

    return dedup


def flatten(it):
    "Flatten one level of nesting"
    return chain.from_iterable(it)


def concatMap(func, it):
    """Map a function over a list and concatenate the results."""
    return flatten(map(func, it))


def immediateConsequence_r(rules: Program, kb: KnowledgeBase) -> KnowledgeBase:
    """
    first the kb is empty. we take Male('Rajiv'), it's a fact so we put it in the knowledge base.
 next: Person(X) <= Male(X). It's a rule. Take the previous kb  and body(i.e. Male(X)) and see if it matches with any fact in the kb. it will match with Male('Rajiv'), so if matched, return Person('Rajiv') and add it to the kb
 next: query1(X) <= Person(X). It's a rule. previous kb = [Male('Rajiv'), Person('Rajiv')]. Take body(i.e. Person(X)).
    take Male('Rajiv') and Person('X'), no match(simple predicate check)
    take Person('Rajiv') and Person(X), there is match, return query1('Rajiv') and add it to kb


    immediateCOnsequence
    :param rules:
    :param kb:
    :return:
    """

    pass


def immediateConsequence(rules: Program, kb: KnowledgeBase) -> KnowledgeBase:
    print("KB")
    print(kb)
    # print('Rules')
    # pprint(rules)

    eval_rule_func = lambda rule: evalRule(kb, rule)
    # print('>>>> Epoch Start')
    # print('Input KB')
    # print(kb)
    flattened_rules = list(concatMap(eval_rule_func, rules))
    kb_flattened_rules = kb + flattened_rules
    # print('Output KB')
    # print(kb_flattened_rules)
    # print('<<<< Epoch Stop')
    # print('Result')
    # pprint(kb_flattened_rules)
    return nub(kb_flattened_rules)


###############################################

"""
query :: String -> Program -> [ Substitution ]
query predSym pr =
  case queryVarsL of
    [ queryVars ] -> zip queryVars <$> relevantKnowledgeBaseSyms
    [] -> error $ "The query '" ++ predSym ++ "' doesn't exist."
    _  -> error $ "The query '" ++ predSym ++ "' has multiple clauses."
  where
  relevantKnowledgeBase = filter ((== predSym) . _predSym) $ solve pr
  relevantKnowledgeBaseSyms = _terms <$> relevantKnowledgeBase

  queryRules = filter ((== predSym) . _predSym . _head) pr
  queryVarsL = _terms . _head <$> queryRules
"""


def query(predSym: str, pr: Program) -> List[Substitution]:
    _get_rules: Callable[[Rule], bool] = lambda rule: rule._head._predSym == predSym
    queryRules = list(filter(_get_rules, pr))
    queryVarsL = list(map(lambda rule: rule._head._terms, queryRules))
    relevantKnowledgeBase = list(filter(lambda x: x._predSym == predSym, solve(pr)))

    # relevantKnowledgeBaseSyms = list(map(lambda x: x._terms, relevantKnowledgeBase))

    _relevantKnowledgeBaseSyms = list(map(lambda x: x._terms, relevantKnowledgeBase))
    print("_relevant knowledge based syms!")
    print(_relevantKnowledgeBaseSyms)
    relevantKnowledgeBaseSyms = list(
        filter(lambda t: not isinstance(t[0], Var), _relevantKnowledgeBaseSyms)
    )
    print(relevantKnowledgeBaseSyms)

    if queryVarsL:
        if len(queryVarsL) == 1:
            queryVars = queryVarsL[0]
            zipper = lambda y: list(zip(queryVars, y))

            return list(map(zipper, relevantKnowledgeBaseSyms))
            pass
        else:
            raise ValueError(f"The query:{predSym} has multiple clauses")
            pass
    else:
        raise ValueError(f"The query:{predSym} does not exist")
    pass

    # def ancestor():
    #     raw_facts = [
    #         [Sym("Andrew Rice"), Sym("Mistral Contrastin")],
    #         [Sym("Dominic Orchard"), Sym("Mistral Contrastin")],
    #         [Sym("Andy Hopper"), Sym("Andrew Rice")],
    #         [Sym("Alan Mycroft"), Sym("Dominic Orchard")],
    #         [Sym("David Wheeler"), Sym("Andy Hopper")],
    #         [Sym("Rod Burstall"), Sym("Alan Mycroft")],
    #         [Sym("Robin Milner"), Sym("Alan Mycroft")]
    #     ]
    #     facts = [Rule(Atom('adviser', terms), []) for terms in raw_facts]
    #     #     [ Rule (Atom "academic_ancestor" [ Var "X", Var "Y" ])
    #     #       [ Atom "adviser" [ Var "X", Var "Y" ] ]
    #     #   , Rule (Atom "academic_ancestor" [ Var "X", Var "Z" ])
    #     #       [ Atom "adviser"          [ Var "X", Var "Y" ]
    #     #       , Atom "academic_ancestor" [ Var "Y", Var "Z" ] ]
    #     #   ]
    #     ancestor_pred = "academic_ancestor"
    #     adviser_pred = "adviser"
    #     X = Var("X")
    #     Y = Var("Y")
    #     Z = Var("Z")
    #     Intermediate = Var('Intermediate')
    #     academic_ancestor = lambda a, b: Atom(ancestor_pred, [a, b])
    #     adviser = lambda a, b: Atom(adviser_pred, [a, b])
    #
    #     base_rule = Rule(academic_ancestor(X, Y), [adviser(X, Y)])
    #     recursive_rule = Rule(academic_ancestor(X, Z), [adviser(X, Y), academic_ancestor(Y, Z)])
    #     rules = [base_rule, recursive_rule]
    #
    #     #   -- Queries
    #     #   [ Rule (Atom "query1" [ Var "Intermediate" ])
    #     #       (fmap (Atom "academic_ancestor")
    #     #         [ [ Sym "Robin Milner", Var "Intermediate" ]
    #     #         , [ Var "Intermediate", Sym "Mistral Contrastin" ] ])
    #     #   , Rule (Atom "query2" [ ])
    #     #       [ Atom "academic_ancestor"
    #     #           [ Sym "Alan Turing", Sym "Mistral Contrastin" ] ]
    #     #   , Rule (Atom "query3" [ ])
    #     #       [ Atom "academic_ancestor"
    #     #           [ Sym "David Wheeler", Sym "Mistral Contrastin" ] ]
    #     #   ]
    #     raw_valids = [[Sym("Robin Milner"), Var("Intermediate")],
    #                   [Var("Intermediate"), Sym("Mistral Contrastin")]]
    #     valid_ancestors = [academic_ancestor(a, b) for a, b in raw_valids]
    #
    #     invalid_ancestors = [academic_ancestor(Sym("Alan Turing"), Sym("Mistral Contrastin"))]
    #
    #     queries = [Rule(Atom("query1", [Intermediate]), valid_ancestors),
    #                Rule(Atom("query2", []), invalid_ancestors)]
    #
    #     return facts + rules + queries


X = Var("X")
Y = Var("Y")
Z = Var("Z")
Intermediate = Var("Intermediate")

ancestor_pred = "academic_ancestor"
adviser_pred = "adviser"

academic_ancestor = lambda a, b: Atom(ancestor_pred, [a, b])
adviser = lambda a, b: Atom(adviser_pred, [a, b])

base_rule = Rule(academic_ancestor(X, Y), [adviser(X, Y)])


def simple_ancestor():
    raw_facts = [
        [Sym("Alan Mycroft"), Sym("Dominic Orchard")],
        [Sym("Robin Milner"), Sym("Alan Mycroft")],
    ]
    facts = [Rule(Atom("adviser", terms), []) for terms in raw_facts]

    recursive_rule = Rule(
        academic_ancestor(X, Z), [adviser(X, Y), academic_ancestor(Y, Z)]
    )
    rules = [base_rule, recursive_rule]

    raw_valids = [
        [Sym("Robin Milner"), Var("Intermediate")],
        [Var("Intermediate"), Sym("Dominic Orchard")],
    ]
    valid_ancestors = [academic_ancestor(a, b) for a, b in raw_valids]

    invalid_ancestors = [
        academic_ancestor(Sym("Alan Turing"), Sym("Mistral Contrastin"))
    ]

    queries = [Rule(Atom("query1", [Intermediate]), valid_ancestors)]

    return facts + rules + queries


def person_query():
    # Facts
    # Male('Rajiv')_
    facts = [Rule(Atom("Male", [Sym("Rajiv")]), [])]
    # Rules
    X = Var("X")
    person = lambda a: Atom("Person", [a])
    male = lambda a: Atom("Male", [a])
    # print('Person')
    # print(person(X))
    # person(X) <= male(X)
    person_rule = lambda a: Rule(person(a), [male(a)])
    rules = [person_rule(X)]
    # print('Person Rule')
    # print(person_rule(X))
    # query1(X) <= person(X)
    query1_rule = Rule(Atom("query1", [X]), [person(X)])
    queries = [query1_rule]

    return facts + rules + queries


if __name__ == "__main__":
    # print('-------Query1-------')
    print(query("query1", person_query()))
    # Eval Rule
    # query1(Intermediate) <= academic_ancestor("Robin Milner",Intermediate),academic_ancestor(Intermediate,"Dominic Orchard")
    # Knowledge Base
    # [adviser("Alan Mycroft","Dominic Orchard"), adviser("Robin Milner","Alan Mycroft"), academic_ancestor(X,Y), academic_ancestor(X,Z), query1(Intermediate), academic_ancestor("Alan Mycroft","Dominic Orchard"), academic_ancestor("Robin Milner","Alan Mycroft"), academic_ancestor("Alan Mycroft",Z), academic_ancestor("Robin Milner",Z)]
    # Walk List
    # [[(Intermediate, "Robin Milner")]]
    # query1 = lambda x: Atom("query1", [x])
    # kb = [adviser("Alan Mycroft", "Dominic Orchard"), adviser("Robin Milner", "Alan Mycroft"), academic_ancestor(X, Y),
    #       academic_ancestor(X, Z), query1(Intermediate), academic_ancestor("Alan Mycroft", "Dominic Orchard"),
    #       academic_ancestor("Robin Milner", "Alan Mycroft"), academic_ancestor("Alan Mycroft", Z),
    #       academic_ancestor("Robin Milner", Z)]
    # atoms = [academic_ancestor("Robin Milner", Intermediate), academic_ancestor(Intermediate, "Dominic Orchard")]
    # print(walk(kb, atoms))

    pass
