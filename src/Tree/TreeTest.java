package Tree;

import testtools.TreeNode;

import java.util.LinkedList;
import java.util.List;

/**
 * Created by guoxi on 12/7/17.
 */
public class TreeTest {
    // TODO
//    input is a string array
//    first we need to transfer it to tree one by one
//    second add them to list for testing later
//    third one more print method to print answer;
    public List<TreeNode> transfer(String[] input) {
        List<TreeNode> list = new LinkedList<>();
        for (String s : input) {
            list.add(TreeNode.generateTree(s));
        }
        return list;
    }
}
