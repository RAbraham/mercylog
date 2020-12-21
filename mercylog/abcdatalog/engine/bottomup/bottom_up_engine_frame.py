from typing import *
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.engine.datalog_engine import DatalogEngine
from mercylog.abcdatalog.util.datastructures.indexable_fact_collection import IndexableFactCollection
from mercylog.abcdatalog.engine.bottomup.eval_manager import EvalManager
#
# /**
#  * A framework for a bottom-up Datalog engine.
#  *
#  */
class BottomUpEngineFrame(DatalogEngine):
# 	/**
# 	 * The evaluation manager for this engine.
# 	 */
# 	private final EvalManager manager;
# 	/**
# 	 * The set of facts that can be derived from the current program.
# 	 */
# 	private volatile IndexableFactCollection facts;
# 	/**
# 	 * Has the engine been initialized?
# 	 */
# 	private volatile boolean isInitialized = false;
#
# 	/**
# 	 * Constructs a bottom-up engine with the provided evaluation manager.
# 	 *
# 	 * @param manager
# 	 *            the manager
# 	 */
    def __init__(self, manager: EvalManager):
        self.manager = manager
        self.isInitialized = False
        self.facts: Optional[IndexableFactCollection] = None
        super(BottomUpEngineFrame, self).__init__()

    def init(self, program: Set[Clause]):
        if self.isInitialized:
            raise ValueError("Cannot initialize an engine more than once.")
        self.manager.initialize(program)
        self.facts = self.manager.eval()
        self.isInitialized = True

    def query(self, q: PositiveAtom) -> Set[PositiveAtom]:
        if not self.isInitialized:
            raise ValueError("Engine must be initialized before it can be queried.")

        r: Set[PositiveAtom] = set()
        a: PositiveAtom
        for a in self.facts.indexInto_patom(q):
            if q.unify(a) is not None:
                r.add(a)
        return r
