import numpy as np
import math
import time
class Recognizer:
    def __init__(self, knowledge, diagonal_weight):
        self.knowledge = knowledge
        self.W = diagonal_weight
        self.matched_keys = []
        self.wdtable = []
        self.dp_planes = []
        self.cost_tables = []

    def d_frame(self, frame_a, frame_b):
        result = 0

        for i in range(15):
            result += pow((frame_a[i]-frame_b[i]), 2)

        return math.sqrt(result)


    def get_dp_plane(self, word_a, word_b):
        dp_plane = []
        for frame_i in word_a:
            row_i = []
            for frame_j in word_b:
                row_i.append(self.d_frame(frame_i, frame_j))
            dp_plane.append(row_i)
        self.dp_planes.append(dp_plane)
        return dp_plane

    def dp_matching(self, dp_plane):
        I = len(dp_plane) #I = # row
        J = len(dp_plane[0])    #J = length of row


        cost_table = [[0 for j in range(J)] for i in range(I)]
        
        #first row
        cost_table[0][0] = dp_plane[0][0]

        for j in range(J-1):
            cost_table[0][j+1] = cost_table[0][j] + dp_plane[0][j+1]

        #first column 
        for i in range(I-1):
            cost_table[i+1][0] = cost_table[i][0] + dp_plane[i+1][0]

        #rest of the table

        for i in range(I-1):
            for j in range(J-1): #current node is (i+1, j+1)                
                top = dp_plane[i+1][j+1] + cost_table[i+1][j]
                left = dp_plane[i+1][j+1] + cost_table[i][j+1]
                diag = self.W * dp_plane[i+1][j+1] + cost_table[i][j]
                cost_table[i+1][j+1] = min([top, left, diag])

        self.cost_tables.append(cost_table)
        return cost_table[I-1][J-1] / (I+J)

    def word_distance_table(self, test_data):
        table = []
        progress = 0
#一番時間がかかるヤツ
        for input_word in test_data:
            score_vector = []
            for temp_word in self.knowledge:
                score = self.dp_matching(self.get_dp_plane(input_word, temp_word))
                score_vector.append(score)
            table.append(score_vector)
            progress+=1
            print(str(progress) + '/100')

        self.wdtable = table
        return table

    def test(self, test_data):
        table = self.word_distance_table(test_data)
        for score_vector in table:
            key = score_vector.index(min(score_vector))
            self.matched_keys.append(key)
#        self.matched_keys = list(map(lambda m: m.index(min(m)), table))

        #calculate accuracy
        print(self.matched_keys)

        count = 0
        for i in range(len(self.matched_keys)):
            if i == self.matched_keys[i]:
                count += 1
        
        print('test accuracy is: ' + str(count/len(self.matched_keys)))



def twodp(table):
    for row in table:
        print(row)

import os
def read_folder(directory):
    data_set = []
    entries_ = os.listdir('Speech/' + directory)
    entries = sorted(entries_)
    for entry in entries:
        f = open('Speech/' + directory+'/'+entry, 'r')
        word = f.read().split('\n')[3:]

        frames_of_word = []

        for frame in word:
            frame_as_list_of_str = frame.split(' ')[:-1]
            frame_as_list_of_num = list(map(lambda x: float(x), frame_as_list_of_str))
            if frame_as_list_of_num:
                frames_of_word.append(frame_as_list_of_num)

        data_set.append(frames_of_word)
    
    return data_set

import sys


template = read_folder(sys.argv[1])
rec = Recognizer(template, 1)
test_set = read_folder(sys.argv[2])
rec.test(test_set)
