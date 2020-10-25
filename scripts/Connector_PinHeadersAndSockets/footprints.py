from enum import Enum
from collections import namedtuple


class SMDfootprintsCannotBeOfAngledPinStyle(Exception):
   """Raised when a SMD-footprint of angeled-oinstyle is to be created."""
   pass


class BodyStyle(Enum):
  HEADER = 'Header'
  SOCKET = 'Socket'


class CaseType(Enum):
  THT = 'THT'
  SMD = 'SMD'


class CaseDirection(Enum):
  LEFT = -1
  RIGHT = 1


class PinStyle(Enum):
  VERTICAL = 'Vertical'
  HORIZONTAL = 'Horizontal'


class Pad(object):

  def __init__(self):
    self.padStyle: CaseType = None
    self.xPos = 0.0
    self.yPos = 0.0
    self.size1 = 0.0
    self.size2 = 0.0
    self.pinNumber = -1


class PadTHT(Pad):

  def __init__(self):
    self.padStyle = CaseType.THT


class PadSMD(Pad):

  def __init__(self):
    self.padStyle = CaseType.SMD


class FootPrint(object):

  def __init__(self):
    self.name = ""
    self.description = ""
    self.keywords = ""
    #self.reference = ""

    self.caseDirection: CaseDirection = 1
    self.caseType: CaseType = None
    self.bodyStyle: BodyStyle = None
    self.pinStyle: PinStyle = None
    self.pitch = 0.0

    self.pins = []
    self.body = []
    self.silk = []
    self.yard = []

  def rowCount(self):
    return len(self.pins)

  def colCount(self):
    if self.rowCount > 0:
      return len(self.pins[0])
    else:
      return 0


class FootPrintSMD(FootPrint):

  def __init__(self):
    self.caseType = CaseType.SMD
    super().__init__()
    if self.pinStyle is PinStyle.HORIZONTAL:
      raise SMDfootprintsCannotBeOfAngledPinStyle()


class FootPrintTHT(FootPrint):

  def __init__(self):
    self.caseType = CaseType.THT
    super().__init__()


class FootPrintBuilder(object):

  def __init__(self, params, cols, rows, footprint):
    self.params = params
    self.footprint: FootPrint = footprint
    self.footprint.pinStyle: PinStyle = params["pinStyle"]
    self.footprint.pitch = params["pitch"]


class PinBuilder(object):

  def __init__(self, params, cols, rows, footprint: FootPrint):
    self.params = params
    self.footprint: FootPrint = footprint

    self.colCount = cols
    self.rowCount = rows
    self.offsetX = 0.0
    self.offsetY = 0.0
    self.direction: CaseDirection = 1

  def build(self):
    self.__calcOffsetX__()
    self.__calcOffsetY__()
    self.__calcDirection__()
    self.__buildRows__()

  def __calcOffsetX__(self):
    self.offsetX = self.params["padOffset"]

  def __calcOffsetY__(self):
    self.offsetY = 0.0

  def __calcDirection__(self):
    self.footprint.caseDirection = self.direction

  def __buildRows__(self):
    for index in range (0, self.rowCount):
      xCoord = self.offsetX + index * self.footprint.pitch * self.direction
      self.__buildCols__(xCoord)

  def __buildCols__(self, xCoord):
    for index in range (0, self.colCount):
      yCoord = self.offsetY - index * self.footprint.pitch
      self.__buildPad__(xCoord, yCoord)

  def __CreateNewPad__(self):
    return None

  def __buildPad__(self, xCoord, yCoord):
    pad: Pad = self.__CreateNewPad__()
    pad.xPos = xCoord
    pad.yPos = yCoord
    return pad


class PinBuilderTHT(PinBuilder):

  def __CreateNewPad__(self):
    return PadTHT()

  def __buildPad__(self, xCoord, yCoord):
    pad: Pad = super().__buildPad__()
    pad.size1 = self.params["holeSize"]
    pad.size2 = self.params["padSize"]
    return pad


class PinBuilderSMD(PinBuilder):

  def __calcOffsetY__(self):
    self.offsetY = ((self.colCount - 1) / 2) * self.footprint.pitch

  def __CreateNewPad__(self):
    return PadSMD()

  def __buildPad__(self, xCoord, yCoord):
    pad: Pad = super().__buildPad__()
    pad.size1 = self.params["padLength"]
    pad.size2 = self.params["padWidth"]
    return pad


class BodyBuilder(object):

  def __init__(self, params, footprint):
    pass


class SilkBuilder(object):

  def __init__(self, params, footprint):
    pass


class TextBuilder(object):

  def __init__(self, params, footprint: FootPrint):
    self.params = params
    self.footprint = FootPrint(footprint)

  def build(self):
    self.footprint.name = self.__buildName__()
    self.footprint.keywords = self.__buildReadableText__(' ')
    self.footprint.description = self.__buildReadableText__(', ')

  def __buildName__(self):
    delimiter = '_'
    myCaseType = (self.footprint.caseType if self.footprint.caseType is CaseType.SMD else "")
    result = self.__buildBasicText__(delimiter)
    return result.format("", "P", myCaseType)

  def __buildReadableText__(self, delimiter):
    myCaseType = self.__getCaseTypeText__(self.footprint.caseType)
    result = self.__buildBasicText__(delimiter)
    return result.format(myCaseType + delimiter, "pitch" + delimiter, "")

  def __buildBasicText__(self, delimiter):
    return 'Pin' \
           + '\{\}' \
           + self.footprint.bodyStyle \
           + delimiter \
           + self.footprint.rowCount \
           + 'x' \
           + self.footprint.colCount \
           + delimiter \
           + '\{\}' \
           + self.footprint.pitch \
           + 'mm' \
           + delimiter \
           + self.footprint.pinStyle \
           + '\{\}'

  def __getCaseTypeText__(self, caseType: CaseType):
    if caseType is CaseType.THT:
      return "Through hole"
    elif caseType is CaseType.SMD:
      return "Surface mount"
    else:
      return ""


class YardBuilder(object):

  def __init__(self, params, footprint):
    pass


