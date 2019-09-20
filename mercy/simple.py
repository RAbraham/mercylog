from dataclasses import dataclass
from abc import ABC
from typing import *

'''


Another appeal of Datalog can be seen in these queries. Datalog is mostly relations (hence the name relational programming). This means there are no inherent inputs and outputs. That’s why we can fill in or leave out either parameter of academicAncestor. You leave a variable in place of the knowledge you want to know and the system fills it for you. This also means you can write a program for a particular input and output relationship in mind and you get the opposite program for free.



data_source Rule = Rule { _head :: Atom, _body :: [ Atom ] }
data_source Atom = Atom { _predSym :: String, _terms :: [ Term ] } deriving Eq
data_source Term = Var String | Sym String deriving Eq
The following rule
'''


class Term(ABC):
    pass


@dataclass
class Sym(Term):
    term: str


@dataclass
class Var(Term):
    term: str


@dataclass
class Atom(object):
    _predSym: str
    _terms: List[Term]


@dataclass
class Rule(object):
    _head: Atom
    _body: List[Atom]


'''
type Program = [ Rule ]
We also need a way of representing the known facts about the universe. We can call this our knowledge base. For simplicity, we use a horribly inefficient list of atoms.

type KnowledgeBase = [ Atom ]
Since we’ll use substitutions to evaluate atoms, we can define that here too.
'''


@dataclass
class Program:
    rules: List[Rule]


@dataclass
class KnowledgeBase:
    atoms: List[Atom]


'''
type Substitution = [ (Term, Term) ]
Our substitutions are simpler than those that are used in λ-calculus. A Haskell tuple (x,c) represents the substitution [c/x] meaning we replace c for x. Here, x is always a variable and c is always a constant (symbol). The variable restriction is usual; it is just not reflected in the type. The constant restriction, however, is not. Datalog doesn’t have function symbols and substituting a variable is not necessary for its evaluation. Like the variable restriction, the constant restriction is also not reflected in the type.

Applying a substitution to an atom or a variable (potentially) makes it ground that is it replaces the variable with a constant.

We can also define the only constant that will be used in the evaluator: the empty substitution.

emptySubstitution :: Substitution
emptySubstitution = []
Mind-blowing, I know.
'''


@dataclass
class Substitution:
    substitutions = List(Tuple(Term, Term))


def emtpy_substitution() -> List[Term]:
    return []


'''
One rule at a time
Let’s focus on evaluating a single rule from our example program.

academicAncestor(X,Z) :- adviser(X,Y), academicAncestor(Y,Z).
We know some facts about the world and using this rule, we want to know some more. There are two ways. One is to gather everything we know about adviser and academicAncestor separately and join them together making sure the second parameter (Y) of adviser matches the first parameter (Y) of academicAncestor. Another way is to look at any one of the atoms and find assignments to its variables and substitute them in the other atom, only then we look for assignments to the remaining variables of this second atom. This approach would work for the example above as follows: find possible assignments to X and Y through adviser, substitute the values of Y in academicAncestor, and finally look for values of academicAncestor in the knowledge base that agree on the newly substituted value of Y to obtain values for Z.

In the context of databases, the first is called join-before-select and the second, not so surprisingly, select-before-join. We’ll implement the latter because it is simpler.2

Since we need unification to obtain substitutions from facts & body atoms and substitution to ground further atoms. We start by implementing those.

substitute :: Atom -> Substitution -> Atom
substitute atom substitution = atom { _terms = map go (_terms atom) }
  where
  go sym@Sym{} = sym
  go var@Var{} = fromMaybe var (var `lookup` substitution)
Substitution is pretty much what you would expect looking up what to substitute for variables and do it whenever it can find a binding otherwise leaving the variable alone.
'''

from multipledispatch import dispatch
from toolz.curried import *


@dispatch(Substitution, Sym)
def go_sub(substitution, symbol):
    return symbol.term


@dispatch(Substitution, Var)
def go_sub(substitution, var):
    # go var@Var{} = fromMaybe var (var `lookup` substitution)
    # Function:	lookup
    # Type:	Eq a => a -> [(a,b)] -> Maybe b
    values = [v for v in substitution if v[0].term == var.term]
    if values:
        value = values[0]
    else:
        value = None
    if value:
        return value
    else:
        return var


def substitute(atom: Atom, substitution: Substitution) -> Atom:
    go_c = curry(go_sub, substitution)
    new_terms = map(go_c, atom._terms)
    return Atom(atom._predSym, new_terms)


'''
unify :: Atom -> Atom -> Maybe Substitution
unify (Atom predSym ts) (Atom predSym' ts')
  | predSym == predSym' = go $ zip ts ts'
  | otherwise           = Nothing
  where
  go :: [ (Term, Term) ] -> Maybe Substitution
  go []                           = Just emptySubstitution
  go ((s@Sym{}, s'@Sym{}) : rest) = if s == s' then go rest else Nothing
  go ((v@Var{}, s@Sym{})  : rest) = do
    incompleteSubstitution <- go rest
    case v `lookup` incompleteSubstitution of
      Just s' | s /= s'   -> Nothing
      _                   -> return $ (v,s) : incompleteSubstitution
  go ((_, Var{}) : _) = error "The second atom is assumed to be ground."
Unification is also simple, in fact, too simple. For one thing, we cheat and unify whenever we have two atoms that have the same predicate symbol. In Datalog, a predicate is determined by its predicate symbol and arity (the number of terms). Here, we assume each predicate symbol determines the arity. More importantly, we throw an error when a term from the second atom is a variable. The reason is unification only occurs between a body atom and a fact. Since facts cannot have variables, this is safe. This is consistent with our earlier assumptions about the form of substitutions.
'''


def unify(atom1: Atom, atom2: Atom):
    predSym = atom1._predSym
    predSym_dash = atom2._predSym
    ts = atom1._terms
    ts_dash = atom2._terms

    if predSym == predSym_dash:
        zipped = list(zip(ts, ts_dash))
        return go_unify(zipped)

    else:
        return None
    pass


def go_unify(zipped: List[Tuple[Term, Term]]):
    if not zipped:
        return emtpy_substitution()

    first_tuple = zipped[0]
    left = first_tuple[0]
    right = first_tuple[1]
    if isinstance(left, Sym) and isinstance(right, Sym):
        s = left.term
        sdash = right.term
        if s == sdash:
            return go_unify(zipped[1:])
        else:
            return []
    # TODO if left is var and right is symbol as below
    if isinstance(left, Var) and isinstance(right, Sym):
        incomplete_substitution = go_unify(zipped[1:])
        vn = [v for v in incomplete_substitution if v[0] == left.term]
        if vn:
            v = vn[0]
            if v.term != right.term:
                return []
            else:
                return [(left, right)] + incomplete_substitution
        else:
            return [(left, right)] + incomplete_substitution

    if isinstance(left, Var) and not isinstance(right, Sym):
        raise ValueError('The second atom is assumed to be ground.')


'''
We take special care of unification of atoms with repeated variables. It requires failing in case of a contradictory variable assignment. Consider unifying p(X,X) with p("a","b").

Next we evaluate an atom into a list of substitutions by finding facts that fit the template provided by a body atom and capturing the assignments to its variables. Those assignments to variables are just the substitutions we are looking for.

evalAtom :: KnowledgeBase -> Atom -> [ Substitution ] -> [ Substitution ]
evalAtom kb atom substitutions = do
  substitution <- substitutions
  let downToEarthAtom = substitute atom substitution
  extension <- mapMaybe (unify downToEarthAtom) kb
  return $ substitution <> extension
Here we do exactly what is described above but build the substitutions by accumulation. This means we have substitutions that we use on the body atom to ground its variables, but then unifying this more down to earth atom (it’s more ground, get it?) with the facts we know gives us extensions to the substitution we started with. Thus, we extend and accumulate substitutions.

'''


def eval_atom(kb: KnowledgeBase, atom: Atom, substitutions: List[Substitution]):
    final_result = []
    for substitution in substitutions:
        down_to_earth_atom = substitute(atom, substitution)
        extensions = []
        for atom in kb.atoms:
            u = unify(down_to_earth_atom, atom)
            if u:
                extensions.append(u)

        result = [substitution] + extensions
        final_result = final_result + result

    return final_result


'''
Now all we need to do is to walk the body and accumulate substitutions, then using these substitutions we deduce new facts based on the head of the rule.

walk :: KnowledgeBase -> [ Atom ] -> [ Substitution ]
walk kb = foldr (evalAtom kb) [ emptySubstitution ]

evalRule :: KnowledgeBase -> Rule -> KnowledgeBase
evalRule kb (Rule head body) = map (substitute head) (walk kb body)
Here’s something to think about. We said the facts we deduce will be ground, but evalRule does not check if the substitution has a binding for all the variables that appear in the head. Does that mean we are potentially concluding non-ground facts? Don’t worry if you’re not sure, we’ll come back to it below.
'''

import operator
import functools

foldr = lambda func, acc, xs: functools.reduce(lambda x, y: func(y, x), xs[::-1], acc)


def walk(kb: KnowledgeBase, atoms: List[Atom]) -> List[Substitution]:
    from toolz import curry
    eval_atom_func = curry(eval_atom, kb)
    foldr eval_atom_func [emtpy_substitution()]
    pass



'''
All at once
All we need now is to evaluate all of the rules together. We’ll do one of the simplest possible things. We’ll evaluate each rule independently and then concatenate the newly derived facts together and bundle them with what we already know. Then repeat the process until we can’t produce new facts any more.

immediateConsequence :: Program -> KnowledgeBase -> KnowledgeBase
immediateConsequence rules kb =
  nub . (kb <>) . concatMap (evalRule kb) $ rules

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
The immediateConsequence function does the bundling step and solve computes the fixpoint from an empty set of facts.

The only thing left unexplained is the isRangeRestricted predicate which ensures the program is well-formed.

Semantic considerations
Now that we have something that almost compiles we can talk about semantics. Starting with the last missing piece: the range restriction predicate followed by termination.

Range restriction and domain independence
In a rule, if every variable in the head appears somewhere in the body, we call the rule range-restricted. We check if every rule is range-restricted before evaluating them in solve.3 This is why we didn’t have to check if there were any variables left in the head after substitution in evalRule. If we can get to the stage of substituting into head, we are guaranteed to find values for each head variable.

isRangeRestricted :: Rule -> Bool
isRangeRestricted Rule{..} =
  vars _head `isSubsetOf` concatMap vars _body
  where
  isSubsetOf as bs = all (`elem` bs) as
  vars Atom{..} = nub $ filter (\case {Var{} -> True; _ -> False}) _terms
There still remains the question of why we need range restriction at all? After all, the ability to deduce generic facts seems useful. For example, stating p(X,X) as a fact is a compact way of saying p is reflexive.

The problem is something called domain independence. It basically means if the set of values a variable can take changes from one database to another (but not the instance itself), queries still compute the same thing. In other words, it prevents your program’s result to change under your feet if the values in your database are the same. Since checking domain independence in general is undecidable, range restriction is a safe syntactic approximation.

In this implementation what this means is if I change the definition of datatype Term so that the symbols do not use String but instead a type for strings up to length 10, if my initial ground facts were all strings of length up to 10, then the results to all queries remain the same. We can’t guarantee the same thing without domain independence.

Another problem is that when a query is posed with free variables, we expect values to be filled for that variable. If we can deduce a generic fact such as p(X,X), then asking for the values of X would enumerate the set of infinite strings.

Bear in mind, there are Datalog variants that lift this restriction. In fact, it wouldn’t be too much work to implement it here. We just need a notion of α-equivalence, a store that can handle non-ground values, and a unification algorithm that handles variables.

Every good thing must come to an end
Does this procedure terminate? Yes, it does. When? So long as you don’t have infinite programs. It would be a cheeky thing to do though. One of the appeals of Datalog is that it is not Turing-complete and every query to the system terminates.

The termination argument is pretty simple. Immediate consequence function is monotone that is the facts it produces encompasses the facts it starts with. Further, the number of facts that can be produced is bounded if we start with a finite database. Our initial set of facts used to kick-start solve is empty. Hence, as long as our program is finite, we have finite number of facts.4 As an upper bound, if we have N constants throughout the program, then for each relation of arity k, we can have at most Nk facts. So the number of facts we can produce is also finite.

One place I’m being a bit loose is the monotone bit. What I said makes sense with sets, but we’re working here with lists. Although [1,2,3] and [2,1,3] encompass each other, they don’t compare equal using ==. The reason this implementation never gets in a cycle is because nub function called on the amalgamation of facts in immediateConsequence preserves the first occurrence of each element in the list. Since we prepend the already known facts before calling nub, == behaves as if it is set equality.

If you want to sound smart explaining all of this and reduce the size of your audience to a group of people who would understand this without you mentioning anyway, you can just say the following. We have a non-empty finite lattice which means it is complete and Knaster-Tarski theorem (which is a very cool theorem ❤️) applied to the immediate consequence monotone function over this complete lattice implies that it has a least fixpoint.

Quality assurance
Time for the litmus test. We can now translate the ancestry program into Haskell.

ancestor :: Program
ancestor =
  -- Facts
  fmap (\terms -> Rule (Atom "adviser" terms) [])
    [ [ Sym "Andrew Rice",     Sym "Mistral Contrastin" ]
    , [ Sym "Dominic Orchard", Sym "Mistral Contrastin" ]
    , [ Sym "Andy Hopper",     Sym "Andrew Rice" ]
    , [ Sym "Alan Mycroft",    Sym "Dominic Orchard" ]
    , [ Sym "David Wheeler",   Sym "Andy Hopper" ]
    , [ Sym "Rod Burstall",    Sym "Alan Mycroft" ]
    , [ Sym "Robin Milner",    Sym "Alan Mycroft" ]
    ] <>
  -- Actual rules
  [ Rule (Atom "academicAncestor" [ Var "X", Var "Y" ])
      [ Atom "adviser" [ Var "X", Var "Y" ] ]
  , Rule (Atom "academicAncestor" [ Var "X", Var "Z" ])
      [ Atom "adviser"          [ Var "X", Var "Y" ]
      , Atom "academicAncestor" [ Var "Y", Var "Z" ] ]
  ] <>
  -- Queries
  [ Rule (Atom "query1" [ Var "Intermediate" ])
      (fmap (Atom "academicAncestor")
        [ [ Sym "Robin Milner", Var "Intermediate" ]
        , [ Var "Intermediate", Sym "Mistral Contrastin" ] ])
  , Rule (Atom "query2" [ ])
      [ Atom "academicAncestor"
          [ Sym "Alan Turing", Sym "Mistral Contrastin" ] ]
  , Rule (Atom "query3" [ ])
      [ Atom "academicAncestor"
          [ Sym "David Wheeler", Sym "Mistral Contrastin" ] ]
  ]
We can make querying a bit more pleasant with a function that returns possible bindings.

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
All it does it to run the program, find the named query and return the bindings to its arguments. Let’s execute all three queries.

> query "query1" ancestor
[[(Intermediate,"Dominic Orchard")],[(Intermediate,"Alan Mycroft")]]
> query "query2" ancestor
[]
> query "query3" ancestor
[[]]
The empty list of variable bindings, [], mean there are no possible assignments that satisfy the query, whereas the singleton empty binding, [[]], means the query is satisfied. It just didn’t have any variables that need to be bound to values.

All three queries return the expected results. Dominic Orchard and Alan Mycroft are between me and Robin Milner. I am not an academic descendant of Alan Turing, but I am of David Wheeler.

Since these three queries run fine, we can safely conclude that the evaluator here is bug-free.

Addressing the turtle in the room
As I mentioned before, this evaluator is inefficient. Discussing the reasons why and what we can do to make it better is not only a software engineering exercise, but also another way of highlighting why Datalog is a good language. The optimisations I discuss here are quite major, but they are not a complete list. There are many other optimisations that draw both from programming languages and database theory literatures.

Optimise for the query
Basically, all I told you about Datalog semantics is incomplete. You’ll struggle to find a resource that discusses Datalog evaluation the way I do because the semantics are always defined with respect to a query. So what we really need is a program query pair. What we compute here is much stronger and is also unnecessary. For example, if the queries were interested only in the adviser relation, computing academicAncestors would be a waste of time.

One way of dealing with this is to use a top-down evaluator which starts from the query and uses resolution which is a proof technique. This allows only the relevant facts to be derived. Most Prolog interpreters use a similar top-down evaluation strategy. It is not preferred in Datalog for various reasons. One of which is that the naïve implementation of it brings non-termination.

We can achieve the same in a bottom-up evaluator (like ours) using magic set transformation. The very long story short, based on the input program, it generates magic rules based on the dataflow of the program and inserts atoms defined by these rules into the original rule bodies to restrict what can be derived. Its effectiveness varies from program to program and there are alternatives to it. If you want to learn more about it, you can look at On the Power of Magic (you must admit, it is a catchy title) by Beeri and Ramakrishnan.

Semi-naïve evaluation
While discussing range restriction, we mentioned that this implementation rederives all the known facts in each iteration. This is awful and is why it is called the naïve evaluation. There is also a modestly named semi-naïve evaluation. It exploits a simple observation. In order to derive a new fact from a rule, at least one new fact of the previous iteration needs to be used.

The way this gets implemented is that we maintain a delta of facts as well as an accumulator and rewrite the rules to make versions of them that use the deltas.

This is particularly effective for the so called linear rules such as the recursive academicAncestor rule which only has one derived predicate in its body. In that case, the semi-naïve evaluation turns a quadratic computation into a linear one.

Incremental evaluation
Datalog is amenable to incremental evaluation. Even in this version of the evaluator, you can see that when a fixpoint is reached, we can enrich the resulting knowledge base with additional facts and apply the fixpoint algorithm again. This performs at least as good as starting from scratch and often much much better.

The situation gets more complicated when there is negation in the language because additional facts invalidate facts that depend on the negation of those facts. This is a particular instance of non-monotonic reasoning. However, Datalog, overall, is still a good language if you’re after incremental evaluation.

Furthermore, the idea of incremental evaluation is intricately connected with maintaining a delta of facts. If your evaluator uses semi-naïve evaluation already, having an incremental evaluator is not much extra effort.

Data structures
Using lists to compute over sets is a bad idea. Depending on the application, hash tables, proper databases, in memory key-value stores, or at the very least of Set and Map modules from the containers package will certainly make things better. Use of sets in general is a good idea because then we don’t have to rely on nub function’s internals for termination as discussed earlier.

Dependency graphs
We evaluate all rules in one pot but that is also very inefficient. We can partition the program by determining dependencies between predicates. This allows us to treat evaluated dependencies as static knowledge, so we have to deal with a smaller collection of changing facts at any one time.

For example in the ancestor program, we would have a graph with adviser and academicAncestor nodes where the former points to the latter and the latter loops around. Meaning we can compute the fixpoint for adviser rules first, then forget about those rules and compute the fixpoint of academicAncestor.

Also if your Datalog variant has stratified negation which is a popular way of incorporating negated atoms, you already have to do the dependency analysis and partition your program. So engineering-wise, this optimisation comes for free.

Parallelisation & distributed computation
Datalog evaluation is great for data_source-parallel computation. Even by inspecting our implementation, it is evident that evaluating all the rules in a given iteration is an embarrassingly parallel problem. The dependency graph can be used to further parallelise the evaluation using work queues. Similarly, the workload can be separated over multiple machines, a bit like MapReduce.

Closing remarks
Short program, long prose is the theme. I hope I managed to give some ideas about how Datalog works. I tried to squeeze in as much semantics and tips for more efficient implementation as possible which is probably more useful than a short program.

If you want to look at Datalog further. Soufflé is a modern variant geared towards program analysis and is blazingly fast.

If you are interested in a more formal treatment of Datalog as well as some of the optimisations I mentioned chapters 12 to 15 of Foundations of Databases by Abiteboul, Hull, and Vianu are probably the best resources which collect everything together in such detail and with modern exposition.

Full program
Here’s the full program for your convenience.

{-# LANGUAGE LambdaCase #-}
{-# LANGUAGE RecordWildCards #-}

module SimpleDatalog where

import Data.Function (fix)
import Data.List (nub, intercalate, isSubsequenceOf)
import Data.Maybe (mapMaybe, fromMaybe, isNothing)

type Program = [ Rule ]

data_source Rule = Rule { _head :: Atom, _body :: [ Atom ] }

data_source Atom = Atom { _predSym :: String, _terms :: [ Term ] } deriving Eq

data_source Term = Var String | Sym String deriving Eq

type KnowledgeBase = [ Atom ]

type Substitution = [ (Term, Term) ]

emptySubstitution :: Substitution
emptySubstitution = []

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

isRangeRestricted :: Rule -> Bool
isRangeRestricted Rule{..} =
  vars _head `isSubsetOf` concatMap vars _body
  where
  isSubsetOf as bs = all (`elem` bs) as
  vars Atom{..} = nub $ filter (\case {Var{} -> True; _ -> False}) _terms

immediateConsequence :: Program -> KnowledgeBase -> KnowledgeBase
immediateConsequence rules kb =
  nub . (kb <>) . concatMap (evalRule kb) $ rules

evalRule :: KnowledgeBase -> Rule -> KnowledgeBase
evalRule kb (Rule head body) = map (substitute head) (walk kb body)

walk :: KnowledgeBase -> [ Atom ] -> [ Substitution ]
walk kb = foldr (evalAtom kb) [ emptySubstitution ]

evalAtom :: KnowledgeBase -> Atom -> [ Substitution ] -> [ Substitution ]
evalAtom kb atom substitutions = do
  substitution <- substitutions
  let downToEarthAtom = substitute atom substitution
  extension <- mapMaybe (unify downToEarthAtom) kb
  return $ substitution <> extension

substitute :: Atom -> Substitution -> Atom
substitute atom substitution = atom { _terms = map go (_terms atom) }
  where
  go sym@Sym{} = sym
  go var@Var{} = fromMaybe var (var `lookup` substitution)

unify :: Atom -> Atom -> Maybe Substitution
unify (Atom predSym ts) (Atom predSym' ts')
  | predSym == predSym' = go $ zip ts ts'
  | otherwise           = Nothing
  where
  go :: [ (Term, Term) ] -> Maybe Substitution
  go []                           = Just emptySubstitution
  go ((s@Sym{}, s'@Sym{}) : rest) = if s == s' then go rest else Nothing
  go ((v@Var{}, s@Sym{})  : rest) = do
    incompleteSubstitution <- go rest
    case v `lookup` incompleteSubstitution of
      Just s' | s /= s'   -> Nothing
      _                   -> return $ (v,s) : incompleteSubstitution
  go ((_, Var{}) : _) = error "The second atom is assumed to be ground."

{-
- adviser("Andrew Rice",     "Mistral Contrastin").
- adviser("Dominic Orchard", "Andrew Rice").
- adviser("Andy Hopper",     "Andrew Rice").
- adviser("Alan Mycroft",    "Dominic Orchard").
- adviser("David Wheeler",   "Andy Hopper").
- adviser("Rod Burstall",    "Alan Mycroft").
- adviser("Robin Milner",    "Alan Mycroft").
-
- academicAncestor(X,Y) :- adviser(X,Y).
- academicAncestor(X,Z) :- adviser(X,Y), academicAncestor(Y,Z).
-
- ?- academicAncestor("Robin Milner", Intermediate),
-    academicAncestor(Intermediate, "Mistral Contrastin").
- ?- academicAncestor("Alan Turing", "Mistral Contrastin").
- ?- academicAncestor("David Wheeler", "Mistral Contrastin").
-}
ancestor :: Program
ancestor =
  -- Facts
  fmap (\terms -> Rule (Atom "adviser" terms) [])
    [ [ Sym "Andrew Rice",     Sym "Mistral Contrastin" ]
    , [ Sym "Dominic Orchard", Sym "Mistral Contrastin" ]
    , [ Sym "Andy Hopper",     Sym "Andrew Rice" ]
    , [ Sym "Alan Mycroft",    Sym "Dominic Orchard" ]
    , [ Sym "David Wheeler",   Sym "Andy Hopper" ]
    , [ Sym "Rod Burstall",    Sym "Alan Mycroft" ]
    , [ Sym "Robin Milner",    Sym "Alan Mycroft" ]
    ] <>
  -- Actual rules
  [ Rule (Atom "academicAncestor" [ Var "X", Var "Y" ])
      [ Atom "adviser" [ Var "X", Var "Y" ] ]
  , Rule (Atom "academicAncestor" [ Var "X", Var "Z" ])
      [ Atom "adviser"          [ Var "X", Var "Y" ]
      , Atom "academicAncestor" [ Var "Y", Var "Z" ] ]
  ] <>
  -- Queries
  [ Rule (Atom "query1" [ Var "Intermediate" ])
      (fmap (Atom "academicAncestor")
        [ [ Sym "Robin Milner", Var "Intermediate" ]
        , [ Var "Intermediate", Sym "Mistral Contrastin" ] ])
  , Rule (Atom "query2" [ ])
      [ Atom "academicAncestor"
          [ Sym "Alan Turing", Sym "Mistral Contrastin" ] ]
  , Rule (Atom "query3" [ ])
      [ Atom "academicAncestor"
          [ Sym "David Wheeler", Sym "Mistral Contrastin" ] ]
  ]

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
My impression is, as time goes on, λ-calculus variants try to tame λ-calculus (simply typed, linear, dependent, etc.) while Datalog variants (relaxed range-restriction, functional symbols, explicit quantification, etc.) let it run wild.↩

As it happens, select-before-join is usually (but certainly not always) the faster approach in real world. However, this doesn’t affect us at all because the performance benefit requires an indexed database for the columns that are grounded by substitution.↩

This is a simple check, but if we wanted, we could make it even neater. Range-restriction is something that can be baked into the Rule datatype using some dependent types. We would need to modify Atom to keep track of its variables, but it is doable. While at it we could also make substitutions keep track of their variables, which would enable us to enforce the assumptions about our substitutions. You see, this is my favourite kind of dependent types. It doesn’t give you full correctness, but eliminates a whole class of software bugs and potentially give you some performance boost. This may very well become a future blog post (famous last words on the topic).↩

Infinite programs are an interesting concept. I can’t think of any use for it though. Also evaluating them is tricky as you can’t traverse all your program statements, rules, etc. Notice that our Datalog evaluator wouldn’t be terminating not only because of a potential infinite facts problem, but because we try to evaluate each rule.↩

Site proudly generated by Hakyll
'''
