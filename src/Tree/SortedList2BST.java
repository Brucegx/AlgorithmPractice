//package Tree;
//
//import testtools.ListNode;
//import testtools.TreeNode;
//
///**
// * Created by guoxi on 12/11/17.
// */
//
////first we need use properties of BST VS sortedList
////we can get sorted list from BST by inorder
////we also can construct BST by inorder
////
////following we use currentNode because inorder, every next node is next tree root;
//public class SortedList2BST {
//    public static void main(String[] args) {
//
//    }
//
//    public TreeNode sortedList2BST(ListNode head) {
//        // first we get list length by getlenth function
//        int len = getLen(head);
//        return helper(0, len - 1);
//    }
//
//    ListNode curNode = head;
//    private TreeNode helper(int start, int end) {
//        if (start > end) {
//            return null;
//        }
//
//        int mid = start + (end - start) / 2;
//        TreeNode left = helper(start, mid - 1);
//        TreeNode root = new TreeNode(curNode.val);
//        curNode = curNode.next;
//        TreeNode right = helper(mid + 1, end);
//        root.left = left;
//        root.right = right;
//        return root;
//    }
//
//    private int getLen (ListNode head) {
//        int len = 1;
//        while(head.hasNext()) {
//            len++;
//        }
//        return len;
//    }
//}
