package Tree;


import testtools.TreeNode;

import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by guoxi on 12/6/17.
 */

//version 1 is BFS to find it is complete tree
//version 2: using recursion by perfect and complete tree;
public class IsCompleteTree {
    public static void main(String[] args) {
        IsCompleteTree test = new IsCompleteTree();
        List<TreeNode> testList = new LinkedList<>();
        TreeNode testNodeYes = TreeNode.generateTree("1,2,3,4,5,6,7");
        TreeNode testNodeNo = TreeNode.generateTree("1,2,3,x,5,6");
        TreeNode testNode2 = TreeNode.generateTree("1,x,2");
        TreeNode testNode1 = TreeNode.generateTree("1");
        TreeNode testC1 = TreeNode.generateTree("1,2,3,4,5");
        TreeNode testC2 = TreeNode.generateTree("1,2,3,4");
        TreeNode testC3 = TreeNode.generateTree("1,2,3,4,5,6");
        testList.add(testNodeYes);
        testList.add(testNodeNo);
        testList.add(testNode2);
        testList.add(testNode1);
        testList.add(testC1);
        testList.add(testC2);
        testList.add(testC3);
        for (TreeNode node : testList) {
            System.out.println(test.recursion(node));
        }
    }

    public boolean BFS (TreeNode root) {
        if (root == null) {
            return true;
        }

        Deque<TreeNode> queue = new LinkedList<>();
        queue.offerFirst(root);
        boolean flag = false;
        while (!queue.isEmpty()) {
            TreeNode cur = queue.pollLast();

            // check left child
            if (cur.left == null) {
                flag = true;
            } else if (flag) {
                return false;
            } else {
                queue.offerFirst(cur.left);
            }

            if (cur.right == null) {
                flag = true;
            } else if (flag) {
                return false;
            } else {
                queue.offerFirst(cur.right);
            }
        }
        return true;
    }

    class ReturnType {
        boolean isComplete;
        boolean isPerfect;
        int height;

        public ReturnType (boolean isComplete, boolean isPerfect, int height){
            this.height = height;
            this.isComplete = isComplete;
            this.isPerfect = isPerfect;
        }
    }

    public boolean recursion (TreeNode root) {
        if (root == null) {
            return true;
        }
        return isComplete(root).isComplete;
    }

    private ReturnType isComplete(TreeNode root) {
        if (root == null) {
            return new ReturnType(true, true, 0);
        }

        ReturnType left = isComplete(root.left);
        ReturnType right = isComplete(root.right);

        if (left.isPerfect && right.isPerfect && left.height == right.height) {
            return new ReturnType(true, true, left.height + 1);
        } else if (left.isComplete && right.isPerfect && left.height == right.height + 1 ||
                left.isPerfect && right.isComplete && left.height == right.height) {
            return new ReturnType(true, false, Math.max(left.height, right.height) + 1);
        }
        return new ReturnType(false, false, Math.max(left.height, right.height) + 1);
    }
}
