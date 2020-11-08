from typing import *
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.util.substitution.substitution import Substitution
from mercylog.abcdatalog.ast.term import Term
from dataclasses import dataclass

I = TypeVar("I")
O = TypeVar("O")


#
# /**
#  * A zero-ary function symbol (i.e., a constant in Datalog).
#  *
#  */

# public class Constant implements Term {
@dataclass(frozen=True)
class Constant(Term):
    name: str
# 	/**
# 	 * Identifier of the constant.
# 	 */
# 	private final String name;
#
# 	/**
# 	 * A map for memoization.
# 	 */
# 	private static final ConcurrentMap<String, Constant> memo = new ConcurrentHashMap<>();
#
# 	/**
# 	 * Returns a constant with the given string identifier.
# 	 *
# 	 * @param name
# 	 *            the string identifier
# 	 * @return the constant
# 	 */
# 	public static Constant create(String name) {
# 		Constant c = memo.get(name);
# 		if (c != null) {
# 			return c;
# 		}
# 		// try creating it
# 		c = new Constant(name);
# 		Constant existing = memo.putIfAbsent(name, c);
# 		if (existing != null) {
# 			return existing;
# 		}
# 		return c;
# 	}

    @staticmethod
    def create(name: str) -> "Constant":
        return Constant(name)


    def getName(self)-> str:
        return self.name


    def __str__(self):
        return self.getName()

    def __repr__(self):
        return self.__str__()

    def accept_term_visitor(self, visitor: TermVisitor[I, O], state: I):
        return visitor.visit_constant(self, state)

    def applySubst(self, subst: Substitution) -> "Term":
        return self
#
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
# package abcdatalog.ast;
#
# import java.util.concurrent.ConcurrentHashMap;
# import java.util.concurrent.ConcurrentMap;
#
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.util.substitution.Substitution;
#
# /**
#  * A zero-ary function symbol (i.e., a constant in Datalog).
#  *
#  */
# public class Constant implements Term {
# 	/**
# 	 * Identifier of the constant.
# 	 */
# 	private final String name;
#
# 	/**
# 	 * A map for memoization.
# 	 */
# 	private static final ConcurrentMap<String, Constant> memo = new ConcurrentHashMap<>();
#
# 	/**
# 	 * Returns a constant with the given string identifier.
# 	 *
# 	 * @param name
# 	 *            the string identifier
# 	 * @return the constant
# 	 */
# 	public static Constant create(String name) {
# 		Constant c = memo.get(name);
# 		if (c != null) {
# 			return c;
# 		}
# 		// try creating it
# 		c = new Constant(name);
# 		Constant existing = memo.putIfAbsent(name, c);
# 		if (existing != null) {
# 			return existing;
# 		}
# 		return c;
# 	}
#
# 	/**
# 	 * Constructs a constant with the given name.
# 	 *
# 	 * @param name
# 	 *            name
# 	 */
# 	private Constant(String name) {
# 		this.name = name;
# 	}
#
# 	public String getName() {
# 		return name;
# 	}
#
# 	@Override
# 	public String toString() {
# 		return this.getName();
# 	}
#
# 	@Override
# 	public <I, O> O accept(TermVisitor<I, O> visitor, I state) {
# 		return visitor.visit(this, state);
# 	}
#
# 	@Override
# 	public Term applySubst(Substitution subst) {
# 		return this;
# 	}
#
# }
