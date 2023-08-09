from PIL import Image, ImageDraw, ImageFont
from foxStitchLib import *
import sys
import os

if __name__ == "__main__":

    print("Reticulating Stitched Foxhole World Map...")

    if len(sys.argv) == 1:
        print("Incorrect Parameters")
        print("Parm One Draw Hexagon Borders - values y or n")
        print("Parm Two Hexagon Border Widths - values 1 through 6")
        print("Usage Example:")
        print("foxStitchPy.py y 3")
        exit(0)

    #Get working directory
    fxRootDirectory = os.path.dirname(__file__)
    print(fxRootDirectory)

    #Set Line Width
    drawHexagonLines = sys.argv[1]
    hexagonLineWidth = sys.argv[2]
    
    #Map Dimensions    
    fxWorldMapColumnHexagonHeight = 7
    fxWorldMapColumnHexagonWidth = 5.5
    fxRegionMapWidth = 1024
    fxRegionMapHeight = 888

    #Create canvas to draw world map
    fxWorldMap = Image.new(mode="RGBA", size=(round(fxWorldMapColumnHexagonWidth * fxRegionMapWidth),fxWorldMapColumnHexagonHeight * fxRegionMapHeight))

    fxWorldHexagonCoordinates = []

    for fxRegionMap in fxRegionMaps:

        #Lookup and calculate position of region map on world map
        fxWorldMapPositions = fxRegionPositions[fxRegionMap[0]]
        fxWorldMapPositionX = round(fxWorldMapPositions[0] * fxRegionMapWidth)
        fxWorldMapPositionY = round(fxWorldMapPositions[1] * fxRegionMapHeight)

        #Open region map image file
        fxRegionMapImage = Image.open(fxRootDirectory + fxRegionMap[1]).convert('RGBA')

        #Calculate Region Hexagon Borders
        #Using the percentage lookup table and the region map width and height determine the offset pixel to start drawing the hexagon.
        fxHexagonCoordinateSet = []
        for fxRegionHexagonBorderPercentage in fxRegionHexBorderPercentages:            
            if fxRegionHexagonBorderPercentage[0] == 0:
                fxWorldMapHexBorderPositionX = fxWorldMapPositionX
            else:
                fxWorldMapHexBorderPositionX = round((fxWorldMapPositionX + (fxRegionMapWidth * (fxRegionHexagonBorderPercentage[0] / 100))))
            if fxRegionHexagonBorderPercentage[1] == 0:
                fxWorldMapHexBorderPositionY = fxWorldMapPositionY		
            else:
                fxWorldMapHexBorderPositionY = round((fxWorldMapPositionY + (fxRegionMapHeight * (fxRegionHexagonBorderPercentage[1] / 100))))
            
            fxHexagonCoordinateSet.append(((fxWorldMapHexBorderPositionX),(fxWorldMapHexBorderPositionY)))
        fxWorldHexagonCoordinates.append(fxHexagonCoordinateSet)

        #Add region map to the world map
        fxWorldMap.paste(fxRegionMapImage, (fxWorldMapPositionX, fxWorldMapPositionY), fxRegionMapImage)

    #Draw hexagons around regions
    if drawHexagonLines == "y":
        fxDrawHexagons = ImageDraw.Draw(fxWorldMap)
    
        for fxHexagonCoordinates in fxWorldHexagonCoordinates:
            for x in range(len(fxHexagonCoordinates)):
                if x == len(fxHexagonCoordinates) - 1:
                    fxDrawHexagons.line((fxHexagonCoordinates[x],fxHexagonCoordinates[0]), fill="black", width=int(hexagonLineWidth))
                else:
                    fxDrawHexagons.line((fxHexagonCoordinates[x],fxHexagonCoordinates[x+1]), fill="black", width=int(hexagonLineWidth))

    #Save world map
    fxWorldMap.save(fxRootDirectory + "\\output\\foxhole-worldmap.png")

    print("Reticulation Complete...")