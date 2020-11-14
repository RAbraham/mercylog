import copy
from typing import *
# import abcdatalog.ast.BinaryDisunifier;
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
# import abcdatalog.ast.BinaryUnifier;
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
# import abcdatalog.ast.Clause;
from mercylog.abcdatalog.ast.clause import Clause
# import abcdatalog.ast.Constant;
from mercylog.abcdatalog.ast.constant import Constant
# import abcdatalog.ast.NegatedAtom;
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
# import abcdatalog.ast.PredicateSym;
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
# import abcdatalog.ast.Premise;
from mercylog.abcdatalog.ast.premise import Premise
# import abcdatalog.ast.Term;
from mercylog.abcdatalog.ast.term import Term
# import abcdatalog.ast.TermHelpers;
from mercylog.abcdatalog.ast.term_helpers import TermHelpers
# import abcdatalog.ast.Variable;
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import DatalogValidationException
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.ast.visitors.crash_premise_visitor import CrashPremiseVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.ast.visitors.term_visitor_builder import TermVisitorBuilder
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator, SemiNaiveClause
from mercylog.abcdatalog.util.substitution.const_only_substitution import ConstOnlySubstitution


# 		PremiseVisitor<Integer, Integer> varFinder = new CrashPremiseVisitor<Integer, Integer>() {
class LocalCrashPremiseVisitor(CrashPremiseVisitor):
    def __init__(self, idxByConj: List[int], tv: TermVisitor[int, int]):
        self.idxByConj = idxByConj
        self.tv = tv

# 			@Override
# 			public Integer visit(AnnotatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
    def visit_annotated_atom(self, atom: AnnotatedAtom, count: int) -> int:
        self.idxByConj.append(count)
        return TermHelpers.fold(atom.getArgs(), self.tv, count)
#
# 			@Override
# 			public Integer visit(BinaryUnifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
    def visit_binary_unifier(self, u: BinaryUnifier, count: int) -> int:
        self.idxByConj.append(count)
        return TermHelpers.fold(u.getArgsIterable(), self.tv, count)
# 			@Override
# 			public Integer visit(BinaryDisunifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
    def visit_binary_disunifier(self, u: BinaryDisunifier, count: int) -> int:
        self.idxByConj.append(count)
        return TermHelpers.fold(u.get_args_iterable(), self.tv, count)
# 			@Override
# 			public Integer visit(NegatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
# 		};
#
    def visit_negated_atom(self, atom: NegatedAtom, count: int):
        self.idxByConj.append(count)
        return TermHelpers.fold(atom.getArgs(), self.tv, count)
#
# /**
#  * This is a substitution tailor-made for a particular clause. Mappings can only
#  * be added to the substitution in the order in which the variables appear in
#  * the clause. The state of the substitution can be reset (so that it "forgets"
#  * the most recent mappings).
#  *
#  */
# public class ClauseSubstitution implements ConstOnlySubstitution {
class ClauseSubstitution(ConstOnlySubstitution):
# 	private final Constant[] subst;
# 	private final Map<Variable, Integer> index;
# 	private final int[] indexByConj;
# 	private int pos = 0;
# 	private final int bodySize;
#
# 	public ClauseSubstitution(SemiNaiveClause c) {
    @staticmethod
    def make_with_seminaive_clause(self, c: SemiNaiveClause):
# 		Map<Variable, Integer> idx = new HashMap<>();
        idx: Dict[Variable, int] = dict()
# 		List<Integer> idxByConj = new ArrayList<>();
        idxByConj: List[int] = []
#
# 		TermVisitor<Integer, Integer> tv = (new TermVisitorBuilder<Integer, Integer>()).onVariable((x, curCount) -> {
        def variable_func(x, curCount):
            if x not in idx:
                idx[x] = curCount
                return curCount + 1
            return curCount

        tv: TermVisitor[int, int] = TermVisitorBuilder.onVariable(variable_func).or_(lambda x, curCount: curCount)
# 			if (idx.get(x) == null) {
# 				idx.put(x, curCount);
# 				return curCount + 1;
# 			}
# 			return curCount;
# 		}).or((x, curCount) -> curCount);
#
# 		PremiseVisitor<Integer, Integer> varFinder = new CrashPremiseVisitor<Integer, Integer>() {
        varFinder: PremiseVisitor[int, int] = LocalCrashPremiseVisitor(idxByConj, tv)
# 			@Override
# 			public Integer visit(AnnotatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(BinaryUnifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(BinaryDisunifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(NegatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
# 		};
#
# 		int count = 0;
        count: int = 0
# 		for (Premise conj : c.getBody()) {
        conj: Premise
        for conj in c.getBody():
# 			count = conj.accept(varFinder, count);
            count = conj.accept_premise_visitor(varFinder, count)
# 		}
#

# 		this.subst = new Constant[count];
        subst = []
# 		this.index = idx;
        index = idx
# 		this.bodySize = c.getBody().size();
        bodySize = len(c.getBody())
# 		this.indexByConj = new int[this.bodySize];
        indexByConj = []
# 		Iterator<Integer> iter = idxByConj.iterator();
        it: Iterator[int] = iter(idxByConj)
        i = 0
# 		for (int i = 0; i < this.bodySize; ++i) {
        while i < self.bodySize:
# 			this.indexByConj[i] = iter.next();
            indexByConj[i] = next(it)
            i += 1
# 		}
        return ClauseSubstitution(subst,index,indexByConj, 0, bodySize)

# 	}
#
# 	private ClauseSubstitution(Constant[] subst, Map<Variable, Integer> index, int[] indexByConj, int pos,
# 			int bodySize) {
# 		this.subst = subst;
# 		this.index = index;
# 		this.indexByConj = indexByConj;
# 		this.pos = pos;
# 		this.bodySize = bodySize;
# 	}

    def __init__(self, subst: List[Constant], index: Dict[Variable, int], indexByConj: List[int], pos: int, bodySize: int):
        self.subst = subst
        self.index = index
        self.indexByConj = indexByConj
        self.pos = pos
        self.bodySize = bodySize
        super(ClauseSubstitution, self).__init__()

#
# 	public ClauseSubstitution getCleanCopy() {
# 		return new ClauseSubstitution(new Constant[subst.length], this.index, this.indexByConj, 0, this.bodySize);
# 	}
    def getCleanCopy(self) -> "ClauseSubstitution":
        return ClauseSubstitution(copy.deepcopy([]), self.index, self.indexByConj, 0, self.bodySize)
#
# 	public boolean add(Variable x, Constant c) {
# 		Integer idx = this.index.get(x);
# 		assert idx != null && idx == this.pos;
# 		this.subst[this.pos++] = c;
# 		return true;
# 	}
    def add(self, x: Variable, c: Constant) -> bool:
        idx: int = self.index.get(x)
        assert idx and idx == self.pos
        self.pos = self.pos + 1
        self.subst[self.pos] = c
        return True
#
# 	public Constant get(Variable x) {
# 		Integer idx = this.index.get(x);
# 		if (idx == null || idx >= this.pos) {
# 			return null;
# 		}
# 		return this.subst[idx];
# 	}
    def get(self, x: Variable) -> Optional[Constant]:
        idx: int = self.index.get(x)
        if not idx or idx >= self.pos:
            return None
        return self.subst[idx]
#
# 	public void resetState(int conj) {
# 		assert conj >= 0 && conj < this.bodySize;
# 		this.pos = this.indexByConj[conj];
# 	}
    def resetState(self, conj: int) -> None:
        assert  conj >= 0 and conj < self.bodySize
        self.pos = self.indexByConj[conj]
#
# 	@Override
# 	public String toString() {
    def __repr__(self):
# 		Set<Entry<Variable, Integer>> entries = this.index.entrySet();
        entries = self.index.items()
# 		int curConj = 0;
        curConj: int = 0
# 		Variable[] orderedVars = new Variable[entries.size()];
        orderedVars: List[Variable] = []
# 		for (Entry<Variable, Integer> entry : entries) {
        for v, k in entries:
# 			orderedVars[entry.getValue()] = entry.getKey();
            orderedVars[v] = k
# 		}
#
# 		StringBuilder sb = new StringBuilder();
# 		sb.append("{ ");
        sb = "{ "
#
# 		for (int i = 0; i < orderedVars.length; ++i) {
        for i, v in enumerate(orderedVars):
# 			if (this.pos == i) {
            if self.pos == i:
# 				sb.append("^ ");
                sb = sb + "^ "
# 			}
# 			while (curConj < this.bodySize && this.indexByConj[curConj] == i) {
            while curConj < self.bodySize and self.indexByConj[curConj] == i:
# 				sb.append("<" + curConj++ + "> ");
                curConj += 1
                sb = sb + "<" + str(curConj) + ">"
# 			}
# 			sb.append(orderedVars[i]);
            sb = sb + str(orderedVars[i])
# 			sb.append(" -> ");
            sb = sb  + " -> "
# 			Constant c = this.subst[i];
            c: Constant = self.subst[i]
# 			if (c != null) {
            if c:
# 				sb.append(c);
                sb = sb + str(c)
# 			} else {
            else:
# 				sb.append("None");
                sb = sb + "None"
# 			}
#
# 			if (i < orderedVars.length - 1) {
            if i < (len(orderedVars) - 1):
# 				sb.append(", ");
                sb = sb + ", "
# 			} else {
            else:
# 				sb.append(" ");
                sb = sb + " "
# 			}
# 		}
#
# 		sb.append("}");
        sb = sb + "}"
# 		return sb.toString();
        return sb
# 	}

# 	@Override
# 	public Term[] apply(Term[] original) {
# 		Term[] terms = new Term[original.length];
# 		for (int i = 0; i < original.length; ++i) {
# 			Term t = original[i];
# 			Term s;
# 			if (t instanceof Variable && (s = this.get((Variable) t)) != null) {
# 				t = s;
# 			}
# 			terms[i] = t;
# 		}
# 		return terms;
# 	}
    def apply(self, original: List[Term]) -> List[Term]:
        terms: List[Term] = []
        for o in original:
            t: Term = o
            s: Term
            if isinstance(t, Variable):
                s = self.get(t)
                if s:
                    t = s
            terms.append(t)
        return terms
#


# }
# /*******************************************************************************
#  * This file is part of the AbcDatalog project.
#  *
#  * Copyright (c) 2016, Harvard University
#  * All rights reserved.
#  *
#  * This program and the accompanying materials are made available under
#  * the terms of the BSD License which accompanies this distribution.
#  *
#  * The development of the AbcDatalog project has been supported by the
#  * National Science Foundation under Grant Nos. 1237235 and 1054172.
#  *
#  * See README for contributors.
#  ******************************************************************************/
# package abcdatalog.util.substitution;
#
# import java.util.ArrayList;
# import java.util.Collections;
# import java.util.HashMap;
# import java.util.HashSet;
# import java.util.Iterator;
# import java.util.List;
# import java.util.Map;
# import java.util.Map.Entry;
# import java.util.Set;
# import java.util.function.Consumer;
#
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Premise;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.TermHelpers;
# import abcdatalog.ast.Variable;
# import abcdatalog.ast.validation.DatalogValidationException;
# import abcdatalog.ast.validation.DatalogValidator;
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
# import abcdatalog.ast.validation.UnstratifiedProgram;
# import abcdatalog.ast.visitors.CrashPremiseVisitor;
# import abcdatalog.ast.visitors.PremiseVisitor;
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.ast.visitors.TermVisitorBuilder;
# import abcdatalog.engine.bottomup.AnnotatedAtom;
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator;
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator.SemiNaiveClause;
#
# /**
#  * This is a substitution tailor-made for a particular clause. Mappings can only
#  * be added to the substitution in the order in which the variables appear in
#  * the clause. The state of the substitution can be reset (so that it "forgets"
#  * the most recent mappings).
#  *
#  */
# public class ClauseSubstitution implements ConstOnlySubstitution {
# 	private final Constant[] subst;
# 	private final Map<Variable, Integer> index;
# 	private final int[] indexByConj;
# 	private int pos = 0;
# 	private final int bodySize;
#
# 	public ClauseSubstitution(SemiNaiveClause c) {
# 		Map<Variable, Integer> idx = new HashMap<>();
# 		List<Integer> idxByConj = new ArrayList<>();
#
# 		TermVisitor<Integer, Integer> tv = (new TermVisitorBuilder<Integer, Integer>()).onVariable((x, curCount) -> {
# 			if (idx.get(x) == null) {
# 				idx.put(x, curCount);
# 				return curCount + 1;
# 			}
# 			return curCount;
# 		}).or((x, curCount) -> curCount);
#
# 		PremiseVisitor<Integer, Integer> varFinder = new CrashPremiseVisitor<Integer, Integer>() {
# 			@Override
# 			public Integer visit(AnnotatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(BinaryUnifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(BinaryDisunifier u, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(u.getArgsIterable(), tv, count);
# 			}
#
# 			@Override
# 			public Integer visit(NegatedAtom atom, Integer count) {
# 				idxByConj.add(count);
# 				return TermHelpers.fold(atom.getArgs(), tv, count);
# 			}
# 		};
#
# 		int count = 0;
# 		for (Premise conj : c.getBody()) {
# 			count = conj.accept(varFinder, count);
# 		}
#
# 		this.subst = new Constant[count];
# 		this.index = idx;
# 		this.bodySize = c.getBody().size();
# 		this.indexByConj = new int[this.bodySize];
# 		Iterator<Integer> iter = idxByConj.iterator();
# 		for (int i = 0; i < this.bodySize; ++i) {
# 			this.indexByConj[i] = iter.next();
# 		}
# 	}
#
# 	private ClauseSubstitution(Constant[] subst, Map<Variable, Integer> index, int[] indexByConj, int pos,
# 			int bodySize) {
# 		this.subst = subst;
# 		this.index = index;
# 		this.indexByConj = indexByConj;
# 		this.pos = pos;
# 		this.bodySize = bodySize;
# 	}
#
# 	public ClauseSubstitution getCleanCopy() {
# 		return new ClauseSubstitution(new Constant[subst.length], this.index, this.indexByConj, 0, this.bodySize);
# 	}
#
# 	public boolean add(Variable x, Constant c) {
# 		Integer idx = this.index.get(x);
# 		assert idx != null && idx == this.pos;
# 		this.subst[this.pos++] = c;
# 		return true;
# 	}
#
# 	public Constant get(Variable x) {
# 		Integer idx = this.index.get(x);
# 		if (idx == null || idx >= this.pos) {
# 			return null;
# 		}
# 		return this.subst[idx];
# 	}
#
# 	public void resetState(int conj) {
# 		assert conj >= 0 && conj < this.bodySize;
# 		this.pos = this.indexByConj[conj];
# 	}
#
# 	@Override
# 	public String toString() {
# 		Set<Entry<Variable, Integer>> entries = this.index.entrySet();
# 		int curConj = 0;
# 		Variable[] orderedVars = new Variable[entries.size()];
# 		for (Entry<Variable, Integer> entry : entries) {
# 			orderedVars[entry.getValue()] = entry.getKey();
# 		}
#
# 		StringBuilder sb = new StringBuilder();
# 		sb.append("{ ");
#
# 		for (int i = 0; i < orderedVars.length; ++i) {
# 			if (this.pos == i) {
# 				sb.append("^ ");
# 			}
# 			while (curConj < this.bodySize && this.indexByConj[curConj] == i) {
# 				sb.append("<" + curConj++ + "> ");
# 			}
# 			sb.append(orderedVars[i]);
# 			sb.append(" -> ");
# 			Constant c = this.subst[i];
# 			if (c != null) {
# 				sb.append(c);
# 			} else {
# 				sb.append("None");
# 			}
#
# 			if (i < orderedVars.length - 1) {
# 				sb.append(", ");
# 			} else {
# 				sb.append(" ");
# 			}
# 		}
#
# 		sb.append("}");
# 		return sb.toString();
# 	}
#
# 	public static void main(String[] args) throws DatalogValidationException {
# 		PredicateSym p0 = PredicateSym.create("p", 0);
# 		PredicateSym q2 = PredicateSym.create("q", 2);
# 		PredicateSym r2 = PredicateSym.create("r", 2);
# 		PredicateSym s3 = PredicateSym.create("s", 3);
#
# 		Variable x, y, z;
# 		x = Variable.create("X");
# 		y = Variable.create("Y");
# 		z = Variable.create("Z");
# 		Constant a, b;
# 		a = Constant.create("a");
# 		b = Constant.create("b");
#
# 		Set<PredicateSym> idbPreds = new HashSet<>();
# 		idbPreds.add(q2);
# 		idbPreds.add(s3);
#
# 		PositiveAtom pAtom = PositiveAtom.create(p0, new Term[] {});
# 		Premise qAtom = PositiveAtom.create(q2, new Term[] { x, y });
# 		Premise rAtom = PositiveAtom.create(r2, new Term[] { x, x });
# 		Premise sAtom = PositiveAtom.create(s3, new Term[] { a, x, z });
# 		Premise u1 = new BinaryUnifier(x, b);
# 		Premise u2 = new BinaryUnifier(z, z);
#
# 		System.out.println("Testing creating substitutions...");
# 		Consumer<Set<SemiNaiveClause>> createAndPrint = clauses -> {
# 			for (SemiNaiveClause c : clauses) {
# 				System.out.println("Substitution for: " + c);
# 				System.out.print("> ");
# 				System.out.println(new ClauseSubstitution(c));
# 			}
# 		};
# 		for (PredicateSym pred : idbPreds) {
# 			System.out.println(pred);
# 		}
# 		DatalogValidator validator = (new DatalogValidator()).withBinaryUnificationInRuleBody();
# 		UnstratifiedProgram prog = validator
# 				.validate(Collections.singleton(new Clause(pAtom, Collections.singletonList(pAtom))));
# 		SemiNaiveClauseAnnotator annotator = new SemiNaiveClauseAnnotator(idbPreds);
# 		createAndPrint.accept(annotator.annotate(prog.getRules().iterator().next()));
# 		prog = validator.validate(Collections.singleton(new Clause(pAtom, Collections.singletonList(qAtom))));
# 		createAndPrint.accept(annotator.annotate(prog.getRules().iterator().next()));
#
# 		List<Premise> l = new ArrayList<>();
# 		l.add(qAtom);
# 		l.add(rAtom);
# 		ValidClause cl = validator.validate(Collections.singleton(new Clause(pAtom, l))).getRules().iterator().next();
# 		createAndPrint.accept(annotator.annotate(cl));
# 		Collections.swap(l, 0, 1);
# 		createAndPrint.accept(annotator.annotate(cl));
# 		l.add(sAtom);
# 		createAndPrint.accept(annotator.annotate(cl));
# 		l.add(u1);
# 		createAndPrint.accept(annotator.annotate(cl));
# 		l.add(u2);
# 		createAndPrint.accept(annotator.annotate(cl));
#
# 		System.out.println("\nTesting adding...");
# 		l.clear();
# 		l.add(qAtom);
# 		l.add(sAtom);
# 		idbPreds.clear();
# 		cl = validator.validate(Collections.singleton(new Clause(pAtom, l))).getRules().iterator().next();
# 		ClauseSubstitution subst = new ClauseSubstitution(annotator.annotate(cl).iterator().next());
# 		System.out.println(subst);
# 		subst.add(x, a);
# 		System.out.println(subst);
# 		try {
# 			subst.add(z, a);
# 			System.err.println("BAD");
# 		} catch (AssertionError e) {
# 			System.out.println("Correctly threw error when adding in wrong order");
# 		}
# 		subst.add(y, b);
# 		System.out.println(subst);
# 		try {
# 			subst.add(x, a);
# 			System.err.println("BAD");
# 		} catch (AssertionError e) {
# 			System.out.println("Correctly threw error when adding in wrong order");
# 		}
# 		subst.add(z, a);
# 		System.out.println(subst);
# 		try {
# 			subst.add(Variable.create("w"), b);
# 			System.err.println("BAD");
# 		} catch (AssertionError e) {
# 			System.out.println("Correctly threw error when adding a variable not in substitution");
# 		}
#
# 		System.out.println("\nTesting getting and resetting...");
# 		subst.resetState(0);
# 		assert subst.get(x) == null;
# 		subst.add(x, a);
# 		assert subst.get(x).equals(a);
# 		subst.add(y, b);
# 		assert subst.get(x).equals(a);
# 		assert subst.get(y).equals(b);
# 		subst.add(z, a);
# 		assert subst.get(x).equals(a);
# 		assert subst.get(y).equals(b);
# 		assert subst.get(z).equals(a);
# 		subst.resetState(1);
# 		assert subst.get(x).equals(a);
# 		assert subst.get(y).equals(b);
# 		assert subst.get(z) == null;
# 	}
#
# 	@Override
# 	public Term[] apply(Term[] original) {
# 		Term[] terms = new Term[original.length];
# 		for (int i = 0; i < original.length; ++i) {
# 			Term t = original[i];
# 			Term s;
# 			if (t instanceof Variable && (s = this.get((Variable) t)) != null) {
# 				t = s;
# 			}
# 			terms[i] = t;
# 		}
# 		return terms;
# 	}
# }
