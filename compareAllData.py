import ast
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import statistics
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

def main():
    versionList = ['66632', '66633', '66634', '190925']
    for version in versionList:
        f = open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances" + version + ".txt", "r")
        data = f.read()
        x = ast.literal_eval(data)
        if version == '66632':
            data66632 = x
        elif version == '66633':
            data66633 = x
        elif version == '66634':
            data66634 = x
        else:
            data190925 = x

    totalList = []
    totalListSmall = []
    for filter in data66632:
        for filter2 in data66633:
            for filter3 in data66634:
                for filter4 in data190925:
                    if filter[0][1:] == filter2[0][1:] == filter3[0][1:] == filter4[0][1:]:

                        sample = [int(filter[1]), int(filter2[1]), int(filter3[1]), int(filter4[1])]

                        totalList.append([str(filter[0][1:]), int(filter[1] + filter2[1] + filter3[1] + filter4[1]),statistics.stdev(sample)])
                        if int(filter[1] + filter2[1] + filter3[1] + filter4[1]) < 1000:
                            totalListSmall.append([str(filter[0][1:]), int(filter[1] + filter2[1] + filter3[1] + filter4[1]),statistics.stdev(sample)])


    makeGraph(totalListSmall)


# print(allCombinations)
# print(combinationValues)

def sortSecond(val):
    return val[1]


# list1 to demonstrate the use of sorting
# using using second key

# sorts the array in ascending according to
# second element
def makeGraph(totalList):
    allCombinationsList = []
    allCombinations = []
    sdList = []
    combinationValues = []
    totalList.sort(key=sortSecond)
    #print(totalList)

    for value in totalList:
        allCombinations.append(value[0].replace("'", "").replace('[','').replace(']',''))
        combinationValues.append(value[1])
        allCombinationsList.append(ast.literal_eval(value[0]))
        sdList.append(value[2])
    objects = allCombinations

    y_pos = np.arange(len(objects))
    performance = combinationValues
    legend_elements = [Patch(facecolor='b', alpha=0.5, label='Machine Learning'),
                       Patch(facecolor='r', alpha=0.5, label='Blob finder'),
                       Patch(facecolor='k', alpha=0.5, label='ClearMap'),]
    i = 0
    for item in allCombinationsList:
        #print(item[0])
        if item[0] == 'machineLearn':

            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='blue',xerr=sdList[i])
        elif item[0] == 'ClearMap':
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='black',xerr=sdList[i])

        else:
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='red',xerr= sdList[i])

        i += 1

    plt.yticks(y_pos, objects,fontsize=8)
    plt.xlabel('Distance to the perfect score')
    plt.title('Combination of the results from 4 datasets')
    for i, v in enumerate(combinationValues):
        plt.text(v +sdList[i], i - .4, str(v), color='black',fontsize=8)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.2)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, - 0.25), handles=legend_elements)

    plt.show()

main()