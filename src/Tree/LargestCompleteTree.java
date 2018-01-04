package Tree;

import testtools.TreeNode;

import java.util.List;

/**
 * Created by guoxi on 12/7/17.
 */
public class LargestCompleteTree {
    public static void main (String[] args) {
        TreeTest testtool = new TreeTest();
        String[] input = new String[] {"1","1,2,3,4,5,11,7,6,8,x,x,x,x,12","1,2,3,4,5,6,7,8"};
        List<TreeNode> array = testtool.transfer(input);
        LargestCompleteTree test = new LargestCompleteTree();
        for (TreeNode n : array) {
            TreeNode a = test.largestCompleteTree(n);
            System.out.println("answer: " + test.largestCompleteTree(n).val);
        }
    }

    class ReturnState {
        int height;
        boolean isComplete;
        boolean isPerfect;
        TreeNode largestNode;

        public ReturnState(int height, boolean isComplete, boolean isPerfect, TreeNode largestNode) {
            this.height = height;
            this.isComplete = isComplete;
            this.isPerfect = isPerfect;
            this.largestNode = largestNode;
        }
    }
    public TreeNode largestCompleteTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        return recursion(root).largestNode;
    }

    private ReturnState recursion(TreeNode root) {
        if (root == null) {
            return new ReturnState(0, true, true, null);
        }

        ReturnState left = recursion(root.left);
        ReturnState right = recursion(root.right);

        // judge is it a perfect
        // judge is it a complete
        // if it will not be
        // case 1 left is return leftheight, and leftnode
        // case 2 right is return rightheight and rightnode
        // case 3 neither all return max
        if (left.isPerfect && right.isPerfect && left.height == right.height) {
            return new ReturnState(left.height + 1, true, true, root);
        } else if (left.isPerfect && right.isComplete && left.height == right.height ||
                left.isComplete && right.isPerfect && left.height == right.height + 1) {
            return new ReturnState(left.height + 1, true, false, root);
        } else if (left.isComplete) {
            return new ReturnState(left.height, false, false, left.largestNode);
        } else if (right.isComplete) {
            return new ReturnState(right.height, false, false, right.largestNode);
        }
        return left.height > right.height ? new ReturnState(left.height, false, false, left.largestNode) :
                new ReturnState(right.height, false, false, right.largestNode);
    }
}
