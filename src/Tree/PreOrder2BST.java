package Tree;

import testtools.TreeNode;

/**
 * Created by guoxi on 12/12/17.
 */

//comment:
//reconstruct a Tree we need know two key point:
//usually we construct it by recursion so,
//first we need know where is root
//second we need know the boundary
//
//PreOrder2BST we can use one preOrder to construct it because BST nataurally has Inorder which property helps us
//to find the boundary
//what we need to do is taht pass the boundary to next level
//AND THE MOST IMPORTANT is we must be clear what is the boundary in current level

public class PreOrder2BST {
    public static void main(String[] args) {
        PreOrder2BST test = new PreOrder2BST();
        System.out.print(test.isBST(new int[] {5,1,3,6,2}, Integer.MIN_VALUE, Integer.MAX_VALUE));
    }

    public TreeNode reconstruct(int[] pre, int start, int end) {
        if (start > end) {
            return null;
        }

        TreeNode root = new TreeNode(pre[start]);
        //if we use binary search way to find mid, it is not a easy binary search we need do more job to implement it
//        int leftEnd = findMid(pre, root.val);
        int leftEnd = start + 1;
        while (leftEnd <= end && pre[leftEnd] < pre[end]) {
            leftEnd++;
        }
        root.left = reconstruct(pre, start + 1, leftEnd - 1);
        root.right = reconstruct(pre, leftEnd, end);
        return root;
    }
    int preIndex = 0;
    public TreeNode recursion(int[] pre, int rootVal) {
        if (preIndex ==  pre.length || pre[preIndex] > rootVal) {
            return null;
        }
        TreeNode root = new TreeNode(pre[preIndex++]);
        root.left = recursion(pre, root.val);
        root.right = recursion(pre, rootVal);
        return root;
    }

    public Boolean isBST(int[] pre, int min, int max) {
        if (preIndex == pre.length || pre[preIndex] > max) {
            return true;
        }
        int curVal = pre[preIndex++];
        if (curVal < min) {
            return false;
        }
        return isBST(pre, min, curVal) && isBST(pre, curVal, max);
    }
}
