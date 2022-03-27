import numpy
import os

out_directory = 'preped/'
data_count = 0
start_year = 2020
end_year = 2020
dev_mode = True
print_final_board_state = False
# output_format = 'TXT'
output_format = 'BIN'
setup_moves = []
setup_mode = True

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
                setup_mode = True
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    lines = []
                    setup_moves.append(0)
                    for line in file_in:
                        if line.count(',') == 2:
                            data_count += 1
                            if int(line.split(',')[2]) == 0 and setup_mode:
                                setup_moves[-1] += 1
                            else:
                                setup_mode = False
                    data_count -= setup_moves[-1]
                    data_count -= 1 #skip learning of winning board state

print('move count = ' + str(data_count))
print('setup_moves length = ' + str(len(setup_moves)))
print(setup_moves)
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
                current_player = 0
                
                #Iterate moves in game
                j = 0
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    lines = []
                    for line in file_in:
                        if i >= data_count:#This is a bug, sometimes i gets larger than the data matrix
                            break
                        if current_player == 1:
                            current_player = -1
                        else:
                            current_player = 1
                        if line.count(',') == 2:
                            col = int(line.split(',')[0])
                            row = int(line.split(',')[1])
                            board[row-1][col-1] = current_player
                            j += 1
                            if j <= setup_moves[game_i]:
                                continue
                            label = numpy.zeros(shape=(20, 20))
                            label[row-1][col-1] = 1
                            labels[i-1] = label.ravel().astype(int)
                            data[i] = board.astype(int)

                            #invert board so all moves are from black perspective
                            if current_player == -1:
                                data[i] = numpy.where(data[i]==1, 3, data[i])
                                data[i] = numpy.where(data[i]==-1, 1, data[i])
                                data[i] = numpy.where(data[i]==3, 1, data[i])
                            i += 1
                    i -= 1#skip learning of last (winning) board state
                game_i += 1
                if print_final_board_state:
                    os.system("python print_board.py " + numpy.array2string(board.ravel().astype(int), max_line_width=10000, separator='_').replace(' ',''))
            group = group +1

print(data)
print(data.shape)

print(labels)
print(labels.shape)

train_count = int((data_count) * 0.7)
test_count = int((data_count) * 0.15)
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
