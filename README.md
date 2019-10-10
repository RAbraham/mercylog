NOTE: EXPERIMENTAL. Do not use in production !!

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