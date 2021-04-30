import numpy
import os

out_directory = 'preped/'
row_count = 0
for year in range(2018, 2021):
    root_dir = 'data\gomocup' + str(year) + 'results'
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
                    next(file_in)
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            row_count = row_count + 1

print('row_count = ' + str(row_count))

data = numpy.zeros(shape=(row_count, 400))
labels = numpy.zeros(shape=(row_count, 1))
i = 0
for year in range(2018, 2021):
    root_dir = 'data\gomocup' + str(year) + 'results'
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
                player = 1
                eof = False
                winner = 0
                j = 0
                with open(in_directory + filename) as file_in:
                    next(file_in)
                    lines = []
                    for line in file_in:
                        if line.count(',') == 2:
                            data[i] = board.ravel().astype(int)
                            i = i + 1
                            j = j + 1
                            board[int(line.split(',')[0])-1][int(line.split(',')[1])-1] = player
                        elif eof:
                            winner = int(line.split(',')[0])
                        elif line.startswith('-1'):
                            eof = True
                        if player == 1:
                            player = 2
                        else:
                            player = 1
                if winner == 1:
                    labels[i-j:i:2] = 1
                else:
                    labels[i+1-j:i:2] = 1
            group = group +1

print(data)
print(data.shape)

print(labels)
print(labels.shape)

shuffled_index = numpy.zeros(row_count).astype(int)
for i in range(row_count):
    shuffled_index[i] = i

numpy.random.shuffle(shuffled_index)
print(shuffled_index)


train_count = int(row_count * 0.6)
test_count = int(row_count * 0.25)
val_count = int(row_count - train_count - test_count)
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
    train_data[i] = data[shuffled_index[i]]
    train_labels[i] = labels[shuffled_index[i]]

for i in range(test_count):
    j = i + train_count    
    test_data[i] = data[shuffled_index[j]]
    test_labels[i] = labels[shuffled_index[j]]

for i in range(val_count):
    j = i + train_count + val_count   
    val_data[i] = data[shuffled_index[j]]
    val_labels[i] = labels[shuffled_index[j]]

print('Shuffled')

with open('preped/train_data.npy', "wb") as f:
    numpy.save(f, train_data)
#    numpy.savetxt(f, train_data.astype(int), fmt='%i', delimiter=",")
with open('preped/train_labels.npy', "wb") as f:
    numpy.save(f, train_labels)
#    numpy.savetxt(f, train_labels.astype(int), fmt='%i', delimiter=",")


with open('preped/test_data.npy', "wb") as f:
    numpy.save(f, test_data)
#    numpy.savetxt(f, test_data.astype(int), fmt='%i', delimiter=",")
with open('preped/test_labels.npy', "wb") as f:
    numpy.save(f, test_labels)
#    numpy.savetxt(f, test_labels.astype(int), fmt='%i', delimiter=",")

with open('preped/val_data.npy', "wb") as f:
    numpy.save(f, val_data)
#    numpy.savetxt(f, val_data.astype(int), fmt='%i', delimiter=",")
with open('preped/val_labels.npy', "wb") as f:
    numpy.save(f, val_labels)
#    numpy.savetxt(f, val_labels.astype(int), fmt='%i', delimiter=",")    
