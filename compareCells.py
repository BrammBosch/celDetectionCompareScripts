import csv
import multiprocessing
import os
import math
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def main():
    versionList = ['66632', '66633', '66634', '190925']

    for version in versionList:


        clearFile = open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances"+ version + ".txt", "w+")
        clearFile.write('')
        clearFile.close()

    pool = multiprocessing.Pool()
    pool.map(callFunc, versionList)


def callFunc(version):
    variatie = 4
    dictPipeline = []
    path = '/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/' + version + '/'
    for filename in os.listdir(path):
        with open(path + filename) as f:
            listPipeline = list(csv.reader(f))
            del listPipeline[0]
        dictPipeline.append([filename, listPipeline])
    # print(dictPipeline)
    with open(
            '/home/bram/Desktop/Jaar_3/donders/report/verslagData/2019-10-29 Data for Bram/csv/S1_' + version + '_Cell_Count_03.csv') as f:
        listCounted = list(csv.reader(f))
        del listCounted[0]

    counted = len(listCounted) + 1

    makeGraph(dictPipeline, counted, version, variatie, listCounted)


def func(key, listCounted, variatie, counted):
    arivis = len(key[1])
    i = 0
    a = 0

    for coord in listCounted:

        # print(listCounted[a])
        for pipelineCoord in key[1]:
            # print(coord[0] + ' ' + pipelineCoord[0] + '-' + coord[1] + ' ' + pipelineCoord[1])
            if float(coord[0]) - variatie <= float(pipelineCoord[0]) <= float(coord[0]) + variatie:
                # print('y ' + coord[0] + ' ' + pipelineCoord[0])
                if float(coord[1]) - variatie <= float(pipelineCoord[1]) <= float(coord[1]) + variatie:
                    # print('ye ' + coord[1] + ' ' + pipelineCoord[1])
                    # print('yes ' + coord[2] + ' ' + pipelineCoord[2])
                    if float(coord[2]) - variatie <= float(pipelineCoord[2]) <= float(coord[2]) + variatie:
                        # print('match ' + coord[0] + '-' + pipelineCoord[0] + '    ' + coord[1] + '-' + pipelineCoord[1] + '    ' + coord[2] + '-' + pipelineCoord[2])
                        i += 1
                        # print('match ' + pipelineCoord[0] + ' ' + pipelineCoord[1] + ' ' + pipelineCoord[2])
        a += 1

    x = arivis
    y = i
    # print(x, y)
    print('\n\n' + key[0])
    print('Manual counts: ' + str(counted))
    print('pipeline counts: ' + str(arivis))
    print('Matches: ' + str(i))
    print('Cells not matched: ' + str(counted - i))
    print('Cells too many: ' + str(arivis - counted))

    # listDataTemp = []
    versionAndFilter = key[0].replace('.csv', '').split('_')
    # print(key)

    if versionAndFilter[2:] != []:
        listDataTemp = (versionAndFilter[1], versionAndFilter[2:], arivis, i, str(counted - i), arivis - counted)
    else:
        listDataTemp = (versionAndFilter[1], 'None', arivis, i, str(counted - i), arivis - counted)

    return listDataTemp, x, y


def makeGraph(dictPipeline, counted, version, variatie, listCounted):
    listX = []
    listY = []
    listLabel = []
    headers = ['Cell Finder', 'Image processing applied', 'Cells found', 'Matches',
               'Cells  not corresponding to manually found cells', 'Cells too many']
    data = []
    data.append(version)
    data.append(headers)
    for key in dictPipeline:
        listDataTemp, x, y = func(key, listCounted, variatie, counted)
        data.append(listDataTemp)
        listX.append(x)
        listY.append(y)
        key[0] = key[0].replace('_', ' ').replace('.csv', '')
        listLabel.append(key[0])

    makeCSV(data)
    refpoint = [counted]
    refpoint2 = refpoint
    listLine = [counted, counted]
    listLine2 = [0, max(listY)]
    listLine3 = [0, max(listX)]
    listLine4 = [counted, counted]
    legend_elements = [Patch(facecolor='b', edgecolor='r', alpha=0.2, label='Not enough matches and not enough cells'),
                       Patch(facecolor='y', edgecolor='r', alpha=0.2, label='Not enough matches and too many cells'),
                       Patch(facecolor='cyan', edgecolor='r', alpha=0.2, label='Too many matches and too many cells'),
                       Patch(facecolor='r', edgecolor='r', alpha=0.2, label='Too many matches and not enough cells'),
                       Line2D([], [], marker='*', color='k', label='ClearMap', linestyle='None'),
                       Line2D([], [], marker='o', color='k', label='Machine learning', linestyle='None'),
                       Line2D([], [], marker='s', color='k', label='Blobfinder', linestyle='None')]
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
    ax.plot(listLine, listLine2, 'r--', label='Divide cell count')
    ax.plot(listLine3, listLine4, 'r--', label='Divide matches')

    ySizeD = plt.ylim()[0]
    ySizeU = plt.ylim()[1]

    xSizeL = plt.xlim()[0]
    xSizeR = plt.xlim()[1]

    listCoord1 = [0, plt.ylim()[1]]
    listCoord2 = listCoord1
    # ax.plot(listCoord1, listCoord2, 'g-', label='Perfect matches line')
    plt.fill([counted, xSizeL, xSizeL, counted], [counted, counted, ySizeD, ySizeD], 'b', alpha=0.2, edgecolor='r')
    plt.fill([counted, xSizeR, xSizeR, counted], [counted, counted, ySizeU, ySizeU], 'cyan', alpha=0.2, edgecolor='r')
    plt.fill([counted, xSizeL, xSizeL, counted], [counted, counted, ySizeU, ySizeU], 'r', alpha=0.2, edgecolor='r')
    plt.fill([counted, xSizeR, xSizeR, counted], [counted, counted, ySizeD, ySizeD], 'y', alpha=0.2, edgecolor='r')

    i = 0
    colorList = []
    allList = []
    for z in listX:
        dist = math.sqrt((listX[i] - counted) ** 2 + (listY[i] - counted) ** 2)
        dist = truncate(dist)
        listFilters = listLabel[i].split(' ')

        allList.append([listFilters,dist])
        color = 'k'
        name = 'Test'
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

    writeList(allList,version)

    plt.show()


def truncate(n):
    return int(n * 1000) / 1000


def makeCSV(data):
    version = data[0]
    del data[0]
    with open('/home/bram/Desktop/Jaar_3/donders/report/celDetectionCsv/' + version + '.csv', 'w+') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def writeList(allList,version):

    f = open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/allDistances"+version + ".txt", "a")

    f.write(str(allList))
    f.close()

main()
