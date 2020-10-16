from typing import *
# import abcdatalog.ast.Head;
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from .head_visitor import HeadVisitor
I = TypeVar("I")
O = TypeVar("O")

class Visitor(HeadVisitor[I, O]):
    def __init__(self, onPositiveAtom: Callable[[PositiveAtom, I], O], otherwise: Callable[[Head, I], O]):
        self.onPositiveAtom = onPositiveAtom
        self.otherwise = otherwise

    def visit(self, atom: PositiveAtom, state: I)-> O:
        if self.onPositiveAtom:
            return self.onPositiveAtom(atom, state)
        return self.otherwise(atom, state)

class HeadVisitorBuilder(Generic[I, O]):
    def __init__(self):
        self._onPositiveAtom = None

    def onPositiveAtom(self, onPositiveAtom: Callable[[PositiveAtom, I], O]) -> "HeadVisitorBuilder[I, O]":
        self._onPositiveAtom = onPositiveAtom
        return self

    def or_(self, f: Callable[[Head, I], O]) -> HeadVisitor[I, O]:
        # return Visitor(f)
        return Visitor(self._onPositiveAtom, f)


    def orNull(self) -> HeadVisitor[I, O]:
        return self.or_(lambda head, state: None)

    def orCrash(self) -> HeadVisitor[I, O]:
        def not_implemented():
            raise NotImplementedError()
        return self.or_(lambda head, state: not_implemented())
    pass
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
# import abcdatalog.ast.Head;
# import abcdatalog.ast.PositiveAtom;
#
# public class HeadVisitorBuilder<I, O> {
# 	private BiFunction<PositiveAtom, I, O> onPositiveAtom;
#
# 	public HeadVisitorBuilder<I, O> onPositiveAtom(BiFunction<PositiveAtom, I, O> onPositiveAtom) {
# 		this.onPositiveAtom = onPositiveAtom;
# 		return this;
# 	}
#
# 	public HeadVisitor<I, O> or(BiFunction<Head, I, O> f) {
# 		return new Visitor(f);
# 	}
#
# 	public HeadVisitor<I, O> orNull() {
# 		return this.or((head, state) -> null);
# 	}
#
# 	public HeadVisitor<I, O> orCrash() {
# 		return this.or((head, state) -> { throw new UnsupportedOperationException(); });
# 	}
#
# 	private class Visitor implements HeadVisitor<I, O> {
# 		private final BiFunction<PositiveAtom, I, O> onPositiveAtom;
# 		private final BiFunction<Head, I, O> otherwise;
#
# 		public Visitor(BiFunction<Head, I, O> otherwise) {
# 			this.onPositiveAtom = HeadVisitorBuilder.this.onPositiveAtom;
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
# 	}
# }
