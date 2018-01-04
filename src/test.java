import java.util.Arrays;

/**
 * Created by guoxi on 6/1/17.
 */
public class test {
    static int search(Dictionary dict, int target) {
        // Write your solution here
        //there two tasks I suppose
        //one is find the bound of right
        if (dict == null){
            return -1;
        }

        int left = 0;
        int right = 1; //conner case input has just one number

        while (dict.get(right) != null && dict.get(right) < target) {
            left = right;
            right = right * 2;
        }
        return binarySearch(dict, target, left, right);
    }

    //search target number suppose we found target in range we already confirmed.
    private static int binarySearch(Dictionary dict, int target, int left, int right) {
        while (left <= right) {//end when left equal to right => last check
            int mid = left + (right - left) / 2;
            if (dict.get(mid) < target) {
                left = mid + 1;
            }else if (dict.get(mid) == null || dict.get(mid) > target ){
                right = mid - 1; //no -1 because I suppose mid can equal to target.
            }  else if (dict.get(mid) == target){
                return mid;
            }
        }
        return -1;
    }
    public static void main(String[] args) {
        //final ArrayDictionary nums = new int[]{ 1, 1, 3, 5, 9, 11, };
        //ArrayDictionary test = new int[]{1, 3, 3, 6, 9, 9, 12, 15};
        int a = search(null, 3);
        System.out.println(a);
    }


    static class ArrayDictionary implements Dictionary {
        final private static int[] nums = new int[]{ 1, 1, 3, 5, 9, 11, };

        //public ArrayDictionary ()
        @Override
        public Integer get(int idx) {
            if (idx < 0 || idx >= nums.length) { return null; }
            return nums[idx];
        }
    }

    interface Dictionary {
        Integer get(int idx);
    }
}
