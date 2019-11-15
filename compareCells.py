import csv
import multiprocessing
import os
import math
import matplotlib.pyplot as plt
import mplcursors

from matplotlib.patches import Patch


def main():
    versionList = ['66632']
    # ,'66633','66634','190925']

    pool = multiprocessing.Pool()
    pool.map(callFunc, versionList)


def callFunc(version):
    variatie = 3
    dictArivis = {}
    path = '/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCells/' + version + '/'
    for filename in os.listdir(path):
        with open(path + filename) as f:
            listArivis = list(csv.reader(f))
            del listArivis[0]
        dictArivis[filename] = listArivis

    with open(
            '/home/bram/Desktop/Jaar_3/donders/report/verslagData/2019-10-29 Data for Bram/csv/S1_' + version + '_Cell_Count_03.csv') as f:
        listCounted = list(csv.reader(f))
        del listCounted[0]
    # print(listCounted)

    # print(dictArivis)
    counted = len(listCounted) + 1

    makeGraph(dictArivis, counted, version, variatie, listCounted)


def func(compare, dictArivis, listCounted, variatie, counted):
    arivis = len(dictArivis[compare])
    i = 0
    a = 0
    for coord in listCounted:

        # print(listCounted[a])
        for arivisCoord in dictArivis[compare]:
            # print(coord[0] + ' ' + arivisCoord[0] + '-' + coord[1] + ' ' + arivisCoord[1])
            if float(coord[0]) - variatie <= float(arivisCoord[0]) <= float(coord[0]) + variatie:
                # print('y ' + coord[0] + ' ' + arivisCoord[0])
                if float(coord[1]) - variatie <= float(arivisCoord[1]) <= float(coord[1]) + variatie:
                    # print('ye ' + coord[1] + ' ' + arivisCoord[1])
                    # print('yes ' + coord[2] + ' ' + arivisCoord[2])
                    if float(coord[2]) - variatie <= float(arivisCoord[2]) <= float(coord[2]) + variatie:
                        # print('match ' + coord[0] + '-' + arivisCoord[0] + '    ' + coord[1] + '-' + arivisCoord[1] + '    ' + coord[2] + '-' + arivisCoord[2])
                        i += 1
                        # print('match ' + arivisCoord[0] + ' ' + arivisCoord[1] + ' ' + arivisCoord[2])
        a += 1

    x = arivis
    y = i
    print(x, y)
    print('Arivis counts: ' + str(arivis))
    print('Matches: ' + str(i))
    print('Cells not matched: ' + str(counted - i))
    print('Cells too many: ' + str(arivis - counted))

    return x, y


def makeGraph(dictArivis, counted, version, variatie, listCounted):
    listX = []
    listY = []
    listLabel = []

    for key in dictArivis:
        print('\n\n' + key)
        x, y = func(key, dictArivis, listCounted, variatie, counted)
        # if not (x - counted) > 100 and not (y -counted) >100:
        listX.append(x)
        listY.append(y)
        key = key.replace('_', ' ').replace('.csv', '')
        listLabel.append(key)

    refpoint = [counted]
    refpoint2 = refpoint
    listLine = [counted, counted]
    listLine2 = [0, max(listY)]
    listLine3 = [0, max(listX)]
    listLine4 = [counted, counted]
    legend_elements = [Patch(facecolor='b', edgecolor='r', alpha=0.2, label='Not enough matches and not enough cells'),
                       Patch(facecolor='y', edgecolor='r', alpha=0.2, label='Not enough matches and too many cells'),
                       Patch(facecolor='cyan', edgecolor='r', alpha=0.2, label='Too many matches and too many cells'),
                       Patch(facecolor='r', edgecolor='r', alpha=0.2, label='Too many matches and not enough cells')

                       ]

    fig = plt.figure()
    fig.suptitle('', fontsize=14, fontweight='bold')

    ax = fig.add_subplot()
    ax.set_title('Arivis results for ' + version)
    ax.set_xlabel('Arivis counts')
    ax.set_ylabel('Matches')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.25,
                     box.width, box.height * 0.8])

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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), handles=legend_elements)
    i = 0
    for z in listX:
        dist = math.sqrt((listX[i] - counted) ** 2 + (listY[i] - counted) ** 2)
        dist = truncate(dist)
        if 'machineLearn' in listLabel[i]:
            point += ax.plot(listX[i], listY[i], 'o',
                             label=listLabel[i] + '\nmatches(y) = ' + str(listY[i]) + '\nCounts in arivis(x) = ' + str(
                                 listX[i]) + '\nDistance to perfect = ' + str(dist))
        else:
            point += ax.plot(listX[i], listY[i], 's',
                             label=listLabel[i] + '\nmatches(y) = ' + str(listY[i]) + '\nCounts in arivis(x) = ' + str(
                                 listX[i]) + '\nDistance to perfect = ' + str(dist))
        i += 1

    mplcursors.cursor(point, hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

    plt.show()
    

def truncate(n):
    return int(n * 1000) / 1000


main()
