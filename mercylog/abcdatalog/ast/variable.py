from typing import *
# from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
# from mercylog.abcdatalog.util.substitution.substitution import Substitution
from mercylog.abcdatalog.ast.term import Term

I = TypeVar("I")
O = TypeVar("O")

#
# /**
#  * A Datalog variable.
#  *
#  */
# public class Variable implements Term {
class Variable(Term):
    # 	/**
    # 	 * Identifier for this variable.
    # 	 */
    # 	private final String name;
    #
    # 	/**
    # 	 * Map for memoization.
    # 	 */
    # 	private static final ConcurrentMap<String, Variable> memo = new ConcurrentHashMap<>();
    memo: Dict[str, "Variable"] = dict()
    #
    # 	/**
    # 	 * Returns a variable with the given string identifier.
    # 	 *
    # 	 * @param name
    # 	 *            the string identifier
    # 	 * @return the variable
    # 	 */
    # 	public static Variable create(String name) {
    # 		Variable c = memo.get(name);
    # 		if (c != null) {
    # 			return c;
    # 		}
    # 		// try creating it
    # 		c = new Variable(name);
    # 		Variable existing = memo.putIfAbsent(name, c);
    # 		if (existing != null) {
    # 			return existing;
    # 		}
    # 		return c;
    # 	}
    @staticmethod
    def create(name: str) -> "Variable":
        c = Variable.memo.get(name)
        if c:
            return c
        c = Variable(name)
        Variable.memo[name] = c
        return c

    #
    # 	/**
    # 	 * Constructs a variable from an identifier.
    # 	 *
    # 	 * @param name
    # 	 *            identifier
    # 	 */
    # 	protected Variable(String name) {
    # 		this.name = name;
    # 	}
    #
    def __init__(self, name: str):
        self.name = name
        super().__init__()

    # 	public String getName() {
    # 		return name;
    # 	}
    #
    def getName(self) -> str:
        return self.name

    # 	@Override
    # 	public String toString() {
    # 		return this.getName();
    # 	}
    #
    def __str__(self):
        return self.getName()

    def __repr__(self):
        return self.getName()

    # 	@Override
    # 	public <I, O> O accept(TermVisitor<I, O> visitor, I state) {
    # 		return visitor.visit(this, state);
    # 	}
    def accept_term_visitor(self, visitor , state: I) -> O:
        return visitor.visit_variable(self, state)

    #
    # 	public static Variable createFreshVariable() {
    # 		return new Variable("_");
    # 	}
    @staticmethod
    def createFreshVariable() -> "Variable":
        return Variable("_")

    #
    # 	@Override
    # 	public Term applySubst(Substitution subst) {
    # 		Term s = subst.get(this);
    # 		return (s != null) ? s : this;
    # 	}
    def applySubst(self, subst) -> "Term":
        s: Term = subst.get(self)
        if s:
            return s
        else:
            return self


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
# package abcdatalog.ast;
#
# import java.util.concurrent.ConcurrentHashMap;
# import java.util.concurrent.ConcurrentMap;
#
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.util.substitution.Substitution;
#
# /**
#  * A Datalog variable.
#  *
#  */
# public class Variable implements Term {
# 	/**
# 	 * Identifier for this variable.
# 	 */
# 	private final String name;
#
# 	/**
# 	 * Map for memoization.
# 	 */
# 	private static final ConcurrentMap<String, Variable> memo = new ConcurrentHashMap<>();
#
# 	/**
# 	 * Returns a variable with the given string identifier.
# 	 *
# 	 * @param name
# 	 *            the string identifier
# 	 * @return the variable
# 	 */
# 	public static Variable create(String name) {
# 		Variable c = memo.get(name);
# 		if (c != null) {
# 			return c;
# 		}
# 		// try creating it
# 		c = new Variable(name);
# 		Variable existing = memo.putIfAbsent(name, c);
# 		if (existing != null) {
# 			return existing;
# 		}
# 		return c;
# 	}
#
# 	/**
# 	 * Constructs a variable from an identifier.
# 	 *
# 	 * @param name
# 	 *            identifier
# 	 */
# 	protected Variable(String name) {
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
# 	public static Variable createFreshVariable() {
# 		return new Variable("_");
# 	}
#
# 	@Override
# 	public Term applySubst(Substitution subst) {
# 		Term s = subst.get(this);
# 		return (s != null) ? s : this;
# 	}
# }
