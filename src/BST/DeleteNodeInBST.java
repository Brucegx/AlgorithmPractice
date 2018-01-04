package BST;

import testtools.TreeNode;

/**
 * Created by guoxi on 1/1/18.
 */
public class DeleteNodeInBST {
    TreeNode pre;
    public static void main(String[] args) {
        TreeNode test = TreeNode.generateTree("5,3,6,2,4,x,7");
        DeleteNodeInBST testcase = new DeleteNodeInBST();
        testcase.deleteNode(test, 3);
    }
    public TreeNode deleteNode(TreeNode root, int key) {
        // conner case
        if (root == null) {
            return null;
        }
        TreeNode target = find(root, key);
        // if not node == key
        if (target == null) {
            return root;
        }
        pre = target;

        TreeNode smallest = findSmallest(target);
        swap(target, smallest);
        System.out.print(smallest.val);
        if(smallest.right != null) {
            pre = smallest;
            TreeNode smallest2 = findSmallest(smallest);
            swap(smallest, smallest2);
            System.out.print("smallest2 is " + smallest2.val);

            pre.right = null;
        } else {
            pre.left = null;
        }
        return root;
    }

    private TreeNode find(TreeNode root, int key) {
        // base case
        while (root != null) {
            if (root.val == key) {
                return root;
            } else if (root.val > key) {
                root = root.left;
            } else {
                root = root.right;
            }
        }
        return null;
    }

    private TreeNode findSmallest(TreeNode root) {
        TreeNode cur = root.right;
        while(cur.left != null){
            pre = cur;
            cur = cur.left;
        }
        return cur;
    }

    private void swap(TreeNode a, TreeNode b) {
        int temp = a.val;
        a.val = b.val;
        b.val = temp;
    }
}
