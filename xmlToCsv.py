import xml.etree.ElementTree as ET
tree = ET.parse('/home/bram/Desktop/Jaar_3/donders/report/verslagData/2019-10-29 Data for Bram/66632_S1_Handcounted/CellCounter_xml.xml')
root = tree.getroot()
f= open("/home/bram/Desktop/Jaar_3/donders/report/verslagData/2019-10-29 Data for Bram/csv/66632_manualBram.csv","w+")
output = ''
for child in root:
    if child.tag == 'Marker_Data':
        for marker in child:
            for markerType in marker:
                for markers in markerType:
                    if markers.tag == 'MarkerX':
                        x = markerType.find('MarkerX').text
                        output += x + ','
                    if markers.tag == 'MarkerY':
                        y = markerType.find('MarkerY').text
                        output += y + ','
                    if markers.tag == 'MarkerZ':
                        z = markerType.find('MarkerZ').text
                        output += z + '\n'
                    #output += x + ',' + y + ',' + 'z' + '\n'

f.write(output)