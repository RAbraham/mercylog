from typing import *
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
from mercylog.abcdatalog.ast.visitors.default_conjunct_visitor import DefaultConjunctVisitor
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor
from mercylog.abcdatalog.ast.visitors.head_visitor_builder import HeadVisitorBuilder
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
## import abcdatalog.parser.DatalogParseException;
## import abcdatalog.parser.DatalogParser;
## import abcdatalog.parser.DatalogTokenizer;

# import abcdatalog.util.graph.Digraph;
# import abcdatalog.util.graph.DirectedEdge;
from mercylog.abcdatalog.util.graph.digraph import Digraph
from mercylog.abcdatalog.util.graph.directed_edge import DirectedEdge
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import DatalogValidationException
# 	private static class AnnotatedEdge implements DirectedEdge<PredicateSym> {
class AnnotatedEdge(DirectedEdge[PredicateSym]):
# 		private final PredicateSym source;
# 		private final PredicateSym dest;
# 		private final boolean isNegated;
#
# 		public AnnotatedEdge(PredicateSym source, PredicateSym dest, boolean isNegated) {
# 			this.source = source;
# 			this.dest = dest;
# 			this.isNegated = isNegated;
# 		}
    def __init__(self, source: PredicateSym, dest: PredicateSym, isNegated: bool):
        self.source = source
        self.dest = dest
        self._isNegated = isNegated
        super(AnnotatedEdge, self).__init__()
#
# 		@Override
# 		public PredicateSym getSource() {
# 			return this.source;
# 		}
    def getSource(self) -> PredicateSym:
        return self.source
#
# 		@Override
# 		public PredicateSym getDest() {
# 			return this.dest;
# 		}
    def getDest(self) -> PredicateSym:
        return self.dest
#
# 		public boolean isNegated() {
# 			return this.isNegated;
# 		}
#
    def isNegated(self) -> bool:
        return self._isNegated
# 		public AnnotatedEdge reverse() {
# 			return new AnnotatedEdge(this.dest, this.source, this.isNegated);
# 		}
    def reverse(self) -> "AnnotatedEdge":
        return AnnotatedEdge(self.dest, self.source, self._isNegated)

# 	}
#
#
    pass
# 		PremiseVisitor<PredicateSym, Void> addEdge = new DefaultConjunctVisitor<PredicateSym, Void>() {
# 			@Override
# 			public Void visit(PositiveAtom atom, PredicateSym headPred) {
# 				if (!program.getEdbPredicateSyms().contains(atom.getPred())) {
# 					graph.addEdge(new AnnotatedEdge(atom.getPred(), headPred, false));
# 				}
# 				return null;
# 			}
#
# 			@Override
# 			public Void visit(NegatedAtom atom, PredicateSym headPred) {
# 				if (!program.getEdbPredicateSyms().contains(atom.getPred())) {
# 					graph.addEdge(new AnnotatedEdge(atom.getPred(), headPred, true));
# 				}
# 				return null;
# 			}
# 		};
class LocalDefaultConjunctVisitor(DefaultConjunctVisitor):
    def __init__(self, program, graph):
        self.program = program
        self.graph = graph

    def visit_positive_atom(self, atom: PositiveAtom, headPred: PredicateSym):
        if atom.getPred() not in self.program.getEdbPredicateSyms():
                self.graph.addEdge(AnnotatedEdge(atom.getPred(), headPred, False))
        pass

    def visit_negated_atom(self, atom: NegatedAtom, headPred: PredicateSym):
        # TODO: duplicate if condition

        if atom.getPred() not in self.program.getEdbPredicateSyms():
            self.graph.addEdge(AnnotatedEdge(atom.getPred(), headPred, True))

    pass
# class StratifiedNegationGraph {

class StratifiedNegationGraph:
# 	public static StratifiedNegationGraph create(UnstratifiedProgram program) throws DatalogValidationException {
    @staticmethod
    def create(program: UnstratifiedProgram)-> "StratifiedNegationGraph":
        graph: Digraph[PredicateSym, AnnotatedEdge] = Digraph()
        getHeadPred: HeadVisitor = HeadVisitorBuilder().onPositiveAtom(lambda atom, nothing: atom.getPred()).orCrash()
        addEdge: PremiseVisitor = LocalDefaultConjunctVisitor(program, graph)

        cl: ValidClause
        for cl in program.getRules():
            pred: PredicateSym = cl.getHead().accept_head_visitor(getHeadPred, None)
            graph.addVertex(pred)
            c: Premise
            for c in cl.getBody():
                c.accept_premise_visitor(addEdge, pred)

# 		List<Set<PredicateSym>> strata = graph.getStronglyConnectedComponents(e -> e.reverse());
        strata: List[Set[PredicateSym]] = graph.getStronglyConnectedComponents(lambda e: e.reverse())
# 		Map<PredicateSym, Integer> predToStratumMap = new HashMap<>();
        predToStratumMap: Dict[PredicateSym, int] = dict()
# 		Iterator<Set<PredicateSym>> iter = strata.iterator();
# 		for (int i = 0; iter.hasNext(); ++i) {
# 			for (PredicateSym pred : iter.next()) {
# 				predToStratumMap.put(pred, i);
# 			}
# 		}
        for i, preds in enumerate(strata):
            pred: PredicateSym
            for pred in preds:
                predToStratumMap[pred] = i
            pass
#
# 		iter = strata.iterator();
# 		for (int i = 0; iter.hasNext(); ++i) {
# 			for (PredicateSym pred : iter.next()) {
# 				for (AnnotatedEdge edge : graph.getOutgoingEdges(pred)) {
# 					if (edge.isNegated() && predToStratumMap.get(edge.getDest()) == i) {
# 						throw new DatalogValidationException("Program cannot be stratified.");
# 					}
# 				}
# 			}
# 		}
#
        for i, preds in enumerate(strata):
            pred: PredicateSym
            for pred in preds:
                edge: AnnotatedEdge
                for edge in graph.getOutgoingEdges(pred):
                    if edge.isNegated() and predToStratumMap.get(edge.getDest()) == i:
                        raise DatalogValidationException("Program cannot be stratified")
# 		return new StratifiedNegationGraph(strata, predToStratumMap);
        return StratifiedNegationGraph(strata, predToStratumMap)
# 	}
#

# 	private final List<Set<PredicateSym>> strata;
# 	private final Map<PredicateSym, Integer> predToStratumMap;
#
# 	private StratifiedNegationGraph(List<Set<PredicateSym>> strata, Map<PredicateSym, Integer> predToStratumMap) {
# 		this.strata = strata;
# 		this.predToStratumMap = predToStratumMap;
# 	}
#
    def __init__(self, strata: List[Set[PredicateSym]], predToStratumMap: Dict[PredicateSym, int]):
        self.strata = strata
        self.predToStratumMap = predToStratumMap

# 	public List<Set<PredicateSym>> getStrata() {
# 		return strata;
# 	}
#
    def getStrata(self) -> List[Set[PredicateSym]]:
        return self.strata
# 	public Map<PredicateSym, Integer> getPredToStratumMap() {
# 		return predToStratumMap;
# 	}
    def getPredToStratumMap(self) -> Dict[PredicateSym, int]:
        return self.predToStratumMap
aaa
#
# 	public static void main(String[] args) throws DatalogParseException {
# 		Consumer<String> test = program -> {
# 			DatalogTokenizer t = new DatalogTokenizer(new StringReader(program));
# 			Set<Clause> ast = null;
# 			try {
# 				ast = DatalogParser.parseProgram(t);
# 			} catch (DatalogParseException e1) {
# 				// TODO Auto-generated catch block
# 				e1.printStackTrace();
# 			}
#
# 			System.out.println("Program: ");
# 			for (Clause cl : ast) {
# 				System.out.println("\t" + cl);
# 			}
# 			try {
# 				UnstratifiedProgram v = (new DatalogValidator()).withAtomNegationInRuleBody().validate(ast);
#
# 				StratifiedNegationGraph g = StratifiedNegationGraph.create(v);
# 				System.out.print("Stratification:\n\t" + g);
# 			} catch (DatalogValidationException e) {
# 				System.out.println("No stratification possible.");
# 			}
#
# 			System.out.println();
# 		};
#
# 		String program = "reachable(X,Y) :- edge(X,Y)." + "reachable(X,Y) :- edge(X,Z), reachable(Z,Y)."
# 				+ "not_reachable(X,Y) :- node(X), node(Y), not reachable(X,Y)."
# 				+ "node(X) :- edge(X,_). node(X) :- edge(_,X).";
# 		test.accept(program);
# 		test.accept("p :- q, not r. q :- r. r :- q.");
# 		test.accept("p :- not q. q :- not p.");
# 		test.accept("tc :- edge.");
# 		test.accept("p :- not q.");
# 	}
#
# 	@Override
# 	public String toString() {
# 		StringBuilder sb = new StringBuilder();
# 		for (int i = 0; i < this.strata.size(); ++i) {
# 			sb.append("[ " + i + ": ");
# 			for (PredicateSym pred : this.strata.get(i)) {
# 				sb.append(pred + " ");
# 			}
# 			sb.append("] ");
# 		}
# 		return sb.toString();
# 	}
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
# package abcdatalog.ast.validation;
#
# import java.io.StringReader;
# import java.util.HashMap;
# import java.util.Iterator;
# import java.util.List;
# import java.util.Map;
# import java.util.Set;
# import java.util.function.Consumer;
#
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Premise;
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
# import abcdatalog.ast.visitors.DefaultConjunctVisitor;
# import abcdatalog.ast.visitors.HeadVisitor;
# import abcdatalog.ast.visitors.HeadVisitorBuilder;
# import abcdatalog.ast.visitors.PremiseVisitor;
# import abcdatalog.parser.DatalogParseException;
# import abcdatalog.parser.DatalogParser;
# import abcdatalog.parser.DatalogTokenizer;
# import abcdatalog.util.graph.Digraph;
# import abcdatalog.util.graph.DirectedEdge;
#
# class StratifiedNegationGraph {
# 	private static class AnnotatedEdge implements DirectedEdge<PredicateSym> {
# 		private final PredicateSym source;
# 		private final PredicateSym dest;
# 		private final boolean isNegated;
#
# 		public AnnotatedEdge(PredicateSym source, PredicateSym dest, boolean isNegated) {
# 			this.source = source;
# 			this.dest = dest;
# 			this.isNegated = isNegated;
# 		}
#
# 		@Override
# 		public PredicateSym getSource() {
# 			return this.source;
# 		}
#
# 		@Override
# 		public PredicateSym getDest() {
# 			return this.dest;
# 		}
#
# 		public boolean isNegated() {
# 			return this.isNegated;
# 		}
#
# 		public AnnotatedEdge reverse() {
# 			return new AnnotatedEdge(this.dest, this.source, this.isNegated);
# 		}
# 	}
#
# 	public static StratifiedNegationGraph create(UnstratifiedProgram program) throws DatalogValidationException {
# 		// Build dependency graph...
# 		Digraph<PredicateSym, AnnotatedEdge> graph = new Digraph<>();
# 		HeadVisitor<Void, PredicateSym> getHeadPred = (new HeadVisitorBuilder<Void, PredicateSym>())
# 				.onPositiveAtom((atom, nothing) -> atom.getPred()).orCrash();
# 		PremiseVisitor<PredicateSym, Void> addEdge = new DefaultConjunctVisitor<PredicateSym, Void>() {
# 			@Override
# 			public Void visit(PositiveAtom atom, PredicateSym headPred) {
# 				if (!program.getEdbPredicateSyms().contains(atom.getPred())) {
# 					graph.addEdge(new AnnotatedEdge(atom.getPred(), headPred, false));
# 				}
# 				return null;
# 			}
#
# 			@Override
# 			public Void visit(NegatedAtom atom, PredicateSym headPred) {
# 				if (!program.getEdbPredicateSyms().contains(atom.getPred())) {
# 					graph.addEdge(new AnnotatedEdge(atom.getPred(), headPred, true));
# 				}
# 				return null;
# 			}
# 		};
# 		for (ValidClause cl : program.getRules()) {
# 			PredicateSym pred = cl.getHead().accept(getHeadPred, null);
# 			graph.addVertex(pred);
# 			for (Premise c : cl.getBody()) {
# 				c.accept(addEdge, pred);
# 			}
# 		}
#
# 		List<Set<PredicateSym>> strata = graph.getStronglyConnectedComponents(e -> e.reverse());
# 		Map<PredicateSym, Integer> predToStratumMap = new HashMap<>();
# 		Iterator<Set<PredicateSym>> iter = strata.iterator();
# 		for (int i = 0; iter.hasNext(); ++i) {
# 			for (PredicateSym pred : iter.next()) {
# 				predToStratumMap.put(pred, i);
# 			}
# 		}
#
# 		iter = strata.iterator();
# 		for (int i = 0; iter.hasNext(); ++i) {
# 			for (PredicateSym pred : iter.next()) {
# 				for (AnnotatedEdge edge : graph.getOutgoingEdges(pred)) {
# 					if (edge.isNegated() && predToStratumMap.get(edge.getDest()) == i) {
# 						throw new DatalogValidationException("Program cannot be stratified.");
# 					}
# 				}
# 			}
# 		}
#
# 		return new StratifiedNegationGraph(strata, predToStratumMap);
# 	}
#
# 	private final List<Set<PredicateSym>> strata;
# 	private final Map<PredicateSym, Integer> predToStratumMap;
#
# 	private StratifiedNegationGraph(List<Set<PredicateSym>> strata, Map<PredicateSym, Integer> predToStratumMap) {
# 		this.strata = strata;
# 		this.predToStratumMap = predToStratumMap;
# 	}
#
# 	public List<Set<PredicateSym>> getStrata() {
# 		return strata;
# 	}
#
# 	public Map<PredicateSym, Integer> getPredToStratumMap() {
# 		return predToStratumMap;
# 	}
#
# 	public static void main(String[] args) throws DatalogParseException {
# 		Consumer<String> test = program -> {
# 			DatalogTokenizer t = new DatalogTokenizer(new StringReader(program));
# 			Set<Clause> ast = null;
# 			try {
# 				ast = DatalogParser.parseProgram(t);
# 			} catch (DatalogParseException e1) {
# 				// TODO Auto-generated catch block
# 				e1.printStackTrace();
# 			}
#
# 			System.out.println("Program: ");
# 			for (Clause cl : ast) {
# 				System.out.println("\t" + cl);
# 			}
# 			try {
# 				UnstratifiedProgram v = (new DatalogValidator()).withAtomNegationInRuleBody().validate(ast);
#
# 				StratifiedNegationGraph g = StratifiedNegationGraph.create(v);
# 				System.out.print("Stratification:\n\t" + g);
# 			} catch (DatalogValidationException e) {
# 				System.out.println("No stratification possible.");
# 			}
#
# 			System.out.println();
# 		};
#
# 		String program = "reachable(X,Y) :- edge(X,Y)." + "reachable(X,Y) :- edge(X,Z), reachable(Z,Y)."
# 				+ "not_reachable(X,Y) :- node(X), node(Y), not reachable(X,Y)."
# 				+ "node(X) :- edge(X,_). node(X) :- edge(_,X).";
# 		test.accept(program);
# 		test.accept("p :- q, not r. q :- r. r :- q.");
# 		test.accept("p :- not q. q :- not p.");
# 		test.accept("tc :- edge.");
# 		test.accept("p :- not q.");
# 	}
#
# 	@Override
# 	public String toString() {
# 		StringBuilder sb = new StringBuilder();
# 		for (int i = 0; i < this.strata.size(); ++i) {
# 			sb.append("[ " + i + ": ");
# 			for (PredicateSym pred : this.strata.get(i)) {
# 				sb.append(pred + " ");
# 			}
# 			sb.append("] ");
# 		}
# 		return sb.toString();
# 	}
# }
