import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)
a = np.load('/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCellsClearMap/190925_ClearMap.npy')
np.savetxt('/home/bram/Desktop/Jaar_3/donders/report/verslagData/detectedCellsClearMap/190925_ClearMap.csv',a,delimiter=',',fmt="%s")
