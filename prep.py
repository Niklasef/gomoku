import subprocess
import numpy
import os
from augment import aug

out_directory = 'preped/'
data_count = 0
start_year = 2018
end_year = 2020
dev_mode = False
visualize = False
output_format = 'BIN'
opening_moves = []
openings = numpy.zeros(shape=(24, 20, 20))
i = 0

with open('openings_freestyle.txt') as f:
    for line in f:
        opening_ser = subprocess.check_output(["py.exe", "opening.py", line, "silent"]).decode("utf-8")
        opening_raveled = numpy.fromstring(opening_ser.replace('[','').replace(']',''), dtype=int, sep='_')
        openings[i] = opening_raveled.reshape(20,20)
        i += 1

for year in range(start_year, end_year+1):
    root_dir = 'data\gomocup' + str(year) + 'results'
    if dev_mode :
        root_dir += '_test'
    for rootdir, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if not dir.startswith('Freestyle'):
                continue
            in_directory = os.path.join(root_dir, dir) + '/'
            print(in_directory)
            for filename in os.listdir(in_directory):
                if not filename.endswith(".psq"): 
                    continue
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    lines = []
                    opening_moves.append(0)
                    board = numpy.zeros(shape=(20,20))
                    found_opening = False
                    player = 1
                    for line in file_in:
                        if line.count(',') == 2:
                            board[int(line.split(',')[1])-1][int(line.split(',')[0])-1] = player
                            player *= -1
                            if found_opening:
                                data_count += 1
                            else:
                                opening_moves[-1] += 1
                            for opening in openings:
                                if numpy.array_equal(board, opening):
                                    found_opening = True
                                    break                            

print('move count = ' + str(data_count))
# data_count = data_count * 2
# print('move count including augmentations = ' + str(data_count))
print('opening_moves length = ' + str(len(opening_moves)))
data = numpy.zeros(shape=(data_count, 20, 20))
labels = numpy.zeros(shape=(data_count, 400))
i = 0
game_i = 0
col = 0
row = 0
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
                j = 0
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            col = int(line.split(',')[0])
                            row = int(line.split(',')[1])
                            if j >= opening_moves[game_i]:#only learn non opening moves
                                label = numpy.zeros(shape=(20, 20))
                                label[row-1][col-1] = 1
                                a_result = aug(board, label)
                                for a in a_result:
                                    data[i] = a[0].astype(int)
                                    labels[i] = a[1].ravel().astype(int)
                                    #invert board so all moves are from black perspective
                                    if current_player == -1:
                                        data[i] = numpy.where(data[i]==1, 3, data[i])
                                        data[i] = numpy.where(data[i]==-1, 1, data[i])
                                        data[i] = numpy.where(data[i]==3, 1, data[i])

                                    i += 1

                            board[row-1][col-1] = current_player
                            j += 1
                            current_player *= -1
                            if visualize:
                                os.system("python print_board.py " + numpy.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
                    print("i = " + str(i))
                game_i += 1
            group = group +1

shuffled_index = numpy.zeros(data_count).astype(int)
for i in range(data_count):
   shuffled_index[i] = i

numpy.random.shuffle(shuffled_index)

if numpy.array_equal(board, openings[10]):
    print("Found opening " + str(filename))
train_count = int((data_count) * 0.99)
test_count = int((data_count) * 0)
val_count = int(data_count - train_count - test_count)
print('train_count = ' + str(train_count))
print('test_count = ' + str(test_count))
print('val_count = ' + str(val_count))

train_data = numpy.zeros(shape=(train_count, 20, 20))
train_labels = numpy.zeros(shape=(train_count, 400))
test_data = numpy.zeros(shape=(test_count, 20, 20))
test_labels = numpy.zeros(shape=(test_count, 400))
val_data = numpy.zeros(shape=(val_count, 20, 20))
val_labels = numpy.zeros(shape=(val_count, 400))

for i in range(train_count):
    train_data[i] = data[shuffled_index[i]]
    train_labels[i] = labels[shuffled_index[i]]

for i in range(test_count):
    j = i + train_count    
    test_data[i] = data[shuffled_index[j]]
    test_labels[i] = labels[shuffled_index[j]]

for i in range(val_count):
    j = i + train_count   
    val_data[i] = data[shuffled_index[j]]
    val_labels[i] = labels[shuffled_index[j]]

with open('preped/train_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, train_data.astype(float), delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, train_data)

with open('preped/train_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, train_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, train_labels)

with open('preped/test_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, test_data.astype(float), delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, test_data)

with open('preped/test_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, test_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, test_labels)

with open('preped/val_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, val_data.astype(float), delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, val_data)

with open('preped/val_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, val_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, val_labels)
