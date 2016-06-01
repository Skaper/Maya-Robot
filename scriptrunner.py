__author__ = 'skaper'
# -*- coding: utf-8 -*-
from srunnerForm import Ui_ScriptRunner
from PyQt4 import QtGui
from PyQt4.QtCore import *
from configobj import ConfigObj
import sys, os, serial, time
hotKey=[]
dict={}
key = '!@#$%^&*()_+QWERTYUIOPASDFGHJKLZXCVBNM'
for elem in key:
    hotKey.append(elem)
pathToScript = 'scripts/'

robotModel = 'Maya'

runinformation = ConfigObj('logs/run_runscrips.info')
runX = int(runinformation['run'])
runX+=1
timerunX = time.ctime()
runinformation['run'] = runX
runinformation['LastRun'] = timerunX


#Подключение arduino
try:
    portLeft = serial.Serial('/dev/arduinoLeft', baudrate=115200, dsrdtr = 1,  timeout=1)
except:
    print 'Error 1.1: Port /dev/arduinoLeft not found'
try:
    portRight = serial.Serial('/dev/arduinoRight', baudrate=115200, dsrdtr = 1,  timeout=1)
except:
    print 'Error 1.2: Port dev/arduinoRight not found'
try:
    portHead = serial.Serial('/dev/arduinoHead', baudrate=115200, dsrdtr = 1,  timeout=1)
except:
    print 'Error 1.3: Port /dev/arduinoHeadMaya not found'

#time.sleep(3)

#if robotModel=='Maya':
#    portHead.write('P1'+'\n')

def playMotionScript(path):
    script = ConfigObj(str(path))
    print path
    headMotionCounterMax = int(script[str(0)])
    print headMotionCounterMax
    headMotionCounter = 1
    while headMotionCounter < headMotionCounterMax:
            sending = script[str(headMotionCounter)]
            if sending[:1] == 'H':
                portHead.write(sending[1:]+'\n')
            if sending[:1]== 'R':
                portRight.write(sending[1:]+'\n')
            if sending[:1] == 'L':
                portLeft.write(sending[1:]+'\n')
            headMotionCounter +=1
            #print headMotionCounter
            time.sleep(.025)


class Editor(QtGui.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_ScriptRunner()
        self.ui.setupUi(self)
        self.loadingProgramm()
        self.show()
        self.ui.tableScripts.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.fillTable()
        self.ui.tableScripts.itemPressed.connect(self.pressEtem)



        '''
        self.ui.ip.setText(str(get_ip_address('wlan2')))
        self.ui.wifiHost.clicked.connect(self.wifiHostEvent)
        self.ui.robotControl.clicked.connect(self.robotControlEvent)
        self.ui.runDemo.clicked.connect(self.runDemoEvent)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6Ev)
        '''
    def fillTable(self):
        allFiles = os.listdir(pathToScript)
        files1 = filter(lambda x: x.endswith('.scr'), allFiles)
        print files1
        files = sorted(files1, key = lambda x: os.path.getctime(pathToScript+x))
        print files
        self.ui.tableScripts.setColumnCount(2)
        self.ui.tableScripts.setRowCount(len(files))
        for i, f in enumerate(files):
            item = QtGui.QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled  | Qt.ItemIsSelectable)
            item.setText(f)
            self.ui.tableScripts.setItem(i, 0, item)
            #print os.path.getatime(pathToScript+f)

            item = QtGui.QTableWidgetItem()
            item.setText(hotKey[i])
            self.ui.tableScripts.setItem(i, 1, item)
            dict[hotKey[i]] = f
        print dict

    def loadingProgramm(self):
        file = range(40)
        numberOfLinesInFile = len(file)
        progressWasCancelled = False
        progress = QtGui.QProgressDialog(
            "Parsing Log", "Stop", 0, numberOfLinesInFile, self)
        labelLogo = QtGui.QLabel("")
        labelLogo.setPixmap(QtGui.QPixmap("img/logorobotcontrol.png"))
        progress.setLabel(labelLogo)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        for lineNumber, line in enumerate(file):
            progress.setValue(lineNumber)
            if progress.wasCanceled():
                progressWasCancelled = True
                break
            time.sleep(0.05)
        progress.setValue(numberOfLinesInFile)
        progress.deleteLater()


    def runMotion(self, files, scriptName):
        print len(files)
        count = 0
        while count <= len(files):
            print '----------'
            if files[count].startswith('delay-'):
                print 'delay'
                timedelay = files[count].split('-')
                try:
                    delay = int(timedelay[1])
                except:
                    delay = 0
                time.sleep(delay)
            else:
                filenm = scriptName.split('.')[0]
                print pathToScript+filenm+'/'+files[count]

                playMotionScript(pathToScript+filenm+'/'+files[count])
            print files[count]
            count +=1



    def runScript(self, file):
        scriptList = ConfigObj(pathToScript+str(file))
        counterMax = int(scriptList[str(0)])
        counter = 1
        motionFiles = []
        while counter<=counterMax:
            #print scriptList[str(counter)]
            motionFiles.append(scriptList[str(counter)])
            counter +=1
        #print motionFiles
        self.runMotion(motionFiles, file)
    def keyPressEvent(self, event):

        if type(event) == QtGui.QKeyEvent:
             keyPress = event.text()
             #keyPress = keyPress.text()
             event.accept()
             try:
                 nameFile =  dict[str(keyPress)]
                 print nameFile
                 self.runScript(nameFile)

             except:
                 print 'no'
        else:
             event.ignore()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            runinformation[str(runX)] = timerunX + ' - ' + time.ctime()
            runinformation.write()
            if robotModel=='Maya':
                portHead.write('P0'+'\n')
        else:
            event.ignore()

    def keyUpdate(self):
        pass

    def pressEtem(self, item):
        print item.text()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
