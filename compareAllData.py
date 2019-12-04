import ast
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import statistics

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing


def main():
    versionList = ['66632', '66633', '66634', '190925']
    for version in versionList:
        f = open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances" + version + ".txt",
                 "r")
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

                        averagePercentage = (filter[2] + filter2[2] + filter3[2] + filter4[2]) / 4
                        totalPercentage = (filter[3] + filter2[3] + filter3[3] + filter4[3]) / 657

                        sample = [int(filter[1]), int(filter2[1]), int(filter3[1]), int(filter4[1])]

                        totalList.append([str(filter[0][1:]), int(filter[1] + filter2[1] + filter3[1] + filter4[1]),
                                          statistics.stdev(sample), averagePercentage, totalPercentage])
                        if int(filter[1] + filter2[1] + filter3[1] + filter4[1]) < 1000:
                            totalListSmall.append(
                                [str(filter[0][1:]), int(filter[1] + filter2[1] + filter3[1] + filter4[1]),
                                 statistics.stdev(sample)])

    makeGraph(totalList)
    percentageToCount(totalList)


# print(allCombinations)
# print(combinationValues)

def sortSecond(val):
    return val[1]


# list1 to demonstrate the use of sorting
# using using second key

# sorts the array in ascending according to
# second element
def percentageToCount(totalList):
    fig = plt.figure()
    fig.suptitle('', fontsize=14, fontweight='bold')

    ax = fig.add_subplot()
    ax.set_title('percentage count ratio')
    ax.set_xlabel('percentage of cells found')
    ax.set_ylabel('percentage correct')
    listX = []
    listY = []
    listFilters = []
    for item in totalList:
        listY.append(item[3])
        listX.append(item[4])
        listFilters.append(item[0])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    legend_elements = [Patch(facecolor='b', edgecolor='r', alpha=0.2, label=''),
                       Patch(facecolor='y', edgecolor='r', alpha=0.2, label=''),
                       Patch(facecolor='cyan', edgecolor='r', alpha=0.2, label=''),
                       Patch(facecolor='r', edgecolor='r', alpha=0.2, label=''),
                       Line2D([], [], marker='*', color='k', label='ClearMap', linestyle='None'),
                       Line2D([], [], marker='o', color='k', label='Machine learning', linestyle='None'),
                       Line2D([], [], marker='s', color='k', label='Blobfinder', linestyle='None')]


    point = ax.plot(1, 1, 'go',
                    label='Perfect data\nx = ' + str(1) + '\ny = ' + str(1))

    i = 0
    colorList = []

    for z in listX:
        filter = ast.literal_eval(listFilters[i])
        color, name = colorFirstFilter(filter)

        if color not in colorList:
            legend_elements.append(Line2D([], [], marker='o', color=color, label=name, linestyle='None'))
        colorList.append(color)

        if 'machineLearn' in filter[0]:
            point += ax.plot(listX[i], listY[i], 'o' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i]*100)) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i]*100)) + '%')
        elif 'blobFinder' in filter[0]:
            point += ax.plot(listX[i], listY[i], 's' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i] * 100)) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i]*100)) + '%')
        else:
            point += ax.plot(listX[i], listY[i], '*' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i]*100)) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i]*100)) + '%')
        i += 1

    ySizeD = plt.ylim()[0]
    ySizeU = plt.ylim()[1]

    xSizeL = plt.xlim()[0]
    xSizeR = plt.xlim()[1]

    squares = 1
    # squares2 = 657

    plt.fill([squares, xSizeL, xSizeL, squares], [squares, squares, ySizeD, ySizeD], 'b', alpha=0.2, edgecolor='r')
    plt.fill([squares, xSizeR, xSizeR, squares], [squares, squares, ySizeU, ySizeU], 'cyan', alpha=0.2, edgecolor='r')
    plt.fill([squares, xSizeL, xSizeL, squares], [squares, squares, ySizeU, ySizeU], 'r', alpha=0.2, edgecolor='r')
    plt.fill([squares, xSizeR, xSizeR, squares], [squares, squares, ySizeD, ySizeD], 'y', alpha=0.2, edgecolor='r')

    mplcursors.cursor(point, hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_elements)

    plt.show()


def makeGraph(totalList):
    allCombinationsList = []
    allCombinations = []
    sdList = []
    combinationValues = []
    totalList.sort(key=sortSecond)
    # print(totalList)

    for value in totalList:
        allCombinations.append(value[0].replace("'", "").replace('[', '').replace(']', ''))
        combinationValues.append(value[1])
        allCombinationsList.append(ast.literal_eval(value[0]))
        sdList.append(value[2])
    objects = allCombinations

    y_pos = np.arange(len(objects))
    performance = combinationValues
    legend_elements = [Patch(facecolor='b', alpha=0.5, label='Machine Learning'),
                       Patch(facecolor='r', alpha=0.5, label='Blob finder'),
                       Patch(facecolor='k', alpha=0.5, label='ClearMap'), ]
    i = 0
    for item in allCombinationsList:
        # print(item[0])
        if item[0] == 'machineLearn':

            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='blue', xerr=sdList[i])
        elif item[0] == 'ClearMap':
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='black', xerr=sdList[i])

        else:
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='red', xerr=sdList[i])

        i += 1

    plt.yticks(y_pos, objects, fontsize=8)
    plt.xlabel('Distance to the perfect score')
    plt.title('Combination of the results from 4 datasets')
    for i, v in enumerate(combinationValues):
        plt.text(v + sdList[i], i - .4, str(v), color='black', fontsize=8)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.2)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, - 0.25), handles=legend_elements)

    plt.show()


def colorFilter(listFilters, keyWord):
    if len(listFilters) > 3:
        if keyWord in listFilters[2] or keyWord in listFilters[3]:
            color = 'b'
            name = keyWord
        else:
            color = 'k'
            name = 'else'
    elif len(listFilters) > 2:
        if keyWord in listFilters[2]:
            color = 'b'
            name = keyWord
        else:
            color = 'k'
            name = 'else'
    else:
        color = 'k'
        name = 'else'
    return color, name


def colorFirstFilter(listFilters):
    print(listFilters)
    if len(listFilters) >= 2:
        print(listFilters[1])
        if 'backgroundCor' in listFilters[1]:
            color = 'r'
            name = 'background correction'
        elif 'denoise' in listFilters[1]:
            color = 'b'
            name = 'denoising filter'
        elif 'enhance' in listFilters[1]:
            color = 'c'
            name = 'enhancement filter'
        elif 'particleEnhance' in listFilters[1]:
            color = 'g'
            name = 'particle enhancement filter'
        elif 'morphology' in listFilters[1]:
            color = 'm'
            name = 'morphology filter'
        else:
            color = 'k'
            name = 'no filter'
    else:
        color = 'k'
        name = 'no filter'
    return color, name



main()
