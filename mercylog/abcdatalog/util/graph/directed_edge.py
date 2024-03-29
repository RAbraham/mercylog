from abc import ABC, abstractmethod

from typing import *

V = TypeVar("V")


class DirectedEdge(ABC, Generic[V]):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def getSource(self) -> V:
        pass

    @abstractmethod
    def getDest(self) -> V:
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
# package abcdatalog.util.graph;
#
# public interface DirectedEdge<V> {
# 	public V getSource();
#
# 	public V getDest();
# }
