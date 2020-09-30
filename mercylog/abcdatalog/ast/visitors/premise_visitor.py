# import abcdatalog.ast.BinaryDisunifier;
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
# import abcdatalog.ast.BinaryUnifier;
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.engine.bottomup.AnnotatedAtom;

public interface PremiseVisitor<I, O> {
	public O visit(PositiveAtom atom, I state);
	
	public O visit(AnnotatedAtom atom, I state);
	
	public O visit(BinaryUnifier u, I state);
	
	public O visit(BinaryDisunifier u, I state);
	
	public O visit(NegatedAtom atom, I state);
}
