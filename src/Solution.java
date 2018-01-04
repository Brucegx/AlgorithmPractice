import java.util.*;

import javafx.util.Pair;
import testtools.*;

public class Solution {
    public static void main(String[] arg) {
        Solution test = new Solution();
        int[][] matrix = {{1,2,3,4},{12,13,14,5},{11,16,15,6},{10,9,8,7}};
        ListNode n = ListNode.generate(new int[]{-10,-3,0,5,9});
        TriTreeNode root = TriTreeNode.generator("1,x,2,3,x,5,6,7,8,x,10,11,12,13");
        for (int i : test.quickSort(new int[] {3,2,4,5,1,9,8,6})) {
            System.out.print(i);
        }

    }
    public int[] quickSort(int[] array) {
        // Write your solution here
        if (array == null || array.length == 0) {
            return array;
        }
        quickSort(array, 0, array.length - 1);
        return array;
    }

    private void quickSort(int[] array, int left, int right) {
        // base case
        if (left > right) {
            return;
        }

        int index = left + (int) (Math.random() * (right - left + 1));
        swap(array, index, right);
        int rightIndex = right - 1;
        int leftIndex = left;
        while (leftIndex <= rightIndex) {
            if (array[leftIndex] < array[right] && array[rightIndex] >= array[right]) {
                leftIndex++;
                rightIndex--;
            } else if (array[leftIndex] > array[right]) {
                swap(array, leftIndex, rightIndex--);
            } else if (array[rightIndex] < array[right]) {
                swap(array, leftIndex++, rightIndex);
            }
        }
        swap(array, right, leftIndex);
        quickSort(array, left,  leftIndex - 1);
        quickSort(array, leftIndex + 1, right);
        return;
    }

    private void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
        return;
    }
    public List<List<Integer>> combinations(int target, int[] coins) {
        // Write your solution here.
        List<List<Integer>> ans = new ArrayList<List<Integer>>();
        List<Integer> com = new LinkedList<>();
        helper(target, coins, com, ans, 0);
        return ans;
    }

    private void helper(int target, int[] coins, List<Integer> com,
                        List<List<Integer>> ans, int index) {
        if (index == coins.length - 1) {
            com.add(target / coins[index]);
            ans.add(new ArrayList<Integer>(com));
            com.remove(com.size() - 1);
            return;
        }

        for (int i = 0; i <= target / coins[index]; i++) {
            com.add(i);
            target = target - coins[index] * i;
            helper(target, coins, com, ans, index + 1);
            com.remove(com.size() - 1);
        }
        return;
    }

    public TreeNode str2tree(String s) {
        char[] string = s.toCharArray();
        int[] index = new int[1];
        if (string.length == 0) {
            return null;
        }
        return helper(string, index);
    }

    private TreeNode helper(char[] string, int[] index) {
        int i = index[0];
        int value;
        if (string[i] == '-') {
            value = 0 - Character.getNumericValue(string[i + 1]);
            i += 2;
        } else {
            value = Character.getNumericValue(string[i++]);
        }

        TreeNode root = new TreeNode(value);

        if (i < string.length && string[i] == '(') {
            index[0] = i + 1;
            root.left = helper(string, index);
            i = index[0];
        }
        if (string[i] == ')') {
            index[0] = i + 1;
            return root;
        }

        if (i < string.length && string[i] == '(') {
            index[0] = i + 1;
            root.right = helper(string, index);
            i = index[0];
        }
        if (string[i] == ')') {
            index[0] = i + 1;
            return root;
        }

        return root;
    }
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans = new LinkedList<List<Integer>>();
        Deque<TreeNode> queue = new LinkedList<>();
        int lastLevel = 0;
        int count = 0;
        if (queue.isEmpty()) {
            queue.offerLast(root);
            lastLevel = 1;
        }
        while(!queue.isEmpty()) {
            List<Integer> level = new LinkedList<>();
            for (int i = 0; i < lastLevel; i++) {
                count = 0;
                TreeNode cur = queue.pollFirst();
                level.add(cur.val);
                if (cur.left != null) {
                    queue.offerLast(cur.left);
                    count++;
                }
                if (cur.right != null) {
                    queue.offerLast(cur.right);
                    count++;
                }
            }
            ans.add(level);
            lastLevel = count;
        }
        return ans;
    }
        private String SPLITER = "X";
        private String NN = "#";
        // Encodes a tree to a single string.
        public String serialize(TreeNode root) {
            if (root == null) {
                return null;
            }
            StringBuilder sb = new StringBuilder();
            buildTree(root, sb);
            return sb.toString();
        }

        private void buildTree(TreeNode root, StringBuilder sb) {
            if (root == null) {
                sb.append(NN).append(SPLITER);
                return;
            }
            sb.append(root.val).append(SPLITER);
            buildTree(root.left, sb);
            buildTree(root.right, sb);
            return;
        }

        // Decodes your encoded data to tree.
        public TreeNode deserialize(String data) {
            if (data == null) {
                return null;
            }
            Deque<String> nodes = new LinkedList<>();
            String[] set = data.split(SPLITER);
            for (String s : set) {
                nodes.offerFirst(s);
            }
            return deserialize(nodes);
        }

        private TreeNode deserialize(Deque<String> nodes) {
            String cur = nodes.pollLast();
            if (cur.equals(NN)) {
                return null;
            }
            TreeNode root = new TreeNode(Integer.parseInt(cur));
            root.left = deserialize(nodes);
            root.right = deserialize(nodes);
            return root;
        }

        public boolean firstWin(int max, int target) {
            return false;
        }


}