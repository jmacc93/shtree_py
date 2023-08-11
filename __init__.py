import copy

# Tree is like: [node1, node2, ..., nodeN]
# Node is like: {'parent_i': int, 'child_i_list': [int, int, ...], 'parent_child_i': int, ...}

'''
List of functions:
* new_node
* add_node
* add_new_node
* remove_node

* add_child
* add_new_child

* add_sibling_adjacent_to
* add_sibling_after
* add_sibling_before
* add_new_sibling_after
* add_new_sibling_before

* add_new_child_structure
* shtree_from_structure

* disconnect_parent
* reparent_node

* get_adjacent_sibling_i
* get_adjacent_sibling
* get_prev_sibling
* get_next_sibling
* get_prev_sibling_i
* get_next_sibling_i
* get_roots

* get_child_i
* get_child
* get_parent_i
* get_parent
* get_first_leaf_i

* child_count
* is_descendant

* remove_disconnected

* deepen
* compactify
* copy_subtree

* prev_siblings
* next_siblings

* each_node_i
* each_child_i
* each_child

* run_shtree_tests
'''

def new_node(**kargs):
  node = {
    'parent_i': None,
    'parent_child_i': None,
    'child_i_list': []
  }
  for key in kargs:
    node[key] = kargs[key]
  return node

def _test_new_node():
  shtree = [new_node(abc=123)]
  assert shtree[0]['abc'] == 123
  assert 'parent_i' in shtree[0]
  assert 'parent_child_i' in shtree[0]
  assert 'child_i_list' in shtree[0]



def add_node(shtree, new_node):
  assert type(new_node) is dict
  assert 'parent_i' in new_node
  assert 'parent_child_i' in new_node
  assert 'child_i_list' in new_node
  
  shtree.append(new_node)
  return len(shtree) - 1


def add_new_node(shtree, **kargs):
  return add_node(shtree, new_node(**kargs))


def remove_node(shtree, node_i, *, and_subtree = True):
  node = shtree[node_i]
  disconnect_parent(shtree, node_i)
  child_i_list = node['child_i_list']
  for child_i in child_i_list:
    if and_subtree:
      for subtree_node_i in [*each_node_i_leaf_first(shtree, child_i)]:
        shtree[subtree_node_i] = None
        # remove_node(shtree, subtree_node_i, and_subtree = False)
    else:
      child = shtree[child_i]
      child['parent_i'] = None
      child['parent_child_i'] = None
  node['child_i_list'] = []
  shtree[node_i] = None

def _test_remove_node():
  import random
  shtree = [new_node()]
  
  # dont remove subtree subtree
  while len(shtree) < 100:
    parent_i = random.randint(0, len(shtree)-1)
    add_new_child(shtree, parent_i)
    _test_all_nodes_consistency(shtree)
  while len(shtree) > 0:
    node_i = random.randint(0, len(shtree)-1)
    remove_node(shtree, node_i, and_subtree = False)
    _test_all_nodes_consistency(shtree)
    compactify(shtree)
    _test_all_nodes_consistency(shtree)
  
  # remove subtrees
  add_new_node(shtree)
  while len(shtree) < 100:
    parent_i = random.randint(0, len(shtree)-1)
    add_new_child(shtree, parent_i)
    _test_all_nodes_consistency(shtree)
  while len(shtree) > 0:
    node_i = random.randint(0, len(shtree)-1)
    remove_node(shtree, node_i)
    _test_all_nodes_consistency(shtree)
    compactify(shtree)
    _test_all_nodes_consistency(shtree)


#######################


def _test_node_properties_exist(shtree, node_i):
  node = shtree[node_i]
  assert 'parent_i' in node
  assert 'parent_child_i' in node
  assert 'child_i_list' in node

def _test_node_parent_exists(shtree, node_i):
  node = shtree[node_i]
  if node['parent_i'] != None:
    assert shtree[node['parent_i']] != None

def _test_node_children_exist(shtree, node_i):
  node = shtree[node_i]
  child_i_list = node['child_i_list']
  for child_i in child_i_list:
    child = shtree[child_i]
    assert child != None

def _test_parent_child_symmetry(shtree, node_i):
  node = shtree[node_i]
  
  parent_node_i = node['parent_i']
  if parent_node_i != None:
    parent_node = shtree[parent_node_i]
    assert parent_node != None
    assert parent_node['child_i_list'][node['parent_child_i']] == node_i
  
  for child_i in node['child_i_list']:
    child = shtree[child_i]
    assert child['parent_i'] == node_i

def _test_all_nodes_consistency(shtree):
  for node_i in range(0, len(shtree)):
    node = shtree[node_i]
    if node != None:
      _test_node_properties_exist(shtree ,node_i)
      _test_node_parent_exists(shtree, node_i)
      _test_node_children_exist(shtree, node_i)
      _test_parent_child_symmetry(shtree, node_i)


def add_child(shtree, parent_i, child_i, position = -1):
  parent = shtree[parent_i]
  reparent_node(shtree, parent_i, child_i, position)
  return child_i

def add_new_child(shtree, parent_i, **kargs):
  new_child_i = add_node(shtree, new_node(**kargs))
  return add_child(shtree, parent_i, new_child_i)

def _test_add_new_child():
  shtree = [new_node(a=1)]
  tmp1 = add_new_child(shtree, 0, a=2)
  tmp2 = add_new_child(shtree, tmp1, a=3)
  tmp3 = add_new_child(shtree, tmp1, a=4)
  tmp4 = add_new_child(shtree, 0, a=5)
  _test_all_nodes_consistency(shtree)
  assert shtree[tmp2]['parent_i'] == tmp1
  assert shtree[shtree[tmp2]['parent_i']]['child_i_list'][shtree[tmp2]['parent_child_i']] == tmp2
  assert shtree[shtree[tmp3]['parent_i']]['child_i_list'][shtree[tmp3]['parent_child_i']] == tmp3
  assert shtree[shtree[tmp4]['parent_i']]['child_i_list'][shtree[tmp4]['parent_child_i']] == tmp4
  assert shtree[0]['parent_i'] == None
  assert len(shtree[tmp4]['child_i_list']) == 0
  assert len(shtree[tmp1]['child_i_list']) == 2

def _test_add_child():
  tree = [new_node()]
  add_child(tree, 0, add_new_node(tree))
  add_child(tree, 0, add_new_node(tree))
  add_child(tree, 0, add_new_node(tree))
  
  add_child(tree, 0, add_new_node(tree), 0)
  assert tree[0]['child_i_list'] == [4, 1, 2, 3]
  _test_all_nodes_consistency(tree)


def add_sibling_adjacent_to(shtree, node_i, new_sibling_i, offset):
  node = shtree[node_i]
  if node['parent_i'] == None:
    return
  
  parent_i = node['parent_i']
  parent = shtree[parent_i]
  parent_child_i_list = parent['child_i_list']
  
  disconnect_parent(shtree, new_sibling_i)
  
  # Get the child position
  new_child_i = node['parent_child_i'] + offset
  if new_child_i < 0:
    new_child_i = 0
  elif new_child_i > len(parent_child_i_list):
    new_child_i = len(parent_child_i_list)
  
  reparent_node(shtree, parent_i, new_sibling_i, new_child_i)
  return new_sibling_i

def add_sibling_after(shtree, node_i, new_sibling):
  return add_sibling_adjacent_to(shtree, node_i, new_sibling, 1)
def add_sibling_before(shtree, node_i, new_sibling):
  return add_sibling_adjacent_to(shtree, node_i, new_sibling, 0)

def add_new_sibling_after(shtree, node_i, **kargs):
  return add_sibling_after(shtree, node_i, add_new_node(shtree, **kargs))
def add_new_sibling_before(shtree, node_i, **kargs):
  return add_sibling_before(shtree, node_i, add_new_node(shtree, **kargs))

def _test_add_sibling_adjacent_to():
  shtree = [new_node()]
  i1 = add_new_child(shtree, 0, a=1)
  i2 = add_new_child(shtree, 0, a=2)
  i3 = add_new_child(shtree, 0, a=3)
  i4 = add_new_child(shtree, 0, a=4)
  i5 = add_new_child(shtree, 0, a=5)
  _test_all_nodes_consistency(shtree)
  assert shtree[0]['child_i_list'] == [i1, i2, i3, i4, i5]
  
  add_sibling_before(shtree, i3, i5)
  _test_all_nodes_consistency(shtree)
  assert shtree[0]['child_i_list'] == [i1, i2, i5, i3, i4]
  
  add_sibling_after(shtree, i3, i1)
  _test_all_nodes_consistency(shtree)
  assert shtree[0]['child_i_list'] == [i2, i5, i3, i1, i4]
  
  import random
  shtree = [new_node()]
  child_i_list = shtree[0]['child_i_list']
  lst_order = [add_new_child(shtree, 0)]
  for i in range(0, 100):
    i = random.randint(0, len(child_i_list)-1)
    node_i = child_i_list[i]
    if random.randint(0, 1) == 0:
      lst_order.insert(i, add_new_sibling_before(shtree, node_i))
    else:
      lst_order.insert(i+1, add_new_sibling_after(shtree, node_i))
    _test_all_nodes_consistency(shtree)
    lst_order == child_i_list
  _test_all_nodes_consistency(shtree)


#######################

def replace_node_with_new(shtree, node_i, *, keep_children = True, **new_properties):
  node = shtree[node_i]
  
  # remove children if required:
  if not keep_children:
    for child_i in [*node['child_i_list']]:
      remove_node(shtree, child_i)
  
  # remove old properties
  for key in [*node.keys()]:
    if key == 'parent_i' or key == 'child_i_list' or key == 'parent_child_i':
      continue # dont remove fundamental node properties
    del node[key]
  
  # add new properties
  node |= new_properties

def _test_replace_node_with_new():
  tree = shtree_from_structure(
    {'a':-1},
    [{'a':7}, [{'a':3}, {'a':1}, {'a':2}], [{'a':6}, {'a':4}, {'a':5}]]
  )
  correct_output = shtree_from_structure(
    {'a':-1},
    [{'a':7}, {'b':100}, [{'a':6}, {'a':4}, {'a':5}]]
  )
  replace_node_with_new(tree, 2, b=100, keep_children=False)
  _test_all_nodes_consistency(tree)
  compactify(tree)
  _test_all_nodes_consistency(tree)
  assert tree == correct_output


## has bug, do later:
# def replace_node(tree, node_i, repl_node_i, *, keep_children = True, keep_repl_children = True, remove = True):
#   node = tree[node_i]
#   repl_node = tree[repl_node_i]
  
#   # remove replacement's children if required:
#   if not keep_repl_children:
#     for child_i in [*repl_node['child_i_list']]:
#       remove_node(tree, child_i)
  
#   # remove or move children if required:
#   if not keep_children:
#     for child_i in [*node['child_i_list']]:
#       remove_node(tree, child_i)
#   else: # move children to replacement
#     for child_i in [*node['child_i_list']]:
#       add_child(tree, repl_node_i, child_i)
  
#   # disconnect replacement from parent
#   disconnect_parent(tree, repl_node_i)
  
#   # reconnect to new parent
#   parent = tree[node['parent_i']]
#   repl_node['parent_i'] = node['parent_i']
#   parent['child_i_list'][node['parent_child_i']] = repl_node_i
#   repl_node['parent_child_i'] = node['parent_child_i']
  
#   if remove:
#     remove_node(tree, node_i)  

#######################


# This creates a new node with `a=1` and with a single child with `a=2`:
#   add_new_child_structure(tree, parent_i, {'a':1}, {'a':2})
# This creates a new node with a child with its own children:
#   add_new_child_structure(tree, parent_i, {'a':1}, [{'b':2}, {'c': 3}])
# The basic form of the significant arguments is:
#   {parent_props...}, {child_props...} or [{child_props}, {child_child_props}, ...]
# Argument lists -> nodes with children
# Argument dicts -> nodes with no children
# See _tryme below
def add_new_child_structure(tree, parent_i, *spec_list):
  for spec in spec_list:
    if type(spec) is dict: # new child with no children
      add_new_child(tree, parent_i, **spec)
    else: # new child with children
      new_child_kwargs = spec[0]
      recursive_specs  = spec[1:]
      child_i = add_new_child(tree, parent_i, **new_child_kwargs)
      add_new_child_structure(tree, child_i, *recursive_specs)

# This is just like add_new_child_structure but without the `tree` and `parent_i` args
def shtree_from_structure(root_kwargs, *spec_list):
  new_tree = [new_node(**root_kwargs)]
  add_new_child_structure(new_tree, 0, *spec_list)
  return new_tree

def _tryme():
  print(deepen(shtree_from_structure({'a':1},
    [{'a':2}, {'a':3}, [{'a':4}, {'a':10}]],
    [{'a':5}, [{'a':6}], [{'a':7}]]
  )))
  
  print(deepen(shtree_from_structure({'a':1}, {'b':2})))

#######################


def disconnect_parent(shtree, node_i):
  node = shtree[node_i]
  parent_i = node['parent_i']
  if parent_i == None:
    return
  
  parent_node = shtree[parent_i]
  node['parent_i'] = None
  
  # Adjust siblings' parent_child_i values
  node_parent_child_i = node['parent_child_i']
  parent_child_i_list = parent_node['child_i_list']
  for i in range(node_parent_child_i + 1, len(parent_child_i_list)):
    parent_child_i = parent_child_i_list[i]
    parent_child_node = shtree[parent_child_i]
    parent_child_node['parent_child_i'] -= 1
  
  # Remove node from parent's child_i_list
  del parent_child_i_list[node_parent_child_i]


def reparent_node(shtree, parent_i, child_i, position_arg = -1):
  parent = shtree[parent_i]
  child  = shtree[child_i]
  
  # Disconnect from parent
  disconnect_parent(shtree, child_i)
  
  parent_child_i_list = parent['child_i_list']
  position = position_arg if position_arg >= 0 else len(parent_child_i_list) + position_arg + 1
  
  # Insert the new child
  parent_child_i_list.insert(position, child_i)
  child['parent_i'] = parent_i
  child['parent_child_i'] = position
  
  # Adjust all child nodes parent_child_i after injection point
  for sibling_i in range(position + 1, len(parent_child_i_list)):
    sibling = shtree[parent_child_i_list[sibling_i]]
    sibling['parent_child_i'] += 1
  
  return child_i

def _test_reparent_node():
  shtree = [new_node(a=1)]; i0 = 0; n0 = shtree[i0]
  i1 = add_new_child(shtree, i0); n1 = shtree[i1]
  i2 = add_new_child(shtree, i0); n2 = shtree[i2]
  
  i3 = add_new_child(shtree, i1); n3 = shtree[i3]
  i4 = add_new_child(shtree, i1); n4 = shtree[i4]
  
  _test_all_nodes_consistency(shtree)
  
  assert n0['child_i_list'] == [i1, i2]
  assert n1['child_i_list'] == [i3, i4]
  assert n2['child_i_list'] == []
  
  assert n3['parent_i'] == i1
  assert n3['parent_child_i'] == 0
  assert n4['parent_i'] == i1
  assert n4['parent_child_i'] == 1
  
  reparent_node(shtree, i2, i3)
  _test_all_nodes_consistency(shtree)
  assert n0['child_i_list'] == [i1, i2]
  assert n1['child_i_list'] == [i4]
  assert n2['child_i_list'] == [i3]
  
  assert n3['parent_i'] == i2
  assert n3['parent_child_i'] == 0
  assert n4['parent_i'] == i1
  assert n4['parent_child_i'] == 0
  
  reparent_node(shtree, i2, i4)
  _test_all_nodes_consistency(shtree)
  assert n0['child_i_list'] == [i1, i2]
  assert n1['child_i_list'] == []
  assert n2['child_i_list'] == [i3, i4]
  
  assert n3['parent_i'] == i2
  assert n3['parent_child_i'] == 0
  assert n4['parent_i'] == i2
  assert n4['parent_child_i'] == 1

#######################

def get_adjacent_sibling_i(shtree, node_i, offset):
  node = shtree[node_i]
  if node['parent_i'] == None:
    return None
  parent = shtree[node['parent_i']]
  if parent == None:
    return None
  
  parent_child_i_list = parent['child_i_list']
  sibling_parent_child_i = node['parent_child_i'] + offset
  if sibling_parent_child_i < 0  or  len(parent_child_i_list) <= sibling_parent_child_i:
    return None # out of bounds
  return parent_child_i_list[sibling_parent_child_i]

def get_adjacent_sibling(shtree, node_i, offset):
  adjacent_sibling_i = get_adjacent_sibling_i(shtree, node_i, offset)
  if adjacent_sibling_i != None:
    return shtree[adjacent_sibling_i]

def get_prev_sibling(shtree, node_i, n = 1):
  return get_adjacent_sibling(shtree, node_i, -n)
def get_next_sibling(shtree, node_i, n = 1):
  return get_adjacent_sibling(shtree, node_i, n)

def get_prev_sibling_i(shtree, node_i, n = 1):
  return get_adjacent_sibling_i(shtree, node_i, -n)
def get_next_sibling_i(shtree, node_i, n = 1):
  return get_adjacent_sibling_i(shtree, node_i, n)


def get_roots(shtree):
  for i, node in enumerate(shtree):
    if node == None:
      continue
    parent_i = node['parent_i']
    if parent_i == None:
      yield i


def is_descendant(shtree, ancestor_i, node_i):
  current_node = shtree[node_i]
  while current_node != None:
    parent_i = current_node['parent_i']
    if parent_i == None:
      return False
    if parent_i == ancestor_i:
      return True
    current_node = shtree[parent_i]
  return False
is_child = is_descendant


def get_child_i(shtree, parent_arg, child_i):
  if type(parent_arg) is int: # parent is node index
    return shtree[parent_arg]['child_i_list'][child_i]
  elif type(parent_arg) is dict: # parent is node
    return parent_arg['child_i_list'][child_i]
def get_child(shtree, parent_arg, child_i):
  return shtree[get_child_i(shtree, parent_arg, child_i)]


def get_parent_i(shtree, node_i):
  return shtree[node_i]['parent_i']
def get_parent(shtree, node_i):
  return shtree[get_parent_i(shtree, node_i)]


def get_first_leaf_i(shtree, start_node_i = 0):
  node_i = start_node_i
  while True:
    node = shtree[node_i]
    if len(node['child_i_list']) > 0:
      node_i = node['child_i_list'][0]
    else:
      return node_i

#######################

def child_count(shtree, node_i):
  return len(shtree[node_i]['child_i_list'])

#######################


def remove_disconnected(shtree, root_i = 0):
  node_i = 0
  while node_i < len(shtree):
    if not is_descendant(shtree, root_i, node_i)  and  node_i != root_i:
      shtree[node_i] = None
    node_i += 1
  compactify(shtree)


def deepen(shtree, root_index = 0):
  tree = copy.deepcopy(shtree)
  
  # Make child_i_list into children property that points to real nodes
  for node_i, node in enumerate(tree):
    if node == None:
      continue
    parent_i = node['parent_i']
    if parent_i == None:
      continue
    
    # Add children property to parent if necessary
    parent = tree[parent_i]
    if 'children' not in parent:
      parent['children'] = [None for i in parent['child_i_list']]
    
    # Add this to parent's children property
    parent['children'][node['parent_child_i']] = node
  #
  
  # Remove child_i_list and parent_i properties
  for i, node in enumerate(tree):
    if node == None:
      continue
    del node['parent_i']
    del node['parent_child_i']
    del node['child_i_list']
  
  return tree[root_index]


def compactify(shtree):
  new_shtree = []
  old_to_new_i = {}
  
  # Copy
  for i, node in enumerate(shtree):
    if node == None:
      continue
    new_node = copy.deepcopy(node)
    new_i = len(new_shtree)
    new_shtree.append(new_node)
    old_to_new_i[i] = new_i
  
  # Replace all old node locations with new locations
  for i, node in enumerate(new_shtree):
    old_parent_i = node['parent_i']
    if old_parent_i != None:
      node['parent_i'] = old_to_new_i.get(old_parent_i, node['parent_i'])
    child_i_list = node['child_i_list']
    for j, old_child_i in enumerate(child_i_list):
      child_i_list[j] = old_to_new_i[old_child_i]
  
  shtree[:] = new_shtree


#######################

def copy_subtree(shtree, root_i):
  new_tree = []
  to_scan = [root_i]
  new_i_map = {} # for replacing node indices in new tree
  
  # copy nodes to new tree
  while len(to_scan) > 0:
    next_i = to_scan.pop()
    new_i_map[next_i] = len(new_tree)
    new_node = copy.deepcopy(shtree[next_i])
    new_tree.append(new_node)
    for child_i in each_child_i(shtree, next_i):
      to_scan.append(child_i)
  
  # replace all node index references with new correct ones
  for node_i, node in enumerate(new_tree):
    if node['parent_i'] != None:
      node['parent_i'] = new_i_map[node['parent_i']]  if node_i > 0 else None
    child_i_list = node['child_i_list']
    for index, old_child_i in enumerate(child_i_list):
      child_i_list[index] = new_i_map[old_child_i]
  
  return new_tree
#

def _test_copy_subtree_full():
  import random
  tree = [new_node(id=random.randint(0, 1e6))]
  for i in range(0, 300):
    node_i = random.randint(0, len(tree)-1)
    add_new_child(tree, node_i, id=random.randint(0, 1e6))
  
  full_copy = copy_subtree(tree, 0)
  _test_all_nodes_consistency(full_copy)
  assert len(tree) == len(full_copy)
  assert id(tree) != id(full_copy)
  assert id(tree[0]) != id(full_copy[0])
  assert deepen(tree) == deepen(full_copy)

  
def _test_copy_subtree_partial():
  import random
  tree = [new_node(id=random.randint(0, 1e6))]
  for i in range(0, 300):
    node_i = random.randint(0, len(tree)-1)
    add_new_child(tree, node_i, id=random.randint(0, 1e6))
  
  partial_copy_1 = copy_subtree(tree, get_child_i(tree, 0, 0))
  _test_all_nodes_consistency(partial_copy_1)
  for i in range(0, 5):
    partial_copy_2 = copy_subtree(tree, random.randint(0, len(tree)-1))
    _test_all_nodes_consistency(partial_copy_2)


#######################

def prev_siblings(shtree, node_i):
  # in parent's child_i_list,
  # iterate backward and yield those nodes
  node = shtree[node_i]
  if node['parent_i'] == None:
    return
  
  parent = shtree[node['parent_i']]
  parent_child_i_list = parent['child_i_list']
  i = node['parent_child_i']-1
  while i >= 0:
    yield parent_child_i_list[i]
    i -= 1

def next_siblings(shtree, node_i):
  # in parent's child_i_list,
  # iterate backward and yield those nodes
  node = shtree[node_i]
  if node['parent_i'] == None:
    return
  
  parent = shtree[node['parent_i']]
  parent_child_i_list = parent['child_i_list']
  i = node['parent_child_i']+1
  while i < len(parent_child_i_list):
    yield parent_child_i_list[i]
    i += 1


def _test_prev_next_siblings():
  shtree = [new_node()]
  for i in range(0, 10):
    add_new_child(shtree, 0)
  _test_all_nodes_consistency(shtree)
  
  child_i_list = shtree[0]['child_i_list']
  middle_child_i = child_i_list[5]
  
  all_prev_siblings = [*prev_siblings(shtree, middle_child_i)]
  all_next_siblings = [*next_siblings(shtree, middle_child_i)]
  assert len(all_prev_siblings) + len(all_next_siblings) + 1 == len(child_i_list)
  
  assert all_prev_siblings == [*reversed(child_i_list[:5])]
  assert all_next_siblings == child_i_list[6:]

#######################

def each_node_i(shtree):
  for i in range(0, len(shtree)):
    if shtree[i] != None:
      yield i


def each_child_i(shtree, parent_i):
  return (child_i for child_i in shtree[parent_i]['child_i_list'])
def each_child(shtree, parent_i):
  return (shtree[child_i] for child_i in shtree[parent_i]['child_i_list'])


def each_node_i_leaf_first(shtree, root_i = 0):
  node_i = get_first_leaf_i(shtree, root_i)
  while True:
    
    # get next node_i first
    next_i = None
    node = shtree[node_i]
    parent_i = node['parent_i']
    if node_i != root_i  and parent_i != None:
      next_i = get_next_sibling_i(shtree, node_i) # try going to next sibling
      
      if next_i != None: # have next sibling
        if child_count(shtree, next_i) > 0: # next has children
          next_i = get_first_leaf_i(shtree, next_i) # descent to first leaf
        
      else: # no next sibling
        next_i = parent_i # go to parent
    
    # then yield
    yield node_i
    
    # and set node_i to next or return
    if next_i == None:
      break
    else:
      node_i = next_i

def _test_each_node_i_leaf_first():
  tree = shtree_from_structure(
    {'a':-1},
    [{'a':7}, [{'a':3}, {'a':1}, {'a':2}], [{'a':6}, {'a':4}, {'a':5}]]
  )
  res = [*map(lambda i: tree[i]['a'], each_node_i_leaf_first(tree, 1))]
  assert res == [1,2,3,4,5,6,7]


#######################

def _misc_test_1():
  tree = [new_node()]
  add_new_child(tree, 0)
  add_new_child(tree, 0)
  add_new_child(tree, 0)
  add_new_child(tree, 0)
  add_new_child(tree, 0)
  i = add_new_sibling_after(tree, 3, asdf=123)
  assert 'asdf' in tree[i]
  
def _misc_test_2():
  tree = [new_node()]
  i1 = add_new_child(tree, 0, a=0)
  i2 = add_new_child(tree, 0, a=0)
  i3 = add_new_child(tree, 0, a=0)
  i4 = add_new_child(tree, 0, a=0)
  i5 = add_new_child(tree, 0, a=0)
  i6 = add_new_child(tree, 0, a=0)
  
  i7 = add_new_sibling_before(tree, i3)
  remove_node(tree, i3)
  ni7 = get_next_sibling_i(tree, i7)
  
  assert ni7 == i4


def run_shtree_tests():
  _test_new_node()
  _test_add_new_child()
  _test_add_child()
  _test_reparent_node()
  _test_remove_node()
  _test_add_sibling_adjacent_to()
  _test_prev_next_siblings()
  _test_replace_node_with_new()
  _test_copy_subtree_full()
  _test_copy_subtree_partial()
  _test_each_node_i_leaf_first()
  _misc_test_1()
  _misc_test_2()


if __name__ == '__main__':
  run_shtree_tests()
  print("Test functions passed")
