import java.util.*;

/**
 * Created by guoxi on 1/22/18.
 */

public class MusicPlayer {
    public static void main (String[] args) {
        String[] case1 = new String[]{"a","b","c","d","e"};
        Music[] testcase = testcaseTran(case1);
        MusicPlayer test = new MusicPlayer(testcase, 3);
        for (int i = 0; i < 15; i++) {
            System.out.println("The " + i +"th song is: " + test.palyRandom().info);
        }
    }
    static class Music {
        String info;
        Music(String info) {
            this.info = info;
        }
    }

    class Entry<Music, Integer> {
        public Music music;
        public Integer index;
        Entry(Music music, Integer index) {
            this.music = music;
            this.index = index;
        }
    }
    public static Music[] testcaseTran (String[] test) {
        Music[] testcase = new Music[test.length];
        for (int i = 0; i < testcase.length; i++) {
            testcase[i] = new Music(test[i]);
        }
        return testcase;
    }

    public Entry[] playList;
    private Deque<Entry> played = new LinkedList<>();
    int playedSize;
    public MusicPlayer (Music[] musics, int k) {
        // step 1, init put music into EntrySet<Music, ArrayIndex>
        playList = init(musics);
        playedSize = k;
    }

    public Music palyRandom() {
        int len = playList.length;
        Random rand = new Random();
        // randomAccess' seed is [0, len - played.size())

        // case 1 if the number of music which already played is still smaller than k
        // we need put music into deque and then swap it into last
        // case 2 if we already played k - 1 songs, we get next song first then nextSong become plyaed one
        // and we need to put it into deque's head and poll tail (first kth played song) out
        // then swap it and update entry;
        int index = rand.nextInt(len - played.size());
        Music nextSong = (Music) playList[index].music;
        played.offerFirst(playList[index]);
        if (played.size() == playedSize) {
            Entry returnSong = played.pollLast();
            swap(returnSong, playList[index]);
        } else {
            swap(playList[index], playList[len - played.size()]);
        }
        return nextSong;
    }

    private void swap (Entry<Music, Integer> a, Entry<Music, Integer> b) {
        int ai = a.index;
        int bj = b.index;
        // swap entry in playlist array
        Entry temp = playList[ai];
        playList[ai] = playList[bj];
        playList[bj] = temp;

        // update entry.index
        Integer tempIndex = a.index;
        a.index = b.index;
        b.index = tempIndex;
        return;
    }


    private Entry[] init (Music[] musics) {
        Entry[] playList = new Entry[musics.length];
        for (int i = 0; i < musics.length; i++) {
            playList[i] = new Entry(musics[i], i);
        }
        return playList;
    }
}
