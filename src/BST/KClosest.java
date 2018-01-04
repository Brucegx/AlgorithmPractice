package BST;

import testtools.TreeNode;

import java.util.*;

/**
 * Created by guoxi on 12/28/17.
 */
public class KClosest {
    public static  void main(String[] args) {
        TreeNode test = TreeNode.generateTree("8,4,15,1,7,10,20,x,x,5,x,9,11,17,25");
        KClosest testcase = new KClosest();
        List<Integer> ans = testcase.closestKValues(test,4,4);
        for(int i : ans) {
            System.out.print(i);
        }

    }
    public List<Integer> closestKValues(TreeNode root, double target, int k) {
        List<Integer> ans = new ArrayList<>();
        if (root == null || k == 0) {
            return ans;
        }
        AscIterator ascIterator = new AscIterator();
        ascIterator.traverse(root, target);
        DesIterator desIterator = new DesIterator();
        desIterator.traverse(root, target);
        double smaller = target;
        double bigger = target;
        if (desIterator.hasNext()) {
            smaller = desIterator.next().val;
        }
        if (ascIterator.hasNext()) {
            bigger = ascIterator.next().val;
        }
        for (int i = 0; i < k; i++) {
            if (Math.abs(target - smaller) >= Math.abs(target - bigger)) {
                ans.add((int) bigger);
                if (desIterator.hasNext()) {
                    bigger = desIterator.next().val;
                } else {
                    bigger = Double.MAX_VALUE;
                }
            } else {
                ans.add((int) smaller);
                if (ascIterator.hasNext()) {
                    smaller = ascIterator.next().val;
                } else {
                    bigger = Double.MAX_VALUE;
                }
            }
        }
        return ans;
    }

    class AscIterator {
        Deque<TreeNode> stack = new LinkedList<>();
        public void traverse (TreeNode root, double target) {
            if (root == null) {
                return;
            }
            while (root != null) {
                if (root.val >= target) {
                    stack.push(root);
                    root = root.left;
                } else {
                    root = root.right;
                }
            }
            return;
        }

        public boolean hasNext() {
            return !stack.isEmpty();
        }

        public TreeNode next() {
            TreeNode cur = stack.pop();
            TreeNode result = cur;
            cur = cur.right;
            while (cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
            return result;
        }
    }

    class DesIterator {
        Deque<TreeNode> stack = new LinkedList<>();
        public void traverse (TreeNode root, double target) {
            if (root == null) {
                return;
            }
            while (root != null) {
                if (root.val < target) {
                    stack.push(root);
                    root = root.right;
                } else {
                    root = root.left;
                }
            }
            return;
        }

        public boolean hasNext() {
            return !stack.isEmpty();
        }

        public TreeNode next() {
            TreeNode cur = stack.pop();
            TreeNode result = cur;
            cur = cur.left;
            while (cur != null) {
                stack.push(cur);
                cur = cur.right;
            }
            return result;
        }
    }
}
