import testtools.TreeNode;

import java.util.*;

/**
 * Created by guoxi on 1/9/18.
 */
public class getUniqueCharacter {
    Deque<Character> stack = new LinkedList<>();// stack ? Deque
    Set<Character> visited = new HashSet<>();
    public int getUnique() {
        if (stack.isEmpty()) {
            throw new NoSuchElementException();
        }
        if (visited.isEmpty()) {
            return stack.pollFirst();
        }
        while (visited.contains(stack.peek())) {
            stack.pollFirst();
        }
        return 0;
    }

    private void helper(char[] input) {
        for (int i = 0; i < input.length; i++) {
            if (visited.contains(input[i])) {
                continue;
            } else {
                stack.offerFirst(input[i]);
            }
        }
    }

    private boolean checkBT (TreeNode root) {
        if (root == null) {
            return true;
        }

        int left = getHeight(root.left);
        int right = getHeight(root.right);
        if (Math.abs(left - right) <= 1) {
            return checkBT(root.left) && checkBT(root.right);
        } else {
            return false;
        }
    }

    private int getHeight(TreeNode root) {
        return 0;
    }


}
