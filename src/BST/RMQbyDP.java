package BST;

/**
 * Created by guoxi on 1/2/18.
 */

//range minimum query (RMQ) solves the problem of
//finding the minimal value in a sub-array of an array of comparable objects
public class RMQbyDP {
    public static void main(String[] args) {
        int[]test = new int[]{1,2,5,8,4,3,5,6,10,3,5,31,43,1,2,3,5,11,1};
        RMQbyDP testcase = new RMQbyDP();
        System.out.print(testcase.findMax(test,13,18));
    }
    public int findMax(int[] range, int start, int end) {
        //init fullfill dp
        int height = findK(range.length);
        int width = range.length;
        int[][] dp = new int[height][width];
        for(int k = 0; k < height; k++) {
            for (int i = 0; i < width; i++) {
                if (k == 0) {
                    dp[k][i] = range[i];
                } else {
                    if (i + (Math.pow(2, k -  1)) < width) {
                        dp[k][i] = Math.max(dp[k - 1][i],dp[k - 1][i + (int) Math.pow(2, k -  1)]);
                    } else {
                        dp[k][i] = Math.max(dp[k - 1][i], dp[k - 1][end - (int) Math.pow(2, k - 1)]);
                    }
                }
            }
        }

        // querey
        int powerK =findK(end - start + 1);
        int startMax = dp[powerK][start];
        int endMax = dp[powerK][end - (int) Math.pow(2, powerK) + 1];
        return Math.max(startMax, endMax);
    }

    private int findK (int bound) {
        int k = 0;
        int i = 1;
        while (i < bound) {
            i = i * 2;
            k++;
        }
        return k - 1;
    }
}
