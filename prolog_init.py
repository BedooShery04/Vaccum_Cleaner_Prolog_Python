# prolog_init.py
from pyswip import Prolog

# Initialise Prolog engine
prolog = Prolog()

# ---- Facts ----
prolog.assertz("room(hall)")
prolog.assertz("room(bedroom)")
prolog.assertz("room(dock)")

# Connections (bidirectional)
prolog.assertz("connected(dock, bedroom)")
prolog.assertz("connected(bedroom, dock)")
prolog.assertz("connected(hall, bedroom)")
prolog.assertz("connected(bedroom, hall)")

# Helper predicates
prolog.assertz("linked(X, Y) :- connected(X, Y)")
prolog.assertz("linked(X, Y) :- connected(Y, X)")
prolog.assertz("member(X, [X|_])")
prolog.assertz("member(X, [_|T]) :- member(X, T)")
prolog.assertz("select(X, [X|T], T)")
prolog.assertz("select(X, [Y|T], [Y|R]) :- select(X, T, R)")

# Action predicates
prolog.assertz(r"can_move(X, Y) :- linked(X, Y), X \= Y")
prolog.assertz(r"can_clean(R) :- R \= dock")