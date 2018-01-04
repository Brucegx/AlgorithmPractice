package BST;

/**
 * Created by guoxi on 1/2/18.
 */
public class RMQbySegmentTree {
    public static void main(String[] args){
        int[] test = new int[]{1,2,5,8,4,3,5,6,10,3,5,31,43,1,2,3,5,11,1};
        RMQbySegmentTree testcase = new RMQbySegmentTree();
        Node root = testcase.init(test);
        System.out.print(testcase.find(root,4,8));
    }
    class Node {
        int max;
        int from;
        int to;
        Node left;
        Node right;

        Node(int from, int to) {
            this.from = from;
            this.to = to;
        }
    }

    public Node init(int[] array) {
        return initHelper(array, 0, array.length - 1);
    }

    private Node initHelper(int[] array, int start, int end) {
        Node node = new Node(start, end);
        int mid = start + (end - start) / 2;
        if (start == end) {
            node.max = array[start];
        } else {
            node.left = initHelper(array, start, mid);
            node.right = initHelper(array, mid + 1, end);
            node.max = Math.max(node.left.max, node.right.max);
        }
        return node;
    }

    public int find(Node root, int start, int end) {
        // base case
        if (start == root.from && end == root.to) {
            return root.max;
        }
        int mid = root.from + (root.to - root.from) / 2;
        // case 1: both on left end <= mid
        // case 2: both on right start >= mid
        // case 2 mid in the middle between start and end

        if (end <= mid) {
            return find(root.left, start, end);
        } else if (start > mid) {
            return find(root.right, start, end);
        } else {
            return Math.max(find(root.left, start, mid), find(root.right, mid + 1, end));
        }
    }
}
