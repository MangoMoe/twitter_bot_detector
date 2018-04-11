from __future__ import (absolute_import, division, print_function, unicode_literals)

import random
import numpy as np
import re
import math

def mode(a, axis=0):
# taken from scipy code
# https://github.com/scipy/scipy/blob/master/scipy/stats/stats.py#L609
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return mostfrequent, oldcounts


class Matrix:

    """
    Unlike the Matrix class defined in toolkit (C++) and toolkitJava,
    data is an array of columns rather than an array of rows.
    This makes computing statistics on columns more efficient.

    For discrete attributes, at least one value must be a float in
    order for numpy array functions to work properly. (The load_arff
    function ensures that all values are read as floats.)
    """

    data = []
    attr_names = []
    str_to_enum = []       # array of dictionaries
    enum_to_str = []       # array of dictionaries
    dataset_name = "Untitled"
    MISSING = float("infinity")

    def __init__(self, matrix=None, row_start=None, col_start=None, row_count=None, col_count=None, arff=None):
        """
        If matrix is provided, all parameters must be provided, and the new matrix will be
        initialized with the specified portion of the provided matrix.
        """
        if arff:
            self.load_arff(arff)
        elif matrix:
            self.init_from(matrix, row_start, col_start, row_count, col_count)

    def init_from(self, matrix, row_start, col_start, row_count, col_count):
        """Initialize the matrix with a portion of another matrix"""
        self.data = [matrix.data[row][col_start:col_start+col_count] for row in range(row_start, row_start+row_count)]
        self.attr_names = matrix.attr_names[col_start:col_start+col_count]
        self.str_to_enum = matrix.str_to_enum[col_start:col_start+col_count]    # array of dictionaries
        self.enum_to_str = matrix.enum_to_str[col_start:col_start+col_count]    # array of dictionaries
        return self

    def add(self, matrix, row_start, col_start, col_count):
        """Appends a copy of the specified portion of a matrix to this matrix"""
        if __debug__ and self.cols < col_count:
            raise Exception("out of range")

        if __debug__:
            for col in range(self.cols):
                if matrix.value_count(col_start + col) != self.value_count(col):
                    raise Exception("incompatible relations")

        for i in range(matrix.rows - row_start):
            self.data.append(matrix.data[row_start + i][col_start:col_start + col_count])

    def add_row(self, matrix, row):
        self.data.append(matrix.data[row])

    def set_size(self, rows, cols):
        """Resize this matrix (and set all attributes to be continuous)"""
        self.data = [[0]*cols for row in range(rows)]
        self.attr_names = [""] * cols
        self.str_to_enum = {}
        self.enum_to_str = {}

    def load_arff(self, filename):
        """Load matrix from an ARFF file"""
        self.data = []
        self.attr_names = []
        self.str_to_enum = []
        self.enum_to_str = []
        reading_data = False

        rows = []           # we read data into array of rows, then convert into array of columns

        f = open(filename)
        for line in f.readlines():
            line = line.rstrip()
            if len(line) > 0 and line[0] != '%':
                if not reading_data:
                    if line.lower().startswith("@relation"):
                        self.dataset_name = line[9:].strip()
                    elif line.lower().startswith("@attribute"):
                        attr_def = line[10:].strip()
                        if attr_def[0] == "'":
                            attr_def = attr_def[1:]
                            attr_name = attr_def[:attr_def.index("'")]
                            attr_def = attr_def[attr_def.index("'")+1:].strip()
                        else:
                            search = re.search(r'(\w*)\s+({.*}|\w+)', attr_def)
                            attr_name = search.group(1)
                            attr_def = search.group(2)
                            # Remove white space from atribute values
                            attr_def = "".join(attr_def.split())

                        self.attr_names += [attr_name]

                        str_to_enum = {}
                        enum_to_str = {}
                        if attr_def.lower() not in ("real", "continuous", "integer"):
                            # attribute is discrete
                            assert attr_def[0] == '{' and attr_def[-1] == '}'
                            attr_def = attr_def[1:-1]
                            attr_vals = attr_def.split(",")
                            val_idx = 0
                            for val in attr_vals:
                                val = val.strip()
                                enum_to_str[val_idx] = val
                                str_to_enum[val] = val_idx
                                val_idx += 1

                        self.enum_to_str.append(enum_to_str)
                        self.str_to_enum.append(str_to_enum)

                    elif line.lower().startswith("@data"):
                        reading_data = True

                else:
                    # reading data
                    row = []
                    val_idx = 0
                    # print("{}".format(line))
                    vals = line.split(",")
                    for val in vals:
                        val = val.strip()
                        if not val:
                            raise Exception("Missing data element in row with data '{}'".format(line))
                        else:
                            row += [float(self.MISSING if val == "?" else self.str_to_enum[val_idx].get(val, val))]

                        val_idx += 1

                    rows += [row]

        f.close()
        self.data=rows

    @property
    def rows(self):
        """Get the number of rows in the matrix"""
        return len(self.data)

    @property
    def cols(self):
        """Get the number of columns (or attributes) in the matrix"""
        return len(self.attr_names)

    def row(self, n):
        """Get the specified row"""
        return self.data[n]

    def col(self, n):
        """Get the specified column"""
        return [row[n] for row in self.data]

    def get(self, row, col):
        """
        Get the element at the specified row and column
        :rtype: float
        """
        return self.data[row][col]

    def set(self, row, col, val):
        """Set the value at the specified row and column"""
        self.data[row][col] = val

    def attr_name(self, col):
        """Get the name of the specified attribute"""
        return self.attr_names[col]

    def set_attr_name(self, col, name):
        """Set the name of the specified attribute"""
        self.attr_names[col] = name

    def attr_value(self, attr, val):
        """
        Get the name of the specified value (attr is a column index)
        :param attr: index of the column
        :param val: index of the value in the column attribute list
        :return:
        """
        return self.enum_to_str[attr][val]

    def value_count(self, col):
        """
        Get the number of values associated with the specified attribute (or columnn)
        0=continuous, 2=binary, 3=trinary, etc.
        """
        return len(self.enum_to_str[col]) if len(self.enum_to_str) > 0 else 0

    def shuffle(self, buddy=None):
        """Shuffle the row order. If a buddy Matrix is provided, it will be shuffled in the same order."""
        if not buddy:
          random.shuffle(self.data)
        else:
          c = list(zip(self.data, buddy.data))
          random.shuffle(c)
          self.data, buddy.data = zip(*c)

    def column_mean(self, col):
        """Get the mean of the specified column"""

        a = np.ma.masked_equal(self.col(col), self.MISSING).compressed()
        return np.mean(a)

    def column_min(self, col):
        """Get the min value in the specified column"""
        a = np.ma.masked_equal(self.col(col), self.MISSING).compressed()
        return np.min(a)

    def column_max(self, col):
        """Get the max value in the specified column"""
        a = np.ma.masked_equal(self.col(col), self.MISSING).compressed()
        return np.max(a)

    def most_common_value(self, col):
        """Get the most common value in the specified column"""
        a = np.ma.masked_equal(self.col(col), self.MISSING).compressed()
        (val, count) = mode(a)
        return val[0]

    # this function removes all values from the matrix that don't have a given value in the given column
    def remove_if_not_match(self, col_num, value):
        new_data = []
        for row in self.data:
            if row[col_num] == value:
                new_data.append(row)
        self.data = new_data

        # for index, row in enumerate(data):
        #     if row[col_num] != value:
        #         # TODO is this inefficient?
        #         del data[index]
        pass

    def normalize(self):
        """Normalize each column of continuous values"""
        for i in range(self.cols):
            if self.value_count(i) == 0:     # is continuous
                min_val = self.column_min(i)
                max_val = self.column_max(i)
                for j in range(self.rows):
                    v = self.get(j, i)
                    if v != self.MISSING:
                        if math.isnan((v - min_val)/(max_val - min_val)):
                            # print("HERE IS A THING: {}".format((v - min_val)/(max_val - min_val)))
                            self.set(j, i, 0.0)
                        else:
                            self.set(j, i, (v - min_val)/(max_val - min_val))

    # def print(self):
    def print_self(self):
        print("@RELATION {}".format(self.dataset_name))
        for i in range(len(self.attr_names)):
            print("@ATTRIBUTE {}".format(self.attr_names[i]), end="")
            if self.value_count(i) == 0:
                print(" CONTINUOUS")
            else:
                print(" {{{}}}".format(", ".join(self.enum_to_str[i].values())))

        print("@DATA")
        for i in range(self.rows):
            r = self.row(i)

            values = []
            for j in range(len(r)):
                if self.value_count(j) == 0:
                    values.append(str(r[j]))
                else:
                    values.append(self.enum_to_str[j][r[j]])

            # values = list(map(lambda j: str(r[j]) if self.value_count(j) == 0 else self.enum_to_str[j][r[j]],
            #                   range(len(r))))
            print("{}".format(", ".join(values)))
