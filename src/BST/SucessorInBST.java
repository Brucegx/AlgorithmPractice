package BST;

import testtools.TreeNode;

import java.util.Deque;
import java.util.LinkedList;

/**
 * Created by guoxi on 1/2/18.
 */
public class SucessorInBST {
    public static void mian (String[] args) {
        TreeNode test = TreeNode.generateTree("20,8,22,4,12,x,x,x,x,10,14");
        SucessorInBST testcase = new SucessorInBST();
        TreeNode ans = testcase.inorderSuccessor(test, test.left);
        System.out.print(ans.val);
        return;
    }
    public TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        Deque<TreeNode> successor = new LinkedList<>();
        TreeNode cur = root;
        successor.push(cur);
        while (cur != null && cur.val != p.val) {
            if (cur.val < p.val) {
                cur = cur.right;
            } else {
                successor.push(cur);
                cur = cur.left;
            }
        }
        // case1 cur == null
        if (cur == null) {
            return cur;
        }
        // case2 cur.val == p.val
        TreeNode temp = cur.right;
        while (temp != null) {
            successor.push(temp);
            temp = temp.left;
        }
        return successor.pop();
    }
}
