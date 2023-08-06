Description
===========

This package contains derivative-free optimization algorithms. All algorithms
have in common that they do not require objective values to be scalar and
finite. A total order on the objective values is sufficient. For example, an
objective function could return a list of values, which are then compared
lexicographically. The package cannot handle constraints explicitly, instead
infeasible solutions should be penalized, e.g., evaluated with the worst
possible function value (possibly infinity).

The package is geared to work with optimization problems as defined in the
package optproblems. The whole package assumes minimization problems
throughout!


Documentation
=============

The documentation is located at
https://ls11-www.cs.tu-dortmund.de/people/swessing/dfoalgos/doc/
