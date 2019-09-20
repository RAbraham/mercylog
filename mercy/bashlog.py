# -*- coding: utf-8 -*-

"""Main module."""
from mercy.lib import util
from pathlib import Path
import subprocess
from typing import *


#    facts(_, S, P, O) :~ cat *.tsv
#         born(X) :- facts(_, X, "<wasBornIn>", Y).
#         born(X) :- facts(_, X, "<wasBornOnDate>", Y).
#         dead(X) :- facts(_, X, "<diedIn>", Y).
#         dead(X) :- facts(_, X, "<diedOnDate>", Y).
#
#         main(X) :- born(X), not dead(X).

# c = Command('cat *.tsv')
# f = Facts('_', 'S', 'P', 'Q')
# data_source = Read(f, c)
# born = Predicate()
# dead = Predicate()
# born('X') <= Facts('_', 'X', "<wasBornIn>", 'Y')
# born('X') <= Facts('_', 'X', "<wasBornOnDate>", 'Y')
# dead('X') <= Facts('_', 'X', "<diedIn>", 'Y')
# dead('X') <= Facts('_', 'X', "<diedOnDate>", 'Y')


class RowFact(object):
    def __init__(self, *variables):
        self._variables = variables

    # def __str__(self):
    #     # facts(_, X, "<wasBornIn>", Y).
    #     strs = []
    #     for v in self.variables:
    #         if isinstance(v, str):
    #             strs.append(f'"{v}"')
    #         else:
    #             strs.append(str(v))
    #
    #     return 'facts(' + ', '.join(strs) + ')'

    def variables(self):
        return self._variables

    def get_clause(self):
        # facts(_, X, "<wasBornIn>", Y).
        strs = []
        for v in self.variables():
            if isinstance(v, str):
                strs.append(f'"{v}"')
            else:
                strs.append(str(v))

        return 'facts(' + ', '.join(strs) + ')'

    def relation(self):
        return self.get_clause()


class Command(object):
    def __init__(self, unix_command: str):
        self.unix_command = unix_command
        pass

    def __str__(self):
        return self.unix_command


class AbstractData(object):
    def persist(self):
        pass

    def clean_up(self):
        pass

    pass


class Data(AbstractData):
    def __init__(self, facts: RowFact, command: Command):
        self.facts = facts
        self.command = command

    # def __str__(self):
    #     # facts(_, S, P, O):~ cat *.tsv
    #     return str(self.facts) + " :~ " + str(self.command)

    def get_clause(self):
        return [self.facts.get_clause() + " :~ " + str(self.command)]

    def get_full_clause(self):
        return '\n'.join(self.get_clause())

    def persist(self):
        pass


class DataList(AbstractData):
    def __init__(self, facts: List):
        self.facts = facts

    # def __str__(self):
    #     fact_str = [str(f) for f in self.facts]
    #     return str('\n'.join(fact_str))

    def get_clause(self):
        fact_str = [f.get_clause() for f in self.facts]
        return fact_str

    def get_full_clause(self):
        return '\n.'.join(self.get_clause()) + '.'

    def persist(self, file_path: Path = None):
        self.folder = util.tmp_folder()
        file_path = self.folder / 'input.tsv'

        import csv

        data = [str(f) for f in self.facts]

        with open(str(file_path), 'w', newline='') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(data)

        return file_path

    def clean_up(self):
        util.remove_dir(self.folder)
        pass


class Variable(object):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class RelationInstance(object):
    def __init__(self, name, *variables):
        self.name = name
        self._variables = variables

    def __le__(self, body: Union[List, Any]):
        if isinstance(body, List):
            b = Facts(*body)
        else:
            b = body
        return Rule(self, b)

    def variables(self):
        return self._variables

    # def __str__(self):
    #     # var_strs = [str(v) for v in self.variables]
    #     return self.relation_x() + '.'

    def get_clause(self):
        # var_strs = [str(v) for v in self.variables]
        return self.relation_x()

    def relation_x(self):
        var_strs = []
        # TODO: Duplicate isinstance check
        for v in self.variables():
            if isinstance(v, str):
                x = f'"{v}"'
            else:
                x = str(v)

            var_strs.append(x)
        a_str = ','.join(var_strs)
        return self.name + '(' + a_str + ')'

    def relation(self):
        return self.relation_x()

    def __invert__(self):
        return InvertedRelationInstance(self)
        pass


class Relation(object):
    def __init__(self, name: str):
        self.name = name

    def name(self):
        return self.name

    def __call__(self, *variables, **kwargs):
        return RelationInstance(self.name, *variables)


#  dead(X) <= m.Row(_, X, "<diedOnDate>", Y),
# iff(m.Row(_, X, "<diedOnDate>", Y)).then(dead(X))

# class IffClause(object):
#     def __init__(self, clauses):
#         # self.clauses = clauses
#         if isinstance(clauses, Tuple):
#             b = Facts(*clauses)
#         else:
#             b = clauses
#         self.facts = b
#
#     def then(self, clause: RelationInstance):
#
#         return Rule(clause, self.facts)
#
#
# def iff(*clauses):
#     return IffClause(clauses)
#

class InvertedRelationInstance(object):
    def __init__(self, relation_instance):
        self.relation_instance = relation_instance
        pass

    # def __str__(self):
    #     return "not " + self.relation_instance.get_clause()
    def get_clause(self):
        return "not " + self.relation_instance.get_clause()

    def relation(self):
        return self.get_clause()

    def variables(self):
        return self.relation_instance.variables()


class Main(object):
    def __init__(self, *variables):
        self.relation_instance = RelationInstance('main', *variables)

    # def __str__(self):
    #     return str(self.relation_instance)

    def get_clause(self):
        return self.relation_instance.get_clause()

    def __le__(self, body: Union[List, Any]):

        # TODO: Duplicate with RelationInstance
        if isinstance(body, List):
            b = Facts(*body)
        else:
            b = body
        return Rule(self, b)

    def relation(self):
        return self.get_clause()


class Facts(object):
    def __init__(self, *fact_list):
        self.fact_list = fact_list

    # def __str__(self):
    #     fact_list_str = [str(f.relation()) for f in self.fact_list]
    #     return ', '.join(fact_list_str)

    def get_clause(self):
        fact_list_str = [f.relation() for f in self.fact_list]
        return ', '.join(fact_list_str)

    pass


class Fact(object):
    def __init__(self, terms):
        self.terms = terms


class Rule(object):
    def __init__(self, head_atom, body_atoms):
        self.head_atom = head_atom
        self.body_atoms = body_atoms
        pass

    # def __str__(self):
    #     if self.body_atoms:
    #         return str(self.head_atom) + ' :- ' + str(self.body_atoms) + '.'
    #     else:
    #         return str(self.head_atom) + '.'
    #     pass
    def relation(self):
        if self.body_atoms:
            mid_fragment = ' :- ' + str(self.body_atoms)
        else:
            mid_fragment = ''

        result = self.head_atom.relation() + mid_fragment
        return result

    def get_clause(self):
        if self.body_atoms:
            mid_fragment = ' :- ' + self.body_atoms.get_clause()
        else:
            mid_fragment = ''
        # print(self.head_atom.relation())
        # print(mid_fragment)
        # return self.head_atom.relation().get_clause() + mid_fragment
        return self.head_atom.relation() + mid_fragment


class Program(object):
    def __init__(self, instructions):
        self.instructions = instructions
        pass

    def __str__(self):
        str_instructions = [i.get_clause() for i in self.instructions]
        return '.\n'.join(str_instructions) + '.'


# def variables(*vars):
#     return [Variable(v) for v in vars]


def query_bash_datalog(program: str, debug: bool = False) -> str:
    bash_text = compile_to_bash(program)
    if debug:
        print('Bash Code')
        print(bash_text)

    return run_bash(bash_text)
    pass


def query(p: Program, r: AbstractData, debug: bool = False):
    try:
        r.persist()
        r_str = r.get_full_clause()
        p_str = str(p)
        program_str = '\n'.join([r_str, p_str])
        if debug:
            print('Datalog')
            print(program_str)
        result = query_bash_datalog(program_str, debug).split('\n')
        return list(filter(None, result))

    finally:
        r.clean_up()


def compile_to_bash(program) -> str:
    tmp_folder = util.tmp_folder()
    try:

        # subprocess.run(["ls", "-l"])
        tmp_datalog_file = tmp_folder / 'program.datalog'
        save_as_file(program, tmp_datalog_file)
        tmp_bash_file = tmp_folder / 'query.sh'
        # command = ["java", "-jar", "bashlog-datalog.jar", "--query-file", str(tmp_datalog_file), "-query-predicate",
        #          "<predicate>",
        #          ">", str(tmp_bash_file)]
        from mercy.config import config
        bashlog_path = str(config.project_root() / "bashlog-datalog.jar")
        command = [
            f"java -jar {bashlog_path} --query-file {str(tmp_datalog_file)} --query-pred main > {str(tmp_bash_file)}"]
        # url = 'https://www.thomasrebele.org/projects/bashlog/api/datalog'
        # file_path = f'@"{str(tmp_datalog_file)}"'
        # command = [f'curl -s --data_source-binary  {file_path} {url} > {str(tmp_bash_file)}']
        # subprocess.run(command, shell=True)
        # TODO: running in shell is dangerous
        subprocess.call(command, shell=True)
        result = tmp_bash_file.read_text()

        return result

    finally:
        util.remove_dir(tmp_folder)
        pass


def save_as_file(program: str, output_file: Path):
    output_file = output_file

    output_file.write_text(program)
    return output_file


def temp_file(file_name) -> Path:
    tmp_folder = util.tmp_folder()

    return tmp_folder / file_name
    pass


def run_bash(program: str) -> str:
    tmp_folder = util.tmp_folder()
    try:
        tmp_file = tmp_folder / 'tmp_file.txt'
        tmp_file.write_text(program)
        result = subprocess.run(['bash', str(tmp_file)], stdout=subprocess.PIPE)
        return result.stdout.decode()
    finally:
        util.remove_dir(tmp_folder)

    pass


class BashlogV1(object):
    _ = Variable('_')

    @staticmethod
    def variables(*vars):
        result = [Variable(v) for v in vars]

        return result

    @staticmethod
    def relation(name):
        return Relation(name)

    @staticmethod
    def row(*args):
        return RowFact(*args)

    @staticmethod
    def main(variables):
        return Main(variables)
        pass

    @staticmethod
    def program(instructions):
        return Program(instructions)

    # @staticmethod
    # def data(facts: Union[str, List]):
    #     if isinstance(facts, str):
    #         return Command(facts)
    #     else:
    #         return DataList(facts)

    @staticmethod
    def data(facts: Union[str, List]):
        if isinstance(facts, str):
            return Command(facts)
        else:
            return DataList(facts)

    @staticmethod
    def fact(*vars):
        return RowFact(*vars)

    # @staticmethod
    # def read(row, command: Command):
    #     return Data(row, command)

    @staticmethod
    def __read__(row, command_str: str):
        command = Command(command_str)
        return Data(row, command)

    @staticmethod
    def command(command_str, columns: int):
        vn = [BashlogV1._ for _ in range(columns)]
        row = RowFact(*vn)
        return BashlogV1.__read__(row, command_str)

    @staticmethod
    def relation(rel: str):
        return Relation(rel)

    @staticmethod
    def query_main(rules: List, r: Data, debug=False):
        p = Program(rules)
        return query(p, r, debug=debug)

    # @staticmethod
    # def query(rules: List, data_source: Read, q: Union[List, RelationInstance, Row], debug=False):
    #     if isinstance(q, list):
    #
    #         vn = [v for ri in q for v in ri.variables() if str(v) != '_' and isinstance(v, Variable)]
    #         print('Vn')
    #         print(vn)
    #     else:
    #         vn = [v for v in q.variables() if str(v) != '_' and isinstance(v, Variable)]
    #
    #     vn_unique = list(set(vn))
    #     print('Vn Unique')
    #     print(vn_unique)
    #     m = Main(*vn_unique) <= q
    #     p = Program(rules + [m])
    #     return query(p, data_source, debug=debug)

    # @staticmethod
    # def run(data_source: Data, rules: List, q: Union[List, RelationInstance, Row], vars: List[Variable] = None, debug=False):
    #     vars = vars or []
    #     if vars:
    #         vn = vars
    #     else:
    #         if isinstance(q, list):
    #
    #             vn = [v for ri in q for v in ri.variables() if str(v) != '_' and isinstance(v, Variable)]
    #         else:
    #             vn = [v for v in q.variables() if str(v) != '_' and isinstance(v, Variable)]
    #
    #     vn_unique = list(set(vn))
    #
    #     m = Main(*vn_unique) <= q
    #     p = Program(rules + [m])
    #     return query(p, data_source, debug=debug)

    @staticmethod
    def run(data_source: Union[List, AbstractData], rules: List, q: Union[List, RelationInstance, RowFact],
            vars: List[Variable] = None,
            debug=False):
        actual_data_source: AbstractData
        if isinstance(data_source, list):
            actual_data_source = DataList(data_source)
        else:
            actual_data_source = data_source

        vars = vars or []
        if vars:
            vn = vars
        else:
            if isinstance(q, list):

                vn = [v for ri in q for v in ri.variables() if str(v) != '_' and isinstance(v, Variable)]
            else:
                vn = [v for v in q.variables() if str(v) != '_' and isinstance(v, Variable)]

        vn_unique = list(set(vn))

        m = Main(*vn_unique) <= q
        p = Program(rules + [m])
        return query(p, actual_data_source, debug=debug)

    # @staticmethod
    # def query(rules: List, data_source: Read, relation: Relation, query_vars: List[Variable] = None, debug=False):
    #     query_vars = query_vars or []
    #
    #     vn_unique = list(set(query_vars))
    #
    #     m = Main(*vn_unique) <= rules
    #     p = Program(rules + [m] )
    #     return query(p, data_source, debug=debug)
    #
    # @staticmethod
    # def read_list(facts):
    #     return DataList(facts)


def bashlog_v1():
    return BashlogV1()
