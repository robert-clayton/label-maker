import pandas as pd
import ThemeManager
from PySide2.QtCore import Signal, QObject

class BoxManager(QObject):
    '''Handles adding and removing rows to and from the dataset'''

    def __init__(self):
        super().__init__()
        self.dataFrame = pd.read_csv(ThemeManager.DATA_PATH)

        # Recent box variables
        self.recentLabelName      = self.loadLabels()[0] if self.loadLabels() else ''
        self.recentIsOccluded     = False
        self.recentIsTruncated    = False
        self.recentIsGroupOf      = False
        self.recentIsDepiction    = False
        self.recentIsInside       = False
    
    def getBoxesForImage(self, imageID):
        matches = self.dataFrame.loc[self.dataFrame['ImageID'] == imageID]
        return [Box(*matchList) for matchList in matches.values.tolist()]

    def addBoxToDataFrame(self, imageID, labelName, xMin, xMax, yMin, yMax, isOccluded, isTruncated, isGroupOf, isDepiction, isInside):
        box =   [imageID, 
                'label-maker', 
                labelName,
                1.0,
                xMin, xMax, yMin, yMax,
                isOccluded,
                isTruncated,
                isGroupOf,
                isDepiction,
                isInside]
        self.dataFrame.loc[len(self.dataFrame)] = box

        self.recentLabelName      = labelName
        self.recentIsOccluded     = isOccluded
        self.recentIsTruncated    = isTruncated
        self.recentIsGroupOf      = isGroupOf
        self.recentIsDepiction    = isDepiction
        self.recentIsInside       = isInside

        return Box(*box)

    def saveDataFrame(self):
        self.dataFrame.to_csv(ThemeManager.DATA_PATH, index=False)

    def loadLabels(self):
        with open(ThemeManager.LABELS_PATH, 'r') as labels:
            return [label.strip() for label in labels]

    def getRecentLabelName(self):     return self.recentLabelName
    def getRecentIsOccluded(self):    return self.recentIsOccluded
    def getRecentIsTruncated(self):   return self.recentIsTruncated
    def getRecentIsGroupOf(self):     return self.recentIsGroupOf
    def getRecentIsDepiction(self):   return self.recentIsDepiction
    def getRecentIsInside(self):      return self.recentIsInside

class Box():
    '''A single row to add to the dataset'''

    def __init__(self, imageID = '', source = '', labelName = '', confidence = 1.0, 
                xMin = 0.0, xMax = 0.0, yMin = 0.0, yMax = 0.0, 
                isOccluded = False, isTruncated = False, isGroupOf = False, 
                isDepiction = False, isInside = False):
        self.imageID    = imageID
        self.source     = source
        self.labelName  = labelName
        self.confidence = confidence
        self.xMin       = xMin
        self.xMax       = xMax
        self.yMin       = yMin
        self.yMax       = yMax
        self.isOccluded = isOccluded
        self.isTruncated= isTruncated
        self.isGroupOf  = isGroupOf
        self.isDepiction= isDepiction
        self.isInside   = isInside

    def getData(self):
        return [self.imageID, self.source, self.labelName, self.confidence, 
                self.xMin, self.xMax, self.yMin, self.yMax, 
                self.isOccluded, self.isTruncated, self.isGroupOf, 
                self.isDepiction, self.isInside]
    
    def getRect(self):
        return (self.xMin, self.xMax, self.yMin, self.yMax)

    def getLabel(self):
        return self.labelName