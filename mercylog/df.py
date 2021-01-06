from mercylog.types import RowRelation

def row(*args, **kwargs):
    # TODO: Assert kwargs are vars or constants. not relations for e.g.
    return RowRelation(kwargs)
