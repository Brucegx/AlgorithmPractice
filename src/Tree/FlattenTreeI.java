package Tree;

import testtools.TriTreeNode;

/**
 * Created by guoxi on 12/8/17.
 */
public class FlattenTreeI {
    public static void main(String[] args) {
        TriTreeNode input = TriTreeNode.generator("1,2,3,4,5,6,x,x,7,x,x,x,x,x,x,x,x,x,x,8,9,10");
        FlattenTreeI test = new FlattenTreeI();
        TriTreeNode ans = test.flattenTreePost(input);
        while(ans != null) {
            System.out.print(ans.val);
            ans = ans.c3;
        }
    }

    public TriTreeNode flattenTreePre(TriTreeNode root) {
        if (root == null) {
            return null;
        }
        TriTreeNode c1Tail = flattenTreePre(root.c1);
        TriTreeNode c2Tail = flattenTreePre(root.c2);
        TriTreeNode c3Tail = flattenTreePre(root.c3);

        TriTreeNode tail = root;
        if (c1Tail != null) {
            tail = c1Tail;
            tail.c3 = root.c2;
        }
        if (c2Tail != null) {
            tail = c2Tail;
            tail.c3 = root.c3;
        }
        if (c3Tail != null) {
            tail = c3Tail;
        }

        if(root.c1 != null) {
            root.c3 = root.c1;
        } else if (root.c2 != null) {
            root.c3 = root.c2;
        }

        root.c1 = root.c2 = null;
        return tail;
    }

    public TriTreeNode flattenTreePost (TriTreeNode root) {
        if (root == null) {
            return null;
        }
        return helper(root);
    }

    private TriTreeNode helper(TriTreeNode root) {
        TriTreeNode head = root;
        if(root.c3 != null) {
            head = connect(root.c3, head, helper(root.c3));
        }
        if(root.c2 != null) {
            head = connect(root.c2, head, helper(root.c2));
        }
        if(root.c1 != null) {
            head = connect(root.c1, head, helper(root.c1));
        }
        root.c3 = root.c2 = root.c1 = null;
        return head;
    }

    private TriTreeNode connect(TriTreeNode newTail, TriTreeNode head, TriTreeNode newHead) {
        newTail.c3 = head;
        return  newHead;
    }
}