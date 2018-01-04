//package Tree;
//
//import testtools.TreeNode;
//
///**
// * Created by guoxi on 12/10/17.
// */
//
////flatten Binary Tree to double linkedlist in place, inorder
////there is two way:
////1. using pre head TreeNode;
////2. recursion
//
//public class FlattenTreeII {
//    public static void main (String[] args) {
//
//    }
//
//    public TreeNode pre;
//    public TreeNode head;
//    public void inOrder(TreeNode root) {
//        if (root == null) {
//            return;
//        }
//
//        inOrder(root.left);
//
//        //TODO
//        // change pre and cur references to double linkedlist
//
//        if (pre != null) {
//            pre.right = root;
//            root.left = pre;
//        } else {
//            pre = root;
//        }
//
//        if (head == null) {
//            head = root;
//        }
//
//        inOrder(root.right);
//        return;
//    }
//
//    class List {
//        TreeNode head;
//        TreeNode tail;
//
//        public List(TreeNode head, TreeNode tail) {
//            this.head = head;
//            this.tail = tail;
//        }
//    }
//
//    public List recursion (TreeNode root) {
//        if (root == null) {
//            return new List(null, null);
//        }
//
//        List left = recursion(root.left);
//
//        if (left.tail != null) {
//            left.tail.right = root;
//            root.left = left.tail;
//        } else {
//            left.tail = root;
//        }
//
//        if (left.head == null) {
//            head =
//        }
//    }
//}
