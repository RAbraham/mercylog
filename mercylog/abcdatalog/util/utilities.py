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
    def get_set_from_map(a_map: Dict[K, Set[V]], key: K) -> Set[V]:
        vals = a_map.get(key)
        if vals is None:
            vals = set()
            a_map[key] = vals
        return vals

    @staticmethod
    def upsert_collection_in_map(a_map: Dict[K, Set[V]], key: K, value: V) -> Dict[K, Set[V]]:
        a_set = a_map.get(key)
        result = a_set or set()
        result = result | {value}
        return {**a_map, **{key: result}}

