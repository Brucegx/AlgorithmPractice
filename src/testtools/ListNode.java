package testtools;

/**
 * Created by guoxi on 6/26/17.
 */
public class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) {
            this.val = val;
            next = null;
        }
        public void add(int value){
            next = new ListNode(value);
        }
        public static ListNode generate (int[] array) {
            ListNode cur = new ListNode(array[0]);
            ListNode head = cur;
            for (int i = 1; i < array.length; i++) {
                ListNode node = new ListNode(array[i]);
                cur.next = node;
                cur = cur.next;
            }
            return head;
        }

    public boolean hasNext() {
        return next != null;
    }
}
