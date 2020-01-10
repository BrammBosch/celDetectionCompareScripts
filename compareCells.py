import csv
import multiprocessing
import os
import math
import matplotlib.pyplot as plt
import mplcursors

from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def main():
    '''
    This function makes use of multiprocessing to show 4 interactive plots at the same time of the 4 versions.
    :return:
    '''
    versionList = ['66632', '66633', '66634', '190925']

    for version in versionList:
        clearFile = open(
            "/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances" + version + ".txt", "w+")
        clearFile.write('')
        clearFile.close()

    pool = multiprocessing.Pool()
    pool.map(callFunc, versionList)


def callFunc(version):
    '''

    :param version: This parameter contains the version number and tells the program which dataset to retrieve.
    :return:
    '''
    variatie = 4
    includeOutliers = False

    listPipeline = []

    testWord = 'Denoise'

    path = '/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/v2/' + version + 'All/'
    # path = '/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/' + version + '/'
    # path = '/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/v2/' + version + testWord + '/'

    for filename in os.listdir(path):
        with open(path + filename) as f:
            listPipelineTemp = list(csv.reader(f))
            del listPipelineTemp[0]
        listPipeline.append([filename, listPipelineTemp])

    with open(
            '/home/bram/Desktop/Jaar_3/donders/report/verslagData/2019-10-29 Data for Bram/csv/S1_' + version + '_Cell_Count_03.csv') as f:
        listCounted = list(csv.reader(f))
        del listCounted[0]

    counted = len(listCounted) + 1

    makeGraph(listPipeline, counted, version, variatie, listCounted, includeOutliers)


def func(key, listCounted, variatie, counted):
    '''

    :param key: The name of pipeline with all cell locations
    :param listCounted: The list of manually counted cells
    :param variatie: The amount of variation in cell locations allowed
    :param counted: The amount of manually counted cells.
    :return:
    This functon returns
    The data stored locally as listDataTemp
    The amount of cells counted in the pipelines as X
    The amount of matches as Y

    '''
    arivis = len(key[1])
    i = 0
    a = 0

    for coord in listCounted:

        # print(listCounted[a])
        for pipelineCoord in key[1]:
            #print(coord[0] + ' ' + pipelineCoord[0] + '-' + coord[1] + ' ' + pipelineCoord[1])
            if float(coord[0]) - variatie <= float(pipelineCoord[0]) <= float(coord[0]) + variatie:
                # print('y ' + coord[0] + ' ' + pipelineCoord[0])
                if float(coord[1]) - variatie <= float(pipelineCoord[1]) <= float(coord[1]) + variatie:
                    # print('ye ' + coord[1] + ' ' + pipelineCoord[1])
                    # print('yes ' + coord[2] + ' ' + pipelineCoord[2])
                    if float(coord[2]) - variatie <= float(pipelineCoord[2]) <= float(coord[2]) + variatie:
                        # print('match ' + coord[0] + '-' + pipelineCoord[0] + '    ' + coord[1] + '-' + pipelineCoord[1] + '    ' + coord[2] + '-' + pipelineCoord[2])
                        i += 1
                        # print('match ' + pipelineCoord[0] + ' ' + pipelineCoord[1] + ' ' + pipelineCoord[2])
                        break
        a += 1

    x = arivis
    y = i


    print('\n\n' + key[0])
    print('manually counted ' + str(counted))
    print('matches ' + str(i))
    print('counts in arivis ' + str(arivis))
    if i != 0:
        fn = (((counted-i)/counted)*100)
        if i > arivis:
            fp = (((i-arivis)/i) * 100)
        else:
            fp = (((arivis-i)/arivis) * 100)

        print('False negative ' + str(fn))
        print('false positives ' + str(fp))


    else:
        fn= 100
        fp = 0
        #print('0')


    # print('Manual counts: ' + str(counted))
    # print('pipeline counts: ' + str(arivis))
    # print('Matches: ' + str(i))
    # print('Cells not matched: ' + str(counted - i))
    # print('Cells too many: ' + str(arivis - counted))

    # listDataTemp = []
    versionAndFilter = key[0].replace('.csv', '').split('_')
    # print(key)

    if versionAndFilter[2:] != []:
        listDataTemp = (versionAndFilter[1], versionAndFilter[2:], arivis, i, str(counted - i), arivis - counted)
    else:
        #print(versionAndFilter)
        listDataTemp = (versionAndFilter[1], 'None', arivis, i, str(counted - i), arivis - counted)

    return listDataTemp, x, y, fn, fp


def makeGraph(listPipeline, counted, version, variatie, listCounted, outliers):
    '''
    :param listPipeline: A list containing the name of a pipeline and all found cell coordinates
    :param counted: The amount of manually counted cells in the version
    :param version: Which version is being plotted
    :param variatie: How much variation in the cell locations is allowed
    :param listCounted: The coordinates of the manually counted cells.
    :param outliers: A boolean to determine whether to include outliers in the plots.
    :return:
    '''
    listX = []
    listY = []
    listLabel = []
    listFN = []
    listFP = []
    headers = ['Cell Finder', 'Image processing applied', 'Cells found', 'Matches',
               'Cells  not corresponding to manually found cells', 'Cells too many']
    data = []
    data.append(version)
    data.append(headers)


    for key in listPipeline:
        listDataTemp, x, y, fn, fp = func(key, listCounted, variatie, counted)

        # print(listDataTemp)
        data.append(listDataTemp)
        dist = math.sqrt((x - counted) ** 2 + (y - counted) ** 2)
        if not outliers and dist < 600:
            listX.append(x)
            listY.append(y)
            key[0] = key[0].replace('_', ' ').replace('.csv', '')
            listLabel.append(key[0])
            listFN.append(fn)
            listFP.append(fp)

        elif outliers:
            listX.append(x)
            listY.append(y)
            key[0] = key[0].replace('_', ' ').replace('.csv', '')
            listLabel.append(key[0])
            listFN.append(fn)
            listFP.append(fp)
    makeCSV(data)
    refpoint = [counted]
    refpoint2 = refpoint
    listLine = [counted, counted]
    listLine2 = [0, max(listY)]
    listLine3 = [0, max(listX)]
    listLine4 = [counted, counted]
    legend_elements = [
        Patch(facecolor='b', edgecolor='r', alpha=0.2, label='Not enough counts but more matches than cells found'),
        Patch(facecolor='y', edgecolor='r', alpha=0.2, label='Not enough matches and too many cells'),
        Patch(facecolor='cyan', edgecolor='r', alpha=0.2, label='Not enough counts and less matches than cells found'),
        Line2D([], [], color='g', label='All found cells match'),

        # Patch(facecolor='r', edgecolor='r', alpha=0.2, label='Too many matches and not enough cells'),
        Line2D([], [], marker='*', color='w', label='ClearMap', linestyle='None', mec='k'),
        #Line2D([], [], marker='o', color='w', label='Machine learning', linestyle='None', mec='k'),
        Line2D([], [], marker='s', color='w', label='Blobfinder', linestyle='None', mec='k')]
    fig = plt.figure()
    fig.suptitle('', fontsize=14, fontweight='bold')

    ax = fig.add_subplot()
    ax.set_title('Pipeline results for ' + version + ' with ' + str(counted) + ' manual counts.')
    ax.set_xlabel('Pipeline counts')
    ax.set_ylabel('Matches')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    point = ax.plot(refpoint, refpoint2, 'go',
                    label='Perfect data\nx = ' + str(refpoint[0]) + '\ny = ' + str(refpoint[0]))
    # ax.plot(listLine, listLine2, 'r--', label='Divide cell count')
    ax.plot(listLine3, listLine4, 'r--', label='Divide matches')

    ySizeD = plt.ylim()[0]
    ySizeU = plt.ylim()[1]

    xSizeL = plt.xlim()[0]
    xSizeR = plt.xlim()[1]

    listCoord1 = [0, refpoint2[0]]
    listCoord2 = listCoord1
    ax.plot(listCoord1, listCoord2, 'g-', label='Perfect matches line')
    plt.fill([counted, 0, 0, counted], [counted, counted, 0, counted], 'b', alpha=0.2, edgecolor='r')
    plt.fill([counted, counted, 0, counted], [counted, counted, 0, 0], 'cyan', alpha=0.2, edgecolor='r')
    # plt.fill([counted, xSizeL, xSizeL, counted], [counted, counted, ySizeU, ySizeU], 'r', alpha=0.2, edgecolor='r')
    plt.fill([counted, xSizeR, xSizeR, counted], [counted, counted, 0, 0], 'y', alpha=0.2, edgecolor='r')

    i = 0
    colorList = []
    allList = []
    for z in listX:
        dist = math.sqrt((listX[i] - counted) ** 2 + (listY[i] - counted) ** 2)
        dist = truncate(dist)
        listFilters = listLabel[i].split(' ')
        match = listY[i]
        total = listX[i]
        if match > total:
            match = total - (match - total)

        if total > counted:
            total = counted - (total - counted)

        try:


            allList.append([listFilters, dist, match / listX[i], total,listFN[i],listFP[i]])
        except ZeroDivisionError:
            allList.append([listFilters, dist, 0, listX[i],listFN[i],listFP[i]])

        keyWord = 'particle'

        # color, name = colorFilter(listFilters, keyWord)
        color, name = colorFirstFilter(listFilters)

        if color not in colorList:
            legend_elements.append(Line2D([], [], marker='o', color=color, label=name, linestyle='None'))
        colorList.append(color)

        if 'machineLearn' in listLabel[i]:
            # point += ax.plot(listX[i], listY[i], 'o' + color,
            point += ax.plot(listX[i], listY[i], 'o' + color,
                             label=listLabel[i] + '\nmatches(y) = ' + str(listY[i]) + '\nCounts in program(x) = ' + str(
                                 listX[i]) + '\nDistance to perfect = ' + str(dist))
        elif 'blobFinder' in listLabel[i]:

            point += ax.plot(listX[i], listY[i], 's' + color,
                             label=listLabel[i] + '\nmatches(y) = ' + str(listY[i]) + '\nCounts in program(x) = ' + str(
                                 listX[i]) + '\nDistance to perfect = ' + str(dist))


        elif 'ClearMap' in listLabel[i]:
            point += ax.plot(listX[i], listY[i], '*k',
                             label=listLabel[i] + '\nmatches(y) = ' + str(listY[i]) + '\nCounts in program(x) = ' + str(
                                 listX[i]) + '\nDistance to perfect = ' + str(dist))

        i += 1
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=legend_elements)
    mplcursors.cursor(point, hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

    writeList(allList, version)

    plt.show()


def truncate(n):
    '''
    This function is used to truncate an integer
    :param n:
    :return:
    '''
    return int(n * 1000) / 1000


def makeCSV(data):
    '''
    This functions creates a csv file that can be opened in excel to show the results of all scripts.
    :param data: The list with all the information
    :param version: The version number
    :return:
    '''
    version = data[0]
    del data[0]
    with open('/home/bram/Desktop/Jaar_3/donders/report/celDetectionCsv/' + version + '.txt', 'w+') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def writeList(allList, version):
    '''

     This function is used to store data locally to use in another script.
    :param allList: A list of data
    :return:
    '''
    f = open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances" + version + ".txt", "a")


    f.write(str(allList))
    f.close()


def colorFilter(listFilters, keyWord):
    '''
    This function can be called to color the pipelines based on one of the filters
    :param listFilters: The combinations of filters used
    :param keyWord: Which filter to base the color in the plot on.
    :return:
    '''
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
    '''
    This functions colors the filters based on the first filter used.
    :param listFilters: The combinations of filters used
    :return:
    '''
    if len(listFilters) > 2:
        if 'backgroundCor' in listFilters[2]:
            color = 'r'
            name = 'background correction'
        elif 'denoise' in listFilters[2]:
            color = 'b'
            name = 'denoising filter'
        elif 'enhance' in listFilters[2]:
            color = 'c'
            name = 'enhancement filter'
        elif 'particleEnhance' in listFilters[2]:
            color = 'g'
            name = 'particle enhancement filter'
        elif 'morphology' in listFilters[2]:
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
