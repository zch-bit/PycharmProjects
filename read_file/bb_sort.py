import sys


def open_file(filename):
    with open(filename, 'r') as f:
        data = f.read().replace('\n', '').split(' ')
        return [int(i) for i in data]


def bb_sort(mylist):
    n = len(mylist)
    for i in range(0, n):
        for j in range(0, n - 1):
            if mylist[j] > mylist[j + 1]:
                t = mylist[j]
                mylist[j] = mylist[j + 1]
                mylist[j + 1] = t
    return mylist


if __name__ == "__main__":
    print bb_sort(open_file(sys.argv[1]))
