import abcdatalog.ast.visitors.HeadVisitor;

/**
 * The head of a clause. This interface is under-specified to allow the addition
 * of new language features.
 *
 */
public interface Head {
	public <I, O> O accept(HeadVisitor<I, O> visitor, I state);
}
