# /**
#  * A utility class for accessing the head of a clause.
#  *
#  */
# public final class HeadHelpers {
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
class HeadHelpers:
#
# 	private HeadHelpers() {
# 		// Cannot be instantiated.
# 	}
#

# 	public static PositiveAtom forcePositiveAtom(Head head) {
# 		return (PositiveAtom) head;
# 	}
# }
    @staticmethod
    def forcePositiveAtom(head: Head) -> PositiveAtom:
        if isinstance(head, PositiveAtom):
            return head
        else:
            raise ValueError(f'Convert head to a Positive atom:{str(head)}')
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
# /**
#  * A utility class for accessing the head of a clause.
#  *
#  */
# public final class HeadHelpers {
#
# 	private HeadHelpers() {
# 		// Cannot be instantiated.
# 	}
#
# 	public static PositiveAtom forcePositiveAtom(Head head) {
# 		return (PositiveAtom) head;
# 	}
# }
