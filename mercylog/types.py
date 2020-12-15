from abc import ABC
from dataclasses import dataclass
from pyrsistent import pvector
from pyrsistent.typing import PVector
from typing import *
from returns.result import Result, Success, Failure
from mercylog.lib import util
from fastcore import all as fc
"""
Glossary:
^^^^^^^^^
**Closed World Assumption**:
The database records some facts about the world. It's possible that we have only partial data about the problem we are trying to model. Some facts may not have been recorded(e.g. failed to be measured or reported). We make a simple assumption that any fact not reported is treated as have not happened. For e.g.
if we are considering a database of marriage facts .e.g marriage('John', 'Mary') and marriage('Bale', 'Sarah'), then if in the real world there was a marriage between Akshay and Sana and it wasn't recorded, then we assume that there was no marriage between Akshay and Sana.

Thus the database is treated as if it has complete information about the world.



**Functional Dependency**:
A functional dependency (FD) is a relationship between two attributes, typically between the primary key and other non-key attributes within a table.
For any relation R, attribute Y is functionally dependent on attribute X (usually the primary key), if for every valid instance of X,
that value of X uniquely determines the value of Y. This relationship is indicated by the representation below :

X ———–> Y

The left side of the above FD diagram is called the determinant, and the right side is the dependent. Here are a few examples.

In the first example, below, SIN determines Name, Address and Birthdate. Given SIN, we can determine any of the other attributes within the table.
SIN   ———-> Name, Address, Birthdate

For the second example, SIN and Course determine the date completed (DateCompleted). This must also work for a composite primary key.
SIN, Course  ———>     DateCompleted

The third example indicates that ISBN determines Title.
ISBN  ———–>  Title
https://opentextbc.ca/dbdesign01/chapter/chapter-11-functional-dependencies/


**Function Symbol**

Datalog has relations with terms that can either be a Symbol(e.g. a string "Toronto") or a logical variable representing symbols. So one can define relations like father("Willy", "Bob") i.e. "Willy"
is the father of "Bob" or father(X,"Bob").  The possible values are fixed as they are values in a datastore.
A function symbol allows us to create hypothetical values so the range of values can be infinite. Consider the following example, where we define what it means for a number `x` to be less than equal to `y`, i.e. `leq(x, y)`:


leq(0, x) ←
leq(next(x), next(y)) ← leq(x, y)
leq(x, +(x, y)) ←
leq(x, z) ← leq(x, y), leq(y, z)

 `next` stands for the successor function i.e. `next(0) = 1`, `next(2)=3`. The function symbols here are `next`, `+`

Function symbols have a `free` interpretation - two terms are considered non equal if they are syntactically different. For e.g. the terms `+(0, next(0))`, `+(next(0), 0)` and `next(0)` though mean the same are non equal.

Function symbols are used in logic programming to
- make certain code more readable and concise,
- allow us to model intricate data structures likes lists and trees and 
- model infinite values

Datalog classically does not support function symbols because it can lead to an infinite set of values and hence not terminate.

However Prolog has function symbols. 

Ref: 
https://artint.info/html/ArtInt_288.html

https://www.cs.toronto.edu/~bonner/courses/2016f/csc324/slides/prolog4a.pdf

Chapter 5 of Greco Book is Function Symbols :)

https://www.seas.harvard.edu/courses/cs152/2014sp/lectures/lec23-prolog.pdf
https://www.cs.cmu.edu/~fp/courses/lp/lectures/26-datalog.pdf
https://www.seas.harvard.edu/courses/cs152/2016sp/lectures/lec19-logicprogramming.pdf


**Ground**

A term or atom is ground if no variables appear in it.
**Declarative Language**:
A language in which the program can be specified in a high level manner as a specification which allows the interpreter to choose different execution and optimization strategies.
"""

Error = str


class Term(ABC):
    """
    Also called attribute in relational programming
    The set from which it can take values is called it's domain
    E.g. A term can be the value 4 from the domain of integers
    """

    pass


@dataclass(frozen=True)
class Variable(Term):
    # Also called term
    name: str

    def __repr__(self):
        return self.name


# v = Variable

_ = Variable("_")
def variables(*names: str) -> Union[Variable, List[Variable]]:
    if len(names) == 0:
        return ValueError("Atleast one name required")
    elif len(names) == 1:
        return Variable(names[0])
    else:
        return [Variable(n) for n in names]



# def __init__(self, name, *variables):
#     self.name = name
#     self._variables = variables

# def __le__(self, body: Union[List, Any]):
#     if isinstance(body, List):
#         b = Facts(*body)
#     else:
#         b = body
#     return Rule(self, b)

# def variables(self):
#     return self._variables

# def get_clause(self):
#     return self.relation_x()

# def relation_x(self):
#     var_strs = []
#     # TODO: Duplicate isinstance check
#     for v in self.variables():
#         if isinstance(v, str):
#             x = f'"{v}"'
#         else:
#             x = str(v)

#         var_strs.append(x)
#     a_str = ','.join(var_strs)
#     return self.name + '(' + a_str + ')'

# def relation(self):
#     return self.relation_x()

# def __invert__(self):
#     return InvertedRelationInstance(self)
#     pass


@dataclass(frozen=True)
class Relation:
    """
    A relation is a like a table in a SQL database. An instance of a relation is called a record

    Also called Atom in Datalog terminology
    Note also that in the context of logic-based languages, a relation's name is also called it's _predicate_
    """

    name: str
    terms: Tuple[Term]

    def __le__(self, body: Union[List, "Relation"]):
        if isinstance(body, List):
            _b = body
            pass
        else:
            _b = [body]

        head_relation = Relation(self.name, self.terms)
        return Rule(head_relation, set(_b))

    def __repr__(self):
        term_str = ", ".join([str(t) for t in self.terms])
        return f"{self.name}({term_str})"

    pass

    def variables(self) -> Sequence[Variable]:
        return [v for v in self.terms if isinstance(v, Variable)]

    def __invert__(self):
        return InvertedRelationInstance(self)
        pass


class InvertedRelationInstance(object):
    def __init__(self, relation_instance):
        self.relation_instance = relation_instance
        pass

    def get_clause(self) -> str:
        return "not " + self.relation_instance.get_clause()

    def relation(self) -> str:
        return self.get_clause()

    def variables(self):
        return self.relation_instance.variables()

@dataclass(frozen=True)
class RelationCreator:
    """
    It allows us to do:
    X = Variable('X')
    person = relation('person')
    person(X) # <----- This
    """

    # Also called predicate
    name: str

    def __call__(self, *terms, **kwargs) -> Relation:
        _terms = tuple([t for t in terms])
        return Relation(self.name, _terms)


@dataclass(frozen=True)
class Rule:
    """
    A Datalog rule r is a logic program rule of the form:
    R0 <- R1, R2, ... Rn. where n >= 0
    Ri are relations where no function symbols appears
    R0 is called the head
    R1, R2.. Rn is called the body

    The meaning of the above rule is if R1,R2...Rn is true, then R0 is true.

    """

    head: Relation
    body: Set[Relation]

    def __repr__(self):
        body = ",".join([str(b) for b in self.body])
        return f"{self.head} <= {body}"


def is_safe(head: Relation, body: Sequence[Relation]) -> bool:
    """
      Every variable appearing in the head should also appear in at least one of the atoms in the body.
        This requirement is called the safety requirement and is used to avoid rules yielding infinite relations from
        finite ones.

    """
    head_vars = head.variables()
    body_vars = util.flatten(relation.variables() for relation in body)

    return set(head_vars).issubset(body_vars)


class Fact:
    """
    A fact is a ground rule with an empty body. We call it a p-fact if p is the predicate symbol in the head.
    For simplicity, we just write a fact as A0 instead of A <-. i.e. dropping the <- symbol.
    """


def relation(predicate: str) -> RelationCreator:
    return RelationCreator(predicate)

class BinaryUnifier:
    def __init__(self, x, y):
        # fc.store_attr()
        self.x = x
        self.y = y
    pass

class BinaryDisunifier:
    def __init__(self, x, y):
        # fc.store_attr()
        self.x = x
        self.y = y


# def run(data_source: DataSource, program: Program, query: Query):


class DataSource:
    pass


class Program:
    pass


class Query:
    pass


class KnowledgeBase:
    """
    It is the union of the the Extensional Database(EDB)(base) and the Intensional Database(IDB)(derived). We will refer to EDB
    as the database D and the IDB as the program P

    Checks to make:
    - Base predicate symbols can appear in the body of rules in P but not in the head. 
    - Derived predicate symbols cannot appear in D and their definition is in P .
    """

    pass


# def require(success: bool, error_message: str) -> Union[bool, str]:
#     if success:
#         return error_message
#     else:
#         return False

def eq(x, y) -> BinaryUnifier:
    return BinaryUnifier(x, y)

def not_eq(x, y) -> BinaryDisunifier:
    return BinaryDisunifier(x, y)

if __name__ == '__main__':
    b = BinaryUnifier("r", "x")
    print(b.x)