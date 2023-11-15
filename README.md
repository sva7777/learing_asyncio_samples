# AsyncIO  
directory basic_samples  

# pi_calculator  
Find PI based on random generator  

# leetcode_helpers  
I solve leetcode problems.  
I solve/debug problems in mind. Sometime using a real debugger is helpful.  
Therefore, sometimes I debug my solution locally.  
There are problems related to linked list and binary tree.  
For example, input is binary tree like this  
![image](https://github.com/sva7777/learning_python/assets/102506105/74367451-e583-401b-a6c5-42f625755cad)

Leetcode specifies binary tree like `root = [3,9,20,null,null,15,7]`  
So, I need a way to convent input data in specified leetcode format into binary tree.  
This can be done using function ConvertListToBinaryTree()  

My code is like  
```
root = [3,9,20,null,null,15,7]  
root= ConvertListToBinaryTree(root)  
```

Same for linked list. I convert from leetcode format to linked list by function  
Leetcode format to represent linked list: `head = [1,2,3,4,5]`  
I use function ConvertListToLinkedList  like this  
```
head=[1,2,3,4,5]  
head = ConvertListToLinkedList(head)
```

Hope these functions will be helpful  

