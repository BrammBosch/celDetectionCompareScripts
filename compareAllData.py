import ast
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import statistics
import numpy as np

plt.rcdefaults()


def main():
    '''
    In this function the datasets are read from local files and stored in list variables
    :return:
    '''
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


def sortSecond(val):
    '''
    A function used to sort on an index in a list.
    :param val: return the value to sort on
    :return:
    '''
    return val[1]


def percentageToCount(totalList):
    '''
    This function creates a scatterplot where the percentage of correct counts is compared against the percentage of
    cells found.
    :param totalList: a list containing all values for the datasets.
    :return:
    '''
    fig = plt.figure()
    fig.suptitle('', fontsize=14, fontweight='bold')

    ax = fig.add_subplot()
    ax.set_title('Amount of cells found with percentage that matches')
    ax.set_xlabel('percentage of cells')
    ax.set_ylabel('percentage correct')
    listX = []
    listY = []
    listFilters = []
    for item in totalList:
        listY.append(item[3] * 100)
        listX.append(item[4] * 100)
        listFilters.append(item[0])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    legend_elements = [  # Patch(facecolor='b', edgecolor='r', alpha=0.2, label='Not all cells were found'),
        # Patch(facecolor='y', edgecolor='r', alpha=0.2, label='More cells are detected than are present in the dataset'),
        # Patch(facecolor='cyan', edgecolor='r', alpha=0.2, label=''),
        # Patch(facecolor='r', edgecolor='r', alpha=0.2, label=''),
        Line2D([], [], marker='*', color='w', label='ClearMap', linestyle='None', mec='k'),
        Line2D([], [], marker='o', color='w', label='Machine learning', linestyle='None', mec='k'),
        Line2D([], [], marker='s', color='w', label='Blobfinder', linestyle='None', mec='k')]

    point = ax.plot(100, 100, 'go', label='Perfect data\nx = ' + str(100) + '\ny = ' + str(100))

    i = 0
    colorList = []

    for z in listX:
        filter = ast.literal_eval(listFilters[i])

        keyWord = 'particle'
        color, name = colorFilter(filter, keyWord)

        # color, name = colorFirstFilter(filter)

        if color not in colorList:
            legend_elements.append(Line2D([], [], marker='o', color=color, label=name, linestyle='None'))
        colorList.append(color)

        if 'machineLearn' in filter[0]:
            point += ax.plot(listX[i], listY[i], 'o' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i])) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i])) + '%')
        elif 'blobFinder' in filter[0]:
            point += ax.plot(listX[i], listY[i], 's' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i])) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i])) + '%')
        else:
            point += ax.plot(listX[i], listY[i], '*' + color,
                             label=totalList[i][0] + '\nAverage percentage correct = ' + str(
                                 "{:.1f}".format(listY[i])) + '%\nAverage amount of cells found = ' + str(
                                 "{:.1f}".format(listX[i])) + '%')
        i += 1

    ax.plot([0, 100], [100, 100], 'g--', label='Divide matches')
    ax.plot([100, 100], [100, 0], 'g--', label='Divide matches')

    mplcursors.cursor(point, hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_elements)
    ax.set_ylim(ymin=0)
    plt.show()


def makeGraph(totalList):
    '''
    This function creates a bar plot to compare the distances in the perfect point plotted in the datasets for each
    pipelines.
    :param totalList: a list containing all values for the datasets.
    :return:
    '''
    allCombinationsList = []
    allCombinations = []
    sdList = []
    combinationValues = []
    totalList.sort(key=sortSecond)

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
        if item[0] == 'machineLearn':

            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='blue', xerr=sdList[i])
        elif item[0] == 'ClearMap':
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='black', xerr=sdList[i])

        else:
            plt.barh(y_pos[i], performance[i], align='center', alpha=0.5, color='red', xerr=sdList[i])

        i += 1

    plt.yticks(y_pos, objects, fontsize=8)
    plt.xlabel('Distance to the perfect score')
    plt.title('Distance to the perfect score in all datasets combined with standard deviation')
    for i, v in enumerate(combinationValues):
        plt.text(v + sdList[i], i - .4, str(v), color='black', fontsize=8)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.2)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, - 0.25), handles=legend_elements)

    plt.show()


def colorFilter(listFilters, keyWord):
    '''
    This filter is used to give pipelines using a certain keyword a color value in the plots.
    :param listFilters: The list of filters used in the pipeline.
    :param keyWord: A string with a keyword which should be given the color blue in the plot.
    :return:
    '''
    if len(listFilters) > 2:
        if keyWord in listFilters[2] or keyWord in listFilters[1]:
            color = 'b'
            name = keyWord
        else:
            color = 'k'
            name = 'else'
    elif len(listFilters) > 1:
        if keyWord in listFilters[1]:
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
    '''
    This function is used to color the results based on the first filter used in the pipelines.
    :param listFilters: A list of filters used in the pipelines.
    :return:
    '''
    if len(listFilters) > 2:
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
