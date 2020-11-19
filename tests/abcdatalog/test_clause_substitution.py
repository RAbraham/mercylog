import pytest
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClause
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
from typing import *

def test_create_substitution_1():
    # PredicateSym p0 = PredicateSym.create("p", 0);
    p0 = PredicateSym.create("p", 0)
    # 		PredicateSym q2 = PredicateSym.create("q", 2);
    q2 = PredicateSym.create("q", 2)
    # 		PredicateSym r2 = PredicateSym.create("r", 2);
    r2 = PredicateSym.create("r", 2)
    # 		PredicateSym s3 = PredicateSym.create("s", 3);
    s3 = PredicateSym.create("s", 3)
    #
    # 		Variable x, y, z;
    x: Variable
    y: Variable
    z: Variable
    # 		x = Variable.create("X");
    x = Variable.create("X")
    # 		y = Variable.create("Y");
    y = Variable.create("Y")
    # 		z = Variable.create("Z");
    z = Variable.create("Z")
    # 		Constant a, b;
    a: Constant
    b: Constant
    # 		a = Constant.create("a");
    a = Constant.create("a")
    # 		b = Constant.create("b");
    b = Constant.create("b")
    #
    # 		Set<PredicateSym> idbPreds = new HashSet<>();
    idbPreds: Set[PredicateSym] = set()
    # 		idbPreds.add(q2);
    idbPreds.add(q2)
    # 		idbPreds.add(s3);
    idbPreds.add(s3)
    #
    # 		PositiveAtom pAtom = PositiveAtom.create(p0, new Term[] {});
    pAtom: PositiveAtom = PositiveAtom.create(p0, [])
    # 		Premise qAtom = PositiveAtom.create(q2, new Term[] { x, y });
    qAtom: Premise = PositiveAtom.create(q2, [x, y])
    # 		Premise rAtom = PositiveAtom.create(r2, new Term[] { x, x });
    rAtom: Premise = PositiveAtom.create(r2, [x, x])
    # 		Premise sAtom = PositiveAtom.create(s3, new Term[] { a, x, z });
    sAtom: Premise = PositiveAtom.create(s3, [a, x, z])
    # 		Premise u1 = new BinaryUnifier(x, b);
    u1: Premise = BinaryUnifier(x, b)
    # 		Premise u2 = new BinaryUnifier(z, z);
    u2: Premise = BinaryUnifier(z, z)
    #

    def createAndPrint(clauses: Set[SemiNaiveClause]):
        c: SemiNaiveClause
        print('>> Clauses')
        print(clauses)
        for c in clauses:
            print(f"Substitution for: {c}")
            print("> ")
            print(ClauseSubstitution.make_with_seminaive_clause(c))
    print('\n')
    for pred in idbPreds:
        print(pred)
        pass
    validator: DatalogValidator = DatalogValidator().withBinaryUnificationInRuleBody()


    annotator: SemiNaiveClauseAnnotator = SemiNaiveClauseAnnotator(idbPreds)
    expected_value = "{ }"
    input_clause = {Clause(pAtom, tuple([pAtom]))}

    assert_annotation(validator, annotator, input_clause, expected_value)
    assert_annotation(validator, annotator, {Clause(pAtom, tuple([qAtom]))}, "{ ^ <0> X -> None, Y -> None }")

    l: List[Premise] = []
    l.append(qAtom)
    l.append(rAtom)

    assert_annotation(validator, annotator, {Clause(pAtom, tuple(l))}, "{ ^ <0> X -> None, Y -> None }")
    l[0], l[1] = l[1], l[0]

    assert_annotation(validator, annotator, [Clause(pAtom, tuple(l))], "{ ^ <0> X -> None, Y -> None }")


    print(">> Current")
    # createAndPrint(annotator.annotate_single(get_cl(validator, {Clause(pAtom, tuple(l))})))
#	System.out.println("\nTesting adding...");
    l = []

#	l.add(qAtom);
    l.append(qAtom)
#	l.add(sAtom);
    l.append(sAtom)
#	idbPreds.clear();
    idbPreds = set()
#	cl = validator.validate(Collections.singleton(new Clause(pAtom, l))).getRules().iterator().next();
#	ClauseSubstitution subst = new ClauseSubstitution(annotator.annotate(cl).iterator().next());
    assert_annotation(validator, annotator, [Clause(pAtom, tuple(l))], "{ ^ <0> X -> None, Y -> None, <1> Z -> None }")
#	System.out.println(subst);
#	subst.add(x, a);
#	System.out.println(subst);
#	try {
#		subst.add(z, a);
#		System.err.println("BAD");
#	} catch (AssertionError e) {
#		System.out.println("Correctly threw error when adding in wrong order");
#	}
#	subst.add(y, b);
#	System.out.println(subst);
#	try {
#		subst.add(x, a);
#		System.err.println("BAD");
#	} catch (AssertionError e) {
#		System.out.println("Correctly threw error when adding in wrong order");
#	}
#	subst.add(z, a);
#	System.out.println(subst);
#	try {
#		subst.add(Variable.create("w"), b);
#		System.err.println("BAD");
#	} catch (AssertionError e) {
#		System.out.println("Correctly threw error when adding a variable not in substitution");
#	}
#
#	System.out.println("\nTesting getting and resetting...");
#	subst.resetState(0);
#	assert subst.get(x) == null;
#	subst.add(x, a);
#	assert subst.get(x).equals(a);
#	subst.add(y, b);
#	assert subst.get(x).equals(a);
#	assert subst.get(y).equals(b);
#	subst.add(z, a);
#	assert subst.get(x).equals(a);
#	assert subst.get(y).equals(b);
#	assert subst.get(z).equals(a);
#	subst.resetState(1);
#	assert subst.get(x).equals(a);
#	assert subst.get(y).equals(b);
#	assert subst.get(z) == null;
#
#
def assert_annotation(validator, annotator, input_clause, expected_value):
    rule = get_cl(validator, input_clause)
    _clause = list(annotator.annotate_single(rule))[0]
    assert str(ClauseSubstitution.make_with_seminaive_clause(_clause)) == expected_value
    return annotator


def get_cl(validator, input_clause):
    prog: UnstratifiedProgram = validator.validate(input_clause)  # ignore
    it = iter(prog.getRules())
    rule = next(it)
    return rule