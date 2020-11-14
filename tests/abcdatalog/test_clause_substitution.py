import pytest
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClause
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
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


#	System.out.println("Testing creating substitutions...");
#	Consumer<Set<SemiNaiveClause>> createAndPrint = clauses -> {
    def createAndPrint(clauses: Set[SemiNaiveClause]):
#		for (SemiNaiveClause c : clauses) {
        c: SemiNaiveClause
        for c in clauses:
#			System.out.println("Substitution for: " + c);
            print(f"Substitution for: {c}")
#			System.out.print("> ");
            print("> ")
#			System.out.println(new ClauseSubstitution(c));
            print(str(ClauseSubstitution.make_with_seminaive_clause(c)))
#		}
#	};
#	for (PredicateSym pred : idbPreds) {
    for pred in idbPreds:
#		System.out.println(pred);
        print(pred)
#	}
    aaa
#	DatalogValidator validator = (new DatalogValidator()).withBinaryUnificationInRuleBody();


#	UnstratifiedProgram prog = validator
#			.validate(Collections.singleton(new Clause(pAtom, Collections.singletonList(pAtom))));
#	SemiNaiveClauseAnnotator annotator = new SemiNaiveClauseAnnotator(idbPreds);
#	createAndPrint.accept(annotator.annotate(prog.getRules().iterator().next()));
#	prog = validator.validate(Collections.singleton(new Clause(pAtom, Collections.singletonList(qAtom))));
#	createAndPrint.accept(annotator.annotate(prog.getRules().iterator().next()));
#
#	List<Premise> l = new ArrayList<>();
#	l.add(qAtom);
#	l.add(rAtom);
#	ValidClause cl = validator.validate(Collections.singleton(new Clause(pAtom, l))).getRules().iterator().next();
#	createAndPrint.accept(annotator.annotate(cl));
#	Collections.swap(l, 0, 1);
#	createAndPrint.accept(annotator.annotate(cl));
#	l.add(sAtom);
#	createAndPrint.accept(annotator.annotate(cl));
#	l.add(u1);
#	createAndPrint.accept(annotator.annotate(cl));
#	l.add(u2);
#	createAndPrint.accept(annotator.annotate(cl));
#
#	System.out.println("\nTesting adding...");
#	l.clear();
#	l.add(qAtom);
#	l.add(sAtom);
#	idbPreds.clear();
#	cl = validator.validate(Collections.singleton(new Clause(pAtom, l))).getRules().iterator().next();
#	ClauseSubstitution subst = new ClauseSubstitution(annotator.annotate(cl).iterator().next());
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