from typing import *
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
I = TypeVar("I")
O = TypeVar("O")

# 	private class Visitor implements PremiseVisitor<I,O> {
class Visitor(PremiseVisitor):

    def __init__(self, otherwise: Callable[[Premise, I], O], onPositiveAtom, onNegatedAtom, onBinaryUnifier, onBinaryDisunifier, onAnnotatedAtom):
        self.otherwise = otherwise
        self.onPositiveAtom = onPositiveAtom
        self.onNegatedAtom = onNegatedAtom
        self.onBinaryUnifier =    onBinaryUnifier
        self.onBinaryDisunifier = onBinaryDisunifier
        self.onAnnotatedAtom = onAnnotatedAtom

#
# 		@Override
# 		public O visit(PositiveAtom atom, I state) {
# 			if (this.onPositiveAtom != null) {
# 				return this.onPositiveAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
    def visit_positive_atom(self, atom: PositiveAtom, state: I) -> O:
        if self.onPositiveAtom:
            return self.onPositiveAtom(atom, state)

        return self.otherwise(atom, state)
#
# 		@Override
# 		public O visit(BinaryUnifier u, I state) {
# 			if (this.onBinaryUnifier != null) {
# 				return this.onBinaryUnifier.apply(u, state);
# 			}
# 			return this.otherwise.apply(u, state);
# 		}
    def visit_binary_unifier(self, u: BinaryUnifier, state: I) -> O:
        if self.onBinaryUnifier:
            return self.onBinaryUnifier(u, state)

        return self.otherwise(u, state)
#
# 		@Override
# 		public O visit(BinaryDisunifier u, I state) {
# 			if (this.onBinaryDisunifier != null) {
# 				return this.onBinaryDisunifier.apply(u, state);
# 			}
# 			return this.otherwise.apply(u, state);
# 		}
    def visit_binary_disunifier(self, u: BinaryDisunifier, state: I) -> O:
        if self.onBinaryDisunifier:
            return self.onBinaryDisunifier(u, state)

        return self.otherwise(u, state)
#
# 		@Override
# 		public O visit(NegatedAtom atom, I state) {
# 			if (this.onNegatedAtom != null) {
# 				return this.onNegatedAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
    def visit_negated_atom(self, atom: NegatedAtom, state: I) -> O:
        if self.onNegatedAtom:
            return self.onNegatedAtom(atom, state)

        return self.otherwise(atom, state)
#
# 		@Override
# 		public O visit(AnnotatedAtom atom, I state) {
# 			if (this.onAnnotatedAtom != null) {
# 				return this.onAnnotatedAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
    def visit_annotated_atom(self, atom: AnnotatedAtom, state: I) -> O:
        if self.onAnnotatedAtom:
            return self.onAnnotatedAtom(atom, state)

        return self.otherwise(atom, state)
# 	}

    pass


class PremiseVisitorBuilder(Generic[I, O]):
# public class PremiseVisitorBuilder<I, O> {
# 	private BiFunction<PositiveAtom, I, O> onPositiveAtom;
# 	private BiFunction<NegatedAtom, I, O> onNegatedAtom;
# 	private BiFunction<BinaryUnifier, I, O> onBinaryUnifier;
# 	private BiFunction<BinaryDisunifier, I, O> onBinaryDisunifier;
# 	private BiFunction<AnnotatedAtom, I, O> onAnnotatedAtom;
    def __init__(self ):
        self._onPositiveAtom = None
        self._onNegatedAtom = None
        self._onBinaryUnifier = None
        self._onBinaryDisunifier = None
        self._onAnnotatedAtom = None
#
# 	public PremiseVisitorBuilder<I, O> onPositiveAtom(BiFunction<PositiveAtom, I, O> onPositiveAtom) {
# 		this.onPositiveAtom = onPositiveAtom;
# 		return this;
# 	}
    def onPositiveAtom(self, onPositiveAtom) -> "PremiseVisitorBuilder":
        self._onPositiveAtom = onPositiveAtom
        return self

#
# 	public PremiseVisitorBuilder<I, O> onNegatedAtom(BiFunction<NegatedAtom, I, O> onNegatedAtom) {
# 		this.onNegatedAtom = onNegatedAtom;
# 		return this;
# 	}
    def onNegatedAtom(self, onNegatedAtom) -> "PremiseVisitorBuilder":
        self._onNegatedAtom = onNegatedAtom
        return self

    #
# 	public PremiseVisitorBuilder<I, O> onBinaryUnifier(BiFunction<BinaryUnifier, I, O> onBinaryUnifier) {
# 		this.onBinaryUnifier = onBinaryUnifier;
# 		return this;
# 	}
    def onBinaryUnifier(self, onBinaryUnifier) -> "PremiseVisitorBuilder":
        self._onBinaryUnifier = onBinaryUnifier
        return self

#
# 	public PremiseVisitorBuilder<I, O> onBinaryDisunifier(BiFunction<BinaryDisunifier, I, O> onBinaryDisunifier) {
# 		this.onBinaryDisunifier = onBinaryDisunifier;
# 		return this;
# 	}
    def onBinaryDisnifier(self, onBinaryDisunifier) -> "PremiseVisitorBuilder":
        self._onBinaryDisunifier = onBinaryDisunifier
        return self

#
# 	public PremiseVisitorBuilder<I, O> onAnnotatedAtom(BiFunction<AnnotatedAtom, I, O> onAnnotatedAtom) {
# 		this.onAnnotatedAtom = onAnnotatedAtom;
# 		return this;
# 	}
    def onAnnotatedAtom(self, onAnnotatedAtom) -> "PremiseVisitorBuilder":
        self._onAnnotatedAtom = onAnnotatedAtom
        return self

#
# 	public PremiseVisitor<I, O> or(BiFunction<Premise, I, O> f) {
# 		return new Visitor(f);
# 	}
    def or_(self, f: Callable[[Premise, I], O]) -> PremiseVisitor[I, O]:
        return Visitor(f, self._onPositiveAtom, self._onNegatedAtom, self._onBinaryUnifier, self._onBinaryDisunifier, self._onAnnotatedAtom)
#
# 	public PremiseVisitor<I, O> orCrash() {
# 		return this.or((conj, state) -> { throw new UnsupportedOperationException(); });
# 	}
    def orCrash(self) -> PremiseVisitor[I, O]:
        def raise_error():
            raise NotImplementedError()
        return self.or_(lambda conj, state: raise_error())

#
# 	public PremiseVisitor<I, O> orNull() {
# 		return this.or((conj, state) -> null);
# 	}
#
    def orNull(self) -> PremiseVisitor[I, O]:
        return self.or_(lambda conj, state: None)
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
# package abcdatalog.ast.visitors;
#
# import java.util.function.BiFunction;
#
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.Premise;
# import abcdatalog.engine.bottomup.AnnotatedAtom;
#
# public class PremiseVisitorBuilder<I, O> {
# 	private BiFunction<PositiveAtom, I, O> onPositiveAtom;
# 	private BiFunction<NegatedAtom, I, O> onNegatedAtom;
# 	private BiFunction<BinaryUnifier, I, O> onBinaryUnifier;
# 	private BiFunction<BinaryDisunifier, I, O> onBinaryDisunifier;
# 	private BiFunction<AnnotatedAtom, I, O> onAnnotatedAtom;
#
# 	public PremiseVisitorBuilder<I, O> onPositiveAtom(BiFunction<PositiveAtom, I, O> onPositiveAtom) {
# 		this.onPositiveAtom = onPositiveAtom;
# 		return this;
# 	}
#
# 	public PremiseVisitorBuilder<I, O> onNegatedAtom(BiFunction<NegatedAtom, I, O> onNegatedAtom) {
# 		this.onNegatedAtom = onNegatedAtom;
# 		return this;
# 	}
#
# 	public PremiseVisitorBuilder<I, O> onBinaryUnifier(BiFunction<BinaryUnifier, I, O> onBinaryUnifier) {
# 		this.onBinaryUnifier = onBinaryUnifier;
# 		return this;
# 	}
#
# 	public PremiseVisitorBuilder<I, O> onBinaryDisunifier(BiFunction<BinaryDisunifier, I, O> onBinaryDisunifier) {
# 		this.onBinaryDisunifier = onBinaryDisunifier;
# 		return this;
# 	}
#
# 	public PremiseVisitorBuilder<I, O> onAnnotatedAtom(BiFunction<AnnotatedAtom, I, O> onAnnotatedAtom) {
# 		this.onAnnotatedAtom = onAnnotatedAtom;
# 		return this;
# 	}
#
# 	public PremiseVisitor<I, O> or(BiFunction<Premise, I, O> f) {
# 		return new Visitor(f);
# 	}
#
# 	public PremiseVisitor<I, O> orCrash() {
# 		return this.or((conj, state) -> { throw new UnsupportedOperationException(); });
# 	}
#
# 	public PremiseVisitor<I, O> orNull() {
# 		return this.or((conj, state) -> null);
# 	}
#
# 	private class Visitor implements PremiseVisitor<I,O> {
# 		private final BiFunction<PositiveAtom, I, O> onPositiveAtom;
# 		private final BiFunction<NegatedAtom, I, O> onNegatedAtom;
# 		private final BiFunction<BinaryUnifier, I, O> onBinaryUnifier;
# 		private final BiFunction<BinaryDisunifier, I, O> onBinaryDisunifier;
# 		private BiFunction<AnnotatedAtom, I, O> onAnnotatedAtom;
# 		private final BiFunction<Premise, I, O> otherwise;
#
# 		public Visitor(BiFunction<Premise, I, O> otherwise) {
# 			this.onPositiveAtom = PremiseVisitorBuilder.this.onPositiveAtom;
# 			this.onNegatedAtom = PremiseVisitorBuilder.this.onNegatedAtom;
# 			this.onBinaryUnifier = PremiseVisitorBuilder.this.onBinaryUnifier;
# 			this.onBinaryDisunifier = PremiseVisitorBuilder.this.onBinaryDisunifier;
# 			this.onAnnotatedAtom = PremiseVisitorBuilder.this.onAnnotatedAtom;
# 			this.otherwise = otherwise;
# 		}
#
# 		@Override
# 		public O visit(PositiveAtom atom, I state) {
# 			if (this.onPositiveAtom != null) {
# 				return this.onPositiveAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
#
# 		@Override
# 		public O visit(BinaryUnifier u, I state) {
# 			if (this.onBinaryUnifier != null) {
# 				return this.onBinaryUnifier.apply(u, state);
# 			}
# 			return this.otherwise.apply(u, state);
# 		}
#
# 		@Override
# 		public O visit(BinaryDisunifier u, I state) {
# 			if (this.onBinaryDisunifier != null) {
# 				return this.onBinaryDisunifier.apply(u, state);
# 			}
# 			return this.otherwise.apply(u, state);
# 		}
#
# 		@Override
# 		public O visit(NegatedAtom atom, I state) {
# 			if (this.onNegatedAtom != null) {
# 				return this.onNegatedAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
#
# 		@Override
# 		public O visit(AnnotatedAtom atom, I state) {
# 			if (this.onAnnotatedAtom != null) {
# 				return this.onAnnotatedAtom.apply(atom, state);
# 			}
# 			return this.otherwise.apply(atom, state);
# 		}
# 	}
# }
