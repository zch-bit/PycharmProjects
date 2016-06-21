import os


def read_in_chunks(filename, chunk_size=1024 * 1024):
    file_object = open(filename)
    size = os.path.getsize(filename)
    # get number of chunks
    num = size / chunk_size + 1
    try:
        while num:
            # Stop when num == 0
            num = num - 1
            chunk_data = file_object.read(chunk_size)
            # Find the last chunk and return
            if len(chunk_data) <= chunk_size:
                return chunk_data
    finally:
        file_object.close()


def tail_line(chunk, n):
    for i in chunk.split('\n')[-n-1:-1]:
        print i


if __name__ == "__main__":
    # test.txt, size: 4.36 GB
    filename = 'test.txt'
    n = 5
    chunk = read_in_chunks(filename)
    tail_line(chunk, n)
