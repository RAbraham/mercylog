from typing import *
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor

#
I = TypeVar("I")
O = TypeVar("O")


class CrashPremiseVisitor(Generic[I, O], PremiseVisitor[I, O]):
    def visit_positive_atom(self, atom: PositiveAtom, state: I) -> O:
        raise NotImplementedError()

    def visit_annotated_atom(self, atom: AnnotatedAtom, state: I) -> O:
        raise NotImplementedError()

    def visit_binary_unifier(self, u: BinaryUnifier, state: I) -> O:
        raise NotImplementedError()

    def visit_binary_disunifier(self, u: BinaryDisunifier, state: I) -> O:
        raise NotImplementedError()

    def visit_negated_atom(self, atom: NegatedAtom, state: I) -> O:
        raise NotImplementedError()


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
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.engine.bottomup.AnnotatedAtom;
#
# public class CrashPremiseVisitor<I, O> implements PremiseVisitor<I, O> {
#
# 	@Override
# 	public O visit(PositiveAtom atom, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# 	@Override
# 	public O visit(AnnotatedAtom atom, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# 	@Override
# 	public O visit(BinaryUnifier u, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# 	@Override
# 	public O visit(BinaryDisunifier u, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# 	@Override
# 	public O visit(NegatedAtom atom, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# }
