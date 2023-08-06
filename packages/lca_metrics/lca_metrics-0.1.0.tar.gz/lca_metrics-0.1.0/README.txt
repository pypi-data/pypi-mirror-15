LCA Metrics
===========

Validation metrics for hierarchical label by Lowest Common Ancestor.

Original paper is (Kosmopoulos, 2015)

Development log
---------------

Version 0.1.0
~~~~~~~~~~~~~

Add dummy node to handle empty set input. If input is empty set, one
assign dummy node as true or predict node to calculate LCA in graph.
More and more the depth become deep, result score becomes lower.
