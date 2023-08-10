# Shallow Trees

This is a python module with a simple implementation of json-compatible shallow trees

A shallow tree is a tree (ie: a container for a graph of nodes referencing other nodes in the container, with no cycles (and technically only one root node, but this allows multiple, making it really a forest)) datastructure where all the nodes are stored in the same place C and reference eachother using locators within C. This has the advantage that: you can have reference cycles (child holds a reference to its parent, which holds a reference to the child), and is still representable in json

This library uses a `list` of `dict` nodes, where a node reference is just the integer index of the node in the list

So each node looks like:
```python
{
  'parent_i': int,          # location of parent node in the shtree list
  'parent_child_i': int,    # the index of this in parent node's `child_i_list`
  'child_i_list': list(int) # this node's children indices in the shtree list
}
```

And the whole shtree list looks like:
```python
list(node)
```

---

This module has tests built in, run them with: `python __init__.py` in a terminal, or by importing the module and calling: `run_shtree_tests()`
