import unittest
import pytest
from mercylog.types import relation, Variable, _

from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import convert

def test_reachable():
    # 		String program = "reachable(X,Y) :- edge(X,Y).
    # 	            	" + "reachable(X,Y) :- edge(X,Z), reachable(Z,Y)."
    # 				        + "not_reachable(X,Y) :- node(X), node(Y), not reachable(X,Y)."
    # 				+ "node(X) :- edge(X,_). node(X) :- edge(_,X).";

    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    reachable = relation("reachable")
    edge = relation("edge")
    not_reachable = relation("not_reachable")
    node = relation("node")

    program = [
        reachable(X, Y) <= edge(X, Y),
        reachable(X, Y) <= [edge(X, Z), reachable(Z, Y)],
        not_reachable(X, Y) <= [node(X), node(Y), ~reachable(X, Y)],
        node(X) <= edge(X, _),
        node(X) <= edge(_, X)
    ]
    abc_program = convert(program)
    # 				UnstratifiedProgram v = (new DatalogValidator()).withAtomNegationInRuleBody().validate(ast);
    from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
    from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
    from mercylog.abcdatalog.ast.validation.stratified_negation_graph import StratifiedNegationGraph
    v: UnstratifiedProgram = DatalogValidator().withAtomNegationInRuleBody().validate(abc_program)
    #
    # 				StratifiedNegationGraph g = StratifiedNegationGraph.create(v);
    g: StratifiedNegationGraph = StratifiedNegationGraph.create(v)
    print('Strata')
    print(g.strata)
    # sorted_strata = sorted(g.strata,key= lambda s: str(list(s)[0]))
    sorted_strata_str = [str(s) for s in g.strata]
    exp = ['{reachable}', '{node}', '{not_reachable}']
    assert sorted_strata_str == exp


    pass

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

if __name__ == '__main__':
    unittest.main()
