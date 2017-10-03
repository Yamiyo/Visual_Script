from TestCase import TestCase
from Executor import Executor
import threading
from Record import *

class TestController:
    def __init__(self):
        self.case = TestCase()
        self.exe = Executor(self.case)
        self.undo = Undo(self.case)
        self.redo = Redo()

    def execute(self, n):
        threading.Thread(target=self.exe.execute, args=(n,)).start()

    def runAll(self):
        from TestCaseUI import TestCaseUI as UI
        self.case.refresh()
        UI.getTestCaseUI().reloadTestCaseUI()
        for i in range(self.case.getSize()):
            print(self.case.getSteps(i).getAction())
            print(self.case.getSteps(i).getValue())
        threading.Thread(target=self.exe.runAll).start()

    def undoClick(self, event=None):
        from TestCaseUI import TestCaseUI as UI
        self.redo.push(self.case)
        self.case = self.undo.pop()
        UI.getTestCaseUI().reloadTestCaseUI()

    def redoClick(self, event=None):
        if self.redo.getSize() == 0: return

        from TestCaseUI import TestCaseUI as UI
        self.undo.push(self.case)
        self.case = self.redo.pop()
        UI.getTestCaseUI().reloadTestCaseUI()

    def insertStep(self, n):
        self.redo.reset()
        self.undo.push(self.case)
        self.case.insert(n=n, act='', val='')

    def removeStep(self, n):
        self.redo.reset()
        self.undo.push(self.case)
        self.case.delete(n)

    def setStep(self, n, image = None):
        if n == None: return

        self.redo.reset()
        self.undo.push(self.case)

        from TestCaseUI import TestCaseUI as UI
        stepList = UI.getTestCaseUI().stepList

        # Handle the exceptions for step n is not exist
        try:
            if image is None:
                self.case.setAction(n, stepList[n].action.get())
                self.case.setValue(n, stepList[n].value.get())
            else:
                self.case.setAction(n, stepList[n].action.get())
                self.case.setValue(n, image)
        except:
            # Handle the invalid input exceptions
            try:
                if image is None:
                    self.case.insert(n=n, act=stepList[n].action.get(), val=stepList[n].value.get())
                else:
                    self.case.insert(n=n, act=stepList[n].action.get(), val=image)
            except Exception as e:
                if stepList[n].value.get() == '':return
                print(str(e))
                return 'Invalid Value'

    def clearTestCase(self):
        from TestCaseUI import TestCaseUI as UI
        self.case.clear()
        UI.getTestCaseUI().clearUI()

    def ShowImageButtonClick(self, n):
        image = self.case.getSteps(n).getValue()
        image.show()
