package Tree;

import testtools.TreeNode;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by guoxi on 12/11/17.
 */
public class ReconstructTree {
    public static void main (String[] args) {
        int[] pre = new int[] {2,1,3,4,5,6,7,8,9};
        int[] in = new int[] {3,1,5,4,6,2,8,7,9};
        ReconstructTree test = new ReconstructTree();
        List<Integer> postOrder = new ArrayList<>();
        TreeNode ans = test.recursion(pre, in, 0, postOrder);
        System.out.print(ans.right.left.val);
        for(int i = 0; i < postOrder.size(); i++) {
            System.out.print(postOrder.get(i));
        }
    }

    int preIndex = 0;
    int inIndex =0;
    public TreeNode recursion (int[] pre, int[] in, int rootVal, List<Integer> postOrder) {
        if (preIndex == pre.length || in[inIndex] == rootVal) {
            return null;
        }

        TreeNode root = new TreeNode(pre[preIndex]);
        preIndex++;
        root.left = recursion(pre, in, root.val, postOrder);
        inIndex++;
        root.right = recursion(pre, in, rootVal, postOrder);
        postOrder.add(root.val);
        return root;
    }
}
