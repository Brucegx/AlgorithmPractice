import java.util.*;

/**
 * Created by guoxi on 2/2/18.
 */
public class WordLadderII {
    public static void main(String[] arg) {
        WordLadderII test = new WordLadderII();
        List<String> testcase = new ArrayList<>();
        //"dog","lot","log","cog"
        String[] a = {"ted","tex","red","tax","tad","den","rex","pee"};
        for (String s : a){
            testcase.add(s);
        }
        List<List<String>> res = test.findLadders("red", "tax", testcase);
        for (List<String> list : res) {
            System.out.println("");
            for (String s : list) {
                System.out.print(s +" => ");
            }
        }
    }

    public List<List<String>> findLadders(String beginWord, String endWord, List<String> wordList) {
        List<List<String>> res = new ArrayList<>();
        List<String> path = new ArrayList<>();
        Set<String> dict = new HashSet<>();
        Set<String> visited = new HashSet<>();
        Map<String, Integer> ladder = new HashMap<>();
        Map<String, List<String>> map = new HashMap<>();
        Deque<String> queue = new LinkedList<>();
        // sanity check
        if (wordList == null || wordList.size() == 0) {
            return res;
        }

        // init state
        // setup dict
        for (String s : wordList) {
            dict.add(s);
        }

        // if endword is not in the dict return res;
        if(!dict.contains(endWord)) {
            return res;
        }

        ladder.put(beginWord, 0);
        queue.offer(beginWord);
        map.put(beginWord, new ArrayList<>());
        visited.add(beginWord);

        int step = 0;// 0 / 1
        int min = Integer.MAX_VALUE;
        // construct a shorest path grapgh by Djiskla
        while(!queue.isEmpty()) {
            int size = queue.size();
            // in same level
            for (int i = 0; i < size; i++) {
                String cur = queue.poll();
                for(int index = 0; index < cur.length(); index++) {
                    for (int j = 0; j < 26; j++) {
                        //update word a-z => newWord
                        char[] oldWord = cur.toCharArray();
                        oldWord[index] = (char) (j + 'a');
                        String newWord = String.valueOf(oldWord);
                        if (!newWord.equals(cur) && dict.contains(newWord)
                                && (!ladder.containsKey(newWord) || ladder.get(newWord) > step)) {
                            ladder.put(newWord, step + 1);
                            visited.add(newWord);
                            map.get(cur).add(newWord);
                            map.put(newWord, new ArrayList<>());
                            queue.offer(newWord);
                        }// after that we update the shortest path and graph
                        if (newWord.equals(endWord)) {
                            min = min > step ? step + 1 : min;
                        }
                    }
                }
            }
            step++;
        }// after that we construct all graph

        // step 2 traverse graph DFS
        if (min == Integer.MAX_VALUE) {
            return res;
        } else {
            findPath(res, beginWord, endWord, path, map);
        }
        return res;
    }

    private void findPath(List<List<String>> res, String curWord, String endWord,
                          List<String> path, Map<String, List<String>> map) {
        // base case
        if (curWord.equals(endWord)) {
            res.add(new ArrayList(path));
            return;
        }

        for (String s : map.get(curWord)) {
            path.add(s);
            findPath(res, s, endWord, path, map);
            path.remove(path.size() - 1);
        }
        return;
    }
}
