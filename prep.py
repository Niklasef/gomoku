import numpy
import os

out_directory = 'preped/'
row_count = 0
game_count = 0
start_year = 2020
stop_year = 2020

#scan data size
for year in range(start_year, stop_year+1):
    result_dir = 'data\gomocup' + str(year) + 'results_test'
    for rootdir, dirs, files in os.walk(result_dir):
        for dir in dirs:
            if not dir.startswith('Freestyle'):
                continue
            in_directory = os.path.join(result_dir, dir) + '/'
            print("in_directory =" + str(in_directory))
            for filename in os.listdir(in_directory):
                if not filename.endswith(".psq"): 
                    continue
                game_count += 1
                with open(in_directory + filename) as file_in:
                    next(file_in)#skip header row
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            row_count += 1
data_count = row_count - (game_count * 6)#skip init rows for each game

print('game_count = ' + str(game_count))
print('row_count = ' + str(row_count))
print('data_count = ' + str(data_count))
data = numpy.zeros(shape=(data_count, 400*2))
labels = numpy.zeros(shape=(data_count, 1))

#structure data
data_index = 0
for year in range(start_year, stop_year+1):
    result_dir = 'data\gomocup' + str(year) + 'results_test'
    group = 1
    for rootdir, dirs, files in os.walk(result_dir):
        for dir in dirs:
            if not dir.startswith('Freestyle'):
                continue
            in_directory = os.path.join(result_dir, dir) + '/'
            print(in_directory)
            for filename in os.listdir(in_directory):
                if not filename.endswith(".psq"): 
                    continue
                board = numpy.zeros(shape=(20,20))
                player = 1
                eof = False
                winner = 0
                data_offset = 0
                with open(in_directory + filename) as file_in:
                    next(file_in)#header
                    row = 1
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            board[int(line.split(',')[0])-1][int(line.split(',')[1])-1] = player
                            if row >= 7:#only add non init rows as actual moves, first six rows are init moves
                                data[data_index,400:] = board.ravel().astype(int)
                                if row >= 8:
                                    data[data_index,:400] = data[data_index,400:]
                                data_index += 1
                                data_offset += 1
                        elif eof:
                            winner = int(line.split(',')[0])
                        elif line.startswith('-1'):
                            eof = True
                        if player == 1:
                            player = 2
                        else:
                            player = 1
                        row += 1
                if winner == 1:
                    labels[data_index-data_offset:data_index:2] = 1
                else:
                    labels[data_index+1-data_offset:data_index:2] = 1
            group = group +1

print(data.shape)
print(data)

print(labels.shape)
print(labels)

#shuffle and store data
shuffled_index = numpy.zeros(data_count).astype(int)
for i in range(data_count):
    shuffled_index[i] = i

#numpy.random.shuffle(shuffled_index)
print(shuffled_index)


#train_count = int(row_count * 0.6)
#test_count = int(row_count * 0.25)
#val_count = int(row_count - train_count - test_count)
train_count = int(data_count)
test_count = 0
val_count = 0
print('train_count = ' + str(train_count))
print('test_count = ' + str(test_count))
print('val_count = ' + str(val_count))

train_data = numpy.zeros(shape=(train_count, 400*2))
train_labels = numpy.zeros(shape=(train_count, 1))
test_data = numpy.zeros(shape=(test_count, 400*2))
test_labels = numpy.zeros(shape=(test_count, 1))
val_data = numpy.zeros(shape=(val_count, 400*2))
val_labels = numpy.zeros(shape=(val_count, 1))

for i in range(train_count):
    train_data[i] = data[i]
    train_labels[i] = labels[i]
#    train_data[i] = data[shuffled_index[i]]
#    train_labels[i] = labels[shuffled_index[i]]

#for i in range(test_count):
#    data_offset = i + train_count    
#    test_data[i] = data[shuffled_index[data_offset]]
#    test_labels[i] = labels[shuffled_index[data_offset]]

#for i in range(val_count):
#    data_offset = i + train_count + val_count   
#    val_data[i] = data[shuffled_index[data_offset]]
#    val_labels[i] = labels[shuffled_index[data_offset]]


print('Shuffled')

with open('preped/train_data.npy', "wb") as f:
    numpy.savetxt(f, train_data)
with open('preped/train_labels.npy', "wb") as f:
    numpy.savetxt(f, train_labels)


with open('preped/test_data.npy', "wb") as f:
    numpy.savetxt(f, test_data)
with open('preped/test_labels.npy', "wb") as f:
    numpy.savetxt(f, test_labels)

with open('preped/val_data.npy', "wb") as f:
    numpy.savetxt(f, val_data)
with open('preped/val_labels.npy', "wb") as f:
    numpy.savetxt(f, val_labels)
