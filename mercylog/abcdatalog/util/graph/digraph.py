from mercylog.abcdatalog.util.box import Box
from mercylog.abcdatalog.util.graph.directed_edge import DirectedEdge

from typing import *

V = TypeVar("V")
E = TypeVar("E")

def dfs_func(v, time: Box, visited: Set, outGoingEdges: Callable, vertices, finishingTimes: Dict[Any, int]):
    time.value = time.value + 1
    visited.add(v)
    for edge in outGoingEdges(v):
        dest = edge.getDest()
        if dest not in visited:
            dfs_func(dest,  time, visited, outGoingEdges, vertices, finishingTimes)
    time.value = time.value + 1
    finishingTimes[v] = time.value

def dfs2_func(v, curComponent, visited: Set, transpose: "Digraph"):
    visited.add(v)
    curComponent.add(v)
    edge: E
    for edge in transpose.getOutgoingEdges(v):
        dest: V = edge.getDest()
        if dest not in visited:
            dfs2_func(dest, curComponent, visited, transpose)

# public class Digraph<V, E extends DirectedEdge<V>> {
class Digraph(Generic[V, E]):
    def __init__(self):
        # 	private Map<V, List<E>> graph = new HashMap<>();
        self.graph: Dict[V, List[E]] = dict()
    pass
#
# 	public void addEdge(E edge) {
    def addEdge(self, edge: E) -> None:
        # 		List<E> neighbors = this.graph.get(edge.getSource());
        # 		if (neighbors == null) {
        # 			neighbors = new LinkedList<>();
        # 			this.graph.put(edge.getSource(), neighbors);
        # 		}
        # 		neighbors.add(edge);
        # 	}
        neighbors: List[E] = self.graph.get(edge.getSource())
        if not neighbors:
            neighbors = []
            self.graph[edge.getSource()] = neighbors

        neighbors.append(edge)

#
# 	public void addVertex(V vertex) {
# 		List<E> neighbors = this.graph.get(vertex);
# 		if (neighbors == null) {
# 			neighbors = new LinkedList<>();
# 			this.graph.put(vertex, neighbors);
# 		}
# 	}
    def addVertex(self, vertex: V) -> None:
        neighbors: List[E] = self.graph.get(vertex)
        if not neighbors:
            neighbors = []
            self.graph[vertex] = neighbors
#
# 	public Iterable<E> getOutgoingEdges(V source) {
# 		List<E> outgoing = this.graph.get(source);
# 		if (outgoing == null) {
# 			return Collections.emptyList();
# 		}
# 		return outgoing;
# 	}
#
    def getOutgoingEdges(self, source: V) -> Iterable[E]:
        outgoing: List[E] = self.graph.get(source)
        if not outgoing:
            return []
        else:
            return outgoing

# 	public Set<V> getVertices() {
# 		return this.graph.keySet();
# 	}
    def getVertices(self) -> Set[V]:
        return set(self.graph.keys())
#
# 	public Digraph<V, E> getTranspose(Function<E, E> reverseEdge) {
# 		Digraph<V, E> t = new Digraph<>();
# 		for (Map.Entry<V, List<E>> e : this.graph.entrySet()) {
# 			t.addVertex(e.getKey());
# 			for (E edge : e.getValue()) {
# 				t.addEdge(reverseEdge.apply(edge));
# 			}
# 		}
# 		return t;
# 	}
    def getTranspose(self, reverseEdge: Callable[[E], E] ) -> "Digraph":
        t: Digraph[V, E] = Digraph()
        for k, v in self.graph.items():
            t.addVertex(k)
            edge: E
            for edge in v:
                t.addEdge(reverseEdge(edge))
        return t

#
# 	public List<Set<V>> getStronglyConnectedComponents(Function<E, E> reverseEdge) {
# 		Box<Integer> time = new Box<>();
# 		Set<V> visited = new HashSet<>();
# 		Map<V, Integer> finishingTimes = new HashMap<>();
# 		Box<Consumer<V>> dfs = new Box<>();
# 		dfs.value = v -> {
# 			++time.value;
# 			visited.add(v);
# 			for (E edge : this.getOutgoingEdges(v)) {
# 				V dest = edge.getDest();
# 				if (!visited.contains(dest)) {
# 					dfs.value.accept(dest);
# 				}
# 			}
# 			finishingTimes.put(v, ++time.value);
# 		};
#
# 		time.value = 0;
# 		for (V vertex : this.getVertices()) {
# 			if (!visited.contains(vertex)) {
# 				dfs.value.accept(vertex);
# 			}
# 		}

#
# 		Digraph<V, E> transpose = this.getTranspose(reverseEdge);
# 		Box<BiConsumer<V, Set<V>>> dfs2 = new Box<>();
# 		dfs2.value = (v, curComponent) -> {
# 			visited.add(v);
# 			curComponent.add(v);
# 			for (E edge : transpose.getOutgoingEdges(v)) {
# 				V dest = edge.getDest();
# 				if (!visited.contains(dest)) {
# 					dfs2.value.accept(dest, curComponent);
# 				}
# 			}
# 		};
#
# 		List<V> orderedVertices = new ArrayList<>();
# 		finishingTimes.entrySet().stream()
# 				.sorted(Map.Entry.comparingByValue(Collections.reverseOrder()))
# 				.forEachOrdered(e -> orderedVertices.add(e.getKey()));
# 		List<Set<V>> components = new ArrayList<>();
# 		visited.clear();
# 		for (V vertex : orderedVertices) {
# 			if (!visited.contains(vertex)) {
# 				Set<V> curComponent = new HashSet<>();
# 				dfs2.value.accept(vertex, curComponent);
# 				components.add(curComponent);
# 			}
# 		}
#
# 		return components;
# 	}
#
    def getStronglyConnectedComponents(self, reverseEdge: Callable[[E], E]) -> List[Set[V]]:
        time: Box[int] = Box()
        visited: Set[V] = set()
        finishingTimes = dict()
        dfs: Box[Callable[[Any]]] = Box()
        dfs.value = dfs_func
        time.value = 0
        vertices = self.getVertices()
        for vertex in vertices:
            if vertex not in visited:
                dfs_func(vertex, time, visited, self.getOutgoingEdges, vertices, finishingTimes)

        transpose: Digraph[V, E] = self.getTranspose(reverseEdge)
        dfs2: Box[Callable[[V, Set[V]]]] = Box()
        dfs2.value = dfs2_func

        orderedVertices: List[V] = []
        items = finishingTimes.items()
        sorted_items = sorted(items, key=lambda i: i[1], reverse=True)
        for e in sorted_items:
            orderedVertices.append(e[0])

        components: List[Set[V]] = []
        visited.clear()
        vertex: V
        for vertex in orderedVertices:
            if vertex not in visited:
                curComponent: Set[V] = set()
                dfs2_func(vertex, curComponent, visited, transpose)
                components.append(curComponent)
            pass


        return components

if __name__ == '__main__':
    class CharEdge(DirectedEdge[str]):
        def __init__(self, source: str, dest: str):
            self.source = source
            self.dest = dest
            super(CharEdge, self).__init__()

        def getSource(self):
            return self.source

        def getDest(self):
            return self.dest

        def reverse(self) -> "CharEdge":
            return CharEdge(self.dest, self.source)
        pass
# 		Digraph<Character, CharEdge> graph = new Digraph<>();
    graph: Digraph[str, CharEdge] = Digraph()

    graph.addEdge(CharEdge('a', 'b'))
    graph.addEdge(CharEdge('b', 'c'))
    graph.addEdge(CharEdge('b', 'e'))
    graph.addEdge(CharEdge('b', 'f'))
    graph.addEdge(CharEdge('c', 'd'))
    graph.addEdge(CharEdge('c', 'g'))
    graph.addEdge(CharEdge('d', 'c'))
    graph.addEdge(CharEdge('d', 'h'))
    graph.addEdge(CharEdge('e', 'a'))
    graph.addEdge(CharEdge('e', 'f'))
    graph.addEdge(CharEdge('f', 'g'))
    graph.addEdge(CharEdge('g', 'f'))
    graph.addEdge(CharEdge('g', 'h'))
    graph.addEdge(CharEdge('h', 'h'))

# 		// Components (in topological order) should be:
# 		// [a, b, e]
# 		// [c, d]
# 		// [f, g]
# 		// [h]
# 		List<Set<Character>> components = graph.getStronglyConnectedComponents(e -> e.reverse());
    components: List[Set[str]] = graph.getStronglyConnectedComponents(lambda e: e.reverse())
# 		for (Set<Character> component : components) {
# 			System.out.println(component);
# 		}
    component: Set[str]
    for component in components:
        print(component)
# 	}
# }

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
# import java.util.ArrayList;
# import java.util.Collections;
# import java.util.HashMap;
# import java.util.HashSet;
# import java.util.LinkedList;
# import java.util.List;
# import java.util.Map;
# import java.util.Set;
# import java.util.function.BiConsumer;
# import java.util.function.Consumer;
# import java.util.function.Function;
#
# import abcdatalog.util.Box;
#
# public class Digraph<V, E extends DirectedEdge<V>> {
# 	private Map<V, List<E>> graph = new HashMap<>();
#
# 	public void addEdge(E edge) {
# 		List<E> neighbors = this.graph.get(edge.getSource());
# 		if (neighbors == null) {
# 			neighbors = new LinkedList<>();
# 			this.graph.put(edge.getSource(), neighbors);
# 		}
# 		neighbors.add(edge);
# 	}
#
# 	public void addVertex(V vertex) {
# 		List<E> neighbors = this.graph.get(vertex);
# 		if (neighbors == null) {
# 			neighbors = new LinkedList<>();
# 			this.graph.put(vertex, neighbors);
# 		}
# 	}
#
# 	public Iterable<E> getOutgoingEdges(V source) {
# 		List<E> outgoing = this.graph.get(source);
# 		if (outgoing == null) {
# 			return Collections.emptyList();
# 		}
# 		return outgoing;
# 	}
#
# 	public Set<V> getVertices() {
# 		return this.graph.keySet();
# 	}
#
# 	public Digraph<V, E> getTranspose(Function<E, E> reverseEdge) {
# 		Digraph<V, E> t = new Digraph<>();
# 		for (Map.Entry<V, List<E>> e : this.graph.entrySet()) {
# 			t.addVertex(e.getKey());
# 			for (E edge : e.getValue()) {
# 				t.addEdge(reverseEdge.apply(edge));
# 			}
# 		}
# 		return t;
# 	}
#
# 	public List<Set<V>> getStronglyConnectedComponents(Function<E, E> reverseEdge) {
# 		Box<Integer> time = new Box<>();
# 		Set<V> visited = new HashSet<>();
# 		Map<V, Integer> finishingTimes = new HashMap<>();
# 		Box<Consumer<V>> dfs = new Box<>();
# 		dfs.value = v -> {
# 			++time.value;
# 			visited.add(v);
# 			for (E edge : this.getOutgoingEdges(v)) {
# 				V dest = edge.getDest();
# 				if (!visited.contains(dest)) {
# 					dfs.value.accept(dest);
# 				}
# 			}
# 			finishingTimes.put(v, ++time.value);
# 		};
#
# 		time.value = 0;
# 		for (V vertex : this.getVertices()) {
# 			if (!visited.contains(vertex)) {
# 				dfs.value.accept(vertex);
# 			}
# 		}
#
# 		Digraph<V, E> transpose = this.getTranspose(reverseEdge);
# 		Box<BiConsumer<V, Set<V>>> dfs2 = new Box<>();
# 		dfs2.value = (v, curComponent) -> {
# 			visited.add(v);
# 			curComponent.add(v);
# 			for (E edge : transpose.getOutgoingEdges(v)) {
# 				V dest = edge.getDest();
# 				if (!visited.contains(dest)) {
# 					dfs2.value.accept(dest, curComponent);
# 				}
# 			}
# 		};
#
# 		List<V> orderedVertices = new ArrayList<>();
# 		finishingTimes.entrySet().stream()
# 				.sorted(Map.Entry.comparingByValue(Collections.reverseOrder()))
# 				.forEachOrdered(e -> orderedVertices.add(e.getKey()));
# 		List<Set<V>> components = new ArrayList<>();
# 		visited.clear();
# 		for (V vertex : orderedVertices) {
# 			if (!visited.contains(vertex)) {
# 				Set<V> curComponent = new HashSet<>();
# 				dfs2.value.accept(vertex, curComponent);
# 				components.add(curComponent);
# 			}
# 		}
#
# 		return components;
# 	}
#
# 	public static void main(String[] args) {
# 		class CharEdge implements DirectedEdge<Character> {
# 			private final char source;
# 			private final char dest;
#
# 			public CharEdge(char source, char dest) {
# 				this.source = source;
# 				this.dest = dest;
# 			}
#
# 			@Override
# 			public Character getSource() {
# 				return this.source;
# 			}
#
# 			@Override
# 			public Character getDest() {
# 				return this.dest;
# 			}
#
# 			public CharEdge reverse() {
# 				return new CharEdge(this.dest, this.source);
# 			}
#
# 		}
#
# 		Digraph<Character, CharEdge> graph = new Digraph<>();
# 		graph.addEdge(new CharEdge('a', 'b'));
# 		graph.addEdge(new CharEdge('b', 'c'));
# 		graph.addEdge(new CharEdge('b', 'e'));
# 		graph.addEdge(new CharEdge('b', 'f'));
# 		graph.addEdge(new CharEdge('c', 'd'));
# 		graph.addEdge(new CharEdge('c', 'g'));
# 		graph.addEdge(new CharEdge('d', 'c'));
# 		graph.addEdge(new CharEdge('d', 'h'));
# 		graph.addEdge(new CharEdge('e', 'a'));
# 		graph.addEdge(new CharEdge('e', 'f'));
# 		graph.addEdge(new CharEdge('f', 'g'));
# 		graph.addEdge(new CharEdge('g', 'f'));
# 		graph.addEdge(new CharEdge('g', 'h'));
# 		graph.addEdge(new CharEdge('h', 'h'));
#
# 		// Components (in topological order) should be:
# 		// [a, b, e]
# 		// [c, d]
# 		// [f, g]
# 		// [h]
# 		List<Set<Character>> components = graph.getStronglyConnectedComponents(e -> e.reverse());
# 		for (Set<Character> component : components) {
# 			System.out.println(component);
# 		}
# 	}
# }
