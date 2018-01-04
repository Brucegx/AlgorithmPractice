package testtools;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

/**
 * Created by guoxi on 7/4/17.
 */
public class TreeNode {
    public int val;
    public TreeNode left;
    public TreeNode right;
    public TreeNode pre;
    public TreeNode head;

    private static String NULL = "x";
    private static String SPELITER = ",";
    public TreeNode(int x) {
        this.val = x;
    }

    public TreeNode() {

    }
    // generate by level order
    public static TreeNode generateTree(String input) {
        if (input == null || input.length() == 0) {
            return null;
        }
        String[] set = input.split(SPELITER);
        Deque<TreeNode> queue = new LinkedList<>();
        int i = 0;
        TreeNode ans = new TreeNode(parse(set[0]));
        queue.offerFirst(ans);
        while (i * 2 + 2 <= set.length) {
            TreeNode root = queue.pollLast();
            if (!set[i * 2 + 1].equals(NULL)) {
                root.left = new TreeNode(parse(set[i * 2 + 1]));
            } else {
                root.left = null;
            }
            if (i * 2 + 3 <= set.length && !set[i * 2 + 2].equals(NULL)) {
                root.right = new TreeNode(parse(set[i * 2 + 2]));
            } else {
                root.right = null;
            }
            queue.offerFirst(root.left);
            queue.offerFirst(root.right);
            i++;
        }
        return ans;
    }

    private static int parse (String input) {
        int val = 0;
            for (int i = 0; i < input.length(); i++) {
                val = val * 10 + Character.getNumericValue(input.charAt(i));
        }
        return val;
    }

    public static void main(String[] arg) {
        System.out.print(generateTree("1,2,3,4,5,6,7"));
    }

    //TODO LIST
    //1) refine by input with x3 represent x x x
    //2) add reconstruct by preOrder
}
