import zlib
import sys

def compress(infile, dst, level=9):
    infile = open(infile, 'rb')
    dst = open(dst, 'wb')
    compress = zlib.compressobj(level)
    data = infile.read(1024)
    while data:
        dst.write(compress.compress(data))
        data = infile.read(1024)
    dst.write(compress.flush())

def decompress(infile, dst):
    infile = open(infile, 'rb')
    dst = open(dst, 'wb')
    decompress = zlib.decompressobj()
    data = infile.read(1024)
    while data:
        dst.write(decompress.decompress(data))
        data = infile.read(1024)
    dst.write(decompress.flush())

if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc != 4):
        print("Usage: -c/-d in_filename out_filename")
        exit(1)
    if(sys.argv[1] == "-c"):
        compress(sys.argv[2], sys.argv[3])
    elif(sys.argv[1] == "-d"):
        decompress(sys.argv[2], sys.argv[3])
