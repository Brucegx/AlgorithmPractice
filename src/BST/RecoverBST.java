package BST;

import testtools.TreeNode;

/**
 * Created by guoxi on 12/30/17.
 */
public class RecoverBST {
    public static void main(String[] args) {
        TreeNode test = TreeNode.generateTree("10,5,15,2,7,12,17,1,3,11,8,6,14,16,19");
        TreeNode test2 = TreeNode.generateTree("2,x,1");
        RecoverBST testcase = new RecoverBST();
        testcase.recoverTree(test2);
        System.out.print(State.node1.val);
        System.out.print(State.node2.val);
    }
    static class State {
        static TreeNode node1;
        static TreeNode node2;
        static boolean foundFirst = false;
    }

    public void recoverTree(TreeNode root) {
        if (root == null) {
            return;
        }
        helper(root, null);
        if (State.foundFirst) {
            swap(State.node1, State.node2);
        }
        return;
    }

    private TreeNode helper(TreeNode root, TreeNode pre) {
        // base case
        if (root == null) {
            return null;
        }

        TreeNode preLeft = helper(root.left, pre);
        // step one: choose which is lattest node
        TreeNode preNode = preLeft == null ? pre : preLeft;
        if (preNode != null && preNode.val > root.val) {
            if (!State.foundFirst) {
                State.node1 = preNode;
                State.node2 = root;
                State.foundFirst = true;
            } else {
                State.node2 = root;
            }
        }
        TreeNode preRight = helper(root.right, root);

        if (preRight != null) {
            return preRight;
        }
        return root;
    }

    private void swap(TreeNode node1, TreeNode node2) {
        int temp = node1.val;
        node1.val = node2.val;
        node2.val = temp;
        return;
    }
}
