from tkinter import *
from GUI.TestStepUI import TestStepUI
import sys
sys.path.append('../TestCase/')
from TestCase import TestCase
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

class TestCaseUI(Frame):
    __single = None
    case = None

    def __init__(self, parent = None, *args, **kwargs):
        if TestCaseUI.__single:
            raise TestCaseUI.__single
            TestCaseUI.__single = self

        Frame.__init__(self, parent, *args, **kwargs, borderwidth =2 ,relief = 'sunken')

        self.canvas = Canvas(self)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        #self.scrollb.grid_forget()

        self.canvas.pack(side="left")
        self.place(x=460, y=300)

        self.lineNumList = []
        self.actionComboList = []
        self.valueList = []
        self.addButtonList = []
        self.removeButtonList = []
        self.executeButtonList = []

        # self.scriptStep = TestStepUI()
        n = 0
        for self.line in range(15):
            # self.scriptStep.newStep(self.listFrame, n)
            self.newStep(n)
            n += 1


    def getTestCaseUI(parent):
        if not TestCaseUI.__single:
            TestCaseUI.__single = TestCaseUI(parent)
        return TestCaseUI.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def addButtonClick(self, n):
        self.line = self.line + 1
        self.newStep(self.line)

        i = self.line
        while i > n:
            action = self.actionComboList[i-1].get()
            self.actionComboList[i].set(str(action))
            self.actionComboList[i-1].set('')
            if str(type(self.valueList[i-1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestCaseImage(i, self.valueList[i-1].image)
                self.TestCaseEntry(i-1)
            else:
                value = self.valueList[i-1].get()
                self.valueList[i].delete(0, 'end')
                self.valueList[i].insert('end', value)
            i = i-1

    def TestCaseImage(self, line, image = None):
        valueImage = Canvas(self.listFrame, bg = '#FFFFFF', height = 100, width = 100)
        valueImage.create_image(0, 0, anchor=NW, image=image)
        valueImage.bind('<Button-1>', lambda event, i=line: self.valueFocusIn(i))
        valueImage.image = image
        self.valueList[line].grid_remove()
        self.valueList[line] = valueImage
        self.valueList[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def TestCaseEntry(self, line):
        value = TestCaseValue(self.listFrame, width = 35)
        value.bind('<FocusIn>', lambda event, i = line: self.valueFocusIn(i))
        self.valueList[line].grid_remove()
        self.valueList[line] = value
        self.valueList[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def removeLineButtonClick(self, n):
        i = n
        while i < self.line:
            action = self.actionComboList[i+1].get()
            self.actionComboList[i].set(str(action))

            if str(type(self.valueList[i+1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestCaseImage(i, self.valueList[i+1].image)
                self.TestCaseEntry(i+1)
            else:
                self.TestCaseEntry(i)
                value = self.valueList[i+1].get()
                self.valueList[i].delete(0, 'end')
                self.valueList[i].insert('end', value)
            i = i+1

        self.lineNumList[self.line].grid_remove()
        self.actionComboList[self.line].grid_remove()
        self.valueList[self.line].grid_remove()
        self.addButtonList[self.line].grid_remove()
        self.removeButtonList[self.line].grid_remove()
        self.executeButtonList[self.line].grid_remove()

        self.lineNumList.pop()
        self.actionComboList.pop()
        self.valueList.pop()
        self.addButtonList.pop()
        self.removeButtonList.pop()
        self.executeButtonList.pop()
        self.line = self.line - 1

    def newStep(self, n):
        if not self.case:
            self.case = TestCase()

        action_value = StringVar()

        lineNum = Label(self.listFrame, text=str(n + 1) + ". ", width=3)
        self.lineNumList.append(lineNum)

        addButton = Button(self.listFrame, command=lambda :self.addButtonClick(n+1), text="+", width=3)
        self.addButtonList.append(addButton)

        removeButton = Button(self.listFrame, command=lambda :self.removeLineButtonClick(n), text="-", width=3)
        self.removeButtonList.append(removeButton)

        executeButton = Button(self.listFrame, text="▶", width=3)
        self.executeButtonList.append(executeButton)

        actionCombo = TestCaseAction(self.listFrame, textvariable=action_value, width=10, height=22, state='readonly')
        self.actionComboList.append(actionCombo)
        value = TestCaseValue(self.listFrame, width=35)
        #value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        #showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)

        self.valueList.append(value)

        lineNum.grid(row=n + 1, column=1)
        addButton.grid(row=n + 1, column=2)
        removeButton.grid(row=n + 1, column=3)
        executeButton.grid(row=n + 1, column=4)
        actionCombo.grid(row=n + 1, column=5, padx=(5, 0), pady=(5, 2.5))
        value.grid(row=n + 1, column=6, padx=(5, 0), pady=(5, 2.5))
