# author: Shamiul Hasan

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
        data.append(int(number))
    dataset.append(data)

uniqueClassList = []

for row in dataset:
    uniqueClassList.append(row[len(row) - 1])

uniqueClassList = list(set(uniqueClassList))
uniqueClassNo = len(uniqueClassList)

print('Unique Classes: ', uniqueClassList)

uniqueFeatureValList = []
for i in range(numberOfFeatures):
    tem = set()
    for row in dataset:
        tem.add(row[i])
    uniqueFeatureVal = list(tem)
    uniqueFeatureValList.append(uniqueFeatureVal)

print('Unique Feature Value List: ', uniqueFeatureValList)

# probability_dict[1] = dict()
# probability_dict[1][1] = 3
# print(probability_dict[1][1])


probability_dict = dict()

featureIdx = 0
for featureRow in uniqueFeatureValList:
    if featureIdx not in probability_dict:
        probability_dict[featureIdx] = dict()
    for thisFeatureValue in featureRow:
        # print(thisFeatureValue)
        if thisFeatureValue not in probability_dict[featureIdx]:
            probability_dict[featureIdx][thisFeatureValue] = dict()

        for thisClassName in uniqueClassList:
            sum = 0
            totalThisClass = 0
            for dataRow in dataset:
                if dataRow[len(dataRow) - 1] == thisClassName:
                    totalThisClass += 1
                if dataRow[featureIdx] == thisFeatureValue and dataRow[len(dataRow) - 1] == thisClassName:
                    sum += 1
            # if thisClassName not in probability_dict[featureIdx][thisFeatureValue]:
            probability_dict[featureIdx][thisFeatureValue][thisClassName] = sum / totalThisClass
    featureIdx += 1

print('posteriori probability dictionary: ', probability_dict)

totalSampleNo = len(dataset)

p_class = dict()
for className in uniqueClassList:
    classCount = 0
    for row in dataset:
        if row[len(row) - 1] == className:
            classCount += 1
    p_class[className] = classCount / totalSampleNo

print('priori : ', p_class)

# testing
test = [10, 18]

print('Result Probability: ')
ans = []
for className in uniqueClassList:
    mul = 1
    for featureIdx in range(len(test)):
        featureVal = test[featureIdx]
        # print(featureVal)
        mul *= probability_dict[featureIdx][featureVal][className]
    mul *= p_class[className]
    ans.append(mul)
    print('For ', className, ': ', mul)

print()
print('#################')
print('Predicted Class: ', ans.index(max(ans)))
print('#################')
