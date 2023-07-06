class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def ConvertListToBinaryTree(items):

    if not items:
        return None

    root_node = TreeNode(items[0])
    nodes = [root_node]
    for i, x in enumerate(items[1:]):
        if x is None:
            continue
        parent_node = nodes[i // 2]
        is_left = (i % 2 == 0)
        node = TreeNode(x)
        if is_left:
            parent_node.left = node
        else:
            parent_node.right = node
        nodes.append(node)

    return root_node


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def ConvertListToLinkedList(list_to_covert):
    tempItem = None
    for item in reversed(list_to_covert):
        node = ListNode(item,tempItem)
        tempItem = node
    return tempItem

def printLinkedList(head):
    while head:
        print(head.val, end="")
        head = head.next
    print("")