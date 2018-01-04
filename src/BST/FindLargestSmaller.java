package BST;

import testtools.TreeNode;

/**
 * Created by guoxi on 12/27/17.
 */
public class FindLargestSmaller {
    public static void main (String[] args) {
        TreeNode test = TreeNode.generateTree("8,4,15,1,7,9,20,x,x,5,x,x,12,17,25");
        FindLargestSmaller testCase = new FindLargestSmaller();
        System.out.print(testCase.findLargestSmaller(test, 10));
    }

    public Integer findLargestSmaller(TreeNode root, int target) {
        if (root == null) {
            return null;
        }
        Integer ans = null;
        while(root != null) {
            // case 1
            if (root.val >= target) {
                root = root.left;
            } else {
                ans = root.val;
                root = root.right;
            }
        }
        return ans;
    }
}
