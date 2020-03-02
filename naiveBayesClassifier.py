# author: Shamiul Hasan
import math

with open('train.txt') as f:
    lines = [line.rstrip() for line in f]

first_line = lines[0].split()

numberOfFeatures = int(first_line[0])
numberOfClasses = int(first_line[1])
numberOfSamples = int(first_line[2])

print('input: ', lines)

dataset = []

for line in lines[1:]:
    line = line.split()
    data = []
    for number in line:
        data.append(float(number))
    dataset.append(data)

print('dataset: ', dataset)
uniqueClassList = []

for row in dataset:
    uniqueClassList.append(int(row[len(row) - 1]))

uniqueClassList = list(set(uniqueClassList))
uniqueClassNo = len(uniqueClassList)

print('Unique Classes: ', uniqueClassList)

totalSampleNo = len(dataset)

p_class = dict()
for className in uniqueClassList:
    classCount = 0
    for row in dataset:
        if row[len(row) - 1] == className:
            classCount += 1
    p_class[className] = classCount / totalSampleNo

print('priori : ', p_class)

# featureIdx = 0
mean_dict = dict()
for className in uniqueClassList:
    if className not in mean_dict:
        mean_dict[className] = dict()

    for featureIdx in range(numberOfFeatures):
        # if className not in mean_dict:
        #     mean_dict[className][featureIdx] = dict()

        count = 0
        sum = 0
        mean = 0
        for row in dataset:
            if row[len(row) - 1] == className:
                count += 1
                sum += row[featureIdx]
        mean = sum / count
        mean_dict[className][featureIdx] = mean

print('mean dict: ', mean_dict)

sigma_dict = dict()

for className in uniqueClassList:
    if className not in sigma_dict:
        sigma_dict[className] = dict()

    for featureIdx in range(numberOfFeatures):
        count = 0
        sum = 0
        mean = 0
        for row in dataset:
            if row[len(row) - 1] == className:
                count += 1
                # print(mean_dict[className][featureIdx])
                # print('jlsd')
                sum = sum + ((row[featureIdx] - mean_dict[className][featureIdx]) * (
                        row[featureIdx] - mean_dict[className][featureIdx]))
        mean = sum / count
        mean = math.sqrt(mean)
        sigma_dict[className][featureIdx] = mean

print('sigma dict: ', sigma_dict)

##################
# test

with open('test.txt') as f:
    lines = [line.rstrip() for line in f]

print('test set: ', lines)

dataset_test = []

for line in lines:
    line = line.split()
    data = []
    for number in line:
        data.append(float(number))
    dataset_test.append(data)

print('dataset: ', dataset_test)


def gaussian(className, featureIdx, featureVal):
    p = 1 / math.sqrt(2 * math.pi * sigma_dict[className][featureIdx] ** 2)
    p *= (math.exp(
        -((featureVal - mean_dict[className][featureIdx]) ** 2) / (2 * (sigma_dict[className][featureIdx] ** 2))))
    return p


print('Result Probability: ')
ans = []
total_test_sample = len(dataset_test)

count = 0
all = []
right = 0
wrong = 0
for row in dataset_test:
    ans.clear()
    for className in uniqueClassList:
        mul = 1
        for featureIdx in range(int(numberOfFeatures)):
            featureVal = row[featureIdx]
            mul *= gaussian(className, featureIdx, featureVal)
        mul *= p_class[className]
        ans.append(mul)

    pd = 1 + ans.index(max(ans))
    all.append(pd)
    if pd == dataset_test[count][len(row) - 1]:
        right += 1
    else:
        wrong += 1

    print('Predicted Class for ', count, ': ', 1 + ans.index(max(ans)))
    count += 1

print('right percentage: ', right * 100 / (right + wrong))
print('wrong percentage: ', wrong * 100 / (right + wrong))
