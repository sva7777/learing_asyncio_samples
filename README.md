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
To debug locally it need convent input data in specified leetcode format into binary tree
This can be done using function ConvertListToBinaryTree()
Code should be like this
```
root = [3,9,20,null,null,15,7]  
root= ConvertListToBinaryTree(root)  
```

Same for linked list. 
Leetcode format to represent linked list: head = [1,2,3,4,5]
Function ConvertListToLinkedList  can be used to convert specified list into linked list

```
head=[1,2,3,4,5]  
head = ConvertListToLinkedList(head)
```
