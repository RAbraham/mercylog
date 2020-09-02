Inspiration
^^^^^^^^^^^

* I got inspired about DSL's by Alan Kay. I was on a constant search for DSLs. I think some way down that path, I learned about declarative languages and Prolog, leading me to know about Datalog.
* I first wanted to build Datalog over Hadoop. And found Cascalog(a Clojure over Hadoop). It seems defunct now and do not go their site! It's taken over and bombarded with SEO text. 

2016 - 2018:
^^^^^^^^^^^^
* Read about AI and Prolog initiatives like KProblog. It seemed exciting. Got a sense that it would not scale. 
* Read ML at scale by Borkar and how Datalog was a natural fit for ML. This got me really interested in Datalog. 
* Read about Dyna for AI (suggested by David Barbour). The creativity of using Datalog for AI and Analytics hit me hard. It's like my mind was pried open.
* Read about Yedalog at Google. It was like what I wanted to build. The dream
* Read about a different twist on Logic Programming i.e. I think the MiniKanren approach. First read about the 'pitfalls' of classic Prolog by Oleg K. He talked about Hansei?
* Read about MiniKanren. It was exciting to see logic programming at it's simplest yet powerful core.
* Implemented MicroKanren in Julia. Though it couldn't handle macros, I read some Clojure code and without executing it, I converted into Julia, another language I wasn't familiar with :)
* Read the Schemer. The wonderful book. Stopped when I realized that it was more expressive than I probably wanted and that I didn't know enough to bring that into reality. Greg Rosenblatt will :)
* Read all about Datomic. It was amazing. The most successful variant of Datalog as we know it and what a practical take with it's entity model and just allowing a three valued tuple. 
* Read about KDDLog and DEALS. It looked the ideal Datalog for knowledge discovery.
* Saw the Dedalus video by Peter Alvaro on Strangeloop. I first heard about Dedalus from David Barbour of Awelon Blue. He mentioned that it was one of the promising systems for writing good code.
* Read the Boom Analytics paper. Got excited about the order of magnitude reduction in code size with Overlog.
* Read the Dedalus paper in part. Got excited about the idea of declaratively specifying time and space in addition to computation.
* Read the MLog paper. My mind started churning. MLog talks about iteration with time steps. Dedalus is about state in time steps. Can they both be combined?
* Read the differential dataflow work by Frank McSherry. Got excited about having a runtime for Dedalus.

2019:
^^^^^
* Read the Bashlog paper. They compiled Datalog to Bash Scripts It excited me to bits. Bashlog showed amazing performance just using core UNIX software and had a comparable performance to most state of the art Datalog impelmentation. I decided to just build a Python wrapper around it. Though I was working all day with my startup, I would work on it for 20 mins a day at night before I slept :). That was the first iteration of mercylog and it worked!
