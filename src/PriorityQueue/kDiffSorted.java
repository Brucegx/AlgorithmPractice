package PriorityQueue;

import testtools.PriorityQueue;

/**
 * Created by guoxi on 1/14/18.
 */
public class kDiffSorted {
    public static void main (String[] args) {
        int[] test = new int[] {3,2,1,5,4,6};
        kDiffSorted testCase = new kDiffSorted();
        test = testCase.kDiffSorted(test, 2);
        for (int i : test) {
            System.out.print(i);
        }
    }

    public int[] kDiffSorted(int[] array, int k) {
        if (array == null || array.length == 0) {
            return array;
        }

        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k + 1);
        for (int i = 0; i <= k; i++) {
            minHeap.offer(array[i]);
        }

        for (int i = 0; i < array.length; i++) {
            array[i] = minHeap.poll();
            if (i + k + 1 < array.length) {
                minHeap.offer(array[i + k + 1]);
            }
        }
        return array;
    }
}
