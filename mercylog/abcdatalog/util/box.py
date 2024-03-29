from typing import *
T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, value: T = None):
        self.value = value


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
# package abcdatalog.util;
#
# public class Box<T> {
# 	public T value;
#
# 	public Box() {};
#
# 	public Box(T value) {
# 		this.value = value;
# 	}
# }
