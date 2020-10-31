NOTE: EXPERIMENTAL. PROTOTYPE FOR DESIGN PURPOSES. Do not use !!

# Vision

Mercylog will be a Datalog based library which investigates the benefits of Datalog to build:
- Applications: 
  - Datalog's expressiveness can allow us to reduce the code required to build applications([Overlog](https://dl.acm.org/citation.cfm?id=1755913.1755937), [Yedalog](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43462.pdf)) 
  - Query data sources with higher expressivity of Datalog([Datomic](https://docs.datomic.com/on-prem/tutorial.html), [DataScript](https://github.com/tonsky/datascript)).
  - We can build specifications which could easily be translatable to code. ([Object-role modeling](http://www.cse.msu.edu/~stire/HomePage/Papers/orm2010.pdf))
  - We can build declarative UIs (source: Greg Rosenblatt, [dbKanren](https://github.com/gregr/dbKanren))
  - Using Python, we can have one language to code end to end(Brython/Pyodide for browsers/phones, Python Extensions for Postgresql)
  - Because Datalog is declarative(capturing the 'What'), when a new technology/library comes along, we can quickly build backends for Mercylog to move from one technology to another, hence maintaining our algorithmic knowledge, business logic and not having to code them again for the new technology(e.g. moving from tensorflow to pytorch, or like Bashlog which is Datalog to bash scripts)
  

- Distributed Systems: By including time in our relations, we make it easier to solve many tough problems in distributed systems(Dedalus, 3DF in Clojure)

- Analytics: 
  - By including time in our relations, we can do high performance incremental analytics(Timely Dataflow or Naiad, Boom Analytics)
  - By including values for relations, we can do probablisitic programming(JudgeD)

- Machine Learning:
  - We can capture machine learning concepts(MLog)
  - By including values for relations, we can explore AI(Yedalog, Dyna)

# Prerequisites:
* Needs Java 8 already installed(for BashLog)
* `pip install mercylog`

# Tutorial
Check out the [tutorial/introduction](https://github.com/RAbraham/mercylog_tutorial) to Mercylog

# Short Introduction
```python
import mercylog

m = mercylog.BashlogV1()
_ = m._

father = m.relation('father')
mother = m.relation('mother')
facts = [
    father('Aks', 'Bob'),
    father('Bob', 'Cad'),
    father('Yan', 'Zer'),
    mother('Mary', 'Marla'),
    mother('Marla', 'Kay'),
    mother('Jane', 'Zanu'),
]

X = m.variables('X')

paternal_grandfather = m.relation('paternal_grandfather')
maternal_grandmother = m.relation('maternal_grandmother')


def transitive(head, clause):
    X, Y, Z = m.variables('X', 'Y', 'Z')
    return head(X, Z) <= [clause(X, Y), clause(Y, Z)]


rules = [
    transitive(paternal_grandfather, father),
    transitive(maternal_grandmother, mother)
]

print(m.run(facts, rules, [paternal_grandfather(X, _)]))  # ['Aks']

print(m.run(facts, rules, [maternal_grandmother(X, _)]))  # ['Mary']

```
