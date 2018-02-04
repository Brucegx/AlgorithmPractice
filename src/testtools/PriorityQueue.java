package testtools;

import java.util.*;

/**
 * Created by guoxi on 1/5/18.
 */
public class PriorityQueue<E> extends AbstractQueue<E> implements java.io.Serializable {
    // define variable
    private int size = 0;
    private static final int DEFAULT_INITAL_CAPACITY = 11;
    private transient Object[] queue;
    private final Comparator<? super E> comparator;

    // create a constructor
    public PriorityQueue () {
        this(DEFAULT_INITAL_CAPACITY);
    }
    public PriorityQueue(int initialCapacity) {
        this(initialCapacity, null);
    }

    public PriorityQueue(int initialCapacity, Comparator<? super E> comparator) {
        if (initialCapacity < 1) {
            throw new IllegalArgumentException();
        }
        this.queue = new Object[initialCapacity];
        this.comparator = comparator;
    }

    // clearify opeartions
    @Override
    public Iterator<E> iterator() {
        return null;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public boolean offer(E e) {
        if (e == null) {
            throw new NullPointerException();
        }
        int i = size;
        if (i >= queue.length) {
            grow(i + 1);
        }
        if (i == 0) {
            queue[0] = e;
        } else {
            percolateUp(i, e);
        }
        size++;
        return true;
    }

    @Override
    public E poll() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        E res = (E) queue[0];
        E e = (E) queue[size - 1];
        percolateDown(0, e);
        size--;
        return res;
    }

    @Override
    public E peek() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        E res = (E) queue[0];
        return res;
    }

    public boolean add(E e) {
        return offer(e);
    }
    // methods pq need to implement for upper opeartions
    private void percolateUp(int i, E e) {
        if (comparator == null) {
            percolateUpComparable(i, e);
        } else {
            percolateUpComparator(i, e);
        }
    }
    private void percolateUpComparable(int i, E e) {
        Comparable<? super E> key = (Comparable<? super E>) e;
        queue[i] = e;
        while (i > 0) {
            int parent = (i - 1) >>> 1;
            Object p = queue[parent];
            if (key.compareTo((E) p) >= 0) { // suppose it is minHeap by defalut, when it is >= 0 means that e is bigger than parent
                break;
            } else {
                queue[i] = p;
                i = parent;
            }
            queue[i] = e;
        }
    }

    private void percolateUpComparator(int i, E e) {
        while (i > 0) {
            int parent = (i - 1) >>> 1;
            Object p = queue[parent];
            if (comparator.compare(e, (E) p) >= 0) { // suppose it is minHeap by defalut, when it is >= 0 means that e is bigger than parent
                break;
            } else {
                queue[i] = p; // if we need percolate up, we just copy parent's value to it's child and keep going to compare
                i = parent;
            }
            queue[i] = e;
        }
    }
    private void percolateDown(int i, E e) {
        if(comparator == null) {
            percolateDownComparable(i, e) ;
        } else {
            percolateDownComparator(i, e);
        }
    }

    private void percolateDownComparable(int i, E e) {
        Comparable<? super E> key = (Comparable<? super E>) e;
        int half = size >>> 1;
        while (i < half) {
            int child = (i << 1) + 1;
            Object min = queue[child];
            int rightChild = child + 1;

            if (rightChild < size && ((Comparable<? super E>) min).compareTo((E) queue[rightChild]) > 0) {
                min = queue[rightChild];
                child = rightChild;
            }// same level comparasion find minimum

            if (key.compareTo((E)min) <= 0) {
                // that is the position
                break;
            }

            queue[i] = min;
            i = child;
        }
        queue[i] = key;
    }

    private void percolateDownComparator(int i, E e) {
        int half = size >>> 1;
        while (i < half) {
            int child = (i << 1) + 1;
            Object min = queue[child];
            int rightChild = child + 1;
            if (rightChild < size && comparator.compare((E) min, (E) queue[rightChild]) > 0) {
                min = queue[rightChild];
                child = rightChild;
            }

            if (comparator.compare(e, (E) min) <= 0) {
                break;
            }

            queue[i] = min;
            i = child;
        }
        queue[i] = e;
    }
    public void heapify() {
        for (int i = (size >>> 1) - 1; i >=0; i--) {
            percolateDown(i, (E) queue[i]);
        }
    }

    private void grow(int i) {
        queue = Arrays.copyOf(queue, i * 2);
    }

}
