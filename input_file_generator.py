#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
import numpy as np

def main():
    if len(sys.argv) != 7:
        print("Usage: >> python {} <filename> <npoints> <xmin> <xmax> <ymin> <ymax>".format(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    npoints = int(sys.argv[2])
    xmin, xmax, ymin, ymax = (float(x) for x in sys.argv[3:])
    xs = np.random.uniform(xmin, xmax, (npoints, 1))
    ys = np.random.uniform(ymin, ymax, (npoints, 1))
    with open(filename, 'w') as out_file:
        for row in range(npoints):
            out_file.write("%.6f\t%.6f\n" % (xs[row], ys[row]))
    print("write {:d} points to {:s}".format(npoints, filename))

if __name__ == "__main__":
    main()
