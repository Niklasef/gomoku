import numpy
import os

out_directory = 'preped/'
row_count = 0
start_year = 2020
end_year = 2020
dev_mode = True
output_format = 'BIN'#'TXT' or 'BIN' 
setup_moves_count = 6

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
                    for line in file_in:
                        if line.count(',') == 2:
                            row_count += 1

print('move count = ' + str(row_count))

data = numpy.zeros(shape=(row_count-setup_moves_count, 400))
labels = numpy.zeros(shape=(row_count-setup_moves_count, 1))
i = 0
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
                eof = False
                winner = 0
                j = 0
                with open(in_directory + filename) as file_in:
                    next(file_in)#Skip initial meta line
                    next(file_in)#Skip initial setup move
                    next(file_in)#Skip initial setup move
                    next(file_in)#Skip initial setup move
                    next(file_in)#Skip initial setup move
                    next(file_in)#Skip initial setup move
                    next(file_in)#Skip initial setup move
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            data[i] = board.ravel().astype(int)
                            i = i + 1
                            j = j + 1
                            board[int(line.split(',')[0])-1][int(line.split(',')[1])-1] = current_player
                        elif eof:
                            winner = int(line.split(',')[0])
                        elif line.startswith('-1'):
                            eof = True
                        if current_player == 1:
                            current_player = 2
                        else:
                            current_player = 1
                if winner == 1:
                    labels[i-j:i:2] = 1
                else:
                    labels[i+1-j:i:2] = 1
            group = group +1

print(data)
print(data.shape)

print(labels)
print(labels.shape)

#shuffled_index = numpy.zeros(row_count).astype(int)
#for i in range(row_count):
#    shuffled_index[i] = i

#numpy.random.shuffle(shuffled_index)
#print(shuffled_index)


train_count = int((row_count - setup_moves_count) * 1)
test_count = int((row_count - setup_moves_count) * 0)
val_count = int((row_count - setup_moves_count) - train_count - test_count)
print('train_count = ' + str(train_count))
print('test_count = ' + str(test_count))
print('val_count = ' + str(val_count))

train_data = numpy.zeros(shape=(train_count, 400))
train_labels = numpy.zeros(shape=(train_count, 1))
test_data = numpy.zeros(shape=(test_count, 400))
test_labels = numpy.zeros(shape=(test_count, 1))
val_data = numpy.zeros(shape=(val_count, 400))
val_labels = numpy.zeros(shape=(val_count, 1))

for i in range(train_count):
    # train_data[i] = data[shuffled_index[i]]
    # train_labels[i] = labels[shuffled_index[i]]
    train_data[i] = data[i]
    train_labels[i] = labels[i]

for i in range(test_count):
    j = i + train_count    
    test_data[i] = data[j]
    test_labels[i] = labels[j]

for i in range(val_count):
    j = i + train_count + val_count   
    val_data[i] = data[j]
    val_labels[i] = labels[j]

print('Shuffled')

with open('preped/train_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, train_data.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, train_data)

with open('preped/train_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, train_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, train_labels)

with open('preped/test_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, test_data.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, test_data)

with open('preped/test_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, test_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, test_labels)

with open('preped/val_data.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, val_data.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, val_data)

with open('preped/val_labels.npy', "wb") as f:
    if output_format == 'TXT':
        numpy.savetxt(f, val_labels.astype(int), fmt='%i', delimiter=",")
    if output_format == 'BIN':
        numpy.save(f, val_labels)
