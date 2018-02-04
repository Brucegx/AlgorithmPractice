import java.util.*;

import javafx.util.Pair;
import testtools.*;
import testtools.PriorityQueue;

public class Solution {

    public void preorder(TreeNode root, List<Integer> res) {
        if (root == null) {
            return;
        }

        res.add(root.val);
        preorder(root.left, res);
        preorder(root.right, res);
        return;
    }

    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordDict = new HashSet<>();
        Set<String> visited = new HashSet<>();
        Deque<String> queue = new LinkedList<>();
        int res = -1;

        if (wordList == null || wordList.size() == 0) {
            return res;
        }
        // preparation
        for(String s : wordList) {
            wordDict.add(s);
        }

        // if the endword is not in list we will return immediatly
        if(!wordDict.contains(endWord)){
            return res;
        }
        res = 1;
        queue.offer(beginWord);
        while(!queue.isEmpty()) {
            int size = queue.size();
            for(int i = 0; i < size; i++) {
                String cur = queue.poll();
                if (cur.equals(endWord)) {
                    return res;
                }
                for (int j = 0; j < cur.length(); j++) {
                    for (int m = 0; m < 26; m++) {
                        String newStr = change(cur, j, m);
                        //System.out.print(newStr);
                        if(wordList.contains(newStr) && !visited.contains(newStr)) {
                            queue.offer(newStr);
                            visited.add(newStr);
                        }
                    }
                }
            }
            res++;
        }
        return -1;
    }

    private String change(String cur, int index, int m) {
        char[] oldStr = cur.toCharArray();
        char reChar = (char) (m + 'a');
        oldStr[index] = reChar;
        //System.out.print(String.valueOf(oldStr));
        return String.valueOf(oldStr);
    }

    public TreeNode construceByPre(int[] input, int start, int end) {
        // base case
        if (start > end) {
            return null;
        }
        TreeNode root = new TreeNode(input[start]);
        int mid = findMid(input, root.val);
        root.left = construceByPre(input, start + 1, mid - 1);
        root.right = construceByPre(input, mid, end);
        return root;
    }

    private int findMid(int[] input, int target) {
        // find the smallest larger than target;
        return -1;
    }

    public TreeNode construceByPreII(int[] input, int[] index, int leftBound, int rightBound) {
        // base case
        if (index[0] == input.length) {
            return null;
        }
        TreeNode root = new TreeNode(input[index[0]++]);
        if ( index[0] < input.length && input[index[0]] < root.val && input[index[0]] > leftBound) {
            root.left = construceByPreII(input, index, leftBound, root.val);
        }
        if (index[0] < input.length && input[index[0]] > root.val && input[index[0]] < rightBound) {
            root.right = construceByPreII(input, index, root.val, rightBound);
        }
        return root;
    }
    class TrieNode {
        int count = 0;
        TrieNode[] children;
        boolean isEnd;
        char val;
        TrieNode(char c) {
            this.val = c;
            children = new TrieNode[26];
        }
    }

    public void insert(String input, TrieNode root) {
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if(root.children[c - 'a'] != null) {
                root.children[c - 'a'].count++;
            } else {
                root.children[c - 'a'] = new TrieNode(c);
                root.children[c - 'a'].count++;
            }
        }
    }

    public List<String> search(TrieNode root) {
        List<String> ans = new LinkedList<>();
        StringBuilder sb = new StringBuilder();
        search(root, ans, sb);
        return ans;
    }

    private void search(TrieNode root, List<String> ans, StringBuilder sb) {
        for (TrieNode t : root.children) {
            if (t.count == 1) {
                sb.append(t.val);
                ans.add(sb.toString());
                sb.deleteCharAt(sb.length() - 1);
            } else {
                sb.append(t.val);
                search(t, ans, sb);
                sb.deleteCharAt(sb.length() - 1);
            }
        }
        return;
    }

    private boolean searchWildCard(TrieNode root, char[] input, int index) {
        if (index == input.length - 1 && root.isEnd &&
                (input[index] == '*' || root.children[input[index] - 'a'] != null)) {
            return true;
        }
            char c = input[index];
            if (c != '*' && root.children[c - 'a'] == null) {
                return false;
            } else if (c != '*') {
                return searchWildCard(root.children[c - 'a'], input, index + 1);
            } else {
                for(TrieNode n : root.children) {
                    if (searchWildCard(n, input, index + 1)) {
                        return true;
                    }
                }
            }
        return false;
    }
    public List<String> permutations(String set) {
        // Write your solution here.
        List<String> ans = new ArrayList<>();
        if (set == null) {
            return ans;
        }
        char[] input = set.toCharArray();
        permutation(input, 0, ans);
        return ans;
    }
    public String decodeString(String s) {
        if (s == null) {
            return null;
        }

        Deque<Integer> count = new LinkedList<>();
        Deque<String> result = new LinkedList<>();
        int i = 0;
        result.push("");
        while (i < s.length()) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                int start = i;
                while (s.charAt(i + 1) >= '0' && s.charAt(i + 1) <= '9') {
                    i++;
                }
                count.push(Integer.parseInt(s.substring(start, i + 1)));
            } else if (ch == '[') {
                i++;
                continue;
//                result.push("");
            } else if (ch == ']') {
                int times = count.poll();
                String cur = result.poll();
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < times; j++) {
                    sb.append(cur);
                }
                result.push(result.poll() + sb.toString());
            } else {
                result.push(result.poll() + ch);
            }
            i++;
        }
        return result.poll();
    }

    private void permutation(char[] input, int index, List<String> ans) {
        // base case
        if (index == input.length) {
            ans.add(new String(input));
            return;
        }

        Set<Character> used = new HashSet<Character>();
        for (int i = index; i < input.length; i++) {
            if (used.add(input[i])) {
                swap(input, index, i);
                permutation(input, index + 1, ans);
                swap(input, index, i);
            }
        }
    }

    private void swap(char[] input, int i, int j) {
        char temp = input[i];
        input[i] = input[j];
        input[j] = temp;
    }
    public String minWindow(String s, String t) {
        HashMap<Character, Integer> tm = new HashMap<>();
        HashMap<Character, Integer> sm = new HashMap<>();
        int counter = 0;
        char[] sArray = s.toCharArray();

        // traverse t first;
        for (Character c : t.toCharArray()) {
            if (tm.containsKey(c)) {
                tm.put(c,tm.get(c) + 1);
            } else {
                tm.put(c, 1);
            }
        }
        int start = -1;
        int end = 0;
        int globalMin = Integer.MAX_VALUE;
        String res = null;
        counter = tm.size();

        // traverse s;
        while (end < s.length()) {
            while (counter > 0 && end <s.length()) {
                char cur = sArray[end];
                // put S[end] to sm first whatever
                if (sm.containsKey(cur)) {
                    sm.put(cur, sm.get(sArray[end]) +1);
                } else {
                    sm.put(cur, 1);
                }

                // if tm has it
                if (tm.containsKey(cur) && sm.get(cur) == tm.get(cur)) {
                    counter--;
                }
                end++;
            }
            while (counter == 0 && start < s.length() - 1) {
                start++;
                char cur = sArray[start];

                // remove one from sm
                sm.put(cur, sm.get(cur) - 1);

                // check if it is valid
                if (tm.containsKey(cur) && sm.get(cur) < tm.get(cur)) {
                    counter++;
                    if (globalMin > (end - start)) {
                        globalMin = end - start;
                        res = s.substring(start, end);
                    }
                }
            }
        }
        return res;
    }

    public double median(int[] a, int[] b) {
        // write your solution here
        if (a == null || b == null) {
            return 0;
        }

        int mid = (a.length + b.length - 1) / 2;
        int ai = 0;
        int bj = 0;
        boolean even = (a.length + b.length) % 2 == 0 ? true : false;
        while (mid > 0) {
            if (ai == a.length) {
                bj += mid;
                return even ? (b[bj] + b[bj + 1]) / 2.0 : b[bj];
            } else if (bj == b.length) {
                ai += mid;
                return even ? (a[ai] + a[ai + 1]) / 2.0 : a[ai];
            } else if (a[ai] > b[bj]) {
                bj++;
            } else {
                ai++;
            }
            mid--;
        }
        if (ai == a.length) {
            return even ? (b[bj] + b[bj + 1]) / 2 : b[bj];
        } else if (bj == b.length) {
            return even ? (a[ai] + a[ai + 1]) / 2 : a[ai];
        }
        return even ? (b[bj] + a[ai]) / 2.0 : Math.min(a[ai], b[bj]);
    }

    public int[] quickSort(int[] array) {
        // Write your solution here
        if (array == null || array.length == 0) {
            return array;
        }
        quickSort(array, 0, array.length - 1);
        return array;
    }

    public double medianbyBS(int[] a, int[] b) {
        // write your solution here
        if (a == null || b == null) {
            return 0;
        }
        int mid = (a.length + b.length) / 2 + 1;
        boolean odd = (a.length + b.length) % 2 == 1 ? true : false;
        return findKthSmall(a, b, 0, 0, mid, odd);
    }

    private double findKthSmall(int[] a, int[] b, int startA, int startB, int k,
                                boolean odd) {
        // base case:
        if (startA == a.length) {
            return odd ? b[startB + k - 1] :
                    (b[startB + k - 1] + b[startB + k - 2]) / 2.0;
        } else if (startB == b.length) {
            return odd ? a[startA + k - 1] :
                    (a[startA + k - 1] + a[startA + k - 2]) / 2.0;
        } else if ( k == 1 && odd) {
            return Math.min(a[startA], b[startB]);
        } else if ( k == 1 && !odd) {
            if (a[startA] > b[startB]) {
                return (b[startB] +
                        a[startA] > b[startB - 1] ? b[startB - 1] : a[startA]) / 2.0;
            } else {
                return (a[startA] +
                        b[startB] > a[startA - 1] ? a[startA - 1] : b[startB]) / 2.0;
            }
        }

        int aHalfKSmall = startA + (k / 2) - 1 < a.length ? a[startA + k / 2 - 1]
        : Integer.MAX_VALUE;
        int bHalfKSmall = startB + (k / 2) - 1 < b.length ? b[startB + k / 2 - 1]
        : Integer.MAX_VALUE;

        if (aHalfKSmall < bHalfKSmall) {
            return findKthSmall(a, b, startA + k / 2, startB, k - k / 2, odd);
        } else {
            return findKthSmall(a, b, startA, startB + k / 2, k - k / 2, odd);
        }
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