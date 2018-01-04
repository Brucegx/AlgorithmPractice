package testtools;

import java.util.Arrays;

/**
 * Created by guoxi on 8/7/17.
 */
public class MyHashMap<K, V> {
    public static class Node<K, V> {
        //there we use static class since:
        // very closely boned to hashmap class
        // we need to  access this class outside from hashmap class
        private final K key;
        private V value;
        Node<K,V> next;

        public Node(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public void setValue(V value) {
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }
    }
    // we should put this node class to hashmap as an inner class, because we will use it only in map. It will be more
    // reasonable and pretty
    private Node<K,V>[] array;
    private int size;
    private final static int DEFAULT_INITIAL_CAPCITY = 17;
    private final static float DEFAULT_LOAD_FACTOR = 0.7f;
    private float loadFactor; // determine when to rehash

    public MyHashMap() {
        this(DEFAULT_INITIAL_CAPCITY, DEFAULT_LOAD_FACTOR);
    }
    // why?

    public MyHashMap(int cap, float loadFactor) {
        if (cap <= 0) {
            throw new IllegalArgumentException("car can not be negative");
        }
        this.array = (Node<K, V>[]) (new Node[cap]);
        this.size = 0;
        this.loadFactor = loadFactor;
    }

    public V put(K key, V value) {
        // insert and update
        int index = getIndex(key);
        Node<K, V> head = array[index];
        //Node<K, V> node = head;
        while (head != null) {
            if (equalsKey(head.getKey(), key)) {
                V preValue = head.getValue();
                head.setValue(value);
                return preValue;
            }
            head = head.next;
        }
        Node<K, V> newHead = new Node<>(key, value);
        newHead.next = array[index];
        array[index] = newHead;// new head is here
        size++;
        if (size > array.length * DEFAULT_LOAD_FACTOR) {
            reHash();
        }
        return null;
    }

    public V remove(K key) {
        int index = getIndex(key);
        Node<K, V> head = array[index];
        Node<K, V> prev = null;
        while (head != null) {
            if(equalsKey(head.getKey(), key)) {
                if (prev == null) {
                    // this is head node
                    array[index] = head.next;
                } else {
                    prev.next = head.next;
                    // prev node jump head node to head.next
                }
                size--;
                return head.getValue();
            }
            prev = head;
            head = head.next;
        }
        return null;
    }

    public V get(K key) {
        int index = getIndex(key);
        Node<K, V> head = array[index];
        while (head != null) {
            if (equalsKey(head.getKey(), key)) {
                return head.getValue();
            }
            head = head.next;
        }
        return null;
    }

    public boolean containsKey(K key) {
        if (isEmpty()) {
            return false;
        }
        int index = getIndex(key);
        Node<K, V> head = array[index];
        while (head != null) {
            if (equalsKey(head.getKey(), key)) {
                return true;
            }
            head = head.next;
        }
        return false;
    }

    public boolean containsValue(V value) {
        if(isEmpty()) {
            return false;
        }
        for (Node<K, V> node : array) {
            while (node != null) {
                if (equalsValue(node.getValue(), value)) {
                    return true;
                }
                node = node.next;
            }
        }
        return false;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void clear() {
        Arrays.fill(array, null);
        size = 0;
    }

    private int getIndex(K key) {
        if (key == null) {
            return 0;
        }
        return (key.hashCode() & 0x7fffffff) % array.length;
        // 0x7fffffff is 01111..11111 & can translate to positive
        // because there is not negative slot index but % can get negative remainder.
    }

    private boolean equalsKey(K key1, K key2) {
        return key1 == null && key2 == null || key1 != null && key1.equals(key2);
    }

    private boolean equalsValue(V v1, V v2) {
        return v1 == null && v2 == null || v1 != null && v1.equals(v2);
    }

    private void reHash() {
        // resize first
        int newSize = DEFAULT_INITIAL_CAPCITY * 2;
        // since we need array.length in getIndex so we need update array
        // use an new array to maintain old array
        Node<K, V>[] oldArray = array;
        array = (Node<K, V>[]) (new Node[newSize]);
        for (Node<K, V> e : oldArray) {
            while (e != null) {
                Node<K, V> next = e.next;

                int i = getIndex(e.getKey());
                e.next = array[i];
                array[i] = e;

                e = next;
                // add node from head of new array
            }
        }
    }
}
