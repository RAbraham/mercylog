import unittest

import mercylog

DIED_DATALOG_PROGRAM = """
facts(_, S, P, O) :~ cat *.tsv
main(X) :- 
   facts(_, X, "<wasBornIn>", Y),
   facts(_, X, "<diedIn>", Y).
"""

LIVING_DATALOG_PROGRAM = """facts(_, S, P, O) :~ cat *.tsv
born(X) :- facts(_, X, "<wasBornIn>", Y).
born(X) :- facts(_, X, "<wasBornOnDate>", Y).
dead(X) :- facts(_, X, "<diedIn>", Y).
dead(X) :- facts(_, X, "<diedOnDate>", Y).
main(X) :- born(X), not dead(X)."""

LIVING_DATALOG_PROGRAM_RULES = """born(X) :- facts(_, X, "<wasBornIn>", Y).
born(X) :- facts(_, X, "<wasBornOnDate>", Y).
dead(X) :- facts(_, X, "<diedIn>", Y).
dead(X) :- facts(_, X, "<diedOnDate>", Y).
main(X) :- born(X), not dead(X)."""

LIVING_DATALOG_PROGRAM_RESULT = '<50_Cent>\n<Adele>\n<Angelina_Jolie>\n<Ariana_Grande>\n<Backstreet_Boys>\n<Barack_Obama>\n<Bill_Clinton>\n<Bill_Gates>\n<Brad_Pitt>\n<Britney_Spears>\n<Brock_Lesnar>\n<Bruno_Mars>\n<Catharina-Amalia,_Princess_of_Orange>\n<Charlie_Sheen>\n<Connie_Talbot>\n<Conor_McGregor>\n<Cristiano_Ronaldo>\n<Dafne_Keen>\n<Daft_Punk>\n<David_Beckham>\n<David_Mazouz>\n<Demi_Lovato>\n<Donald_Trump>\n<Dwayne_Johnson>\n<Eminem>\n<Emma_Stone>\n<Emma_Watson>\n<Finn_Wolfhard>\n<Frankie_Jonas>\n<Gaten_Matarazzo>\n<George_H._W._Bush>\n<George_W._Bush>\n<Harshaali_Malhotra>\n<Jackie_Evancho>\n<Jacob_Tremblay>\n<James,_Viscount_Severn>\n<Jazz_Jennings>\n<Jennifer_Aniston>\n<Jennifer_Lawrence>\n<John_Cena>\n<Johnny_Depp>\n<Justin_Bieber>\n<Katy_Perry>\n<Kendrick_Lamar>\n<Kim_Kardashian>\n<Kristen_Stewart>\n<LaMelo_Ball>\n<Lady_Louise_Windsor>\n<Laurie_Hernandez>\n<LeBron_James>\n<Leonardo_DiCaprio>\n<Lil_Pump>\n<Lionel_Messi>\n<Mackenzie_Foy>\n<Maddie_Ziegler>\n<Madison_De_La_Garza>\n<Madonna_(entertainer)>\n<Manny_Pacquiao>\n<Mariah_Carey>\n<Mark_Zuckerberg>\n<Megan_Fox>\n<Michael_Jordan>\n<Michael_Phelps>\n<Mike_Tyson>\n<Miley_Cyrus>\n<Millie_Bobby_Brown>\n<Neymar>\n<Nicki_Minaj>\n<Noah_Cyrus>\n<Novak_Djokovic>\n<O._J._Simpson>\n<Peyton_Manning>\n<Prince_George_of_Cambridge>\n<Prince_Philip,_Duke_of_Edinburgh>\n<Princess_Charlotte_of_Cambridge>\n<Rafael_Nadal>\n<Roger_Federer>\n<Ronaldinho>\n<Ronda_Rousey>\n<Rowan_Blanchard>\n<Ryan_Reynolds>\n<Salman_Khan>\n<Sarah_Palin>\n<Scarlett_Johansson>\n<Selena_Gomez>\n<Serena_Williams>\n<Skai_Jackson>\n<Sunny_Leone>\n<Sylvester_Stallone>\n<Taylor_Swift>\n<The_Undertaker>\n<Tiger_Woods>\n<Tom_Brady>\n<Tom_Cruise>\n<Tom_Hardy>\n<Vladimir_Putin>\n<Wayne_Rooney>\n<Will_Smith>\n<Willow_Shields>\n<Willow_Smith>\n<Yara_Shahidi>\n'

tsv_data = 'cat data/*.tsv'


class BashLogTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.m = mercylog.BashlogV1()
        pass

    def test_bashlog_fact(self):
        #         born(X) :- facts(_, X, "<wasBornIn>", Y).
        #         born(X) :- facts(_, X, "<wasBornOnDate>", Y).
        #         dead(X) :- facts(_, X, "<diedIn>", Y).
        #         dead(X) :- facts(_, X, "<diedOnDate>", Y).
        #
        #         main(X) :- born(X), not dead(X).

        # TODO: S, P, O are not used in the program?
        m = self.m
        X, Y = m.variables('X', 'Y')
        born = m.relation('born')
        dead = m.relation('dead')
        fact = lambda predicate: m.fact(m._, X, predicate, Y)
        rules = [
            born(X) <= fact("<wasBornIn>"),
            born(X) <= fact("<wasBornOnDate>"),
            dead(X) <= fact("<diedIn>"),
            dead(X) <= fact("<diedOnDate>"),
            m.main(X) <= [born(X), ~dead(X)]
        ]

        p = m.program(rules)
        self.assertEqual(str(p), LIVING_DATALOG_PROGRAM_RULES)

    def test_bashlog_fact_result_dead(self):
        m = self.m
        X, Y = m.variables('X', 'Y')
        _ = m._
        facts = m.command(tsv_data, columns=4)

        born = m.relation('born')
        dead = m.relation('dead')

        rules = [born(X, Y) <= m.fact(_, X, "<wasBornIn>", Y),
                 dead(X, Y) <= m.fact(_, X, "<diedIn>", Y)]
        result = m.run(facts, rules, [born(X, Y), dead(X, Y)], [X])

        self.assertEqual(result, ['<Archimedes>', '<Confucius>', '<Marilyn_Monroe>', '<William_Shakespeare>'])
        pass

    def test_bashlog_fact_result_living(self):
        m = self.m
        _ = m._
        X, Y = m.variables('X', 'Y')
        facts = m.command(tsv_data, columns=4)
        fact = lambda x, y, predicate: m.fact(_, x, predicate, y)
        abstract_fact = lambda relation, predicate: relation(_, X, predicate, Y)
        born = m.relation('born')
        dead = m.relation('dead')
        living = m.relation('living')
        rules = [born(X) <= fact(X, Y, "<wasBornIn>"),
                 born(X) <= abstract_fact(m.fact, "<wasBornOnDate>"),
                 dead(X) <= m.fact(_, X, "<diedIn>", Y),
                 dead(X) <= m.fact(_, X, "<diedOnDate>", Y),
                 living(X) <= [born(X), ~dead(X)]
                 ]

        exp = filter_empty(LIVING_DATALOG_PROGRAM_RESULT.split('\n'))

        result1 = m.run(facts, rules, [born(X), ~dead(X)])
        self.assertEqual(result1, exp)

        result2 = m.run(facts, rules, living(X))
        self.assertEqual(result2, exp)

    def test_bashlog_fact_all_people(self):
        m = self.m
        # facts(_, S, P, O) :~ cat *.tsv
        #
        # type(X, Y) :- facts(_, X, "rdf:type", Y).
        # subclass(X, Y) :- facts(_, X, "rdfs:subclassOf", Y).
        # type(X, Z) :- type(X, Y), subclass(Y, Z).
        #
        # main(X) :- type(X, "<wordnet_person_100007846>").

        # TODO: S, P, O are not used in the program?
        _ = m._
        X, Y, Z = m.variables('X', 'Y', 'Z')
        facts = m.command(tsv_data, columns=4)
        atype = m.relation('atype')
        subclass = m.relation('subclass')
        rules = [
            atype(X, Y) <= m.fact(_, X, "rdf:type", Y),
            subclass(X, Y) <= m.fact(_, X, "rdfs:subclassOf", Y),
            atype(X, Z) <= [atype(X, Y), subclass(Y, Z)]
        ]

        exp_result = '<50_Cent>\n<Abraham>\n<Adele>\n<Angelina_Jolie>\n<Archimedes>\n<Ariana_Grande>\n<Bill_Gates>\n<Bob_Marley>\n<Brad_Pitt>\n<Britney_Spears>\n<Brock_Lesnar>\n<Bruno_Mars>\n<Charlie_Sheen>\n<Che_Guevara>\n<Christopher_Columbus>\n<Clint_Eastwood>\n<Dafne_Keen>\n<David_Beckham>\n<David_Bowie>\n<David_Mazouz>\n<Demi_Lovato>\n<Dwayne_Johnson>\n<Elvis_Presley>\n<Eminem>\n<Emma_Stone>\n<Emma_Watson>\n<Finn_Wolfhard>\n<Frankie_Jonas>\n<Freddie_Mercury>\n<Gaten_Matarazzo>\n<Gautama_Buddha>\n<George_Washington>\n<Hannibal>\n<Harshaali_Malhotra>\n<Heath_Ledger>\n<Jacob_Tremblay>\n<Jennifer_Aniston>\n<Jennifer_Lawrence>\n<Joan_of_Arc>\n<John_Cena>\n<John_Lennon>\n<Johnny_Depp>\n<Joseph_Stalin>\n<Justin_Bieber>\n<Kanye_West>\n<Katy_Perry>\n<Kendrick_Lamar>\n<Kim_Kardashian>\n<Kristen_Stewart>\n<Lady_Gaga>\n<Leonardo_DiCaprio>\n<Lil_Wayne>\n<Mackenzie_Foy>\n<Madison_De_La_Garza>\n<Madonna_(entertainer)>\n<Mahatma_Gandhi>\n<Marco_Polo>\n<Mariah_Carey>\n<Marilyn_Monroe>\n<Mark_Wahlberg>\n<Mark_Zuckerberg>\n<Megan_Fox>\n<Mila_Kunis>\n<Miley_Cyrus>\n<Millie_Bobby_Brown>\n<Moses>\n<Muhammad>\n<Muhammad_Ali>\n<Natalie_Portman>\n<Noah_Cyrus>\n<Prince_(musician)>\n<Rihanna>\n<Robin_Williams>\n<Rowan_Blanchard>\n<Ryan_Reynolds>\n<Salman_Khan>\n<Scarlett_Johansson>\n<Selena_Gomez>\n<Skai_Jackson>\n<Spartacus>\n<Steve_Jobs>\n<Sylvester_Stallone>\n<Taylor_Swift>\n<Tom_Cruise>\n<Tom_Hardy>\n<Tupac_Shakur>\n<Vladimir_Putin>\n<Will_Smith>\n<William_Shakespeare>\n<William_Wallace>\n<Willow_Shields>\n<Willow_Smith>\n<Yara_Shahidi>\n'

        result = m.run(facts, rules, atype(X, "<wordnet_person_100007846>"))
        self.assertEqual(result, filter_empty(exp_result.split('\n')))
        pass

    def test_bashlog_facts_from_list(self):
        m = self.m
        _ = m._
        # TODO: S, P, O are not used in the program?
        X, Y, Z = m.variables('X', 'Y', 'Z')

        father_of = m.relation('fatherOf')
        atype = m.relation('type')
        grandfather_of = m.relation('grandfatherOf')

        facts = [
            atype("Pop", "Rajiv", "father"),
            atype("Sajan", "Anisha", "father"),
            atype("Rajiv", "Aks", "father"),
        ]

        rules = [father_of(X, Y) <= atype(X, Y, "father"),
                 grandfather_of(X, Y) <= [father_of(X, Z), father_of(Z, Y)]]

        grandfather1 = m.run(facts, rules, grandfather_of(X, m._))
        self.assertEqual(['Pop'], grandfather1)

        grandfather2 = m.run(facts, rules, grandfather_of(X, Y), [X])
        self.assertEqual(['Pop'], grandfather2)

        self.assertEqual(grandfather1, grandfather2)

        grandson = m.run(facts, rules, grandfather_of(m._, Y))
        self.assertEqual(['Aks'], grandson)

    def test_bashlog_actual_facts_from_list(self):
        m = self.m

        X, Y, Z = m.variables('X', 'Y', 'Z')
        father_of = m.relation('fatherOf')
        grandfather_of = m.relation('grandfatherOf')

        facts = [
            father_of("Pop", "Rajiv"),
            father_of("Sajan", "Anisha"),
            father_of("Rajiv", "Aks"),
        ]
        rules = [grandfather_of(X, Y) <= [father_of(X, Z), father_of(Z, Y)]]

        grandfather1 = m.run(facts, rules, grandfather_of(X, m._))
        self.assertEqual(['Pop'], grandfather1)

        grandfather2 = m.run(facts, rules, grandfather_of(X, Y), [X])
        self.assertEqual(['Pop'], grandfather2)

        self.assertEqual(grandfather1, grandfather2)

        grandson = m.run(facts, rules, grandfather_of(m._, Y))
        self.assertEqual(['Aks'], grandson)


def filter_empty(result):
    return list(filter(None, result))


if __name__ == '__main__':
    unittest.main()
