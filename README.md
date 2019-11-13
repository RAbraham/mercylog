NOTE: EXPERIMENTAL. Do not use in production !!

# Vision

MerycyLog is a Datalog inspired library which allows developers to build
- Applications: Datalog's expressiveness can allow us to reduce the code required to build applications and maintain state(Datomic, Datahike, DataScript, Yedalog, Overlog/Dedalus/Boom). Using Python, we can have one language to code end to end(Transcrypt/Pyodide for browsers, Python Extensions for Postgresql)
- distributed systems: By including time in our relations, we make it easier to solve many tough problems in distributed systems(Dedalus, 3df-clojure)
- analytics: 
  - By including time in our relations, we can do high performance incremental analytics(Timely Dataflow or Naiad, Boom Analytics)
  - By including values for relations, we can do probablisitic programming(judgeD, Yedalog, Dyna)

- Machine Learning:
  - We can capture machine learning concepts(MLog) 
- Engineering: 
    - Because Datalog is declarative(capturing the 'What'), when a new technology/library comes along, we can quickly build backends for Mercylog to move from one technology to another, hence maintaining our algorithmic knowledge, business logic and not having to code them again for the new technology(e.g. moving from tensorflow to pytorch)
    - Functional?

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