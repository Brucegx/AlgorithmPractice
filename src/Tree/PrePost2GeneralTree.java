package Tree;

import testtools.TriTreeNode;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by guoxi on 12/13/17.
 */

public class PrePost2GeneralTree {
    class TreeNode {
        int val;
        List<TreeNode> childrenList;
        public TreeNode (Integer val) {
            this.val = val;
            childrenList = new ArrayList<>();
        }
    }
    public static void main(String[] args) {

    }

    int preIndex = 0;
    int postIndex = 0;
    public TreeNode recursion(int[] pre, int[] post, int preIndex, int postIndex) {
        TreeNode root = new TreeNode(pre[preIndex++]);
        while(post[postIndex] != root.val) {
            root.childrenList.add(recursion(pre, post, preIndex, postIndex));
        }
        postIndex++;
        return root;
    }
}
