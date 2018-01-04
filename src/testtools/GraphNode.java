package testtools;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by guoxi on 8/28/17.
 */
public class GraphNode {
    public int key;
    public List<GraphNode> neighbors;
    public GraphNode(int key) {
        this.key = key;
        this.neighbors = new ArrayList<GraphNode>();
        }
    }