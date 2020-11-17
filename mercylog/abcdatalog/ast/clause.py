from typing import *
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.premise import Premise
"""
 * A clause consisting of a head and a body, the latter of which is a list of
 * premises. The standard interpretation is that the head of a clause is
 * considered to hold if each premise in the body holds.
 *
"""
from dataclasses import dataclass
from typing import *
@dataclass(frozen=True)

# public class Clause {
#  	private final Head head;
#
# 	protected final List<Premise> body;
class Clause:
	head: Head
	body: Tuple[Premise]

# 	/**
# 	 * Returns the head of this clause.
# 	 *
# 	 * @return the head
# 	 */
# 	public Head getHead() {
# 		return this.head;
# 	}
	def getHead(self) -> Head:
		return self.head

#
# 	/**
# 	 * Returns the body of this clause.
# 	 *
# 	 * @return the body
# 	 */
# 	public List<Premise> getBody() {
# 		return this.body;
# 	}
#
	def getBody(self) -> Tuple[Premise]:
		return self.body

	def __str__(self):
		body_texts = [str(b) for b in self.getBody()]
		result = str(self.getHead()) + ' :- ' + ','.join(body_texts) + '.'
		return result

	def __repr__(self):
		return self.__str__()

# ----------------------------------------------------------------------------------
# public class Clause {
#  	private final Head head;
#
# 	protected final List<Premise> body;
#
#  	public Clause(Head head, List<Premise> body) {
#  		this.head = head;
#  		this.body = body;
#  	}
#
# 	/**
# 	 * Returns the head of this clause.
# 	 *
# 	 * @return the head
# 	 */
# 	public Head getHead() {
# 		return this.head;
# 	}

#
# 	/**
# 	 * Returns the body of this clause.
# 	 *
# 	 * @return the body
# 	 */
# 	public List<Premise> getBody() {
# 		return this.body;
# 	}
#
# 	@Override
# 	public int hashCode() {
# 		final int prime = 31;
# 		int result = 1;
# 		result = prime * result + ((body == null) ? 0 : body.hashCode());
# 		result = prime * result + ((head == null) ? 0 : head.hashCode());
# 		return result;
# 	}
#
# 	@Override
# 	public boolean equals(Object obj) {
# 		if (this == obj)
# 			return true;
# 		if (obj == null)
# 			return false;
# 		if (getClass() != obj.getClass())
# 			return false;
# 		Clause other = (Clause) obj;
# 		if (body == null) {
# 			if (other.body != null)
# 				return false;
# 		} else if (!body.equals(other.body))
# 			return false;
# 		if (head == null) {
# 			if (other.head != null)
# 				return false;
# 		} else if (!head.equals(other.head))
# 			return false;
# 		return true;
# 	}
#
# 	@Override
# 	public String toString() {
# 		StringBuilder sb = new StringBuilder();
# 		sb.append(this.getHead());
# 		if (!this.getBody().isEmpty()) {
# 			sb.append(" :- ");
# 			for (int i = 0; i < this.getBody().size(); ++i) {
# 				sb.append(this.getBody().get(i));
# 				if (i < this.getBody().size() - 1) {
# 					sb.append(", ");
# 				}
# 			}
# 		}
# 		sb.append('.');
# 		return sb.toString();
# 	}
#
# }
