
from collections import namedtuple


class CaseType:
    THT = 'THT'
    SMD = 'SMD'


class PinStyle:
    STRAIGHT = 'Straight'
    ANGLED   = 'Angled'


class FootPrint (object):

  def __init__(params):
    self.pinStyle = params["pinStyle"]
    self.pitch = params["pitch"]


class FootPrintSMD (FootPrint):

  def __init__(params):
    self.caseType = CaseType.SMD
    super().__init__(params)


class FootPrintTHT