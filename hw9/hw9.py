import numpy as np

# reconstruct alignments from previous matrix
def buildAlignment(prev, seq1, seq2):

    align1 = ""
    align2 = ""

    # iterators for previous matrix
    i, j = len(seq1), len(seq2)

    while True:

        # reached top left of memory table
        if i < 1 and j < 1:
            break

        # out of bounds
        if i < 0 or j < 0:
            raise Exception("i or j iterator in buildAlignment negative! i:{}, j:{}".format(i, j))

        # move to next point in path
        direction, i, j = prev[i][j][0]
        
        # check if horizontal
        # both chars for seq added, could be mismatch
        if direction == "d":
            align1 = seq1[i] + align1
            align2 = seq2[j] + align2 
            continue
       
        # check if vertical
        # add underscore to "j" seqence: seq2
        elif direction == "v":
            align1 = seq1[i] + align1
            align2 = "-" + align2    
            continue

        # check if vertical
        # add underscore to "i" seqence: seq1
        elif direction == "h":
            align1 = "-" + align1
            align2 = seq2[j] + align2  
            continue

    return (align1, align2)


def prevCell(horizontal, vertical, diagonal, min_value):
    
    prev_cell = { "h": False, "v": False, "d": False }

    if min_value == horizontal:
        prev_cell["h"] = True
    
    if min_value == vertical:
        prev_cell["v"] = True
    
    if min_value == diagonal:
        prev_cell["d"] = True

    return prev_cell


def prevList(i, j, prev_cell):

    prev_locations = []

    if prev_cell["h"]:
        prev_locations.append( ( "h", i, j-1 ) )
    if prev_cell["v"]:
        prev_locations.append( ( "v", i-1, j ) )
    if prev_cell["d"]:
        prev_locations.append( ( "d", i-1, j-1 ) )

    return prev_locations


# take in a list and returns all the indicies of min elements
# outputs a list containing all found min elements
def argmin(array):

    min_indicies = []

    # find smallest element
    min_ele = min(array)

    # add all indicies with min element to list
    for i, ele in enumerate(array):
        if ele == min_ele:
            min_indicies.append(i)

    return min_indicies, min_ele

# dynamic programming solution to calculate edit distance
# adapted from DPV Section 6.3
# Input: two strings, seq1 and seq2
# Output: the edit distance and the corresponding optimal alignment
def editDistance(seq1, seq2):

    m, n = len(seq1)+1, len(seq2)+1 # add one for dummy char
    E = np.zeros((m, n), dtype=int) # initialize memory table
    
    # matrix to store previous values to reconstruct alignment
    # store a dict at each matrix index 
    prev = np.zeros((m, n), dtype=list)

    # fill first column with i values
    for i in range(m):
        E[i][0] = i
        if i != 0:
            prev[i][0] = [ ( "v", i-1, 0 ) ] # initialize prev values for base col
        
    # fill first row with i values
    for i in range(n):
        E[0][i] = i
        if i != 0:
            prev[0][i] = [ ( "v", 0, i-1 ) ] # initialize prev values for base row
       
    # fill table row by row, left to right
    # save location of previous for alignment construction
    for i in range(1, m):
        for j in range(1, n):

            # value from horizontal cell
            h = E[i][j-1] + 1

            # value from vertical cell
            v = E[i-1][j] + 1

            # value from diagonal cell, check if chars match
            if seq1[i-1] == seq2[j-1]:
                d = E[i-1][j-1]
            else:
                d = E[i-1][j-1] + 1 # not same char, increment edit distance
            
            # find min edit distance for current subproblem
            edit_costs = [ h, v, d ]
            min_indicies, min_value = argmin(edit_costs)
            
            # set edit distance for cell
            E[i][j] = min_value

            # check if more then one solution
            if len(min_indicies) > 1:
                #min_value = edit_costs[min_indicies[0]] # put value in table
                pass
            # only one min element found
            else:
                pass
            
            # list of prev locations for current location in matrix
            prev_cell_info = prevCell(h, v, d, min_value) 
            prev[i][j] = prevList(i, j, prev_cell_info)
            # print('ON: ({}, {})'.format(i,j))
            # print(prev_cell_info)
            # print('PREV: {}'.format(prev[i][j]))
            # print()

    edit_distance = E[m-1][n-1]
    seq1_alignment, seq2_alignment = buildAlignment(prev, seq1, seq2)

    return edit_distance, (seq1_alignment, seq2_alignment)


def splitStr(str):

    buffer = ""
    segments = []
    for i, char in enumerate(str):

        # new segment every 80 chars 
        if (i+1) % 80 == 0 and i != 0:
            buffer += char
            segments.append(buffer)
            buffer = ""

        # check if on last char
        elif i == len(str)-1:
            buffer += char
            segments.append(buffer)

        else:
            buffer += char
    
    return segments
        

# throws error if arrays are not the same length
def lenCheck(array1, array2):
    
    if len(array1) != len(array2):
        raise Exception("Array lengths do not match!")


def formatAlignment(alignment):
    
    str1, str2 = alignment
    alignment_len = len(str1)

    lenCheck(str1, str2) # check same length

    str1_segments, str2_segments = [], []
    if alignment_len > 80:

        # break strings up into 80 char chunks
        str1_segments = splitStr(str1)
        str2_segments = splitStr(str2)
    else:
        return str1 + "\n" + str2

    buffer = ""
    # build buffer to output
    for i in range(len(str1_segments)):
        buffer += str1_segments[i] + "\n" + str2_segments[i] + "\n\n"

    return buffer


# answer validator check edit distance with number of mismatches and gaps
def answerValid(edit_distance, alignment):

    lenCheck(alignment[0], alignment[1])

    edit_counter = 0
    for i in range(len(alignment[0])):
        if alignment[0][i] != alignment[1][i]:
            edit_counter += 1

    if edit_counter != edit_distance:
        return False
    else:
        return True


# driver code for distance algorithm
def run(file_name):

    f_in = open(file_name, "r")

    seq1, seq2 = "", ""
    started_seq1, started_seq2 = False, False

    # read in data from files
    for line in f_in: 

        # reading first sequence
        if line[0] == ">" and not started_seq1:
            started_seq1 = True
            continue

        # reading second sequence
        elif line[0] == ">" and started_seq1:
            started_seq2 = True 
            continue

        # remove new lines and build buffers
        if started_seq1 and not started_seq2:
            seq1 += line.strip(' \n')
        else:
            seq2 += line.strip(' \n')

    # find the distance and alignment
    edit_distance, alignment = editDistance(seq1, seq2)

    # verify answer
    if answerValid(edit_distance, alignment):
        
        # format alignment
        buffer = formatAlignment(alignment)

        # print the distance and alignment
        print("Edit Distance: {}".format(edit_distance))
        print("Alignment:")
        print(buffer)

        print("Answer verified with answerValid() ✔\n")
    
    else: 
        print("Answer failed answerValid() check ✘\n")

            

# test gene sequencses
files = [ "cox1-protein.fasta.txt",     
          "cox1-dna.fasta.txt" ]

# test all input files
for file in files:
    run(file)
