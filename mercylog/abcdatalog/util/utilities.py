from typing import *

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")

# /**
#  * "Static" class containing utility methods.
#  *
#  */
# public final class Utilities {
class Utilities:
#
# 	private Utilities() {
# 		// Cannot be instantiated.
# 	}
#
# 	public static final int concurrency = Runtime.getRuntime()
# 			.availableProcessors();
#
    @staticmethod
# 	public static <T> Set<T> createConcurrentSet() {
    def createConcurrentSet() -> Set[T]:
# 		return Collections.newSetFromMap(createConcurrentMap());
        return set()
# 	}
#
# 	public static <K, V> ConcurrentMap<K, V> createConcurrentMap() {
# 		return new ConcurrentHashMap<>(16, 0.75f, concurrency);
# 	}
#
# 	/**
# 	 * Returns the set in map associated with key, creating a new set if needed.
# 	 *
# 	 * @param map
# 	 *            the map
# 	 * @param key
# 	 *            the key
# 	 * @return the set
# 	 */
# 	public static <K, V> Set<V> getSetFromMap(Map<K, Set<V>> map, K key) {
    @staticmethod
    def getSetFromMap(map: Dict[K, Set[V]], key: K)-> Set[V]:
# 		Set<V> vals = map.get(key);
        vals = map.get(key)
# 		if (vals == null) {
        if vals is None:
# 			vals = new LinkedHashSet<>();
            vals = set()
# 			map.put(key, vals);
            map[key] = vals
# 		}
# 		return vals;
        return vals
# 	}
#
# }
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
# import java.util.Collections;
# import java.util.LinkedHashSet;
# import java.util.Map;
# import java.util.Set;
# import java.util.concurrent.ConcurrentHashMap;
# import java.util.concurrent.ConcurrentMap;
#
# /**
#  * "Static" class containing utility methods.
#  *
#  */
# public final class Utilities {
#
# 	private Utilities() {
# 		// Cannot be instantiated.
# 	}
#
# 	public static final int concurrency = Runtime.getRuntime()
# 			.availableProcessors();
#
# 	public static <T> Set<T> createConcurrentSet() {
# 		return Collections.newSetFromMap(createConcurrentMap());
# 	}
#
# 	public static <K, V> ConcurrentMap<K, V> createConcurrentMap() {
# 		return new ConcurrentHashMap<>(16, 0.75f, concurrency);
# 	}
#
# 	/**
# 	 * Returns the set in map associated with key, creating a new set if needed.
# 	 *
# 	 * @param map
# 	 *            the map
# 	 * @param key
# 	 *            the key
# 	 * @return the set
# 	 */
# 	public static <K, V> Set<V> getSetFromMap(Map<K, Set<V>> map, K key) {
# 		Set<V> vals = map.get(key);
# 		if (vals == null) {
# 			vals = new LinkedHashSet<>();
# 			map.put(key, vals);
# 		}
# 		return vals;
# 	}
#
# }
