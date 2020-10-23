from typing import *

from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
#
from typing import *

I = TypeVar("I")
O = TypeVar("O")

# 	private class Visitor implements TermVisitor<I, O> {
class Visitor(TermVisitor[I, O]):
    def __init__(self, onVariable: Callable[[Variable, I], O], onConstant: Callable[[Constant, I], O], otherwise: Callable[[Term, I], O]):
        self.onVariable = onVariable
        self.onConstant = onConstant
        self.otherwise = otherwise
        super(Visitor, self).__init__()
#
# 		@Override
# 		public O visit(Variable t, I state) {
# 			if (onVariable != null) {
# 				return onVariable.apply(t, state);
# 			}
# 			return otherwise.apply(t, state);
# 		}
    def visit_variable(self, t: Variable, state: I) -> O:
        if self.onVariable:
            return self.onVariable(t, state)
        return self.otherwise(t, state)
#
# 		@Override
# 		public O visit(Constant t, I state) {
# 			if (onConstant != null) {
# 				return onConstant.apply(t, state);
# 			}
# 			return otherwise.apply(t, state);
# 		}
    def visit_constant(self, t: Constant, state: I) -> O:
        if self.onConstant:
            return self.onConstant(t, state)
        return self.otherwise(t, state)
# 	}
    pass
# public class TermVisitorBuilder<I, O> {
class TermVisitorBuilder(Generic[I, O]):
# 	private BiFunction<Variable, I, O> onVariable;
# 	private BiFunction<Constant, I, O> onConstant;
    def __init__(self):
        self._onVariable = None
        self._onConstant = None
#
# 	public TermVisitorBuilder<I, O> onVariable(BiFunction<Variable, I, O> f) {
# 		this.onVariable = f;
# 		return this;
# 	}
    def onVariable(self, f: Callable[[Variable, I], O]) -> "TermVisitorBuilder[I, O]":
        self._onVariable = f
        return self
#
# 	public TermVisitorBuilder<I, O> onConstant(BiFunction<Constant, I, O> f) {
# 		this.onConstant = f;
# 		return this;
# 	}
    def onConstant(self, f: Callable[[Constant, I], O]) -> "TermVisitorBuilder[I, O]":
        self._onConstant = f
        return self
#
#
# 	public TermVisitor<I, O> or(BiFunction<Term, I, O> f) {
# 		return new Visitor(f);
# 	}
    def or_(self, f: Callable[[Term, I], O]) -> TermVisitor[I, O]:
        return Visitor(self._onVariable, self._onConstant, f)
#
# 	public TermVisitor<I, O> orNull() {
# 		return this.or((t, state) -> null);
# 	}
    def orNull(self) -> TermVisitor[I, O]:
        return self.or_(lambda t, state: None)
#
# 	public TermVisitor<I, O> orCrash() {
# 		return this.or((t, state) -> { throw new UnsupportedOperationException(); });
# 	}
    def orCrash(self) -> TermVisitor[I, O]:
        def raise_error():
            raise NotImplementedError()
        return self.or_(lambda t, state: raise_error())

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
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.Variable;
#
# public class TermVisitorBuilder<I, O> {
# 	private BiFunction<Variable, I, O> onVariable;
# 	private BiFunction<Constant, I, O> onConstant;
#
# 	public TermVisitorBuilder<I, O> onVariable(BiFunction<Variable, I, O> f) {
# 		this.onVariable = f;
# 		return this;
# 	}
#
# 	public TermVisitorBuilder<I, O> onConstant(BiFunction<Constant, I, O> f) {
# 		this.onConstant = f;
# 		return this;
# 	}
#
# 	public TermVisitor<I, O> or(BiFunction<Term, I, O> f) {
# 		return new Visitor(f);
# 	}
#
# 	public TermVisitor<I, O> orNull() {
# 		return this.or((t, state) -> null);
# 	}
#
# 	public TermVisitor<I, O> orCrash() {
# 		return this.or((t, state) -> { throw new UnsupportedOperationException(); });
# 	}
#
# 	private class Visitor implements TermVisitor<I, O> {
# 		private final BiFunction<Variable, I, O> onVariable;
# 		private final BiFunction<Constant, I, O> onConstant;
# 		private final BiFunction<Term, I, O> otherwise;
#
# 		public Visitor(BiFunction<Term, I, O> otherwise) {
# 			this.onVariable = TermVisitorBuilder.this.onVariable;
# 			this.onConstant = TermVisitorBuilder.this.onConstant;
# 			this.otherwise = otherwise;
# 		}
#
# 		@Override
# 		public O visit(Variable t, I state) {
# 			if (onVariable != null) {
# 				return onVariable.apply(t, state);
# 			}
# 			return otherwise.apply(t, state);
# 		}
#
# 		@Override
# 		public O visit(Constant t, I state) {
# 			if (onConstant != null) {
# 				return onConstant.apply(t, state);
# 			}
# 			return otherwise.apply(t, state);
# 		}
# 	}
# }
