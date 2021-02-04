# /**
#  * A utility class for accessing the head of a clause.
#  *
#  */
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom


class HeadHelpers:
    @staticmethod
    def force_positive_atom(head: Head) -> PositiveAtom:
        if isinstance(head, PositiveAtom):
            return head
        else:
            raise ValueError(f"Convert head to a Positive atom:{str(head)}")
