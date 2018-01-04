package testtools;

import java.util.NoSuchElementException;

/**
 * Created by guoxi on 7/22/17.
 * Demo of minHeap implementation, demonstration of percolateUp / percolateDown methods and
 * how to utilize these methods to do basic heap operations.
 * public method I need to do basic heap operations
 * size(), isEmpty(), isFull(), peek(), poll(), offer(), update(int index, int value), heapify()
 * there are some property we need kwno:
 * 1. minHeap datastructure is CBT and implemented by a array
 * 2. prent = i, leftchild = i * 2 + 1, right chid = i * 2 + 2 => child = (child - 1) / 2
 */
public class minHeap {
    //constructor
    private int[] heapArray;
    private int size;
    private int maxsize;
    public minHeap (int maxsize, int[] heapArray){
        this.maxsize = maxsize;
        this.heapArray = heapArray;
        if (heapArray.length == 0) {
            heapArray = new int[maxsize];
            this.size = 0;
        }
        this.size = heapArray.length;
        heapify();
    }

    public int size () {
        return size;
    }

    public boolean isEmpty () {
        return size == 0;
    }

    public boolean isFull () {
        return size == maxsize;
    }

    public int peek () {
        if (size == 0) {
            return -1;
        }
        return heapArray[0];
    }

    public void offer (int ele) {
        if (size == maxsize) {
            int[] newArray = new int[(int) (heapArray.length * 1.5)];//why?
            copy (heapArray, newArray);
            heapArray = newArray;
            maxsize = heapArray.length;
        }
        heapArray[size] = ele;
        percolateUp(heapArray, size);
        size++;
        return;
    }

    public int poll() {
        if (size == 0) {
            throw new NoSuchElementException("heap is empty");
        }
        int result = heapArray[0];
        heapArray[0] = heapArray[size - 1];
        size--;
        percolateDown(heapArray, 0);
        return result;
    }

    public void update (int index, int value) {
        if (index < 0 || index > size - 1) {
            throw new ArrayIndexOutOfBoundsException("invalid index range");
        }
        int prev = heapArray[index];
        heapArray[index] = value;
        if (value > prev) {
            percolateDown(heapArray, index);
        } else {
            percolateUp(heapArray, index);
        }
        return;
    }

    public void heapify() {
        for (int i = size / 2 - 1; i >= 0; i--) {
            percolateDown(heapArray, i);
        }
    }

    //by the way we still need percolateUp && percolateDown method and swap helpe method to do above motheds
    public void percolateUp (int[] array, int index) {
        //compareTo(parent)
        while (index != 0) {
            int parent = (index - 1) / 2;
            if (array[index] > array[parent]) {
                return;
            } else {
                swap(array, index, parent);
            }
            index = parent;
        }
    }

    public void percolateDown (int[] array, int index) {
        while(index <= (size - 2) / 2) {
            int leftchild = index * 2 + 1;
            int rightchild = index * 2 + 2;
            int swapIndex = leftchild;
            if (rightchild < size - 1 && array[rightchild] < array[leftchild]) {
                swapIndex = rightchild;
            }
            if (array[index] > array[swapIndex]) {
                swap(array, swapIndex, index);
            } else {
                break;
            }
            index = swapIndex;
        }
    }

    public void swap (int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
        return;
    }

    public void copy (int[] prevArray, int[] newArray) {
        for(int i = 0; i < prevArray.length; i++) {
            newArray[i] = prevArray[i];
        }
    }
}
