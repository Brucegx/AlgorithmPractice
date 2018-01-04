package testtools;

import java.util.ArrayList;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by guoxi on 12/8/17.
 */
public class TriTreeNode {
    public int val;
    public TriTreeNode c1;
    public TriTreeNode c2;
    public TriTreeNode c3;
    List<TriTreeNode> level = new ArrayList<>();

    private static String NULL = "x";
    private static String SPELITER = ",";

    public TriTreeNode(int val) {
        this.val = val;
    }


    public static TriTreeNode generator(String input) {
        if (input == null || input.length() == 0) {
            return null;
        }

        String[] set = input.split(SPELITER);
        Deque<TriTreeNode> queue = new LinkedList<>();
        TriTreeNode startRoot = new TriTreeNode(parse(set[0]));
        queue.addFirst(startRoot);
        int index = 1;
        while(!queue.isEmpty()) {
            TriTreeNode root = queue.pollLast();
            if (root != null) {
                TriTreeNode c1 = null;
                if (index >= set.length || set[index].equals(NULL)) {
                    root.c1 = c1;
                } else {
                    c1 = new TriTreeNode(parse(set[index]));
                    root.c1 = c1;
                }
                queue.addFirst(c1);
                index++;
                TriTreeNode c2 = null;
                if (index >= set.length || set[index].equals(NULL)) {
                    root.c2 = c2;
                } else {
                    c2 = new TriTreeNode(parse(set[index]));
                    root.c2 = c2;
                }
                queue.addFirst(c2);
                index++;
                TriTreeNode c3 = null;
                if (index >= set.length || set[index].equals(NULL)) {
                    root.c3 = c3;
                } else {
                    c3 = new TriTreeNode(parse(set[index]));
                    root.c3 = c3;
                }
                queue.addFirst(c3);
                index++;
                }
            }


        return startRoot;
    }

    private static int parse (String input) {
        int val = 0;
        for (int i = 0; i < input.length(); i++) {
            val = val * 10 + Character.getNumericValue(input.charAt(i));
        }
        return val;
    }
}
