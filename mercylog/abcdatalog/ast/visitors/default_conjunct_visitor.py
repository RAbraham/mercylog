
# import abcdatalog.ast.BinaryDisunifier;
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
# import abcdatalog.ast.BinaryUnifier;
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
# import abcdatalog.ast.NegatedAtom;
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
# import abcdatalog.engine.bottomup.AnnotatedAtom;
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor

from typing import *

I = TypeVar("I")
O = TypeVar("O")



#
# public class DefaultConjunctVisitor<I, O> implements PremiseVisitor<I, O> {
class DefaultConjunctVisitor(Generic[I, O], PremiseVisitor[I, O]):
#
# 	@Override
# 	public O visit(PositiveAtom atom, I state) {
# 		return null;
# 	}
    def visit_positive_atom(self, atom: PositiveAtom, state: I)-> O:
        return None
#
# 	@Override
# 	public O visit(AnnotatedAtom atom, I state) {
# 		return null;
# 	}
    def visit_annotated_atom(self, atom: AnnotatedAtom, state: I) -> O:
        return None
#
# 	@Override
# 	public O visit(BinaryUnifier u, I state) {
# 		return null;
# 	}
    def visit_binary_unifier(self, u: BinaryUnifier, state: I) -> O:
        return None
#
# 	@Override
# 	public O visit(BinaryDisunifier u, I state) {
# 		return null;
# 	}
#
    def visit_binary_disunifier(self, u: BinaryDisunifier, state: I) -> O:
        return None
# 	@Override
# 	public O visit(NegatedAtom atom, I state) {
# 		return null;
# 	}
#
    def visit_negated_atom(self, atom: NegatedAtom, state: I) -> O:
        return None
# }
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
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.engine.bottomup.AnnotatedAtom;
#
# public class DefaultConjunctVisitor<I, O> implements PremiseVisitor<I, O> {
#
# 	@Override
# 	public O visit(PositiveAtom atom, I state) {
# 		return null;
# 	}
#
# 	@Override
# 	public O visit(AnnotatedAtom atom, I state) {
# 		return null;
# 	}
#
# 	@Override
# 	public O visit(BinaryUnifier u, I state) {
# 		return null;
# 	}
#
# 	@Override
# 	public O visit(BinaryDisunifier u, I state) {
# 		return null;
# 	}
#
# 	@Override
# 	public O visit(NegatedAtom atom, I state) {
# 		return null;
# 	}
#
# }
