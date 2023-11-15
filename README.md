# AsyncIO  
directory basic_samples  

# pi_calculator  
Find PI based on random generator  

# leetcode_helpers  
Leecode site have problems related to linked list and binary tree.
For example, input is binary tree like this  
Leetcode specifies binary tree like root = [3,9,20,null,null,15,7]  
![image](https://github.com/sva7777/learning_python/assets/102506105/74367451-e583-401b-a6c5-42f625755cad)  
Leetcode specifies binary tree like `root = [3,9,20,null,null,15,7]`  
The `ConvertListToBinaryTree` function takes a list of items as input and converts it into a binary tree  

Code should be like this  
```
root = [3,9,20,null,null,15,7]  
root= ConvertListToBinaryTree(root)  
```

Same for linked list. 
Leetcode format to represent linked list: `head = [1,2,3,4,5]`  
The `ConvertListToLinkedList` function takes a list of items as input and converts it into a linked list.  
It iterates over the items in reverse order and creates a new node for each item, with the current item as its value and the previous node as its next node.  
The function returns the head of the linked list.  

Code should be like this  
```
head=[1,2,3,4,5]  
head = ConvertListToLinkedList(head)
```

Both functions are defined in the main.py file in the leetcode_helpers directory.  

