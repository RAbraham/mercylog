from typing import *
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.head_helpers import HeadHelpers
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.term_helpers import TermHelpers
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.visitors.crash_premise_visitor import CrashPremiseVisitor
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor
from mercylog.abcdatalog.ast.visitors.head_visitor_builder import HeadVisitorBuilder
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor_builder import PremiseVisitorBuilder
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.ast.visitors.term_visitor_builder import TermVisitorBuilder
from mercylog.abcdatalog.util.box import Box
from mercylog.abcdatalog.util.substitution.term_unifier import TermUnifier
from mercylog.abcdatalog.util.substitution.union_find_based_unifier import UnionFindBasedUnifier
from mercylog.abcdatalog.ast.validation.unstratified_program import UnStratifiedProgram

# 	public static final class ValidClause extends Clause {
#
# 		private ValidClause(Head head, List<Premise> body) {
# 			super(head, body);
# 		}
#
# 	}


class ValidClause(Clause):
    def __init__(self, head: Head, body: List[Premise]):
        super().__init__(head, body)

# 	private final static class True {
#
# 		private True() {
# 			// Cannot be instantiated.
# 		}
#
# 		private static class TruePred extends PredicateSym {
#
# 			protected TruePred() {
# 				super("true", 0);
# 			}
#
# 		};
#
# 		private final static PositiveAtom trueAtom = PositiveAtom.create(new TruePred(), new Term[] {});
#
# 		public static PositiveAtom getTrueAtom() {
# 			return trueAtom;
# 		}
# 	}
#

class TruePred(PredicateSym):
    def __init__(self):
        super().__init__("true", 0)

class TrueAtom:
    trueAtom: PositiveAtom = PositiveAtom.create(TruePred(), [])

    @staticmethod
    def getTrueAtom() -> PositiveAtom:
        return TrueAtom.trueAtom


#
# /**
#  * A validator for a set of clauses. It converts a set of clauses to a program, which
#  * consists of a set of initial facts and a set of rules for deriving new facts. The
#  * rules in a program are guaranteed to be valid.
#  *
#  */
def add_to_edb(atom, nothing, edbPredicateSymbols):
    edbPredicateSymbols.add(atom.getPred())
    return None


# public class DatalogValidator {
class DatalogValidator:
# 	private boolean allowBinaryUnification;
# 	private boolean allowBinaryDisunification;
# 	private boolean allowNegatedBodyAtom;
#
# 	public DatalogValidator withBinaryUnificationInRuleBody() {
# 		this.allowBinaryUnification = true;
# 		return this;
# 	}
    def __init__(self):
        self.allowBinaryUnification = False
        self.allowBinaryDisunification = False
        self.allowNegatedBodyAtom = False

    def withBinaryUnificationInRuleBody(self) -> "DatalogValidator":
        self.allowBinaryUnification = True
        return self

    def withBinaryDisunificationInRuleBody(self) -> "DatalogValidator":
        self.allowBinaryDisunification = True
        return self
#
# 	public DatalogValidator withAtomNegationInRuleBody() {
# 		this.allowNegatedBodyAtom = true;
# 		return this;
# 	}
    def withAtomNegationInRuleBody(self) -> "DatalogValidator":
        self.allowNegatedBodyAtom = True
        return self
#
# 	public UnstratifiedProgram validate(Set<Clause> program) throws DatalogValidationException {
# 		return validate(program, false);
# 	}
    def validate(self, program: Set[Clause]) -> UnStratifiedProgram:
        return self.validate(program, False)
#
# 	public UnstratifiedProgram validate(Set<Clause> program, boolean treatIdbFactsAsClauses) throws DatalogValidationException {
    def validate(self, program: Set[Clause], treatIdbFactsAsClauses: bool) -> UnStratifiedProgram:
# 		Set<ValidClause> rewrittenClauses = new HashSet<>();
        rewrittenClauses: Set[ValidClause] = set()
# 		for (Clause clause : program) {
        for clause in program:
# 			rewrittenClauses.add(checkRule(clause));
            rewrittenClauses.add(self.checkRule(clause))
# 		}
# 		rewrittenClauses.add(new ValidClause(True.getTrueAtom(), Collections.emptyList()));
        rewrittenClauses.add(ValidClause(TrueAtom.getTrueATom(), []))
#
# 		Set<ValidClause> rules = new HashSet<>();
        rules: Set[ValidClause] = set()
# 		Set<ValidClause> bodilessClauses = new HashSet<>();
        bodilessClauses: Set[ValidClause] = set()
#
# 		Set<PredicateSym> edbPredicateSymbols = new HashSet<>();
        edbPredicateSymbols: Set[PredicateSym] = set()
# 		Set<PredicateSym> idbPredicateSymbols = new HashSet<>();
        idbPredicateSymbols: Set[PredicateSym] = set()
#
        getHeadAsAtom: HeadVisitor = HeadVisitorBuilder().onPositiveAtom(lambda atom, nothing: atom).orCrash()
# 		PremiseVisitor<Void, Void> getBodyPred = (new PremiseVisitorBuilder<Void, Void>())
# 				.onPositiveAtom((atom, nothing) -> {
# 					edbPredicateSymbols.add(atom.getPred());
# 					return null;
# 				}).onNegatedAtom((atom, nothing) -> {
# 					edbPredicateSymbols.add(atom.getPred());
# 					return null;
# 				}).orNull();

        add_atom = lambda atom, nothing: add_to_edb(atom, nothing, edbPredicateSymbols)
        getBodyPred: PremiseVisitor = PremiseVisitorBuilder().onPositiveAtom(add_atom).onNegatedAtom(add_atom).orNull()
        aaa
# 		for (ValidClause cl : rewrittenClauses) {
# 			PositiveAtom head = cl.getHead().accept(getHeadAsAtom, null);
# 			List<Premise> body = cl.getBody();
# 			if (body.isEmpty()) {
# 				bodilessClauses.add(cl);
# 				edbPredicateSymbols.add(head.getPred());
# 			} else {
# 				idbPredicateSymbols.add(head.getPred());
# 				rules.add(cl);
# 				for (Premise c : body) {
# 					c.accept(getBodyPred, null);
# 				}
# 			}
# 		}
#
# 		Set<PositiveAtom> initialFacts = new HashSet<>();
# 		edbPredicateSymbols.removeAll(idbPredicateSymbols);
# 		for (ValidClause cl : bodilessClauses) {
# 			PositiveAtom head = HeadHelpers.forcePositiveAtom(cl.getHead());
# 			if (treatIdbFactsAsClauses && idbPredicateSymbols.contains(head.getPred())) {
# 				rules.add(cl);
# 			} else {
# 				initialFacts.add(head);
# 			}
# 		}
#
# 		return new Program(rules, initialFacts, edbPredicateSymbols, idbPredicateSymbols);
# 	}
    pass
#
# 	private ValidClause checkRule(Clause clause) throws DatalogValidationException {
# 		Set<Variable> boundVars = new HashSet<>();
# 		Set<Variable> possiblyUnboundVars = new HashSet<>();
# 		TermUnifier subst = new UnionFindBasedUnifier();
#
# 		TermVisitor<Set<Variable>, Set<Variable>> tv = (new TermVisitorBuilder<Set<Variable>, Set<Variable>>())
# 				.onVariable((x, set) -> {
# 					set.add(x);
# 					return set;
# 				}).or((x, set) -> set);
#
# 		TermHelpers.fold(HeadHelpers.forcePositiveAtom(clause.getHead()).getArgs(), tv, possiblyUnboundVars);
#
# 		Box<Boolean> hasPositiveAtom = new Box<>(false);
# 		PremiseVisitor<DatalogValidationException, DatalogValidationException> cv = new CrashPremiseVisitor<DatalogValidationException, DatalogValidationException>() {
#
# 			@Override
# 			public DatalogValidationException visit(PositiveAtom atom, DatalogValidationException e) {
# 				TermHelpers.fold(atom.getArgs(), tv, boundVars);
# 				hasPositiveAtom.value = true;
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(BinaryUnifier u, DatalogValidationException e) {
# 				if (!allowBinaryUnification) {
# 					return new DatalogValidationException("Binary unification is not allowed: ");
# 				}
# 				TermHelpers.fold(u.getArgsIterable(), tv, possiblyUnboundVars);
# 				TermHelpers.unify(u.getLeft(), u.getRight(), subst);
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(BinaryDisunifier u, DatalogValidationException e) {
# 				if (!allowBinaryDisunification) {
# 					return new DatalogValidationException("Binary disunification is not allowed: ");
# 				}
# 				TermHelpers.fold(u.getArgsIterable(), tv, possiblyUnboundVars);
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(NegatedAtom atom, DatalogValidationException e) {
# 				if (!allowNegatedBodyAtom) {
# 					return new DatalogValidationException("Negated body atoms are not allowed: ");
# 				}
# 				TermHelpers.fold(atom.getArgs(), tv, possiblyUnboundVars);
# 				return e;
# 			}
#
# 		};
#
# 		for (Premise c : clause.getBody()) {
# 			DatalogValidationException e = c.accept(cv, null);
# 			if (e != null) {
# 				throw e;
# 			}
# 		}
#
# 		for (Variable x : possiblyUnboundVars) {
# 			if (!boundVars.contains(x) && !(subst.get(x) instanceof Constant)) {
# 				throw new DatalogValidationException("Every variable in a rule must be bound, but " + x
# 						+ " is not bound in the rule " + clause
# 						+ " A variable X is bound if 1) it appears in a positive (non-negated) body atom, or 2) it is explicitly unified with a constant (e.g., X=a) or with a variable that is bound (e.g., X=Y, where Y is bound).");
# 			}
# 		}
#
# 		List<Premise> newBody = new ArrayList<>(clause.getBody());
# 		if (!hasPositiveAtom.value && !newBody.isEmpty()) {
# 			newBody.add(0, True.getTrueAtom());
# 		}
#
# 		return new ValidClause(clause.getHead(), newBody);
# 	}
#
# 	private static final class Program implements UnstratifiedProgram {
# 		private final Set<ValidClause> rules;
# 		private final Set<PositiveAtom> initialFacts;
# 		private final Set<PredicateSym> edbPredicateSymbols;
# 		private final Set<PredicateSym> idbPredicateSymbols;
#
# 		public Program(Set<ValidClause> rules, Set<PositiveAtom> initialFacts, Set<PredicateSym> edbPredicateSymbols,
# 				Set<PredicateSym> idbPredicateSymbols) {
# 			this.rules = rules;
# 			this.initialFacts = initialFacts;
# 			this.edbPredicateSymbols = edbPredicateSymbols;
# 			this.idbPredicateSymbols = idbPredicateSymbols;
# 		}
#
# 		public Set<ValidClause> getRules() {
# 			return this.rules;
# 		}
#
# 		public Set<PositiveAtom> getInitialFacts() {
# 			return this.initialFacts;
# 		}
#
# 		public Set<PredicateSym> getEdbPredicateSyms() {
# 			return this.edbPredicateSymbols;
# 		}
#
# 		public Set<PredicateSym> getIdbPredicateSyms() {
# 			return this.idbPredicateSymbols;
# 		}
#
# 	}
#
# 	private final static class True {
#
# 		private True() {
# 			// Cannot be instantiated.
# 		}
#
# 		private static class TruePred extends PredicateSym {
#
# 			protected TruePred() {
# 				super("true", 0);
# 			}
#
# 		};
#
# 		private final static PositiveAtom trueAtom = PositiveAtom.create(new TruePred(), new Term[] {});
#
# 		public static PositiveAtom getTrueAtom() {
# 			return trueAtom;
# 		}
# 	}
#
# 	public static final class ValidClause extends Clause {
#
# 		private ValidClause(Head head, List<Premise> body) {
# 			super(head, body);
# 		}
#
# 	}
#
# }

    pass


# import java.util.ArrayList;
# import java.util.Collections;
# import java.util.HashSet;
# import java.util.List;
# import java.util.Set;
#
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.Head;
# import abcdatalog.ast.HeadHelpers;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Premise;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.TermHelpers;
# import abcdatalog.ast.Variable;
# import abcdatalog.ast.visitors.CrashPremiseVisitor;
# import abcdatalog.ast.visitors.HeadVisitor;
# import abcdatalog.ast.visitors.HeadVisitorBuilder;
# import abcdatalog.ast.visitors.PremiseVisitor;
# import abcdatalog.ast.visitors.PremiseVisitorBuilder;
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.ast.visitors.TermVisitorBuilder;
# import abcdatalog.util.Box;
# import abcdatalog.util.substitution.TermUnifier;
# import abcdatalog.util.substitution.UnionFindBasedUnifier;
#
# /**
#  * A validator for a set of clauses. It converts a set of clauses to a program, which
#  * consists of a set of initial facts and a set of rules for deriving new facts. The
#  * rules in a program are guaranteed to be valid.
#  *
#  */
# public class DatalogValidator {
# 	private boolean allowBinaryUnification;
# 	private boolean allowBinaryDisunification;
# 	private boolean allowNegatedBodyAtom;
#
# 	public DatalogValidator withBinaryUnificationInRuleBody() {
# 		this.allowBinaryUnification = true;
# 		return this;
# 	}
#
# 	public DatalogValidator withBinaryDisunificationInRuleBody() {
# 		this.allowBinaryDisunification = true;
# 		return this;
# 	}
#
# 	public DatalogValidator withAtomNegationInRuleBody() {
# 		this.allowNegatedBodyAtom = true;
# 		return this;
# 	}
#
# 	public UnstratifiedProgram validate(Set<Clause> program) throws DatalogValidationException {
# 		return validate(program, false);
# 	}
#
# 	public UnstratifiedProgram validate(Set<Clause> program, boolean treatIdbFactsAsClauses) throws DatalogValidationException {
# 		Set<ValidClause> rewrittenClauses = new HashSet<>();
# 		for (Clause clause : program) {
# 			rewrittenClauses.add(checkRule(clause));
# 		}
# 		rewrittenClauses.add(new ValidClause(True.getTrueAtom(), Collections.emptyList()));
#
# 		Set<ValidClause> rules = new HashSet<>();
# 		Set<ValidClause> bodilessClauses = new HashSet<>();
#
# 		Set<PredicateSym> edbPredicateSymbols = new HashSet<>();
# 		Set<PredicateSym> idbPredicateSymbols = new HashSet<>();
#
# 		HeadVisitor<Void, PositiveAtom> getHeadAsAtom = (new HeadVisitorBuilder<Void, PositiveAtom>())
# 				.onPositiveAtom((atom, nothing) -> atom).orCrash();
# 		PremiseVisitor<Void, Void> getBodyPred = (new PremiseVisitorBuilder<Void, Void>())
# 				.onPositiveAtom((atom, nothing) -> {
# 					edbPredicateSymbols.add(atom.getPred());
# 					return null;
# 				}).onNegatedAtom((atom, nothing) -> {
# 					edbPredicateSymbols.add(atom.getPred());
# 					return null;
# 				}).orNull();
# 		for (ValidClause cl : rewrittenClauses) {
# 			PositiveAtom head = cl.getHead().accept(getHeadAsAtom, null);
# 			List<Premise> body = cl.getBody();
# 			if (body.isEmpty()) {
# 				bodilessClauses.add(cl);
# 				edbPredicateSymbols.add(head.getPred());
# 			} else {
# 				idbPredicateSymbols.add(head.getPred());
# 				rules.add(cl);
# 				for (Premise c : body) {
# 					c.accept(getBodyPred, null);
# 				}
# 			}
# 		}
#
# 		Set<PositiveAtom> initialFacts = new HashSet<>();
# 		edbPredicateSymbols.removeAll(idbPredicateSymbols);
# 		for (ValidClause cl : bodilessClauses) {
# 			PositiveAtom head = HeadHelpers.forcePositiveAtom(cl.getHead());
# 			if (treatIdbFactsAsClauses && idbPredicateSymbols.contains(head.getPred())) {
# 				rules.add(cl);
# 			} else {
# 				initialFacts.add(head);
# 			}
# 		}
#
# 		return new Program(rules, initialFacts, edbPredicateSymbols, idbPredicateSymbols);
# 	}
#
# 	private ValidClause checkRule(Clause clause) throws DatalogValidationException {
# 		Set<Variable> boundVars = new HashSet<>();
# 		Set<Variable> possiblyUnboundVars = new HashSet<>();
# 		TermUnifier subst = new UnionFindBasedUnifier();
#
# 		TermVisitor<Set<Variable>, Set<Variable>> tv = (new TermVisitorBuilder<Set<Variable>, Set<Variable>>())
# 				.onVariable((x, set) -> {
# 					set.add(x);
# 					return set;
# 				}).or((x, set) -> set);
#
# 		TermHelpers.fold(HeadHelpers.forcePositiveAtom(clause.getHead()).getArgs(), tv, possiblyUnboundVars);
#
# 		Box<Boolean> hasPositiveAtom = new Box<>(false);
# 		PremiseVisitor<DatalogValidationException, DatalogValidationException> cv = new CrashPremiseVisitor<DatalogValidationException, DatalogValidationException>() {
#
# 			@Override
# 			public DatalogValidationException visit(PositiveAtom atom, DatalogValidationException e) {
# 				TermHelpers.fold(atom.getArgs(), tv, boundVars);
# 				hasPositiveAtom.value = true;
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(BinaryUnifier u, DatalogValidationException e) {
# 				if (!allowBinaryUnification) {
# 					return new DatalogValidationException("Binary unification is not allowed: ");
# 				}
# 				TermHelpers.fold(u.getArgsIterable(), tv, possiblyUnboundVars);
# 				TermHelpers.unify(u.getLeft(), u.getRight(), subst);
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(BinaryDisunifier u, DatalogValidationException e) {
# 				if (!allowBinaryDisunification) {
# 					return new DatalogValidationException("Binary disunification is not allowed: ");
# 				}
# 				TermHelpers.fold(u.getArgsIterable(), tv, possiblyUnboundVars);
# 				return e;
# 			}
#
# 			@Override
# 			public DatalogValidationException visit(NegatedAtom atom, DatalogValidationException e) {
# 				if (!allowNegatedBodyAtom) {
# 					return new DatalogValidationException("Negated body atoms are not allowed: ");
# 				}
# 				TermHelpers.fold(atom.getArgs(), tv, possiblyUnboundVars);
# 				return e;
# 			}
#
# 		};
#
# 		for (Premise c : clause.getBody()) {
# 			DatalogValidationException e = c.accept(cv, null);
# 			if (e != null) {
# 				throw e;
# 			}
# 		}
#
# 		for (Variable x : possiblyUnboundVars) {
# 			if (!boundVars.contains(x) && !(subst.get(x) instanceof Constant)) {
# 				throw new DatalogValidationException("Every variable in a rule must be bound, but " + x
# 						+ " is not bound in the rule " + clause
# 						+ " A variable X is bound if 1) it appears in a positive (non-negated) body atom, or 2) it is explicitly unified with a constant (e.g., X=a) or with a variable that is bound (e.g., X=Y, where Y is bound).");
# 			}
# 		}
#
# 		List<Premise> newBody = new ArrayList<>(clause.getBody());
# 		if (!hasPositiveAtom.value && !newBody.isEmpty()) {
# 			newBody.add(0, True.getTrueAtom());
# 		}
#
# 		return new ValidClause(clause.getHead(), newBody);
# 	}
#
# 	private static final class Program implements UnstratifiedProgram {
# 		private final Set<ValidClause> rules;
# 		private final Set<PositiveAtom> initialFacts;
# 		private final Set<PredicateSym> edbPredicateSymbols;
# 		private final Set<PredicateSym> idbPredicateSymbols;
#
# 		public Program(Set<ValidClause> rules, Set<PositiveAtom> initialFacts, Set<PredicateSym> edbPredicateSymbols,
# 				Set<PredicateSym> idbPredicateSymbols) {
# 			this.rules = rules;
# 			this.initialFacts = initialFacts;
# 			this.edbPredicateSymbols = edbPredicateSymbols;
# 			this.idbPredicateSymbols = idbPredicateSymbols;
# 		}
#
# 		public Set<ValidClause> getRules() {
# 			return this.rules;
# 		}
#
# 		public Set<PositiveAtom> getInitialFacts() {
# 			return this.initialFacts;
# 		}
#
# 		public Set<PredicateSym> getEdbPredicateSyms() {
# 			return this.edbPredicateSymbols;
# 		}
#
# 		public Set<PredicateSym> getIdbPredicateSyms() {
# 			return this.idbPredicateSymbols;
# 		}
#
# 	}
#
# 	private final static class True {
#
# 		private True() {
# 			// Cannot be instantiated.
# 		}
#
# 		private static class TruePred extends PredicateSym {
#
# 			protected TruePred() {
# 				super("true", 0);
# 			}
#
# 		};
#
# 		private final static PositiveAtom trueAtom = PositiveAtom.create(new TruePred(), new Term[] {});
#
# 		public static PositiveAtom getTrueAtom() {
# 			return trueAtom;
# 		}
# 	}
#
# 	public static final class ValidClause extends Clause {
#
# 		private ValidClause(Head head, List<Premise> body) {
# 			super(head, body);
# 		}
#
# 	}
#
# }
