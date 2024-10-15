'''
LibreOffice Calc python macros for satisfactory calculator.
To run go to LibreOffice Calc document
Tools -> Run Macros... -> calculator -> Select Macro
'''
import uno

def __loadDocument():
    desktop = XSCRIPTCONTEXT.getDesktop()
    document = desktop.getCurrentComponent()
    return document

def __loadSheet(idx=-1, document=None):
    if document == None:
        document = __loadDocument()
    if idx == -1:
        sheet = document.CurrentController.ActiveSheet
        return sheet
    elif type(idx) == str:
        sheet = document.getSheets().getByName(idx)
        return sheet
    sheet = document.getSheets().getByIndex(idx)
    return sheet

def helloWorld():
    # oDoc = XSCRIPTCONTEXT.getDocument()
    # oSheet = oDoc.getSheets().getByIndex(0)
    # refCell = oSheet.getCellByPosition(0,0)
    # outCell = oSheet.getCellByPosition(1,0)
    # outCell.String = refCell.String

    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()

    active_sheet = model.CurrentController.ActiveSheet
    recipe_sheet = model.getSheets().getByName("recipes")
    active_sheet.getCellByPosition(0,0).String = recipe_sheet.getCellByPosition(0,0)

    return None

def test():
    document = __loadDocument()
    sheet = __loadSheet()
    sheet.getCellByPosition(3,0).String = document.Sheets.Count

    return None

def setActive():
    document = __loadDocument()
    count = document.Sheets.Count

    for idx in range(count):
        sheet = __loadSheet(idx)
        sheet.getCellByPosition(1,0).String = ""

    sheet = __loadSheet()
    sheet.getCellByPosition(1,0).String = "Active Factory"
    
    return None

def getActive():
    document = __loadDocument()

def itemLoader():
    ...