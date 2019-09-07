# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:59:54 2019

@author: exs1084
"""

def kmlHeader():
    ret = ""
    ret += """<?xml version="1.0" encoding="UTF-8"?>\n
    <kml xmlns="http://www.opengis.net/kml/2.2">\n
    <Document>\n
    <Style id="yellowPoly">\n
        <LineStyle>\n
            <color>Af00ffff</color>\n
            <width>6</width>\n
        </LineStyle>\n
        <PolyStyle>\n
            <color>7f00ff00</color>\n
        </PolyStyle>\n
    </Style>\n
    <Placemark><styleUrl>#yellowPoly</styleUrl>\n
    <LineString>\n
    <Description>.</Description>\n
        <extrude>1</extrude>\n
        <tesselate>1</tesselate>\n
        <coordinates>\n"""
    return ret
def kmlTail():
    ret = ""
    ret += """    \t</coordinates>
        </LineString>
        </Placemark>
        </Document>
        </kml>"""
    return ret

def writeDataToKML(data, outFile):
    for x in data:
        outFile.write("%s,%s\n"%(x[0],x[1]))
    return

def line1Good(line):
    if len(line) is not 13:
        return False
    if line[0] != "$GPRMC":
        return False
    return True
    
def line2Good(line):
    if len(line) is not 15:
        return False
    if line[0] != "$GPGGA":
        return False
    return True
    
def degreeToDec(string, direction):
    degrees=0
    minutes=0
    if direction == 'N' or direction == 'S':
        degrees = float(string[0:2])
        minutes = float(string[2:])
    else:
        degrees = float(string[0:3])
        minutes = float(string[3:])
    decimal = degrees + minutes/60
    if direction == 'S' or direction == 'W':
        return decimal * -1
    else:
        return decimal
    

def GPSToKML(inFilename, outFilename):
    inFile = open(inFilename, "r")#open file
    outFile = open(outFilename, "w")#open file
    outFile.write(kmlHeader())
    data = list()
    rawline1 = inFile.readline()
    timesWritten=0
    while rawline1:
        line1 = rawline1.split(',')
        if line1Good(line1):
            rawline2 = inFile.readline()
            if not rawline2:
                break
            line2 = rawline2.split(',')
            if line2Good(line2):
                lat = (degreeToDec(line1[3], line1[4]) + degreeToDec(line2[2], line2[3]))/2
                lon = (degreeToDec(line1[5], line1[6]) + degreeToDec(line2[4], line2[5]))/2
                speed = float(line1[7])
                if speed > 5:#5 knots = 6.9mph
                    data.append([lon, lat])
                    if(len(data)>100):
                        writeDataToKML(data, outFile)
                        data = list()
                rawline1 = inFile.readline()
            else:
                line1 = line2
        else:
            rawline1 = inFile.readline()
    
    #write to a kml file after here?
    outFile.write(kmlTail())
    return "pickle"





def main():
    inFile = "2019_03_05__RIT_to_Home.txt"
    outFile = inFile[:-3] + "kml"
    GPSToKML(inFile, outFile)
    
if __name__ == "__main__":
    main()