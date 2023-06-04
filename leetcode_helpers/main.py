class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def ConvertListToBinaryTree(items):
    n = len(items)

    if n == 0:
        return None

    def inner(index: int = 0) -> TreeNode:
        if n <= index or items[index] is None:
            return None

        node = TreeNode(items[index])
        node.left = inner(2 * index + 1)
        node.right = inner(2 * index + 2)
        return node

    return inner()


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