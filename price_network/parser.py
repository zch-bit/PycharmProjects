#! usr/bin/env python

'''
    Instruction:
    - 1. Clean data by function 'clean_data(f1, f2)', it takes a long time to clean data, this has been done,
    and new_data.csv is the output file.
    - 2. For each input, first check if it is valid, for a valid input, it should be targeted as a model, then
    return a make-model pair.
    - 3. Find top 20 related cars by seaching count number in  new_data.csv, and pring out.

    Data clean output file:
        - new_data.csv

    Final related car file:
        - output.json

'''

import csv
import json
import re
import pandas
import time

try:
    from sets import Set
except ImportError:
    Set = set

model_list = []
make_list = []

# load file when start running.
with open('models.csv', 'rU') as model_file:
    model_csv = csv.reader(model_file)
    for i in model_csv:
        model_list.append(i)

with open('makes.csv', 'rU') as makes_file:
    makes_csv = csv.reader(makes_file)
    for i in makes_csv:
        make_list.append(i)


def read_csv(filename):
    """ Read csv file by column, convert result
        to a dictionary: first(of each column): others in the column.
    """
    info = []
    result = {}
    with open(filename, 'rU') as csvfile:
        # Read csv file by Row.
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Reading from content into a list.
        for row in content:
            info.append(row)
    # Save result into a  dict:(Title: items)
    for i in range(0, len(info[0])):
        temp = []
        for j in range(1, len(info)):
            temp.append(info[j][i].lower())
        result[info[0][i]] = temp
    return result


def read_to_dict(filename):
    """ Read csv file by row, return a (id: make) pair.
    """
    id_make = {}
    with open(filename, 'rU') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Reading from content into a list.
        for row in content:
            if row[0] != 'MakeID':
                id_make[row[0]] = row[1].lower()
    # print id_make
    return id_make


def write_to_file(info, file_name):
    """ Save info into file, if has some dict,
        combine all together.
    """
    try:
        with open(file_name, 'rb') as fr:
            old = json.load(fr)
            new = dict(old.items() + info.items())
    except Exception:
        new = info
    try:
        with open(file_name, 'w') as f:
            json.dump(new, f)
    except Exception as e:
        print str(e)


def search_csv(filename, str):
    """ Find a str in .csv file, if found, return the whole row.
    """
    result = []
    temp = []
    df = pandas.read_csv(filename, dtype='str')
    data = df.values
    if True:
        for row in data:
            for field in row:
                if field.lower() == str:
                    for item in row:
                        # save in a list
                        temp.append(item)
                    result.append(temp)
                    temp = []
    # return a list of list
    return result


def find_whole_word(w):
    """ Helper function to seek a whole word, rather than substring.
    """
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def get_models_makes(model_file, makes_file):
    # Read two files to get a list of makes and models.
    id_models = read_csv(model_file)
    brand_and_id = read_csv(makes_file)

    makes = brand_and_id['Make']
    models = id_models['Name']
    return models, makes


def interp(str):
    # input: as raw input
    # output: make-model pair
    # Find any models exists in raw input to temp list.
    temp = []
    for model in models:
        if find_whole_word(model)(str.lower()):
            temp.append(model)
    # if no model found, return invalid input.
    if len(temp) == 0:
        return 0
    else:
        md = max(temp, key=len)
    # check if model in raw input.
    if md != '':
        # Find make by model.
        id_row = search_csv('models.csv', md)
        # Check if a model has multi-make.
        if len(id_row) <= 1:
            # Get make id.
            id = id_row[0][0]
            # Search for make by make id in makes.csv.
            mk = search_csv('makes.csv', id)[0][1].lower()
            result = mk + ' ' + md
            return result
        else:
            return 0
    else:
        return 0


def find_related(filename, str):
    """
        Take any str as input, check if input can be a valid make-model pair,
        Then find related make-model pair by searching datas.csv.
    """
    keyword = interp(str)
    # Check if input can be a make-model pair.
    if not keyword:
        raise Exception("Invalid input, please input at least a model.")

    rows = search_csv(filename, keyword)
    print '\n Searching for related models...\n'
    # rows is sorted by the csv file structure.

    related_set = Set()
    related_list = []
    for row in rows:
        temp_list = []
        for i in row:
            if i not in keyword \
                    and not i.isdigit() \
                    and keyword not in i:
                print "Check if %s is related to input..." % i
                pair = interp(i)
                if pair:
                    if pair in related_set:
                        # In case we have two pairs with same first value.
                        continue
                    else:
                        related_set.add(pair)
                        temp_list.append(pair)
                        temp_list.append(row[2])
                else:
                    continue
        if len(temp_list) > 0:
            related_list.append(tuple(temp_list))
        # No more then 20 related, first one as the origin make-model.
        if len(related_set) > 18:
            break
    final_set = sorted(set(related_list), key=lambda x: int(x[1]), reverse=True)
    related = [keyword] + [i[0] for i in final_set]

    output = {}
    output[keyword] = related

    print "\n Related make-model pairs: ", output

    write_to_file(output, 'output.json')
    print '-------- final result ----------'
    print json.dumps(output, indent=4)


def clean_data(input_file, output_file):
    """ Clean raw data in input_file and save into output_file.
    """
    time_start = time.time()
    # helper dict with: <pairs: count>
    count_dict = {}

    df = pandas.read_csv(input_file)
    data = df.values
    if len(data):
        # Start from 1, if 'kw1', 'kw2', 'count' jumpt to next line.
        for row in data[1:]:
            new_row = []
            for i in row[0:2]:
                j = interp(i)
                # Good make-model pair
                if j != 0:
                    new_row.append(j)
                else:
                    continue
            # Ordered two make-model pairs.
            if len(new_row) > 1:
                # print "new_row", new_row
                temp = sorted(new_row)
                # include count number.
                temp.append(row[2])
                # Save this as key: key, count as value for easy look-up.
                if temp[0] != temp[1]:
                    pair = temp[0] + '_' + temp[1]
                    if count_dict.has_key(pair):
                        count_dict[pair] = int(count_dict[pair]) + int(temp[2])
                    else:
                        count_dict[pair] = int(temp[2])
    # Sort the key-value pair by value, from big to small.
    new_cnt = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # Write new content into file.
    with open(output_file, 'w') as fw:
        csv_writer = csv.writer(fw)
        for item in new_cnt:
            row = item[0].split('_') + [item[1]]
            csv_writer.writerow(row)
    ti = time.time() - time_start
    print "Data cleaning finished, used %s seconds. New file: '/%s'." % (round(ti, 2), output_file)


if __name__ == "__main__":
    models, makes = get_models_makes('models.csv', 'makes.csv')
    '''
    # clean_data('data.csv', 'new_data.csv')
    # For testing, it took 31s to run.
    clean_data('data_300.csv', 'new_data_300.csv')
    '''
    # Get a list of all models and makes.
    print 'Input tests:\n'

    test = interp('used honda accord')
    print "Result is: %s  \n" % test

    test1 = interp('TOYOTA PRIUS C')
    print "Result is: %s \n" % test1

    test2 = interp('2012 200')
    # if Result is : 0, means invalid input.
    print "Result is: %s \n" % test2

    test3 = interp('2012 camry')
    print "Result is: %s \n" % test3

    test4 = interp('used honda')
    print "Result is: %s \n" % test4

    test5 = interp('less than $20000')
    print "Result is: %s \n" % test5

    test6 = interp('less than $20000 camry')
    print "Result is: %s \n" % test6

    test6 = interp('2012')
    print "Result is: %s \n" % test6

    test7 = interp('mx-3')
    print "Result is: %s \n" % test7

    test8 = interp('tsx wagon')
    print "Result is: %s \n" % test8

    test9 = interp('acura tl')
    print "Result is: %s \n" % test9

    print "Find realted cars:\n"

    find_related('new_data.csv', '2012 acura ilx')

    find_related('new_data.csv', 'mitsubishi outlander')

    print "---------- Read from file: ---------"
    with open('output.json', 'rb') as f:
        print json.dumps(json.load(f), indent=4)
