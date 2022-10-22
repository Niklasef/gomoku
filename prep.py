# TODO: Augmentations
# TODO: Shuffling

import subprocess
import sys
import numpy
import os
from augment import aug

CHUNK_COUNT = 10

def save(data, file_index):
    train_count = int((CHUNK_COUNT) * 0.99)
    test_count = int((CHUNK_COUNT) * 0)
    val_count = int(CHUNK_COUNT - train_count - test_count)
    print('saving with file index = ' + str(file_index))

    train_data = numpy.zeros(shape=(train_count, 20, 20))
    train_labels = numpy.zeros(shape=(train_count, 400))
    test_data = numpy.zeros(shape=(test_count, 20, 20))
    test_labels = numpy.zeros(shape=(test_count, 400))
    val_data = numpy.zeros(shape=(val_count, 20, 20))
    val_labels = numpy.zeros(shape=(val_count, 400))

    for i in range(train_count):
        train_data[i] = data[i]
        train_labels[i] = labels[i]

    for i in range(test_count):
        j = i + train_count    
        test_data[i] = data[j]
        test_labels[i] = labels[j]

    for i in range(val_count):
        j = i + train_count   
        val_data[i] = data[j]
        val_labels[i] = labels[j]

    with open(f'preped/train_data_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, train_data.astype(float), delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, train_data)

    with open(f'preped/train_labels_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, train_labels.astype(int), fmt='%i', delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, train_labels)

    with open(f'preped/test_data_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, test_data.astype(float), delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, test_data)

    with open(f'preped/test_labels_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, test_labels.astype(int), fmt='%i', delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, test_labels)

    with open(f'preped/val_data_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, val_data.astype(float), delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, val_data)

    with open(f'preped/val_labels_{str(file_index)}.npy', "wb") as f:
        if output_format == 'TXT':
            numpy.savetxt(f, val_labels.astype(int), fmt='%i', delimiter=",")
        if output_format == 'BIN':
            numpy.save(f, val_labels)

out_directory = 'preped/'
start_year = 2021
end_year = 2021
dev_mode = True
visualize = False
if len(sys.argv) >= 2 and sys.argv[1] == "visualize":
    visualize = True
output_format = 'BIN'
opening_moves = []
openings = numpy.zeros(shape=(24, 20, 20))
i = 0

with open('openings_freestyle.txt') as f:
    for line in f:
        opening_ser = subprocess.check_output(["python.exe", "opening.py", line, "silent"]).decode("utf-8")
        opening_raveled = numpy.fromstring(opening_ser.replace('[','').replace(']',''), dtype=int, sep='_')
        openings[i] = opening_raveled.reshape(20,20)
        i += 1

print('opening_moves length = ' + str(len(opening_moves)))
data = numpy.zeros(shape=(CHUNK_COUNT, 20, 20))
labels = numpy.zeros(shape=(CHUNK_COUNT, 400))
i = 0
game_i = 0
col = 0
row = 0
file_index = 0
for year in range(start_year, end_year+1):
    root_dir = 'data\gomocup' + str(year) + 'results'
    if dev_mode :
        root_dir += '_test'    
    group = 1
    for rootdir, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if not dir.startswith('Freestyle'):
                continue
            in_directory = os.path.join(root_dir, dir) + '/'
            print(in_directory)
            for filename in os.listdir(in_directory):
                if not filename.endswith(".psq"): 
                    continue
                board = numpy.zeros(shape=(20,20))
                current_player = 1
                
                #Iterate moves in game
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    lines = []
                    found_opening = False
                    for line in file_in:
                        if line.count(',') == 2:
                            col = int(line.split(',')[0])
                            row = int(line.split(',')[1])
                            if found_opening:#only learn non opening moves
                                label = numpy.zeros(shape=(20, 20))
                                label[row-1][col-1] = 1
                                data[i] = board.astype(int)
                                labels[i] = label.ravel().astype(int)
                                #invert board so all moves are from black perspective
                                if current_player == -1:
                                    data[i] = numpy.where(data[i]==1, 3, data[i])
                                    data[i] = numpy.where(data[i]==-1, 1, data[i])
                                    data[i] = numpy.where(data[i]==3, 1, data[i])
                                i += 1
                                if i == CHUNK_COUNT:
                                    i = 0
                                    save(data, file_index)
                                    file_index += 1
                                    data = numpy.zeros(shape=(CHUNK_COUNT, 20, 20))
                            else:
                                for opening in openings:
                                    if numpy.array_equal(board, opening) and not numpy.array_equal(board, numpy.zeros(shape=(20,20))):
                                        found_opening = True
                                        break
                            board[row-1][col-1] = current_player
                            current_player *= -1
                            if visualize:
                                os.system("python print_board.py " + numpy.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
                    print("i = " + str(i))
                game_i += 1
            group = group +1
    save(data, file_index)
