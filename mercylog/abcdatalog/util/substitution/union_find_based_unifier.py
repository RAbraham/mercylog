import copy
from typing import *

# import abcdatalog.ast.Constant;
from mercylog.abcdatalog.ast.constant import Constant

# import abcdatalog.ast.Term;
from mercylog.abcdatalog.ast.term import Term

# import abcdatalog.ast.Variable;
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.util.substitution.term_unifier import TermUnifier

#
# /**
#  * A mapping from variables to terms. Implemented using a union-find data
#  * structure.
#  *
#  */

# public class UnionFindBasedUnifier implements TermUnifier {
class UnionFindBasedUnifier(TermUnifier):
    # 	/**
    # 	 * Map implementation of a union-find (also known as a disjoint-set) data
    # 	 * structure. This represents a substitution in that a variable is treated
    # 	 * as bound to the representative element of the set it is in. If there is a
    # 	 * constant in the set, the representative element will be a constant.
    # 	 */
    # 	private final Map<Term, Term> uf;
    #
    # 	/**

    def __init__(self, other: "UnionFindBasedUnifier" = None):
        if other:
            self.uf = copy.copy(other)
        else:
            self.uf = {}
        super().__init__()

    # 	/**
    # 	 * Retrieves the mapping of a variable.
    # 	 *
    # 	 * @param x
    # 	 *            the variable
    # 	 * @return the term that the variable is bound to, or null if the variable
    # 	 *         is not in the substitution
    # 	 */
    # 	@Override
    # 	public Term get(Variable x) {
    # 		return this.find(x);
    # 	}

    def get(self, x: Variable) -> Term:
        return self.get(x)

    def apply(self, original: List[Term]) -> List[Term]:
        r: List[Term] = []
        for o in original:
            t = o
            if isinstance(t, Variable):
                s = self.get(t)
                if s:
                    t = s
            r.append(t)

        return r

    # 	/**
    # 	 * Creates a substitution from unifying two lists of terms.
    # 	 *
    # 	 * @param xs
    # 	 *            the first list
    # 	 * @param ys
    # 	 *            the second list
    # 	 * @return the substitution, or null if the two lists do not unify
    # 	 */
    # 	public static UnionFindBasedUnifier fromTerms(List<Term> xs, List<Term> ys) {
    @staticmethod
    def fromTerms(xs: List[Term], ys: List[Term]) -> Optional["UnionFindBasedUnifier"]:

# 		// Lists of different sizes cannot be unified.
# 		if (xs.size() != ys.size()) {
# 			return null;
# 		}
        if len(xs) != len(ys):
            return None
#
# 		// Initialize union-find data structure so that each term from both
# 		// lists is in a singleton set.
# 		UnionFindBasedUnifier r = new UnionFindBasedUnifier();
        r = UnionFindBasedUnifier()

# 		for (Term x : xs) {
# 			r.uf.put(x, x);
# 		}
        for x in xs:
            r.uf[x] = x
# 		for (Term y : ys) {
# 			r.uf.put(y, y);
# 		}
        for y in ys:
            r.uf[y] = y
#
# 		// Generate substitution by iterating through both atoms concurrently.
# 		Iterator<Term> xiter = xs.iterator();
# 		Iterator<Term> yiter = ys.iterator();
        zipped = zip(xs, ys)
# 		while (xiter.hasNext()) {
        for x, y in zipped:
# 			Term x = xiter.next();
# 			Term y = yiter.next();
#
# 			Term xroot = r.find(x);
# 			Term yroot = r.find(y);
#
            xroot = r.find(x)
            yroot = r.find(y)

# 			// Already in same set.
# 			if (xroot == yroot)
# 				continue;
#
            if xroot == yroot:
                continue
# 			// Two constants cannot be unified.
# 			if (xroot instanceof Constant && yroot instanceof Constant) {
# 				return null;
# 			}
            if isinstance(xroot, Constant) and isinstance(yroot, Constant):
                return None
#
# 			r.union(xroot, yroot);
            r.union(xroot, yroot)
# 		}
#
# 		return r;
        return r
# 	}
#
        pass
    # 	/**
    # 	 * Creates a substitution from unifying two arrays of terms.
    # 	 *
    # 	 * @param xs
    # 	 *            the first array
    # 	 * @param ys
    # 	 *            the second array
    # 	 * @return the substitution, or null if the two lists do not unify
    # 	 */
    # 	public static Substitution fromTerms(Term[] elts, Term[] elts2) {
    # 		// TODO this is inefficient
    # 		return fromTerms(Arrays.asList(elts), Arrays.asList(elts2));
    # 	}
    #

    # 	/**
    # 	 * Adds a mapping from a variable to a term. Throws an
    # 	 * IllegalArgumentException if doing so would result in a variable mapping
    # 	 * to multiple constants.
    # 	 *
    # 	 * @param v
    # 	 *            the variable
    # 	 * @param t
    # 	 *            the term
    # 	 * @throws IllegalArgumentException
    # 	 *             If the variable is already mapped to a different term
    # 	 */
    # 	public void put(Variable v, Term t) {
    def put(self, v: Variable, t: Term) -> None:
# 		Term vroot = this.find(v);
        vroot = self.find(v)
# 		if (vroot == null) {
# 			vroot = v;
# 		}
        if not vroot:
            vroot = v
#
# 		Term troot = this.find(t);
        troot = self.find(t)
# 		if (troot == null) {
# 			troot = t;
# 		}
        if not troot:
            troot = t
#
# 		if (vroot.equals(troot))
# 			return;
        if vroot == troot:
            return None
#
# 		if (vroot instanceof Constant && troot instanceof Constant) {
# 			throw new IllegalArgumentException("Variable " + v.getName()
# 					+ " already mapped to " + ((Constant) vroot).getName()
# 					+ "; cannot remap to " + ((Constant) troot).getName() + ".");
# 		}
#         TODO: This check seems duplicated
        if isinstance(vroot, Constant) and isinstance(troot, Constant):
            raise ValueError(f"Variable {v.getName()} already mapped to {vroot.getName()};"
                             f"cannot remap to {troot.getName()}." )

#
# 		this.uf.put(v, vroot);
        self.uf[v] = vroot
# 		this.uf.put(t, troot);
        self.uf[t] = troot
# 		union(v, t);
        self.union(v, t)
# 	}
#
    pass
    # 	/**
    # 	 * Unions the sets of two terms in the union-find data structure.
    # 	 *
    # 	 * @param x
    # 	 *            the first term
    # 	 * @param y
    # 	 *            the second term
    # 	 */
    def union(self, x: Term, y:Term) -> None:
        xroot: Term = self.find(x)
        yroot: Term = self.find(y)
        assert xroot and yroot
        # Keep constants at the root of tree
        if isinstance(xroot, Constant):
            self.uf[yroot] = xroot
        else:
            self.uf[xroot] = yroot
        pass
    # 	/**
    # 	 * Retrieves the representative element of the set that contains a certain
    # 	 * term in the union-find data structure.
    # 	 *
    # 	 * @param x
    # 	 *            the term
    # 	 * @return the representative element, or null if the provided term is not
    # 	 *         in the data structure
    # 	 */
    # 	private Term find(Term x) {
    # 		Term child = x;
    # 		Term parent = this.uf.get(child);
    # 		if (parent == null) {
    # 			return null;
    # 		}
    #
    # 		// When the child is equal to the parent, we have reached the root.
    # 		while (!child.equals(parent)) {
    # 			Term grandparent = this.uf.get(parent);
    # 			// Simple path compression.
    # 			this.uf.put(child, grandparent);
    # 			child = grandparent;
    # 			parent = this.uf.get(child);
    # 		}
    # 		return parent;
    # 	}

    def find(self, x: Term) -> Optional[Term]:
        child: Term = x
        parent: Term = self.uf.get(child)
        if not parent:
            return None
        # When the child is equal to the parent, we have reached the root.
        while child != parent:
            grandparent: Term = self.uf.get(parent)
        #     Simple path compression
            self.uf[child] = grandparent
            child = grandparent
            parent = self.uf.get(child)

        return parent

    def __str__(self):
        elements = []
        for k,v in self.uf.items():
            if isinstance(k, Variable):
                s = f"{k}->{self.find(k)}"
                elements.append(s)
        _strs = ", ".join(elements)
        result = "[" + _strs + "]"
        return result

    # 	@Override
    # 	public boolean unify(Variable u, Term v) {
    # 		Term uroot = this.find(u);
    # 		if (uroot == null) {
    # 			uroot = u;
    # 		}
    #
    # 		Term vroot = this.find(v);
    # 		if (vroot == null) {
    # 			vroot = v;
    # 		}
    #
    # 		if (uroot.equals(vroot)) {
    # 			return true;
    # 		}
    #
    # 		if (vroot instanceof Constant && uroot instanceof Constant) {
    # 			return false;
    # 		}
    #
    # 		this.uf.put(v, vroot);
    # 		this.uf.put(u, uroot);
    # 		union(v, u);
    # 		return true;
    # 	}
    #
    # }
    def unify(self, u: Variable, v: Term) -> bool:
        uroot: Term = self.find(u)
        if not uroot:
            uroot = u
        vroot: Term = self.find(v)
        if not vroot:
            vroot = v

        if uroot == vroot:
            return True

        if isinstance(vroot, Constant) and isinstance(uroot, Constant):
            return False

        self.uf[v] = vroot
        self.uf[u] = uroot
        self.union(v, u)
        return True


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
# import java.util.Arrays;
# import java.util.Iterator;
# import java.util.LinkedHashMap;
# import java.util.List;
# import java.util.Map;
#
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.Variable;
#
# /**
#  * A mapping from variables to terms. Implemented using a union-find data
#  * structure.
#  *
#  */
# public class UnionFindBasedUnifier implements TermUnifier {
# 	/**
# 	 * Map implementation of a union-find (also known as a disjoint-set) data
# 	 * structure. This represents a substitution in that a variable is treated
# 	 * as bound to the representative element of the set it is in. If there is a
# 	 * constant in the set, the representative element will be a constant.
# 	 */
# 	private final Map<Term, Term> uf;
#
# 	/**
# 	 * Constructs an empty substitution.
# 	 */
# 	public UnionFindBasedUnifier() {
# 		this.uf = new LinkedHashMap<>();
# 	}
#
# 	/**
# 	 * Constructs a substitution from another substitution.
# 	 *
# 	 * @param other
# 	 *            the other substitution
# 	 */
# 	public UnionFindBasedUnifier(UnionFindBasedUnifier other) {
# 		this.uf = new LinkedHashMap<>(other.uf);
# 	}
#
# 	/**
# 	 * Retrieves the mapping of a variable.
# 	 *
# 	 * @param x
# 	 *            the variable
# 	 * @return the term that the variable is bound to, or null if the variable
# 	 *         is not in the substitution
# 	 */
# 	@Override
# 	public Term get(Variable x) {
# 		return this.find(x);
# 	}
#
# 	@Override
# 	public Term[] apply(Term[] original) {
# 		Term[] r = new Term[original.length];
# 		for (int i = 0; i < original.length; ++i) {
# 			Term t = original[i];
# 			if (t instanceof Variable) {
# 				Term s = this.get((Variable) t);
# 				if (s != null) {
# 					t = s;
# 				}
# 			}
# 			r[i] = t;
# 		}
# 		return r;
# 	}
#
# 	/**
# 	 * Creates a substitution from unifying two lists of terms.
# 	 *
# 	 * @param xs
# 	 *            the first list
# 	 * @param ys
# 	 *            the second list
# 	 * @return the substitution, or null if the two lists do not unify
# 	 */
# 	public static UnionFindBasedUnifier fromTerms(List<Term> xs, List<Term> ys) {
# 		// Lists of different sizes cannot be unified.
# 		if (xs.size() != ys.size()) {
# 			return null;
# 		}
#
# 		// Initialize union-find data structure so that each term from both
# 		// lists is in a singleton set.
# 		UnionFindBasedUnifier r = new UnionFindBasedUnifier();
# 		for (Term x : xs) {
# 			r.uf.put(x, x);
# 		}
# 		for (Term y : ys) {
# 			r.uf.put(y, y);
# 		}
#
# 		// Generate substitution by iterating through both atoms concurrently.
# 		Iterator<Term> xiter = xs.iterator();
# 		Iterator<Term> yiter = ys.iterator();
# 		while (xiter.hasNext()) {
# 			Term x = xiter.next();
# 			Term y = yiter.next();
#
# 			Term xroot = r.find(x);
# 			Term yroot = r.find(y);
#
# 			// Already in same set.
# 			if (xroot == yroot)
# 				continue;
#
# 			// Two constants cannot be unified.
# 			if (xroot instanceof Constant && yroot instanceof Constant) {
# 				return null;
# 			}
#
# 			r.union(xroot, yroot);
# 		}
#
# 		return r;
# 	}
#
# 	/**
# 	 * Creates a substitution from unifying two arrays of terms.
# 	 *
# 	 * @param xs
# 	 *            the first array
# 	 * @param ys
# 	 *            the second array
# 	 * @return the substitution, or null if the two lists do not unify
# 	 */
# 	public static Substitution fromTerms(Term[] elts, Term[] elts2) {
# 		// TODO this is inefficient
# 		return fromTerms(Arrays.asList(elts), Arrays.asList(elts2));
# 	}
#
# 	/**
# 	 * Adds a mapping from a variable to a term. Throws an
# 	 * IllegalArgumentException if doing so would result in a variable mapping
# 	 * to multiple constants.
# 	 *
# 	 * @param v
# 	 *            the variable
# 	 * @param t
# 	 *            the term
# 	 * @throws IllegalArgumentException
# 	 *             If the variable is already mapped to a different term
# 	 */
# 	public void put(Variable v, Term t) {
# 		Term vroot = this.find(v);
# 		if (vroot == null) {
# 			vroot = v;
# 		}
#
# 		Term troot = this.find(t);
# 		if (troot == null) {
# 			troot = t;
# 		}
#
# 		if (vroot.equals(troot))
# 			return;
#
# 		if (vroot instanceof Constant && troot instanceof Constant) {
# 			throw new IllegalArgumentException("Variable " + v.getName()
# 					+ " already mapped to " + ((Constant) vroot).getName()
# 					+ "; cannot remap to " + ((Constant) troot).getName() + ".");
# 		}
#
# 		this.uf.put(v, vroot);
# 		this.uf.put(t, troot);
# 		union(v, t);
# 	}
#
# 	/**
# 	 * Unions the sets of two terms in the union-find data structure.
# 	 *
# 	 * @param x
# 	 *            the first term
# 	 * @param y
# 	 *            the second term
# 	 */
# 	private void union(Term x, Term y) {
# 		Term xroot = this.find(x);
# 		Term yroot = this.find(y);
# 		assert xroot != null && yroot != null;
#
# 		// Keep constants at root of tree.
# 		if (xroot instanceof Constant) {
# 			this.uf.put(yroot, xroot);
# 		} else {
# 			this.uf.put(xroot, yroot);
# 		}
# 	}
#
# 	/**
# 	 * Retrieves the representative element of the set that contains a certain
# 	 * term in the union-find data structure.
# 	 *
# 	 * @param x
# 	 *            the term
# 	 * @return the representative element, or null if the provided term is not
# 	 *         in the data structure
# 	 */
# 	private Term find(Term x) {
# 		Term child = x;
# 		Term parent = this.uf.get(child);
# 		if (parent == null) {
# 			return null;
# 		}
#
# 		// When the child is equal to the parent, we have reached the root.
# 		while (!child.equals(parent)) {
# 			Term grandparent = this.uf.get(parent);
# 			// Simple path compression.
# 			this.uf.put(child, grandparent);
# 			child = grandparent;
# 			parent = this.uf.get(child);
# 		}
# 		return parent;
# 	}
#
# 	@Override
# 	public String toString() {
# 		StringBuilder sb = new StringBuilder();
# 		sb.append("[");
# 		for (Iterator<Term> it = this.uf.keySet().iterator(); it.hasNext();) {
# 			Term key = it.next();
# 			if (key instanceof Variable) {
# 				sb.append(key + "->" + find(key));
# 				if (it.hasNext()) {
# 					sb.append(", ");
# 				}
# 			}
# 		}
# 		sb.append("]");
# 		return sb.toString();
# 	}
#
# 	@Override
# 	public boolean unify(Variable u, Term v) {
# 		Term uroot = this.find(u);
# 		if (uroot == null) {
# 			uroot = u;
# 		}
#
# 		Term vroot = this.find(v);
# 		if (vroot == null) {
# 			vroot = v;
# 		}
#
# 		if (uroot.equals(vroot)) {
# 			return true;
# 		}
#
# 		if (vroot instanceof Constant && uroot instanceof Constant) {
# 			return false;
# 		}
#
# 		this.uf.put(v, vroot);
# 		this.uf.put(u, uroot);
# 		union(v, u);
# 		return true;
# 	}
#
# }
