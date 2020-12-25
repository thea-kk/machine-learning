import sys

class BST:
    def __init__(self, l, v, p):
        self._level = l
        self._value = v
        self._parent = p
        self._left = None
        self._right = None

def tree_info(a_list):

    ''' Collect the information about a list of tree nodes.
    E.g. the root of the tree, the frequency of each node, the position of each node in the list
    '''

    node_info = {'root': '', 'values': []}

    for node in a_list:
        i = 1

        for element in node:

            if element != 'x':

                node_info[element] = node_info.get(element, {'frequency': 0})

                # count the frequency of each node in the list
                node_info[element]['frequency'] += 1

                # get the position of each node in the input list
                if i == 1:
                    node_info[element]['index'] = a_list.index(node)

                    # store all nodes in a list in ascending order
                    node_info['values'].append(int(element))

            i += 1

    # built in sort function: O(nlogn) time complexity
    node_info['values'].sort()

    # find the root of the tree
    # rationale: root only appeared once in the input list
    # O(n) time complexity
    for node in node_info.keys():

        if (node != 'root') and (node != 'values'):

            if node_info[node]['frequency'] == 1:
                node_info['root'] = node
                break

    return node_info


def mirror_BST(node, node_list, tree, tree_dict):

    ''' Build a mirrored binary tree structure
    by reversing left and right nodes as stated in the input list
    '''

    left = node[2]
    right = node[1]

    if (left == 'x') and (right == 'x'):
        return

    # left branch
    if left != 'x':
        tree._left = BST(tree._level + 1, int(left), tree)
        next_node = tree_dict[left]['index']
        mirror_BST(node_list[next_node], node_list, tree._left, tree_dict)

    # right branch
    if right != 'x':
        tree._right = BST(tree._level + 1, int(right), tree)
        next_node = tree_dict[right]['index']
        mirror_BST(node_list[next_node], node_list, tree._right, tree_dict)

def sort_mirrorBST(tree, data):

    ''' Convert a mirrored binary tree to a binary search tree
    by doing in-order traversal
    '''

    if tree is not None:

        sort_mirrorBST(tree._left, data)
        tree._value = next(data)
        sort_mirrorBST(tree._right, data)

def pre_order_traversal(n):
    global RESULT

    if n is not None:

        RESULT += (str(n._value) + ' ')
        pre_order_traversal(n._left)
        pre_order_traversal(n._right)


num_line = int(sys.stdin.readline())
for _ in range(num_line):
    '''The time complexity of this algorithm is 
    O(3n + nlogn + n)  (tree_info function) +
    O(n) (mirror_BST function) + 
    n (sort_mirrorBST function) + 
    n (pre-order traversal)
    i.e. O(3n + nlogn + n + n + n + n) = O(nlogn) '''

    RESULT = ''
    a = [s.split(':') for s in sys.stdin.readline().split()]

    tree_dict = tree_info(a)

    # build a mirrored binary tree
    root = tree_dict['root']
    bst = BST(0, int(root), None)
    mirror_BST(a[tree_dict[root]['index']], a, bst, tree_dict)

    # convert the tree to a binary search tree
    values = iter(tree_dict['values'])
    sort_mirrorBST(bst, values)

    # perform pre-order traversal of the tree
    pre_order_traversal(bst)
    print(RESULT[:-1])