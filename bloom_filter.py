__author__ = 'Jeevan'

import numpy as np
import string
import random
import math
import matplotlib.pyplot as plt


def djb2(str,rand_hash):
    '''
    DJB2 algorithm to calculate hash value for a give string
    :param str: The String to which we need hash value
    :param rand_hash: Random value to make different hash values
    :return: Returns hash value for the passed string taken modulo of 1000
    '''

    _hash = rand_hash
    for i in xrange(0, len(str)):
       _hash = ((_hash << 5) + _hash) + ord(str[i])

    return _hash%1000

def sdbm(str,rand_hash):
    '''
    SDBM algorithm to calculate hash value for a give string
    :param str: The String to which we need hash value
    :param rand_hash: Random value to make different hash values
    :return: Returns hash value for the passed string taken modulo of 1000
    '''

    _hash = 0
    for i in xrange(0, len(str)):
       _hash = ord(str[i]) + (_hash << rand_hash) + (_hash << 16) - _hash

    return _hash%1000

def bar_graph(false_positive,false_positive1):
    '''
    This function draws a bar chart for the given false positive values for both of the algorithms. Bar chart
    with X-axis has number of randomly inserted string such as (100, 1000, 10000, 100000, 1 million) and y-axis
    has number of false positives for each of the algorithm
    :param false_positive: List of No. of false positives for DJB2 algorithm
    :param false_positive1: List of No. of false positives for SDBM algorithm
    :return: Returns a bar chart for both of the false positive vales
    '''

    djb2 = false_positive
    sdbm = false_positive1
    yer = (2, 3, 4, 1, 2)
    p1 = plt.bar(np.arange(5) , djb2,0.35, color='g', yerr=yer,label='DJB2')
    p2 = plt.bar(np.arange(5) + 0.35, sdbm, 0.35,color='b',yerr=yer,label='SDBM')
    plt.ylabel('False Positives for 1 million words')
    plt.xlabel('No. Of Words Inserted')
    plt.title('Bloom Filter False Positives')
    plt.xticks(np.arange(5)+0.35/2., ('100', '1000', '10000', '100000', '1000000') )
    plt.legend()
    plt.show()



def validate(bloom_filter,bloom_filter1,validate_strings,rand):
    '''
    The validate function validates the two Bloom Filter arrays with the given 1 million
    strings and returns the false positives for both of the algorithms DJB2 and SDBM
    :param bloom_filter: contain bloom filter used to set DJB2 algorithm
    :param bloom_filter1: contain bloom filter used to set SDBM algorithm
    :param validate_strings: contains 1 million words to be validated
    :param rand: contains the list of random values used to calculate 8 different hash values for each hash algorithm
    :return: count of false positives for each algorithm
    '''
    false_positive = 0
    false_positive1 = 0

    for i in range(validate_strings.size):
        bloom_check = []
        bloom_check1 = []

        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[0])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[1])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[2])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[3])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[4])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[5])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[6])])
        bloom_check.append(bloom_filter[0,djb2(validate_strings[i],rand[7])])

        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[0])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[1])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[2])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[3])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[4])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[5])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[6])])
        bloom_check1.append(bloom_filter1[0,sdbm(validate_strings[i],rand[7])])

        # print bloom_check
        if all(x == 1 for x in bloom_check):
            false_positive += 1

        if all(x == 1 for x in bloom_check1):
            false_positive1 += 1

    # print false_positive
    return false_positive,false_positive1
    # exit(0)

if __name__ == '__main__':
   '''
    Bloom filters are initialized with 0's and strings to be validated are fetched from the text file
    into validate_strings. rand contains the list of 8 random numeric values to be used for the hash function.
    After inserting 100, 1000, 10000, 100000, 1 million words, the program calls validate function to calculate the
    counts of false positives
   '''
   bloom_filter = np.zeros((1,1000),dtype=int)
   bloom_filter1 = np.zeros((1,1000),dtype=int)
   validate_strings = np.loadtxt("A.txt",str,skiprows=0)
   rand = [17, 16, 9, 8, 13, 12, 3, 14]
   false_positive = []
   false_positive1 = []
   hash = []
   j = 2
   for i in range(1,1000001):
       if i%math.pow(10,j)==0:
           print i,' words Inserted..Validating Bloomfilter with given 1 million data'
           # np.savetxt('bloom_filter.out',bloom_filter1,fmt='%i')
           x,y = validate(bloom_filter,bloom_filter1,validate_strings,rand)
           false_positive.append(x)
           false_positive1.append(y)
           j += 1
       str = ''.join(random.choice(string.ascii_letters) for i in range(10))
       '''
       Bloom filter is set to 1 for the positions the 8 DJB2 hash functions returns
       '''
       bloom_filter[0,djb2(str,rand[0])]=1
       bloom_filter[0,djb2(str,rand[1])]=1
       bloom_filter[0,djb2(str,rand[2])]=1
       bloom_filter[0,djb2(str,rand[3])]=1
       bloom_filter[0,djb2(str,rand[4])]=1
       bloom_filter[0,djb2(str,rand[5])]=1
       bloom_filter[0,djb2(str,rand[6])]=1
       bloom_filter[0,djb2(str,rand[7])]=1
       '''
       Bloom filter is set to 1 for the positions the 8 Sdbm hash functions returns
       '''
       bloom_filter1[0,sdbm(str,rand[0])]=1
       bloom_filter1[0,sdbm(str,rand[1])]=1
       bloom_filter1[0,sdbm(str,rand[2])]=1
       bloom_filter1[0,sdbm(str,rand[3])]=1
       bloom_filter1[0,sdbm(str,rand[4])]=1
       bloom_filter1[0,sdbm(str,rand[5])]=1
       bloom_filter1[0,sdbm(str,rand[6])]=1
       bloom_filter1[0,sdbm(str,rand[7])]=1

   bar_graph(false_positive,false_positive1)

