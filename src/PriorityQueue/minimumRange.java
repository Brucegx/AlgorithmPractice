package PriorityQueue;

import testtools.PriorityQueue;

import java.util.Comparator;
//import java.util.PriorityQueue;

/**
 * Created by guoxi on 1/11/18.
 */
//k sorted arrays merge, pick one element from each of them, what is the smallers range?
//Example:
//        {1,5,11}
//        {2,4,20}
//        {6,15}
//[1,2,6] - 5
//[4,5,6] is the smallest range, should return 2;
public class MinimumRange {
    public static void main (String[] args) {
        int[][] test = {{1,5,11},{2,4,20},{6,15}};
        MinimumRange run = new MinimumRange();
        System.out.print(run.minimumRange(test));
    }

    class Cell {
        int row;
        int col;
        int val;
        public Cell(int row, int col, int val) {
            this.row = row;
            this.col = col;
            this.val = val;
        }
    }

    class MyComparator implements Comparator<Cell> {
        @Override
        public int compare(Cell c1, Cell c2) {
            return Integer.compare(c1.val, c2.val);
        }
    }
    public int minimumRange(int[][] arrays) {
        if (arrays == null || arrays.length == 0) {
            return -1;
        }
        int row = arrays[0].length;
        int col = arrays.length;

        int minRange = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        PriorityQueue<Cell> minHeap = new PriorityQueue<>(col, new MyComparator());
        // put first k elements into minHeap
        for (int i = 0; i < col; i++) {
            minHeap.offer(new Cell(i, 0, arrays[i][0]));
            max = Math.max(arrays[i][0], max);
        }

        // traverse all elements until
        while (minHeap.size() == col) {
            Cell cur = minHeap.poll();
            minRange = Math.min(minRange, max - cur.val);
            if (cur.col + 1 < arrays[cur.row].length) {
                Cell next = new Cell(cur.row, cur.col + 1, arrays[cur.row][cur.col + 1]);
                minHeap.offer(next);
                max = Math.max(max, next.val);
            }
        }
        return minRange;
    }
}
