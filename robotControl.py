__author__ = 'skaper'
# -*- coding: utf-8 -*-
import sys, time
from PyQt4 import QtGui
from PyQt4 import QtCore
from configobj import ConfigObj
import serial
import voicesynth
import os
import threading
import shutil
from pygame import mixer

import imp

sys.path.append('forms/')
from formRobotControl import Ui_inmoovform

pathToMotion = 'motions/'
pathToScripts = 'scripts/'


robotModel = 'Maya'

###
api_key = 'dde5a9d3-d633-46e4-86d5-9e8724868f0c'
###



#Настройка модуля голосового синтезатора
robotVoice = voicesynth.Voice('mp3', api_key)
#robotVoice.voiceConfig(lang='ru-RU', speaker='omazh', robot='true')

runinformation = ConfigObj('logs/runinformation.info')
runX = int(runinformation['run'])
runX+=1
timerunX = time.ctime()
runinformation['run'] = runX
runinformation['LastRun'] = timerunX

errorLogs = ConfigObj('logs/error_logs.logs')
lastError = ''
lastErrorTime = time.ctime()
errorReplat = 1


def errorHandler(errorType):
    global lastError, errorReplat, lastErrorTime
    if errorType!=lastError:
        errorTime = time.ctime()
        if errorTime != lastErrorTime:
            errorLogs[str(runX)+' at '+errorTime] = errorType
            errorLogs.write()
            lastErrorTime = errorTime
        else:
            errorLogs[str(runX)+'.' +str(errorReplat) +' at '+errorTime] = errorType
            errorLogs.write()
            errorReplat +=1
        print errorType

        lastError = errorType


def portsConnected(left='/dev/arduinoLeft', right='/dev/arduinoRight', head='/dev/arduinoHeadMaya0'):
    global portLeftConnect, portRightConnect, portHeadConnect, portLeft, portHead, portRight
    try:
        portLeft = serial.Serial('/dev/ttyACM1af', baudrate=115200, dsrdtr = 1,  timeout=1)
        portLeftConnect = True
    except:
        errorHandler('Error 1.1.1: Port /dev/arduinoLeft not found')
        portLeftConnect = False
    try:
        portRight = serial.Serial('/dev/ttyAjCM08', baudrate=115200, dsrdtr = 1,  timeout=1)
        portRightConnect = True
    except:
        errorHandler('Error 1.1.2: Port /dev/ttyACM1 not found')
        portRightConnect = False
    try:
        portHead = serial.Serial('/dev/ttyACM0', baudrate=9600, dsrdtr = 1,  timeout=1)
        portHeadConnect = True
    except:
        errorHandler('Error 1.1.3: Port /dev/arduinoHeadMaya not found')
        portHeadConnect = False

portsConnected()
#time.sleep(2)


#Загрузка файла конфигураций
config = ConfigObj('conf.ini')

global headMotion
global headMotionCounter
headMotion = 0
motionTime = 0.0
headMotionCounter = 1
#Отправка на arduino и запись движений
timeDeleySend = time.time()
def sendLeft(sendinf):
    global timeDeleySend
    if portLeftConnect and time.time() - timeDeleySend > .2:
        #portLeft.write(sendinf+'\n')
        portHead.write(sendinf+'\n')
        timeDeleySend = time.time()
        print sendinf
        global motionTime
        global headMotionCounter
        if headMotion:
            motionRecAll[str(headMotionCounter)] = 'L'+sendinf
            motionRecAll.write()
            motionTime = motionTime + 0.025
            headMotionCounter +=1
    else: errorHandler('Error 1.2.1: No connection to the left port')

def sendRight(sendinf):
    #if portRightConnect:
    if portHeadConnect:
        global motionTime
        #portRight.write(sendinf+'\n')
        portHead.write(sendinf+'\n')
        global headMotionCounter
        if headMotion:
            motionRecAll[str(headMotionCounter)] = 'R'+sendinf
            motionRecAll.write()
            motionTime = motionTime + 0.025
            headMotionCounter +=1
    else: errorHandler('Error 1.2.2: No connection to the right port')


motionRecAll = ConfigObj('motions/motion.txt')

def sendHead(sendinf):
    global motionTime
    global headMotionCounter
    if portHeadConnect:
        portHead.write(sendinf+'\n')
        if headMotion:
            motionRecAll[str(headMotionCounter)] = 'H'+sendinf
            motionRecAll.write()
            motionTime = motionTime + 0.025
            headMotionCounter +=1
    else: errorHandler('Error 1.2.3: No connection to the head port')

def playMotionScript(path):
    script = ConfigObj(str(path))
    headMotionCounterMax = int(script[str(0)])
    headMotionCounter = 1
    while headMotionCounter < headMotionCounterMax:
            sending = script[str(headMotionCounter)]
            if sending[:1] ==    'H':
                sendHead(sending[1:])
                #portHead.write(sending[1:]+'\n')
            if sending[:1]== 'R':
                sendRight(sending[1:])
            if sending[:1] == 'L':
                sendLeft(sending[1:])
            headMotionCounter +=1
            #print headMotionCounter
            time.sleep(.025)

mouthMotionTalk = 0
class RobotLoad():

    def getAllRobotsModels(self):
        models = ['Maya', 'Vasja']
        print models
        return models

    def setRobotModel(self, model):
        if model=='Maya':
            sendHead('P1')

    def playMP3(self, path, speed=1):
        global mouthMotionTalk
        mouthMotionTalk = 1
        mixer.init(16000, -16, speed, 2048)
        mixer.music.load(path)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue
        mouthMotionTalk = 0

emotion = 'good'
sayText = ''
mouth_move = 0
def voice(arg2, voice_stop):
    global mouth_move
    robotLoad = RobotLoad()
    while(not voice_stop.is_set()):
        if sayText != '':
            robotVoice.say(emotion, sayText, play=0)
            mouth_move = 1
            robotLoad.playMP3('voiceSynthFile/say.mp3')
            mouth_move = 0


def mouth(arg3, mouth_stop):
    while(not mouth_stop.is_set()):
        while mouth_move:
            portHead.write('S|D11>100'+'\n')
            time.sleep(0.25)
            portHead.write('S|D11>40'+'\n')
            time.sleep(0.25)

voice_stop = threading.Event()
voice=threading.Thread(target=voice, args=(2, voice_stop))
#voice.start()

mouth_stop = threading.Event()
mouth=threading.Thread(target=mouth, args=(2, mouth_stop))
#mouth.start()


class Editor(QtGui.QMainWindow):


    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_inmoovform()
        self.ui.setupUi(self)

        #Загрузка и выбор робота
        self.robotLoad = RobotLoad()
        modelDialog = QtGui.QInputDialog()
        modelDialog.setWindowModality(QtCore.Qt.WindowModal)
        self.robotModel = modelDialog.getItem(self, 'Select the model of the robot', 'Model:', self.robotLoad.getAllRobotsModels() )
        self.loadingProgramm()
        self.robotLoad.setRobotModel(str(self.robotModel[0]))

        self.show()

        #Настройка голоса
        #self.ui.sayLang.activated[str].connect(self.langSettings)

        self.ui.motionStop.setEnabled(False)
        #Активность кнопок управления скриптами
        #self.ui.listWidget.setEnabled(False)
        self.ui.delItemFromMain.setEnabled(False)
        self.ui.appendItem.setEnabled(False)
        #self.ui.delItemFromMain.setEnabled(False)
        #self.ui.scriptRun.setEnabled(False)
        #self.ui.scriptClear.setEnabled(False)


        #Обработка нажатия в списках скриптов и движений
        self.ui.motionList.itemPressed.connect(self.enterMotion)
        self.ui.listWidget.itemPressed.connect(self.enterMotionMain)


        #Обработчик ползунков головы
        self.headSliders()

        #Обработчик ползунков левой руки
        self.leftHendSliders()

        #Обработчик ползунков правой руки
        self.rightHendSliders()

        #Обработчик RGB Emotion led
        self.ui.redSlider.valueChanged.connect(self.redSliderEvent)
        self.ui.greenSlider.valueChanged.connect(self.greenSliderEvent)
        self.ui.blueSlider.valueChanged.connect(self.blueSliderEvent)

        self.ui.runScriptFromList.clicked.connect(self.runScriptFromL)
        self.ui.appendItem.clicked.connect(self.appendItemMailList)
        self.ui.scriptRun.clicked.connect(self.runMailScript)
        self.ui.addDelay.clicked.connect(self.addNewDelay)
        self.ui.delItemFromMain.clicked.connect(self.delItemMain)
        self.ui.scriptSave.clicked.connect(self.saveMainScript)
        self.ui.delMotion.clicked.connect(self.deliteScript)
        self.ui.scriptOpen.clicked.connect(self.openFile)

        #Обработка событий кнопки и поля ввода для речи
        self.ui.lineSay.returnPressed.connect(self.sayEvent)
        self.ui.say.clicked.connect(self.sayEvent)
        self.ui.seveSettings.clicked.connect(self.seveSettingsEvent)

        #старт записи движений:
        self.ui.motionRec.clicked.connect(self.motionRec)

        #Проиграть запись движений
        self.ui.motionPlay.clicked.connect(self.motionPlay)

        #остановка записи движения
        self.ui.motionStop.clicked.connect(self.motionStop)

        #Главная картинка
        self.ui.imagerobot.setPixmap(QtGui.QPixmap("robot.png"))

        self.ui.scriptNew.clicked.connect(self.scriptNew)
        self.ui.scriptClear.clicked.connect(self.scritClear)

        #Загрузка начальных настроек серво и ползунков
        self.settingsSet()

        self.motionListUpdate()

    def loadingProgramm(self):
        file = range(40)
        numberOfLinesInFile = len(file)
        progressWasCancelled = False
        progress = QtGui.QProgressDialog(
            "Parsing Log", "Stop", 0, numberOfLinesInFile, self)
        labelLogo = QtGui.QLabel("")
        labelLogo.setPixmap(QtGui.QPixmap("img/logorobotcontrol.png"))
        progress.setLabel(labelLogo)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        for lineNumber, line in enumerate(file):
            progress.setValue(lineNumber)
            if progress.wasCanceled():
                progressWasCancelled = True
                break
            time.sleep(0.05)
        progress.setValue(numberOfLinesInFile)
        progress.deleteLater()


    def scritClear(self):
        quit_msg = "Are you sure you want to clear script list?"
        dialog =  QtGui.QMessageBox.question(self, 'Message',
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if dialog == QtGui.QMessageBox.Yes:
            self.ui.listWidget.clear()
        else:
            pass

    def scriptNew(self, notclearList = True):
        print self.ui.listWidget.count()
        if self.ui.listWidget.count() > 0:
            quit_msg = "Are you sure you want to clear script list?"
            dialog =  QtGui.QMessageBox.question(self, 'Message',
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if dialog == QtGui.QMessageBox.Yes:
                listHaveItems = False
            else:
                return 0
        else:
            listHaveItems = False
        file = QtGui.QInputDialog.getText(self, 'Enter script file name:', 'Name:')
        nameFile = str(file[0])
        print file
        if file[1] and not listHaveItems and file[0]!='':
            if not nameFile=='':
                self.ui.nameMainScript.setText(os.path.dirname(__file__)+'/'+ pathToScripts + nameFile)
            if not notclearList:
                self.ui.listWidget.clear()
                print 'clear list'
        elif file[0]=='' and file[1]:
            QtGui.QMessageBox.critical(self, u'Error', u'Not specified script name')
            return 0

    def addItemTo(self, wiget, text, opened = False):
        if text.split('-')[0] == 'delay':
            item = QtGui.QListWidgetItem(text)
            item.setBackgroundColor(QtCore.Qt.blue)
            item.setForeground(QtCore.Qt.white)
        elif not opened:
            item = QtGui.QListWidgetItem(self.enterMotionScript)
            item.setBackgroundColor(QtCore.Qt.green)
        elif opened:
            item = QtGui.QListWidgetItem(text)
            item.setBackgroundColor(QtCore.Qt.green)
        wiget.addItem(item)

    def openFile(self):
        _filter = '*.scr'
        openFile = str(QtGui.QFileDialog.getOpenFileName(self, 'Set file', 'scripts', _filter))
        try:
            scrips = ConfigObj(openFile)
            openFile = openFile.split('.scr')
            self.ui.listWidget.clear()
            count = 1
            countMax = scrips['0']
            while count <= int(countMax):
                self.addItemTo(self.ui.listWidget, scrips[str(count)], opened=True)
                count+=1
            print str(openFile)
            self.ui.nameMainScript.setText(openFile[0])
        except:
            print 'error Not found script motions'


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            runinformation[str(runX)] = timerunX + ' - ' + time.ctime()
            runinformation.write()
            if robotModel=='Maya':
                sendHead('P0')
            voice_stop.set()
            mouth_stop.set()
        else:
            event.ignore()

    def deliteScript(self):
        if self.enterMotionScript:
            quit_msg = "Are you sure want to permanently delete this movement?"
            dialog =  QtGui.QMessageBox.question(self, 'Message',
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if dialog == QtGui.QMessageBox.Yes:
                os.remove(pathToMotion+str(self.enterMotionScript))
                self.motionListUpdate()
            else:
                pass


    def saveMainScript(self):
        nameScript = str(self.ui.nameMainScript.text())
        if nameScript=='':
            self.scriptNew(notclearList=True)
            nameScript = str(self.ui.nameMainScript.text())
            if nameScript == '':
                QtGui.QMessageBox.critical(self, u'Error', u'Not specified script name')
                return 0
        if os.path.exists(nameScript+'.scr'):
            os.remove(nameScript+'.scr')
        open(nameScript+'.scr', 'wr').close()
        scriptFile = ConfigObj(nameScript+'.scr')
        items = []
        counter = 1
        if not os.path.exists(nameScript):
            os.makedirs(nameScript)
        else:
            shutil.rmtree(nameScript)
            os.makedirs(nameScript)
        for index in xrange(self.ui.listWidget.count()):
            a = self.ui.listWidget.item(index)
            a = a.text()
            a= str(a)
            if not a.startswith('delay-') and not os.path.exists(nameScript+a):
                shutil.copy(pathToMotion+a, nameScript)
            scriptFile[str(counter)] = str(a)

            counter+=1
        scriptFile[str(0)] = str(counter-1)
        scriptFile.write()


    def delItemMain(self):
        if self.enterMotionMainScript:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(self.enterMotionMainScript))

    #Добавляем задрежку в лист скрипта
    def addNewDelay(self):
        self.addItemTo(self.ui.listWidget, 'delay-'+self.ui.delayVal.text())


    def setMotionTime(self):
        self.ui.motionTime.setText(str(motionTime))


    def enterMotionMain(self, item):
        self.ui.delItemFromMain.setEnabled(True)
        self.enterMotionMainScript =  item
        #print self.enterMotionScript

    def enterMotion(self, item):
        self.ui.appendItem.setEnabled(True)
        self.enterMotionScript =  item.text()
        #print self.enterMotionScript

    def runMailScript(self):
        nameScript = str(self.ui.nameMainScript.text())
        if os.path.exists(nameScript):
            self.runScript(nameScript)
        elif self.ui.listWidget.count()>0:
            self.runScript()


    def runScript(self, nameScript=pathToMotion):
        items = []
        for index in xrange(self.ui.listWidget.count()):
                a = self.ui.listWidget.item(index)
                a = a.text()
                items.append(str(a))

        for path in items:
                if path.startswith('delay-'):
                    timedelay = path.split('-')
                    try:
                        delay = int(timedelay[1])
                    except:
                        delay = 0
                    time.sleep(delay)
                else:

                    motionPath = str(nameScript)+'/'+path
                    if os.path.exists(motionPath):
                        #print str(nameScript)+'/'+path
                        pass
                    else:
                        a = self.ui.listWidget.item(index)
                        a = a.text()
                        a= str(a)
                        shutil.copy(pathToMotion+a, motionPath)
                    playMotionScript(str(nameScript)+'/'+path)
        else:
            pass

    def runScriptFromL(self):
        if self.enterMotionScript:
            playMotionScript(pathToMotion + self.enterMotionScript)

    #Добавляет действие из списка действий в лист скрипта
    def appendItemMailList(self):
        if self.enterMotionScript:
            self.addItemTo(self.ui.listWidget, self.enterMotionScript)

    def motionListUpdate(self):
        self.ui.motionList.clear()
        for f in os.listdir(pathToMotion):
            self.ui.motionList.addItem(f)

    def motionPlay(self):
        self.ui.motionRec.setEnabled(False)
        nameScript = self.ui.scriptName.text()
        print nameScript
        path = pathToMotion + str(nameScript)+'.txt'
        playMotionScript(path)

    def motionStop(self):
        global headMotion, motionTime, headMotionCounter
        self.ui.motionPlay.setEnabled(True)
        self.ui.motionRec.setEnabled(True)
        self.ui.motionStop.setEnabled(False)
        motionTime = 0.0
        self.setMotionTime()
        self.motionListUpdate()

        headMotion = 0

        motionRecAll[str(0)] = headMotionCounter-1
        motionRecAll.write()
        headMotionCounter = 1
    def motionRec(self):
        global headMotion
        global motionRecAll
        self.ui.motionPlay.setEnabled(False)
        self.ui.motionRec.setEnabled(False)
        self.ui.motionStop.setEnabled(True)
        headMotion = 1
        nameScript = self.ui.scriptName.text()
        print nameScript

        if os.path.exists(pathToMotion+str(nameScript)+'txt'):
            os.remove(pathToScripts+nameScript+'scr')
        open(pathToMotion + str(nameScript)+'.txt', 'wr').close()
        motionRecAll = ConfigObj(pathToMotion + str(nameScript)+'.txt')

    def setColorLed(self):
        red = str(self.ui.redSlider.value())
        green = str(self.ui.greenSlider.value())
        blue = str(self.ui.blueSlider.value())
        self.ui.colorLed.setStyleSheet("background-color: rgb("+red+", "+green+", "+blue+");\n"
                                    "border:1px solid rgb(255, 170, 255);")

    def leftHendSliders(self):
        self.ui.lbiceps.valueChanged.connect(self.eventlbiceps)
        self.ui.lbiceps.valueChanged.connect(self.setMotionTime)
        self.ui.lomoplate.valueChanged.connect(self.eventlOmoplate)
        self.ui.lomoplate.valueChanged.connect(self.setMotionTime)
        self.ui.lshoulder.valueChanged.connect(self.eventlShoulder)
        self.ui.lshoulder.valueChanged.connect(self.setMotionTime)
        self.ui.lpalm.valueChanged.connect(self.eventlPalm)
        self.ui.lpalm.valueChanged.connect(self.setMotionTime)
        self.ui.lrotate.valueChanged.connect(self.eventlRotate)
        self.ui.lrotate.valueChanged.connect(self.setMotionTime)
        self.ui.lfingers1.valueChanged.connect(self.eventlFinger1)
        self.ui.lfingers1.valueChanged.connect(self.setMotionTime)
        self.ui.lfingers2.valueChanged.connect(self.eventlFinger2)
        self.ui.lfingers2.valueChanged.connect(self.setMotionTime)
        self.ui.lfingers3.valueChanged.connect(self.eventlFinger3)
        self.ui.lfingers3.valueChanged.connect(self.setMotionTime)
        self.ui.lfingers4.valueChanged.connect(self.eventlFinger4)
        self.ui.lfingers4.valueChanged.connect(self.setMotionTime)
        self.ui.lfingers5.valueChanged.connect(self.eventlFinger5)
        self.ui.lfingers5.valueChanged.connect(self.setMotionTime)
    def rightHendSliders(self):
        self.ui.rbiceps.valueChanged.connect(self.eventrbiceps)
        self.ui.rbiceps.valueChanged.connect(self.setMotionTime)
        self.ui.romoplate.valueChanged.connect(self.eventrOmoplate)
        self.ui.romoplate.valueChanged.connect(self.setMotionTime)
        self.ui.rshoulder.valueChanged.connect(self.eventrShoulder)
        self.ui.rshoulder.valueChanged.connect(self.setMotionTime)
        self.ui.rpalm.valueChanged.connect(self.eventrPalm)
        self.ui.rpalm.valueChanged.connect(self.setMotionTime)
        self.ui.rrotate.valueChanged.connect(self.eventrRotate)
        self.ui.rrotate.valueChanged.connect(self.setMotionTime)
        self.ui.rfingers1.valueChanged.connect(self.eventrFinger1)
        self.ui.rfingers1.valueChanged.connect(self.setMotionTime)
        self.ui.rfingers2.valueChanged.connect(self.eventrFinger2)
        self.ui.rfingers2.valueChanged.connect(self.setMotionTime)
        self.ui.rfingers3.valueChanged.connect(self.eventrFinger3)
        self.ui.rfingers3.valueChanged.connect(self.setMotionTime)
        self.ui.rfingers4.valueChanged.connect(self.eventrFinger4)
        self.ui.rfingers4.valueChanged.connect(self.setMotionTime)
        self.ui.rfingers5.valueChanged.connect(self.eventrFinger5)
        self.ui.rfingers5.valueChanged.connect(self.setMotionTime)
    def headSliders(self):
        self.ui.mouth.valueChanged.connect(self.eventMouth)
        self.ui.mouth.valueChanged.connect(self.setMotionTime)
        self.ui.udrotate.valueChanged.connect(self.eventUD)
        self.ui.udrotate.valueChanged.connect(self.setMotionTime)
        self.ui.rlrotate.valueChanged.connect(self.eventRL)
        self.ui.rlrotate.valueChanged.connect(self.setMotionTime)


    def redSliderEvent(self):
        red =  str(self.ui.redSlider.value())
        self.ui.redText.setText(red)
        self.setColorLed()
        portHead.write("L|D1>" + red + "\n")
        portHead.write("R|D1>" + red + "\n")
    def greenSliderEvent(self):
        green = str(self.ui.greenSlider.value())
        self.ui.greenText.setText(str(green))
        self.setColorLed()
        portHead.write("L|D2>" + green + "\n")
        portHead.write("R|D2>" + green + "\n")
    def blueSliderEvent(self):
        blue = str(self.ui.blueSlider.value())
        self.ui.blueText.setText(str(blue))
        self.setColorLed()
        portHead.write("L|D3>" + blue + "\n")
        portHead.write("R|D3>" + blue + "\n")
    def seveSettingsEvent(self):
        config['minMouth'] = self.ui.minMouth.text()
        config['maxMouth'] = self.ui.maxMouth.text()
        config['strMouth'] = self.ui.strMouth.text()
        config['mouthPin'] = self.ui.pinMouth.text()

        config['minUDRotate'] = self.ui.minUDRotate.text()
        config['maxUDRotate'] = self.ui.maxUDRotate.text()
        config['strUDRotate'] = self.ui.strUDRotate.text()
        config['udRotatePin'] = self.ui.pinUDRotate.text()

        config['minRLRotate'] = self.ui.minRLRotate.text()
        config['maxRLRotate'] = self.ui.maxRLRotate.text()
        config['strRLRotate'] = self.ui.strRLRotate.text()
        config['rlRotatePin'] = self.ui.pinRLRotate.text()

        config.write()
        self.settingsSet()

    def settingsSet(self):
        self.ui.minMouth.setText(config['minMouth'])
        self.ui.maxMouth.setText(config['maxMouth'])
        self.ui.strMouth.setText(config['strMouth'])
        self.ui.pinMouth.setText(config['mouthPin'])

        self.ui.mouth.setMinimum(int(config['minMouth']))
        self.ui.mouth.setMaximum(int(config['maxMouth']))
        self.ui.mouth.setValue(int(config['strMouth']))
        portSend = 'S|D'+str(config['mouthPin']) +'>'+str(config['strMouth'])
        sendHead(portSend)

        self.ui.minUDRotate.setText(config['minUDRotate'])
        self.ui.maxUDRotate.setText(config['maxUDRotate'])
        self.ui.strUDRotate.setText(config['strUDRotate'])
        self.ui.pinUDRotate.setText(config['udRotatePin'])

        self.ui.udrotate.setMinimum(int(config['minUDRotate']))
        self.ui.udrotate.setMaximum(int(config['maxUDRotate']))
        self.ui.udrotate.setValue(int(config['strUDRotate']))
        time.sleep(.05)
        portSend = 'S|D'+str(config['udRotatePin']) +'>'+str(config['strUDRotate'])
        sendHead(portSend)

        self.ui.minRLRotate.setText(config['minRLRotate'])
        self.ui.maxRLRotate.setText(config['maxRLRotate'])
        self.ui.strRLRotate.setText(config['strRLRotate'])
        self.ui.pinRLRotate.setText(config['rlRotatePin'])

        self.ui.rlrotate.setMinimum(int(config['minRLRotate']))
        self.ui.rlrotate.setMaximum(int(config['maxRLRotate']))
        self.ui.rlrotate.setValue(int(config['strRLRotate']))
        time.sleep(.05)
        portSend = 'S|D'+str(config['rlRotatePin']) +'>'+str(config['strRLRotate'])
        sendHead(portSend)

    def sayEvent(self):
        global emotion
        global sayText
        print unicode(self.ui.lineSay.text())
        lang = str(self.ui.sayLang.currentText())
        spiker = str(self.ui.sayVoice.currentText())
        option = str(self.ui.sayOption.currentText())
        emotion = str(self.ui.sayEmotion.currentText())
        _speed = int(self.ui.saySpeed.currentText())
        print lang
        robotVoice.voiceConfig(lang, spiker, option, _speed)
        sayText = unicode(self.ui.lineSay.text())
        #robotVoice.say(emotion, sayText, play=0)
        #self.robotLoad.playMP3('voiceSynthFile/say.mp3')


    def eventMouth(self, _type):
        self.ui.labelmouth.setText(str(self.ui.mouth.value()))
        angle = self.ui.mouth.value()
        portSend = 'S|D'+str(config['mouthPin']) +'>'+str(angle)
        print portSend
        sendHead(portSend)

    def eventUD(self, _type):
        self.ui.labeludrotate.setText(str(self.ui.udrotate.value()))
        angle = self.ui.udrotate.value()
        portSend = 'S|D'+str(config['udRotatePin']) +'>'+str(angle)
        print portSend
        sendHead(portSend)

    def eventRL(self, _type):
        self.ui.labelrlrotate.setText(str(self.ui.rlrotate.value()))
        angle = self.ui.rlrotate.value()
        portSend = 'S|D'+str(config['rlRotatePin']) +'>'+str(angle)
        print portSend
        sendHead(portSend)

    def eventlbiceps(self, _type):
        self.ui.labellbiceps.setText(str(self.ui.lbiceps.value()))
        angle = self.ui.lbiceps.value()
        portSend = 'S|D'+str(config['lBicepsPin']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)

    def eventlOmoplate(self, _type):
        self.ui.labellomoplate.setText(str(self.ui.lomoplate.value()))
        angle = self.ui.lomoplate.value()
        portSend = 'S|D'+str(config['lOmoplatePin']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)

    def eventlShoulder(self, _type):
        self.ui.labellshoulder.setText(str(self.ui.lshoulder.value()))
        angle = self.ui.lshoulder.value()
        portSend = 'S|D'+str(config['lShouderPin']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)

    def eventlRotate(self, _type):
        self.ui.labelrotate.setText(str(self.ui.lrotate.value()))
        angle = self.ui.lrotate.value()
        portSend = 'S|D'+str(config['lRotatePin']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)

    def eventlPalm(self, _type):
        self.ui.labellpalm.setText(str(self.ui.lpalm.value()))
        angle = self.ui.lpalm.value()
        portSend = 'S|D'+str(config['lPalmPin']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)

    def eventlFinger1(self, _type):
        angle = self.ui.lfingers1.value()
        portSend = 'S|D'+str(config['lFingerPin1']) +'>'+str(angle)

        sendLeft(portSend)

    def eventlFinger2(self, _type):
        angle = self.ui.lfingers2.value()
        portSend = 'S|D'+str(config['lFingerPin2']) +'>'+str(angle)

        sendLeft(portSend)

    def eventlFinger3(self, _type):
        angle = self.ui.lfingers3.value()
        portSend = 'S|D'+str(config['lFingerPin3']) +'>'+str(angle)

        sendLeft(portSend)

    def eventlFinger4(self, _type):
        angle = self.ui.lfingers4.value()
        portSend = 'S|D'+str(config['lFingerPin4']) +'>'+str(angle)

        sendLeft(portSend)

    def eventlFinger5(self, _type):
        angle = self.ui.lfingers5.value()
        portSend = 'S|D'+str(config['lFingerPin5']) +'>'+str(angle)
        print portSend
        sendLeft(portSend)



    def eventrbiceps(self, _type):
        self.ui.labelrbiceps.setText(str(self.ui.rbiceps.value()))
        angle = self.ui.rbiceps.value()
        portSend = 'S|D'+str(config['rBicepsPin']) +'>'+str(angle)

        sendRight(portSend)

    def eventrOmoplate(self, _type):
        self.ui.labelromoplate.setText(str(self.ui.romoplate.value()))
        angle = self.ui.romoplate.value()
        portSend = 'S|D'+str(config['rOmoplatePin']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrShoulder(self, _type):
        self.ui.labelrshoulder.setText(str(self.ui.rshoulder.value()))
        angle = self.ui.rshoulder.value()
        portSend = 'S|D'+str(config['rShouderPin']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrRotate(self, _type):
        self.ui.labelrrotate.setText(str(self.ui.rrotate.value()))
        angle = self.ui.rrotate.value()
        portSend = 'S|D'+str(config['rRotatePin']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrPalm(self, _type):
        self.ui.labelrpalm.setText(str(self.ui.rpalm.value()))
        angle = self.ui.rpalm.value()
        portSend = 'S|D'+str(config['rPalmPin']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrFinger1(self, _type):
        angle = self.ui.rfingers1.value()
        portSend = 'S|D'+str(config['rFingerPin1']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrFinger2(self, _type):
        angle = self.ui.rfingers2.value()
        portSend = 'S|D'+str(config['rFingerPin2']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrFinger3(self, _type):
        angle = self.ui.rfingers3.value()
        portSend = 'S|D'+str(config['rFingerPin3']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrFinger4(self, _type):
        angle = self.ui.rfingers4.value()
        portSend = 'S|D'+str(config['rFingerPin4']) +'>'+str(angle)
        print portSend
        sendRight(portSend)

    def eventrFinger5(self, _type):
        angle = self.ui.rfingers5.value()
        portSend = 'S|D'+str(config['rFingerPin5']) +'>'+str(angle)
        print portSend
        sendRight(portSend)



def main():
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


