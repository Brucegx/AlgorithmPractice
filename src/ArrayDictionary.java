/**
 * Created by guoxi on 6/1/17.
 */
public class ArrayDictionary implements Dictionary {
    final private static int[] nums = new int[]{ 1, 1, 3, 5, 9, 11, };

    @Override
    public Integer get(int idx) {
        if (idx < 0 || idx >= nums.length) { return null; }
        return nums[idx];
    }
}