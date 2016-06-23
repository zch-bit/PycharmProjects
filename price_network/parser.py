#! usr/bin/env python

'''
    Output file:
        - output.json
'''

import csv
import json
import re

try:
    from sets import Set
except ImportError:
    Set = set

model_list = []
make_list = []

# Read file when start running.
with open('models.csv', 'rU') as model_file:
    model_csv = csv.reader(model_file)
    for i in model_csv:
        model_list.append(i)

with open('makes.csv', 'rU') as makes_file:
    makes_csv = csv.reader(makes_file)
    for i in makes_csv:
        make_list.append(i)


def read_csv(filename):
    """ Read csv file, convert result
        to a dictionary and return.
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
    """ Read csv file, return a dict(id: make)
    """
    id_make = {}
    with open(filename, 'rU') as csvfile:
        # Read csv file by Row.
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Reading from content into a list.
        for row in content:
            if row[0] != 'MakeID':
                id_make[row[0]] = row[1].lower()
                # Save result into a dictionary as: id : make
    # print id_make
    return id_make


def write_to_file(info, file_name):
    """ Save info into file, if has some dict,
        combine all together.
    """
    new = {}
    try:
        with open(file_name, 'rb') as fr:
            old = json.load(fr)
            new = dict(old.items() + info.items())
    except Exception as e:
        new = info
    try:
        with open(file_name, 'w') as f:
            # Save the dict into file.
            json.dump(new, f)
    except Exception as e:
        print str(e)


def search_csv(filename, str):
    """ Find a str in .csv file, if found, return the whole row.
    """
    result = []
    temp = []
    with open(filename, 'rU') as f:
        content = csv.reader(f)
        for row in content:
            for field in row:
                if field.lower() == str:
                    for item in row:
                        # save in a list
                        temp.append(item)
                    result.append(temp)
                    temp = []
    # return a list of list
    # if not found, return []
    return result


def findWholeWord(w):
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
        if findWholeWord(model)(str.lower()):
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


def find_related(str):
    """
        Take any str as input, check if input can be a valid make-model pair,
        Then find related make-model pair by searching datas.csv.
    """
    keyword = interp(str)
    # Check if input can be a make-model pair.
    if not keyword:
        raise Exception("Invalid input, please input at least a model.")

    rows = search_csv('data.csv', keyword)
    print '\n Searching for related models...\n'
    # rows is sorted by the csv file structure.

    related_set = Set()
    related_list = []
    for row in rows:
        temp_list = []
        for i in row:
            if not i in keyword \
                    and not i.isdigit() \
                    and not keyword in i:
                print "Check if %s is related." % i
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


if __name__ == "__main__":
    # Get a list of all models and makes.
    models, makes = get_models_makes('models.csv', 'makes.csv')

    # Test cases
    print 'make-model pair tests: '

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

    find_related('2012 acura ilx')

    find_related('mitsubishi outlander')

    print "---------- Read from file: ---------"
    with open('output.json', 'rb') as f:
        print json.dumps(json.load(f), indent=4)
