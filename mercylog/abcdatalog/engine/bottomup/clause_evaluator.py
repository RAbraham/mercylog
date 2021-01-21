from functools import partial
from typing import *
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.term_helpers import TermHelpers
from mercylog.abcdatalog.ast.visitors.crash_head_visitor import CrashHeadVisitor
from mercylog.abcdatalog.ast.visitors.crash_premise_visitor import CrashPremiseVisitor
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import (
    SemiNaiveClause,
)
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom, Annotation
from mercylog.abcdatalog.util.substitution.const_only_substitution import (
    ConstOnlySubstitution,
)
from mercylog.abcdatalog.util.substitution.term_unifier import TermUnifier


class LocalActionCrashPremiseVisitor(CrashPremiseVisitor):
    def __init__(self, get_facts, next_action):
        self.get_facts = get_facts
        self.next_action = next_action
        super(LocalActionCrashPremiseVisitor, self).__init__()

    def visit_annotated_atom(self, atom: AnnotatedAtom, i: int):
        def annotated_atom_func(s, next_action):
            #     s.resetState(i); // TODO is this necessary?
            s.resetState(i)
            facts: Iterator[PositiveAtom] = list(iter(self.get_facts(atom, s)))
            for fact in facts:
                s.resetState(i)
                if unifyAtomWithFact(atom.asUnannotatedAtom(), fact, s):
                    next_action(s)

        partial_annotated_atom_func = partial(
            annotated_atom_func, next_action=self.next_action
        )
        return partial_annotated_atom_func

    def visit_negated_atom(self, atom: NegatedAtom, i: int):
        def negated_func(s):
            _facts = self.get_facts(
                AnnotatedAtom(atom.asPositiveAtom(), Annotation.IDB), s
            )
            facts = list(iter(_facts))
            for fact in facts:
                s.resetState(i)
                if unifyAtomWithFact(atom.asPositiveAtom(), fact, s):
                    return
            self.next_action(s)

        return negated_func

    def visit_binary_unifier(self, u: BinaryUnifier, i: int):
        def binary_unifier_func(s):
            unify_func = get_unify_func(s)
            if unify_func(u.getLeft(), u.getRight(), s):
                self.next_action(s)

        return binary_unifier_func

    def visit_binary_disunifier(self, u: BinaryDisunifier, i: int):
        def binary_disunifier_func(s):
            unify_func = get_unify_func(s)
            if not unify_func(u.get_left(), u.get_right(), s):
                self.next_action(s)

        return binary_disunifier_func


def get_unify_func(s):
    def null_func(*args):
        raise ValueError("This Function Should not have been called")

    unify_func = null_func
    if isinstance(s, ConstOnlySubstitution):
        unify_func = TermHelpers.unify_const_only_substitution
    elif isinstance(s, TermUnifier):
        unify_func = TermHelpers.unify_term_unifier
    else:
        assert f"Invalid for TermHelper. Only two options available:s:{type(s)}"

    return unify_func


def unifyAtomWithFact(
    atom: PositiveAtom, fact: PositiveAtom, s: ClauseSubstitution
) -> bool:
    assert atom.getPred() == fact.getPred()
    atomArgs = atom.getArgs()
    factArgs = fact.getArgs()
    for af in zip(atomArgs, factArgs):
        unify_func = get_unify_func(s)
        if not unify_func(af[0], af[1], s):
            return False
    return True


class LocalCrashPremiseVisitor(CrashPremiseVisitor):
    def __init__(self, substTemplate, secondAction):
        self.substTemplate = substTemplate
        self.secondAction = secondAction
        super(LocalCrashPremiseVisitor, self).__init__()

    def visit_func(self, fact, atom):
        s: ClauseSubstitution = self.substTemplate.getCleanCopy()
        if unifyAtomWithFact(atom.asUnannotatedAtom(), fact, s):
            self.secondAction(s)

    def visit_annotated_atom(self, atom: AnnotatedAtom, nothing):
        return partial(self.visit_func, atom=atom)


class LocalCrashHeadVisitor(CrashHeadVisitor):
    def __init__(self, newFact):
        self.newFact = newFact
        super(LocalCrashHeadVisitor, self).__init__()

    def visit(self, head, nothing) -> Callable[[ClauseSubstitution], None]:
        return lambda s: self.newFact(head, s)


def make_action(cl: SemiNaiveClause, i: int, new_fact, get_facts):
    if i == len(cl.getBody()):
        return cl.getHead().accept_head_visitor(LocalCrashHeadVisitor(new_fact), None)
    next_action = make_action(cl, i + 1, new_fact, get_facts)

    return cl.getBody()[i].accept_premise_visitor(
        LocalActionCrashPremiseVisitor(get_facts, next_action), i
    )


#
# /**
#  * This class provides a way to derive all the new facts that are derivable from
#  * a given rule, given an initial fact that unifies with the first atom in the
#  * body of the clause. It is the workhorse of the bottom-up evaluation engines.
#  *
#  */
class ClauseEvaluator:
    # 	// TODO We can make this smarter by using fact that ahead of time we know
    # 	// which terms are going to be variables and which are going to be constant,
    # 	// so we can skip checks.

    def __init__(
        self,
        cl: SemiNaiveClause,
        new_fact: Callable[[PositiveAtom, ClauseSubstitution], None],
        get_facts: Callable[[AnnotatedAtom, ClauseSubstitution], Iterable[PositiveAtom]],
    ):
        assert cl.getBody()
        self.newFact = new_fact
        self.getFacts = get_facts
        self.substTemplate = ClauseSubstitution.make_with_seminaive_clause(cl)

        second_action = make_action(cl, 1, self.newFact, self.getFacts)
        self.firstAction = cl.getBody()[0].accept_premise_visitor(
            LocalCrashPremiseVisitor(self.substTemplate, second_action), None
        )

    def evaluate(self, new_fact: PositiveAtom):
        self.firstAction(new_fact)
