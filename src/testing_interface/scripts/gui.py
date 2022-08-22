#!/usr/bin/env python2

import rospy
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow
from widgetNames import *
from chaosState import GazeboModels
from gazebo_msgs.srv import GetWorldProperties, GetModelProperties
from chaosState import GetModelLocation, SetModelLocation
from PyQt5.QtCore import QStringListModel
import random
from graph import PlotGraph
from threading import Thread
import matplotlib
import time
import math
import random
from decimal import Decimal,getcontext
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtGui import QPixmap
from addObjectData import objectList 
#from collections import OrderedDict

class Worker(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal(object)
    #result = pyqtSignal(object)

    def __init__(self , listofalltargets , track , rangeofAcceptance, canvas , graphListbox , moni_time , cmd):
        super(Worker, self).__init__()
        self.listofalltargets = listofalltargets
        self.tracking = track
        self.canvas = canvas
        self.rangeofAcceptance = rangeofAcceptance
        self.graphListbox = graphListbox
        self.moni_time = moni_time
        self.cmd = cmd

    def run(self):
        #Long-running task.        
                os.system('pkill -f arm_controller.py')
                os.system('pkill -f state.py')
                os.system('pkill -f move2tray.py')
                os.system('pkill -f move2tray_2.py')
                os.system('pkill -f move2tray_3.py')
                os.system('pkill -f move2tray_4.py')
                os.system('pkill -f back2zero.py')
                os.system('roslaunch gear_control armcontrol.launch &') 
                # os.system(self.cmd.text() + ' &') 
                initPlot = PlotGraph(self.listofalltargets,len(self.listofalltargets),self.rangeofAcceptance.value(),1 , self.moni_time)#,self.rangeofAcceptance.value(),self.saveInit.get())
        
                child = [None]*10 
                index = 0
                for each in self.listofalltargets:
                        child[index]=Thread(target= initPlot.threadGetLoc, args=(each,index,))           
                        child[index].setDaemon(True)
                        child[index].start()
                        index +=1
                
                for i in range(0,index):
                        child[i].join()

                allReturn = []
                for i in range(0,index):
                        allReturn.append(initPlot.returnQue[i])

                self.monitoringPlot = initPlot.plotGraphs(allReturn)
                self.progress.emit(self.monitoringPlot)
                self.index = 0
                self.canvas.plot(self.monitoringPlot[self.index],self.graphListbox,[0] , [0]  ,[0] ,[0], True)
                
                self.finished.emit()

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100 ):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
 
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        
        
    def plot(self , data , graphListbox , initialx , initialy , initialz , initial_t , check = None , nodeTerminationData=None , newrng = None):
        # print(len(data))

        
        t  = data[0]
        x  = data[1]
        y  = data[2]
        z  = data[3]
        # t0 = data[5]
        
        if check:
                del initialx[:]
                del initialy[:]
                del initialz[:]
                del initial_t[:]

                for ele in data[1]:
                        initialx.append(ele)
                for ele in data[2]:        
                        initialy.append(ele)
                for ele in data[3]:
                        initialz.append(ele)
                for ele in data[5]:
                        initial_t.append(ele)

                if newrng:
                        # mean = (x + y + z) / 3                    
                        print('length of array :: ' , len(x))
                        print(type(x))
                        print(x[0])

                        lowerX = np.array(initialx) - float(newrng)/100.0
                        lowerY = np.array(initialy) - float(newrng)/100.0
                        lowerZ = np.array(initialz) - float(newrng)/100.0

                        upperX = np.array(initialx) + float(newrng)/100.0
                        upperY = np.array(initialy) + float(newrng)/100.0
                        upperZ = np.array(initialz) + float(newrng)/100.0

                        t0 = np.array(initial_t)
                else:
                        lowerX = data[6]
                        upperX = data[7]
                        lowerY = data[8]
                        upperY = data[9]
                        lowerZ = data[10]
                        upperZ = data[11]
                        t0 = data[5]

        else:
                if newrng:
                        # mean = (x + y + z) / 3                    
                        
                        # print(type(initialx))
                        # print(initialx[0])

                        lowerX = np.array(initialx) - float(newrng)/100.0
                        lowerY = np.array(initialy) - float(newrng)/100.0
                        lowerZ = np.array(initialz) - float(newrng)/100.0

                        upperX = np.array(initialx) + float(newrng)/100.0
                        upperY = np.array(initialy) + float(newrng)/100.0
                        upperZ = np.array(initialz) + float(newrng)/100.0

                        t0 = np.array(initial_t)
                # else:
                        # lowerX = data[6]
                        # upperX = data[7]
                        # lowerY = data[8]
                        # upperY = data[9]
                        # lowerZ = data[10]
                        # upperZ = data[11]                
                
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(t,x, 'r-' , label = 'x-axis')
        ax.plot(t,y, 'b-' , label = 'y-axis')
        ax.plot(t,z, 'g-' , label = 'z-axis')
        if nodeTerminationData:
                
                graphListbox.clear()
                count = 1
                reversed_dictionary = {value : key for (key, value) in nodeTerminationData.items()}
                lst = sorted(reversed_dictionary.items())
               
                for index, tuple in enumerate(lst):
                            
                        ax.bar(tuple[0],(max([max(x),max(y),max(z)])-min([min(x),min(y),min(z)])),width = 0.5,bottom = min([min(x),min(y),min(z)]) , color='orange' , alpha = 0.5)
                        ax.annotate(count ,(tuple[0] , max([max(x),max(y),max(z)])))
                        string = str(count) + " --> " + tuple[1] + " :: at " + str(tuple[0]) + " secs"
                        graphListbox.addItem(string)
                        count = count + 1
                        
 

        ax.fill_between(t0,lowerX,upperX, facecolor='red',alpha=0.2 , label = 'Tolerance x-axis')
        ax.fill_between(t0,lowerY,upperY, facecolor='blue',alpha=0.2 , label = 'Tolerance y-axis')
        ax.fill_between(t0,lowerZ,upperZ, facecolor='green',alpha=0.2 ,label = 'Tolerance z-axis' )
        ax.set_ylim(emit = True , auto = True)
        ax.set_xlabel('Time of Simulation(seconds)' , fontweight ='bold')
        ax.set_ylabel('Location' ,fontweight ='bold' )
        ax.legend(loc = 'lower center' , ncol = 6 , bbox_to_anchor = (0.5, -0.5))
        
        ax.set_title(data[4])
        self.fig.subplots_adjust(bottom = 0.3)
        self.fig.canvas.draw_idle()
 

# Main class of the GUI#

class GUI(QMainWindow):


    def __init__(self, MainWindow):
        super(GUI, self).__init__(MainWindow)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 528)
        
        self.allGazeboObjects = None
        self.per_listBox = None
        self.mon_listBox = None
        self.index = None
        self.initial_pos = {} # {object: []}
        self.initial_x_pos = None
        self.initial_y_pos = None
        self.initial_z_pos = None
        self.perturbation_X = None
        self.rangeofAcceptance = None
        self.perturbation_Z = None
        self.listofalltargets = []
        #self.rangeofAcceptance = 0.25
        self.monitoringPlot = None
        self.index = 0
        self.tracking = 0
        self.killNodeData = {}
        self.activeNodesData = {}
        
        self.count1 = -1
        self.count2 = -1
        self.t_run = 0
        self.initial_x_data = [0]
        self.initial_y_data = [0]
        self.initial_z_data = [0]
        self.t_initial = [0]
    def monitoringPlot_val(self , result1):
        self.monitoringPlot = result1    

    def switchGraph(self):
        check = self.checkBox.isChecked()
        if self.index >= (len(self.monitoringPlot) - 1):
            self.index = 0
       
        else: 
            self.index +=1 
        if not self.rangeBox.text():
                self.canvas.plot(self.monitoringPlot[self.index], self.graphListbox,self.initial_x_data , self.initial_y_data ,self.initial_z_data,self.t_initial,check , self.killNodeData , 0)
        else:
                self.canvas.plot(self.monitoringPlot[self.index], self.graphListbox,self.initial_x_data , self.initial_y_data ,self.initial_z_data,self.t_initial,check,self.killNodeData ,int(self.rangeBox.text
                 ()))
        


    def refreshGraph(self):
        if not self.rangeBox.text():
                return    
        newrng = int(self.rangeBox.text())
        print(newrng)
        check = self.checkBox.isChecked()
        print(check)
        
        # for index in range(len(self.monitoringPlot)):
        self.canvas.plot(self.monitoringPlot[self.index], self.graphListbox,self.initial_x_data , self.initial_y_data ,self.initial_z_data,self.t_initial,check,self.killNodeData ,newrng)
        # self.canvas.plot(self.monitoringPlot[self.index], self.graphListbox,self.killNodeData ,newrng)           
    

#     def toolTip(self):
#         count1 = self.mon_listBox.count()
#         print(count1)
#         if count1 < 1 :
#                 self.mf_actionButtonsrun.setToolTip("Please Select Object(s) for Monitoring")
#         else:
#                 # self.mf_actionButtonsrun.setToolTip("You have selected", count1, "models") 
#                 self.gear_controller()

      
    
    def gear_controller(self):

        count1 = self.mon_listBox.count()
        print(count1)
        if count1 < 1 or not self.simtimebox.text():
                # self.mf_actionButtonsrun.setToolTip("Please Select models for Monitoring")
                
                # error_dialog = QtWidgets.QErrorMessage(self)
                # error_dialog.setWindowModality(QtCore.Qt.WindowModal)
                # error_dialog.showMessage('Please Select Object(s) for Monitoring or Give some monitoring time')
                # error_dialog.setGeometry(400,300,100,200)

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Please Select Object(s) for Monitoring or Give some monitoring time")
                msgBox.setWindowTitle("Error Message")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setGeometry(400,300,100,200)
                x = msgBox.exec_()

                
                
               
                
        else:
               

                listofalltargets = []
        

                count =  self.mon_listBox.count()   
                for index in xrange(count):
                        con = self.mon_listBox.item(index).text()
                        con = con.split('::')
                        
                        # listofalltargets.append(self.mon_listBox.item(index).text()) 
                        listofalltargets.append(con[0]) 
                        print(listofalltargets)

                track = self.tracking
                canvas = self.canvas
                # Step 2: Create a QThread object
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = Worker(listofalltargets , track , self.rangeofAcceptance ,canvas , self.graphListbox , int(self.simtimebox.text()) , self.terminal)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                #self.worker.progress.connect(self.reportProgress)
                # Step 6: Start the thread
                self.thread.start()
                self.worker.progress.connect(self.monitoringPlot_val)
                # Final resets
                #self.mf_actionButtonsrun.setEnabled(False)
                self.createChaosButton.setEnabled(True)
                self.thread.finished.connect(
                lambda: self.mf_actionButtonsrun.setEnabled(True)
                )
                self.mf_subframe2tabWidget.setCurrentIndex(2)
        

    def recordNodes(self):
        self.t_run = int(time.time())    
        self.mf_actionButtonsrun.setEnabled(False)
        QApplication.processEvents()
        if not self.checkBox.isChecked():
                self.activeNodesData.clear()
                return
        import subprocess
        proc=subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
        output=proc.communicate()[0]
        list_of_nodes = output.splitlines()
        for nodes in list_of_nodes:
                self.activeNodesData.setdefault(nodes , 0)

        simtime_value = int(self.simtimebox.text())
        
        
        t = self.simtimebox.text()


        timeT1 = int(time.time())
        while (int(time.time()) - timeT1) < int(t) :
                proc=subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
                output=proc.communicate()[0]
                list_of_nodes = output.splitlines()
                for nodes in list_of_nodes:
                        self.activeNodesData.setdefault(nodes , int(time.time()) - timeT1)
        print(self.activeNodesData)    
        
# This is the main frame of the interface #
         
    def mainInterface(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

# Main frame inside the central widget of the window #

        self.mainframe = QtWidgets.QFrame(self.centralwidget)
        self.mainframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainframe.setObjectName("mainframe")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.mainframe)
        self.gridLayout_10.setObjectName("gridLayout_10")

# Sub frame inside the main frame of the window #

        self.mf_subframe1 = QtWidgets.QFrame(self.mainframe)
        self.mf_subframe1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mf_subframe1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mf_subframe1.setObjectName("mf_subframe1")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.mf_subframe1)
        self.gridLayout_9.setObjectName("gridLayout_9")

# Heading of the GUI  window #
        myFont=QtGui.QFont()
        myFont.setBold(True)
        self.headingLabel = QtWidgets.QLabel(self.mf_subframe1)
        self.headingLabel.setObjectName("headingLabel")
        self.headingLabel.setAlignment(Qt.AlignCenter)
        self.headingLabel.setFont(myFont)
        self.headingLabel.adjustSize()
         

        self.gridLayout_9.addWidget(self.headingLabel, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.mf_subframe1, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.mainframe, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

###############################
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 22))
        # self.menuEdit = QtWidgets.QMenu(self.menubar)
        # # self.menuEdit.triggered.connect(showMaximized())
        # MainWindow.setMenuBar(self.menubar)
        
        # self.actionMaximize = QtWidgets.QAction(MainWindow)
        # self.menuEdit.addAction(self.actionMaximize)
        # self.menubar.addAction(self.menuEdit.menuAction())
        # self.actionMaximize.triggered.connect(self.maximizeAction)

# Calling other functions defined in the GUI class of the Main Window #

        self.actionButtons(MainWindow)
        self.objectDetailsPanel(MainWindow)
        self.interactionPanel(MainWindow)
        self.perturbationPanel(MainWindow)
        self.monitoringGraph(MainWindow)
        self.chaosPanel(MainWindow)
        self.objectAdd( MainWindow)
        self.mf_subframe2tabWidget.setCurrentIndex(0)
        self.perturbationtabWidget.setCurrentIndex(0)
        widgetnames(self, MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

# Calling other functions defined in the GUI class of the Main Window  #

# Function for getting the model location values #

#     def menuAction(self, MainWindow):
#         MainWindow.showMaximized()
    
    def getObjectDetails(self):
        con = self.list_Models.currentText()
        print(con)
        conUnlinked = con.split(':')[0]
        initModel = GetModelLocation(conUnlinked)
        linkedModel = GetModelLocation(con)
        # print(linkedModel)
        data = initModel.showGazeboModels()
        getMass = linkedModel.showObjectMass()
        # print(getMass)
        # print(data)
        self.getLocationBox.setText(str(data))
        self.getMassBox.setText(str(getMass))

# Function for adding models to monitoring list #

    def monitoringBoxAddItem(self):
        con = self.monitoringBox.currentText()
        print(con)
        # con = con.split('::')
        # print(con)
        self.mon_listBox.addItem(con)
        self.count1 = self.mon_listBox.count()
        if self.count1 > 0 :
                self.mf_actionButtonsrun.setToolTip("Objects are selected")
                self.mf_actionButtonsrun.setEnabled(True)

        items1 = []
        for i in range(self.mon_listBox.count()):
                items1.append(self.mon_listBox.item(i).text())
        unique_items_set = set(items1)
        self.mon_listBox.clear()
        for i in unique_items_set:
                self.mon_listBox.addItem(i)
        
       
        # self.listofalltargets.append(con[0])
        # print(self.listofalltargets)
        # for index in xrange(self.mon_listBox.count()):
        #         print(self.mon_listBox.item(index).text())

    def monitoringBoxDeleteItem(self):
        con = self.monitoringBox.currentText()
        con = con.split('::')
        # items = self.per_listBox.selectedItems()
        # self.per_listBox.takeItem(items)
        for SelectedItem in self.mon_listBox.selectedItems():
            self.mon_listBox.takeItem(self.mon_listBox.row(SelectedItem))




# Function for adding models to perturbation list #

    def locModelLoc(self):
        con = self.perturbationBox.currentText()
        # print(con)
        con = con.split('::')
        self.per_listBox.addItem(con[0])
        items = []
        for i in range(self.per_listBox.count()):
                items.append(self.per_listBox.item(i).text())
        unique_items_set = set(items)
        self.per_listBox.clear()
        for i in unique_items_set:
                self.per_listBox.addItem(i)


# Function for deleting models to perturbation list #

    def deleteModeLoc(self):
        con = self.perturbationBox.currentText()
        con = con.split('::')
        # items = self.per_listBox.selectedItems()
        # self.per_listBox.takeItem(items)
        for SelectedItem in self.per_listBox.selectedItems():
            self.per_listBox.takeItem(self.per_listBox.row(SelectedItem))


# Add function for objectAddTab #

    def objectAddListItemSelect(self):
        
        con = self.objectAddListBox.currentText()
        os.system('rosrun gazebo_ros spawn_model -database '+ con + ' -sdf -model ' + self.objectEdit.text() + ' -y ' + self.yPosition.text() + ' -x ' + self.xPosition.text())
        # con = con.split('::')
        
        self.objectAddList.addItem(self.objectEdit.text())
        items = []
        
        for i in range(self.objectAddList.count()):
                items.append(self.objectAddList.item(i).text())
        
        unique_items_set = set(items)
        self.objectAddList.clear()
        
        for i in unique_items_set:
                self.objectAddList.addItem(i)
        
        self.objectEdit.clear()
        self.yPosition.clear()
        self.xPosition.clear()
#Delete function for objcetAddTab#

    def objectAddListItemRemove(self):
        con = self.objectAddList.currentItem()
        temp = "'{model_name: " + con.text() + "}'"
        os.system("rosservice call gazebo/delete_model " + temp) 
        # con = con.split('::')
        # items = self.per_listBox.selectedItems()
        # self.per_listBox.takeItem(items)
        for SelectedItem in self.objectAddList.selectedItems():
                self.objectAddList.takeItem(self.objectAddList.row(SelectedItem))


# Function for adding multi object perturbation #

    def initChaos(self):
        
        self.allObjects = list()

        for index in xrange(self.per_listBox.count()):
                self.allObjects.append(self.per_listBox.item(index).text())
                
        print(self.allObjects)
        l= len(self.allObjects)
        for i in range (0, l):
                mdlName = self.allObjects[i]
                print(mdlName)
                getLocation = GetModelLocation(mdlName)
                print(getLocation)
                getLoc = getLocation.showGazeboModels()
                print(getLoc)

                initial_x_pos = -1*float(getLoc.pose.position.y)
                print(initial_x_pos)
                initial_y_pos = float(getLoc.pose.position.x)
                print(initial_y_pos)
                initial_z_pos = float(getLoc.pose.position.z)

                if i not in self.initial_pos:
                        self.initial_pos[i]=[initial_x_pos, initial_y_pos]
                val_x = float(self.perturbation_X.value())
                # print(val_x)
                val_y = float(self.rangeofAcceptance.value())
                val_z = float(self.perturbation_Z.value())

       

# self.selected_model_call(i)
                
                randomness_x = random.uniform(-(val_x/float(1000)), (val_x/float(1000)))
                randomness_y = random.uniform(-(val_y/float(1000)), (val_y/float(1000)))
# val_perturb_x = initial_x_pos+randomness_x
                
                
# val_perturb_y = initial_y_pos+randomness_y

                val_perturb_x = self.initial_pos[i][0]+randomness_x
                print("This is the initial position of the object:")
                print(self.initial_pos[i][0])
                
                
                val_perturb_y = self.initial_pos[i][1]+randomness_y
                print(self.initial_pos[i][1])
            
                val_perturb_z = 1.0
                setModelPostionChaosInit = SetModelLocation()
                setModelPostionChaosInit.setGazeboModel(mdlName,val_perturb_x,val_perturb_y,val_perturb_z)



    
        


# Create Chaos Tab Functions
    def displayActiveNodes(self):
        self.count1 = -1
        if not self.activeNodesData:
                self.chaos_listBox_1.clear()
                import subprocess
                proc=subprocess.Popen("rosnode list", shell=True, stdout=subprocess.PIPE)
                output=proc.communicate()[0]
                list_of_nodes = output.splitlines()

                for node in range (len(list_of_nodes)):
                        self.chaos_listBox_1.addItem(list_of_nodes[node])
                        self.count1 = self.count1 + 1
                        #self.chaos_listBox_1.item(node).setForeground(QColor('bla'))
                         
        else:
                self.chaos_listBox_1.clear()
                idx = 0
                for key,value in self.activeNodesData.items():
                        if not value:
                                self.chaos_listBox_1.addItem(key)
                                self.chaos_listBox_1.item(idx).setForeground(QColor('green'))
                                idx = idx + 1
                                self.count1 = self.count1 + 1
                        else:
                                self.chaos_listBox_1.addItem(key)
                                self.chaos_listBox_1.item(idx).setForeground(QColor('red'))
                                idx = idx + 1
                                self.count1 = self.count1 + 1



        if self.checkBox.isChecked():
                for index in range (self.chaos_listBox_1.count()):
                        item = self.chaos_listBox_1.item(index)
                        item.setFlags(Qt.NoItemFlags)  
#     def buttonunset(self):
# self.createChaosButton.setEnabled(True)    
#     def buttonunset(self):
#         self.createChaosButton.setEnabled(False)
#         self.killNodesRandomly()
         


    def killNodesRandomly(self):
        t_killnode = int(time.time()) - self.t_run
        if not self.simtimebox.text():
                self.chaos_listBox_3.clear()
                self.chaos_listBox_3.addItem("Please Enter the lambda value")
                return
        self.createChaosButton.setEnabled(False)
        self.mf_subframe2tabWidget.setCurrentIndex(2)
        # self.perturbationtabWidget.setCurrentIndex(1)
        QApplication.processEvents()
        import subprocess  
        import datetime
        sim_time = int(self.simtimebox.text()) - t_killnode
        no_of_nodes = self.chaos_listBox_2.count()

        getcontext().prec = 2 * sim_time
        _labmda = Decimal(no_of_nodes) / Decimal(sim_time)
        
        timeslist = []
        
        for i in range(no_of_nodes):
                timeNext = Decimal(-math.log(1.0 - random.random())) /Decimal(_labmda)
                timeslist.append(timeNext)

        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.chaos_listBox_3.addItem("The start time of simulation :: " + date_time + "\n")

        node_to_be_killed = []
        node_to_be_killed = [(self.chaos_listBox_2.item(i)) for i in range(self.chaos_listBox_2.count())]
          
        
        timeT = int(time.time())
        for i in range(no_of_nodes):
               
                now = datetime.datetime.now()
                date_time = now.strftime("%d/%m/%Y %H:%M:%S")
                
                self.chaos_listBox_3.addItem(date_time)
                              
                nodekill = random.choice(node_to_be_killed)
                row1 = node_to_be_killed.index(nodekill)  
                node_to_be_killed.remove(nodekill)

                self.chaos_listBox_2.takeItem(row1)

                proc=subprocess.Popen("rosnode kill "+nodekill.text(), shell=True, stdout=subprocess.PIPE)
                self.killNodeData.setdefault(nodekill.text(),int(time.time())-timeT)
                output=proc.communicate()[0]
                self.chaos_listBox_3.addItem(output)
                time.sleep(timeslist[i])
                
                
                
                
                
                
                     

    def addNode(self):
            #count1 = 0
            current_select_1 = self.chaos_listBox_1.currentItem()
            if not current_select_1:
                    self.chaos_listBox_3.addItem("No node selected :: Please select node")
                    return
            if not self.removeNodeButton.isChecked():
                    self.removeNodeButton.setEnabled(True)
            
            if not self.removeallNodeButton.isChecked():
                    self.removeallNodeButton.setEnabled(True)   

            node_name_1 = current_select_1.text()
            
            if self.activeNodesData:    
                self.chaos_listBox_2.addItem(node_name_1)    
                self.count2 = self.count2 + 1
                if self.activeNodesData[node_name_1]:
                        self.chaos_listBox_2.item(self.count2).setForeground(QColor('red'))
                else:
                        self.chaos_listBox_2.item(self.count2).setForeground(QColor('green'))
                        
                
                self.chaos_listBox_1.takeItem(self.chaos_listBox_1.row(current_select_1))
                self.count1 = self.count1 - 1
            else:
                self.chaos_listBox_2.addItem(node_name_1)    
                self.chaos_listBox_1.takeItem(self.chaos_listBox_1.row(current_select_1))  

            if not self.chaos_listBox_1.count():
                    self.addNodeButton.setEnabled(False)
                    self.addallNodeButton.setEnabled(False)

    def addallNode(self):
        #    idx = 0
            list_of_nodes = [(self.chaos_listBox_1.item(i)) for i in range(self.chaos_listBox_1.count())]
        #     if not list_of_nodes:
        #             self.chaos_listBox_3.addItem("All nodes are already selected")
        #             return
            if self.activeNodesData:    

                for node in list_of_nodes:
                        self.chaos_listBox_2.addItem(node.text())
                        self.count2 = self.count2 + 1  
                        self.chaos_listBox_1.takeItem(self.chaos_listBox_1.row(node))
                        self.count1 = self.count1 - 1
                        if self.activeNodesData[node.text()]:
                                self.chaos_listBox_2.item(self.count2).setForeground(QColor('red'))
                                
                        else:
                                self.chaos_listBox_2.item(self.count2).setForeground(QColor('green'))
            else:
                for node in list_of_nodes:
                        self.chaos_listBox_2.addItem(node.text())
                        self.chaos_listBox_1.takeItem(self.chaos_listBox_1.row(node))


            self.addallNodeButton.setEnabled(False)
            self.addNodeButton.setEnabled(False)
            self.removeallNodeButton.setEnabled(True) 
            self.removeNodeButton.setEnabled(True)           

    def removeNode(self):
            current_select_2 = self.chaos_listBox_2.currentItem()
            if not current_select_2:
                    self.chaos_listBox_3.addItem("No node selected :: Please select node")
                    return
            if not self.addNodeButton.isChecked():
                    self.addNodeButton.setEnabled(True)
            

            if not self.addallNodeButton.isChecked():
                    self.addallNodeButton.setEnabled(True)        
            
            node_name_2 = current_select_2.text()
            if self.activeNodesData:    

                self.chaos_listBox_1.addItem(node_name_2)

                self.count1 = self.count1 + 1
                if self.activeNodesData[node_name_2]:
                        self.chaos_listBox_1.item(self.count1).setForeground(QColor('red'))
                else:
                        self.chaos_listBox_1.item(self.count1).setForeground(QColor('green'))

                      
                self.chaos_listBox_2.takeItem(self.chaos_listBox_2.row(current_select_2))
                self.count2 = self.count2 - 1
            else:
                self.chaos_listBox_1.addItem(node_name_2)
                self.chaos_listBox_2.takeItem(self.chaos_listBox_2.row(current_select_2))

  
            #self.chaos_listBox_2.takeItem(self.chaos_listBox_2.row(current_select_2)) 
            
            if not self.chaos_listBox_2.count():
                    self.removeNodeButton.setEnabled(False)
                    self.removeallNodeButton.setEnabled(False)  
    
    def removeallNode(self):
            list_of_nodes = [(self.chaos_listBox_2.item(i)) for i in range(self.chaos_listBox_2.count())]
        #     if not list_of_nodes:
        #             self.chaos_listBox_3.addItem("All nodes are already deleted")
        #             return
            if self.activeNodesData:    

                for node in list_of_nodes:
                        self.chaos_listBox_1.addItem(node.text())
                        self.count1 = self.count1 + 1  
                        self.chaos_listBox_2.takeItem(self.chaos_listBox_2.row(node))
                        self.count2 = self.count2 - 1
                        if self.activeNodesData[node.text()]:
                                self.chaos_listBox_1.item(self.count1).setForeground(QColor('red'))
                                
                        else:
                                self.chaos_listBox_1.item(self.count1).setForeground(QColor('green'))
            else:
                 for node in list_of_nodes:     
                                self.chaos_listBox_1.addItem(node.text())
                                self.chaos_listBox_2.takeItem(self.chaos_listBox_2.row(node))
      
            self.removeallNodeButton.setEnabled(False)
            self.removeNodeButton.setEnabled(False)
            self.addallNodeButton.setEnabled(True)
            self.addNodeButton.setEnabled(True)

    def clearScreen(self):
            self.chaos_listBox_3.clear()


#     def sliderValue(self) 
    def resetTextbox(self):
        
        self.getLocationBox.clear()
        self.getMassBox.clear()

    def refreshObjectList(self):    
        gazeboModelInstance = GazeboModels()
        self.allGazeboObjects = gazeboModelInstance.getAllModels() 
        self.perturbationBox.addItems(self.allGazeboObjects)
        self.monitoringBox.addItems(self.allGazeboObjects)




# This is the function for Object Details panel, subframe2 consists of the interaction and object details panel #

    def objectDetailsPanel(self,MainWindow):
        self.mf_subframe2 = QtWidgets.QFrame(self.mainframe)
        self.mf_subframe2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mf_subframe2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mf_subframe2.setObjectName("mf_subframe2")

        self.gridLayout_8 = QtWidgets.QGridLayout(self.mf_subframe2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.mf_subframe2tabWidget = QtWidgets.QTabWidget(self.mf_subframe2)
        self.mf_subframe2tabWidget.setObjectName("mf_subframe2tabWidget")
# interaction tab declaration #
        self.interactionTab = QtWidgets.QWidget()
        self.interactionTab.setObjectName("interactionTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.interactionTab)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.mf_subframe2tabWidget.addTab(self.interactionTab, "")
# object details tab declaration #       
        self.objectdetailsTab = QtWidgets.QWidget()
        self.objectdetailsTab.setObjectName("objectdetailsTab")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.objectdetailsTab)
# object Addition tab declaration # 
       

        self.objectdetailsTabframe1 = QtWidgets.QFrame(self.objectdetailsTab)
        # self.objectdetailsTabframe1.setGeometry(QtCore.QRect(0, 0, 581, 563))
        self.objectdetailsTabframe1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.objectdetailsTabframe1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.objectdetailsTabframe1.setObjectName("objectdetailsTabframe1")
        self.chaosGrid_1 = QtWidgets.QGridLayout(self.objectdetailsTabframe1)
        self.chaosGrid_1.setObjectName("chaosGrid_1")
        
       

        spacerItem = QtWidgets.QSpacerItem(133, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.chaosGrid_1.addItem(spacerItem, 2, 3, 1, 2)
# reset button widget in object details tab #

        self.resetButton = QtWidgets.QPushButton(self.objectdetailsTabframe1)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.resetTextbox)
        self.resetButton.setGeometry(450, 8,80,25)
        self.chaosGrid_1.addWidget(self.resetButton, 0, 4, 1, 1)

# select button widget in object detials tab #

        self.selectButton = QtWidgets.QPushButton(self.objectdetailsTabframe1)
        self.selectButton.setObjectName("selectButton")
        self.selectButton.setGeometry(350, 8,80,25)
        self.chaosGrid_1.addWidget(self.selectButton, 0, 3, 1, 1)
        self.selectButton.clicked.connect(self.getObjectDetails)
        

#combo box for main page + add item for perturbation + get model from gazebo world
        self.list_Models = QtWidgets.QComboBox(self.objectdetailsTabframe1)
        self.list_Models.setObjectName("list_Models")
        self.list_Models.setEditable(True)
        self.list_Models.setEditText("Select Gazebo Objects")
        self.list_Models.setInsertPolicy(QComboBox.InsertAlphabetically)
        policy = self.list_Models.insertPolicy()

        self.chaosGrid_1.addWidget(self.list_Models, 0, 0, 1, 3)
        gazeboModelInstance = GazeboModels()
        self.allGazeboObjects = gazeboModelInstance.getAllModels()
        self.list_Models.addItems(self.allGazeboObjects)
# #       
        self.chaosGrid_1.addWidget(self.list_Models, 0, 0, 1, 2)

        # spacerItem1 = QtWidgets.QSpacerItem(156, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.chaosGrid_1.addItem(spacerItem1, 2, 0, 1, 1)

# text box to display the model location details #
        spacerItem = QtWidgets.QSpacerItem(69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.chaosGrid_1.addItem(spacerItem, 2, 0, 1, 1)

        self.getLocationBox = QtWidgets.QTextEdit(self.objectdetailsTabframe1)
        self.getLocationBox.setObjectName("getLocationBox")
        self.chaosGrid_1.addWidget(self.getLocationBox, 2, 1, 1, 1)

        self.getMassBox = QtWidgets.QTextEdit(self.objectdetailsTabframe1)
        self.chaosGrid_1.addWidget(self.getMassBox, 2, 2, 1, 3)

        self.getLocationLabel = QtWidgets.QLabel(self.objectdetailsTabframe1)
        self.getLocationLabel.setObjectName("getLocationLabel")
        self.chaosGrid_1.addWidget(self.getLocationLabel, 1, 1, 1, 1)

        self.getMassLabel = QtWidgets.QLabel(self.objectdetailsTabframe1)
        self.chaosGrid_1.addWidget(self.getMassLabel, 1, 2, 1, 3)

        spacerItem1 = QtWidgets.QSpacerItem(59, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.chaosGrid_1.addItem(spacerItem1, 2, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 339, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_1.addItem(spacerItem2, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 339, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_1.addItem(spacerItem3, 3, 3, 1, 1)
       


       

        # spacerItem2 = QtWidgets.QSpacerItem(20, 288, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.chaosGrid_1.addItem(spacerItem2, 3, 1, 1, 1)
        self.gridLayout_11.addWidget(self.objectdetailsTabframe1, 0, 0, 1, 1)
        
        self.chaosTab = QtWidgets.QWidget()
        self.chaosTab.setObjectName("chaosTab")
        # self.objectdetailsTabframe1 = QtWidgets.QFrame(self.chaosTab)
        self.chaosGrid = QtWidgets.QGridLayout(self.chaosTab)
        self.chaosGrid.setObjectName("chaosGrid")
        self.mf_subframe2tabWidget.addTab(self.chaosTab, "")
        
        self.monitoringGraphtab = QtWidgets.QWidget()
        self.mf_subframe2tabWidget.addTab(self.monitoringGraphtab, "")

        self.mf_subframe2tabWidget.addTab(self.objectdetailsTab, "")
       
#################################################################################
        self.objectAddTab = QtWidgets.QWidget()
        self.objectAddTab.setObjectName("objectAddTab")
        self.objectAddGrid = QtWidgets.QGridLayout(self.objectAddTab)
        self.objectAddGrid.setObjectName("objectAddGrid")
        self.mf_subframe2tabWidget.addTab(self.objectAddTab, "")
        

        

        
        


       

        self.gridLayout_8.addWidget(self.mf_subframe2tabWidget, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.mf_subframe2, 1, 0, 1, 1)

#  This is the function for interaction panel inside the main frame #

    def interactionPanel(self,MainWindow):
# Creating frame for interaction tab #

        self.interactionTabframe1 = QtWidgets.QFrame(self.interactionTab)
        self.interactionTabframe1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.interactionTabframe1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.interactionTabframe1.setObjectName("interactionTabframe1")

        self.gridLayout_5 = QtWidgets.QGridLayout(self.interactionTabframe1)
        self.gridLayout_5.setObjectName("gridLayout_5")
# heading of the perturbation list box #

        self.perturbationLabel = QtWidgets.QLabel(self.interactionTabframe1)
        self.perturbationLabel.setObjectName("perturbationLabel")
        self.gridLayout_5.addWidget(self.perturbationLabel, 0, 0, 1, 3)
        self.perturbationLabel.adjustSize()
# heading of the monitoring list box #
        self.monitoringLabel = QtWidgets.QLabel(self.interactionTabframe1)
        self.monitoringLabel.setObjectName("monitoringLabel")
        self.gridLayout_5.addWidget(self.monitoringLabel, 0, 4, 1, 3)

# refresh Button #
        self.refreshButton = QtWidgets.QPushButton(self.interactionTabframe1)
        self.gridLayout_5.addWidget(self.refreshButton, 0, 6, 1, 1)
        self.refreshButton.clicked.connect(self.refreshObjectList)

# perturbation combo box  #
        self.perturbationBox = QtWidgets.QComboBox(self.interactionTabframe1)
        self.perturbationBox.setObjectName("perturbationBox")
        self.perturbationBox.addItems(self.allGazeboObjects)
        self.perturbationBox.setEditable(True)
        self.perturbationBox.setEditText("Select Gazebo Objects")
        self.perturbationBox.setInsertPolicy(QComboBox.InsertAlphabetically)
        policy = self.perturbationBox.insertPolicy()
        # self.perturbationBox.InsertAlphabetically(self.allGazeboObjects)
        self.gridLayout_5.addWidget(self.perturbationBox, 1, 0, 1, 1)
# perturbation add button #
        self.per_addButton = QtWidgets.QPushButton(self.interactionTabframe1)
        self.per_addButton.setObjectName("per_addButton")
        self.per_addButton.clicked.connect(self.locModelLoc)
        self.gridLayout_5.addWidget(self.per_addButton, 1, 1, 1, 1)
# perturbation remove button #
        self.per_removeButton = QtWidgets.QPushButton(self.interactionTabframe1)
        self.per_removeButton.setObjectName("per_removeButton")
        self.per_removeButton.clicked.connect(self.deleteModeLoc)
        self.gridLayout_5.addWidget(self.per_removeButton, 1, 2, 1, 1)
# monitoring combo box #
        self.monitoringBox = QtWidgets.QComboBox(self.interactionTabframe1)
        self.monitoringBox.setObjectName("monitoringBox")
        self.monitoringBox.addItems(self.allGazeboObjects)
        self.monitoringBox.setEditable(True)
        self.monitoringBox.setEditText("Select Gazebo Objects")
        self.monitoringBox.setInsertPolicy(QComboBox.InsertAlphabetically)
        policy = self.monitoringBox.insertPolicy()
        self.gridLayout_5.addWidget(self.monitoringBox, 1, 4, 1, 1)
#  monitoring add button #
        self.mon_addButton = QtWidgets.QPushButton(self.interactionTabframe1)
        self.mon_addButton.setObjectName("mon_addButton")
        self.mon_addButton.clicked.connect(self.monitoringBoxAddItem)
        self.gridLayout_5.addWidget(self.mon_addButton, 1, 5, 1, 1)
# monitoring remove button #
        self.mon_removeButton = QtWidgets.QPushButton(self.interactionTabframe1)
        self.mon_removeButton.setObjectName("mon_removeButton")
        self.mon_removeButton.clicked.connect(self.monitoringBoxDeleteItem)
        self.gridLayout_5.addWidget(self.mon_removeButton, 1, 6, 1, 1)
# perturbation list box #
        self.per_listBox = QtWidgets.QListWidget(self.interactionTabframe1)
        self.per_listBox.setObjectName("per_listBox")
        self.listWidgetItem = QtWidgets.QListWidgetItem()
        self.gridLayout_5.addWidget(self.per_listBox, 2, 0, 1, 3)
# perturbation list box scroll bar #
        # self.per_listBox_scrollBar = QtWidgets.QScrollBar(self.interactionTabframe1)
        # self.per_listBox_scrollBar.setOrientation(QtCore.Qt.Vertical)
        # self.per_listBox_scrollBar.setObjectName("per_listBox_scrollBar")
        # self.gridLayout_5.addWidget(self.per_listBox_scrollBar, 2, 3, 1, 1)
# monitoring list box #
        self.mon_listBox = QtWidgets.QListWidget(self.interactionTabframe1)
        self.mon_listBox.setObjectName("mon_listBox")
        self.gridLayout_5.addWidget(self.mon_listBox, 2, 4, 1, 3)
# monitoring list box scroll bar #
        # self.mon_listBox_scrollBar = QtWidgets.QScrollBar(self.interactionTabframe1)
        # self.mon_listBox_scrollBar.setOrientation(QtCore.Qt.Vertical)
        # self.mon_listBox_scrollBar.setObjectName("mon_listBox_scrollBar")
        # self.gridLayout_5.addWidget(self.mon_listBox_scrollBar, 2, 7, 1, 1)
        # self.perturbationTab2 = QtWidgets.QWidget()
        # self.perturbationTab2.setObjectName("perturbationTab2")
        # self.perturbationtabWidget.addTab(self.perturbationTab2, "")
        self.gridLayout_6.addWidget(self.interactionTabframe1, 0, 0, 1, 1)

# contains the perturbation x,y,z sliders #

    def perturbationPanel(self,MainWindow):
        self.interactionTabframe1label3 = QtWidgets.QLabel(self.interactionTabframe1)
      
        self.gridLayout_5.addWidget(self.interactionTabframe1label3, 3, 1, 1, 8)
      

        # hintButton = QtWidgets.QPushButton(self.interactionTabframe1)
        # hintButton.setGeometry(740,145, 25, 25)
        # hintButton.resize(25,25)
        # hintButton.setStyleSheet("border:0px solid blue;border-radius:10px;")
        # hintButton.setIcon(QIcon('/home/amitash01/aws_chaos_robo/src/interface/src/interface_app/scripts/images/hint.png'))
        # self.gridLayout_5.addWidget(self.interactionTabframe1label3, 3, 1, 1, 10)
        # hintButton.setToolTip('Location Chaos : Perturbation range is 0-100. where 0 means no perturbation and \n 100 means 100/1000 of object present location in respective direction')


        self.perturbationtabWidget = QtWidgets.QTabWidget(self.interactionTabframe1)
       
        self.perturbationTab1 = QtWidgets.QWidget()

        

        self.gridLayout_4 = QtWidgets.QGridLayout(self.perturbationTab1)

        self.perturbationFrame1 = QtWidgets.QFrame(self.perturbationTab1)
        self.perturbationFrame1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.perturbationFrame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.perturbationFrame1)
# perturbation in X direction #
        self.perturbationFrame1verticalLayout = QtWidgets.QVBoxLayout()
        
       
        self.perturbation_X = QtWidgets.QSlider(self.perturbationFrame1)
        self.perturbation_X.setOrientation(QtCore.Qt.Horizontal)
       
        self.perturbation_X.setRange(0, 100)
   
        self.perturbation_X.setTickPosition(QSlider.TicksBelow)
        self.perturbation_X.setTickInterval(5)
        
       
        xBox = QtWidgets.QHBoxLayout()
        xBox.addStretch()
        xBox.setSpacing(0)
        xBox.setContentsMargins(0,0,0,0)
        xBox.setAlignment(Qt.AlignRight)
       
        self.perturbation_X.valueChanged.connect(self.updateLabelx)
        self.labelx = QtWidgets.QLabel('0', self.perturbationFrame1)
        self.labelx1 = QtWidgets.QLabel('%', self.perturbationFrame1)
        self.labelx.setAlignment(Qt.AlignRight)
        self.labelx.setMinimumWidth(80)
        # self.labelx1.setAlignment(Qt.AlignRight)
        # self.labelx1.setGeometry(793,35,10,80)
        # self.labelx1.setMinimumWidth(80)



        self.perturbationFrame1verticalLayout.addWidget(self.perturbation_X)
        xBox.addWidget(self.labelx)
        xBox.addWidget(self.labelx1)
        self.perturbationFrame1verticalLayout.addLayout(xBox)
        # self.perturbationFrame1verticalLayout.addWidget( self.labelx)
        # self.perturbationFrame1verticalLayout.addWidget( self.labelx1)

        self.x_label = QtWidgets.QLabel(self.perturbationFrame1)
        self.x_label.setAlignment(Qt.AlignLeft)
        self.perturbationFrame1verticalLayout.addWidget(self.x_label)
        self.perturbationFrame1verticalLayout.setSpacing(0)
        self.perturbationFrame1verticalLayout.setContentsMargins(0,0,0,0)
        
        
# perturbation in Y direction #
        yBox = QtWidgets.QHBoxLayout()
        yBox.addStretch()
        yBox.setSpacing(0)
        yBox.setContentsMargins(0,0,0,0)
        yBox.setAlignment(Qt.AlignRight)
        self.perturbation_Y = QtWidgets.QSlider(self.perturbationFrame1)
        self.perturbation_Y.setOrientation(QtCore.Qt.Horizontal)
        self.perturbation_Y.setRange(0, 100)
        self.perturbation_Y.setTickPosition(QSlider.TicksBelow)
        self.perturbation_Y.setTickInterval(5)
        self.perturbationFrame1verticalLayout.addWidget(self.perturbation_Y)


        self.perturbation_Y.valueChanged.connect(self.updateLabely)
        self.labely = QtWidgets.QLabel('0', self.perturbationFrame1)
        self.labely1 = QtWidgets.QLabel('%', self.perturbationFrame1)
        self.labely.setAlignment(Qt.AlignRight)
        self.labely.setMinimumWidth(80)

        # self.perturbationFrame1verticalLayout.addWidget( self.labely)

        yBox.addWidget(self.labely)
        yBox.addWidget(self.labely1)
        self.perturbationFrame1verticalLayout.addLayout(yBox)

        self.y_label = QtWidgets.QLabel(self.perturbationFrame1)
        self.y_label.setAlignment(Qt.AlignLeft)
        self.perturbationFrame1verticalLayout.addWidget(self.y_label)
# perturbation in Z direction #
        self.perturbation_Z = QtWidgets.QSlider(self.perturbationFrame1)
        self.perturbation_Z.setOrientation(QtCore.Qt.Horizontal)
       
        self.perturbation_Z.setRange(0, 100)
   
        self.perturbation_Z.setTickPosition(QSlider.TicksBelow)
        self.perturbation_Z.setTickInterval(5)
        
       
        zBox = QtWidgets.QHBoxLayout()
        zBox.addStretch()
        zBox.setSpacing(0)
        zBox.setContentsMargins(0,0,0,0)
        zBox.setAlignment(Qt.AlignRight)
       
        self.perturbation_Z.valueChanged.connect(self.updateLabelz)
        self.labelz = QtWidgets.QLabel('0', self.perturbationFrame1)
        self.labelz1 = QtWidgets.QLabel('%', self.perturbationFrame1)
        self.labelz.setAlignment(Qt.AlignRight)
        self.labelz.setMinimumWidth(80)
        



        self.perturbationFrame1verticalLayout.addWidget(self.perturbation_Z)
        zBox.addWidget(self.labelz)
        zBox.addWidget(self.labelz1)
        self.perturbationFrame1verticalLayout.addLayout(zBox)
        # self.perturbationFrame1verticalLayout.addWidget( self.labelx)
        # self.perturbationFrame1verticalLayout.addWidget( self.labelx1)

        self.z_label = QtWidgets.QLabel(self.perturbationFrame1)
        self.z_label.setAlignment(Qt.AlignLeft)
        self.perturbationFrame1verticalLayout.addWidget(self.z_label)

        # valx = float(self.perturbation_X.value())
        # print(valx)
               
        # valy = float(self.rangeofAcceptance.value())
        # valz = float(self.perturbation_Z.value())

        # if (valx > 0 or valy > 0  or valz > 0):
       
        # if (self.labelx > 0 or self.labely > 0  or self.labelz > 0):
        #         self.mf_actionButtonschaos.setEnabled(True)


# range of acceptance #
        rBox = QtWidgets.QHBoxLayout()
        rBox.addStretch()
        rBox.setSpacing(0)
        rBox.setContentsMargins(0,0,0,0)
        rBox.setAlignment(Qt.AlignRight)
        self.rangeofAcceptance = QtWidgets.QSlider(self.perturbationFrame1)
        self.rangeofAcceptance.setOrientation(QtCore.Qt.Horizontal)
        self.rangeofAcceptance.setRange(0, 100)
        self.rangeofAcceptance.setTickPosition(QSlider.TicksBelow)
        self.rangeofAcceptance.setTickInterval(5)
        self.perturbationFrame1verticalLayout.addWidget(self.rangeofAcceptance)


        self.rangeofAcceptance.valueChanged.connect(self.updateLabelr)
        self.labelr = QtWidgets.QLabel('0', self.perturbationFrame1)
        self.labelr1 = QtWidgets.QLabel('%', self.perturbationFrame1)
        self.labelr.setAlignment(Qt.AlignRight)
        self.labelr.setMinimumWidth(80)

        # self.perturbationFrame1verticalLayout.addWidget( self.labely)

        rBox.addWidget(self.labelr)
        rBox.addWidget(self.labelr1)
        self.perturbationFrame1verticalLayout.addLayout(rBox)

        self.rangeofAcceptanceLabel = QtWidgets.QLabel(self.perturbationFrame1)
        self.rangeofAcceptanceLabel.setAlignment(Qt.AlignLeft)
        self.perturbationFrame1verticalLayout.addWidget(self.rangeofAcceptanceLabel)


        self.gridLayout_3.addLayout(self.perturbationFrame1verticalLayout, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.perturbationFrame1, 0, 0, 8, 8)
        self.perturbationtabWidget.addTab(self.perturbationTab1, "")
        # self.monitoringResultTab = QtWidgets.QWidget()
        # self.perturbationtabWidget.addTab(self.monitoringResultTab, "")
        self.gridLayout_5.addWidget(self.perturbationtabWidget, 4, 0, 1, 8)

    
        # self.gridLayout_5.addWidget(self.perturbationtabWidget, 4, 0, 1, 8)
##..................................................##
    def monitoringGraph(self,MainWindow):

        qlayout = QtWidgets.QHBoxLayout(self.monitoringGraphtab)
        self.monitoringGraphtab.setLayout(qlayout)
        
        qscroll = QtWidgets.QScrollArea(self.monitoringGraphtab)
        qscroll.setGeometry(QtCore.QRect(0, 0, 500, 500))
        qlayout.addWidget(qscroll)
       
        qscrollContents = QtWidgets.QWidget()
        
        qscrollLayout = QtWidgets.QVBoxLayout(qscrollContents)
        qscrollLayout.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
        

 

        qscroll.setWidget(qscrollContents)
        qscroll.setWidgetResizable(True)
       

 

        # self.scrollGrid = QtWidgets.QGridLayout() 
        qfigWidget = QtWidgets.QWidget(qscrollContents)

 

                 
                     
        # self.canvas = Canvas( qfigWidget, width=8, height=2)
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addStretch()
        hbox3.setContentsMargins(0,0,0,0)
        hbox3.setAlignment(Qt.AlignLeft)
        self.canvas = Canvas( qfigWidget, width=9, height=4)
        hbox3.addWidget(self.canvas)
        # self.canvas.setMinimumSize(100,150)
        spacerItemCanvas = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hbox3.addItem(spacerItemCanvas)
        # qscrollLayout.addLayout(hbox3)
       
       
               
        self.canvas.setParent(qfigWidget)
        toolbar = NavigationToolbar(self.canvas, qfigWidget)

 

        
                      
                
               
        plotLayout = QtWidgets.QVBoxLayout()

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch()
        hbox2.setSpacing(460)
        hbox2.setContentsMargins(0,0,0,0)
        # hbox2.setAlignment(Qt.AlignRight)
        # self.Button = QtWidgets.QPushButton(qfigWidget)
        # self.Button.setFixedSize(QtCore.QSize(90,25))
        self.LabelForCanvas1 = QtWidgets.QLabel('Select Monitoring Time (in seconds)', qfigWidget)
        self.LabelForCanvas1.setAlignment(Qt.AlignLeft)
        # self.LabelForCanvas1.setGeometry(0,0,100,0)
        self.LabelForCanvas2 = QtWidgets.QLabel('Deviation in Trajectory (in %)', qfigWidget)
        spacerItemCanvaslabel = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.LabelForCanvas.setFixedSize(QtCore.QSize(90,25))
        # hbox2.addWidget(self.Button)
        hbox2.addWidget(self.LabelForCanvas1)
        hbox2.addWidget(self.LabelForCanvas2)
        hbox2.addItem(spacerItemCanvaslabel)
        # plotLayout.addLayout(hbox2)


    #########

        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch()
        hbox1.setSpacing(10)
        hbox1.setContentsMargins(0,0,0,0)
        hbox1.setAlignment(Qt.AlignLeft)
        

 
        self.simtimebox = QtWidgets.QLineEdit(qfigWidget)
        self.simtimebox.setFixedSize(180,25)
        self.onlyint = QIntValidator()
        self.simtimebox.setValidator(self.onlyint)
        self.simtimebox.setToolTip("This value determines parameter lambda for poisson distribution.\n It is calculated as follows:\nlambda =  no.of nodes to be killed/Entered sim time")
        
        spacerItemnew = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.nextButtonForCanvas = QtWidgets.QPushButton(qfigWidget)
        self.nextButtonForCanvas.setObjectName("nextButtonForCanvas")
        self.nextButtonForCanvas.setFixedSize(QtCore.QSize(90,25))
        self.nextButtonForCanvas.setGeometry(0,0,90,25)
        self.refreshButtonForCanvas = QtWidgets.QPushButton(qfigWidget)
        self.refreshButtonForCanvas.setFixedSize(QtCore.QSize(90,25))
  
        self.nextButtonForCanvas.clicked.connect(self.switchGraph)
        self.refreshButtonForCanvas.clicked.connect(self.refreshGraph)

 


        self.rangeBox = QtWidgets.QLineEdit(qfigWidget)
        self.rangeBox.setFixedSize(180,25)
        self.onlyint = QIntValidator()
        self.rangeBox.setValidator(self.onlyint)
        # self.percentage = QtWidgets.QLabel(qfigWidget)
        spacerItemnew1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

 
        hbox1.addWidget(self.simtimebox)
        
        hbox1.addItem(spacerItemnew)

        hbox1.addWidget(self.nextButtonForCanvas)
        # hbox1.setContentsMargins(0,0,0,0)
        hbox1.addWidget(self.refreshButtonForCanvas)
        hbox1.addWidget(self.rangeBox)
        # hbox1.addWidget(self.percentage)
        hbox1.addItem(spacerItemnew1)
       
  
        # plotLayout.addWidget(self.nextButtonForCanvas)
        # plotLayout.addWidget(self.refreshButtonForCanvas)
        # plotLayout.addLayout(hbox1)



 

        # plotLayout.addWidget(self.canvas)
        # plotLayout.addWidget(toolbar)

 

        hbox = QtWidgets.QHBoxLayout()
        
        self.graphListbox = QtWidgets.QListWidget(qfigWidget)
        self.graphListbox.setFixedSize(QtCore.QSize(800,200))
       
        hbox.addWidget(self.graphListbox)



        
               
        # plotLayout.addWidget(toolbar)
        plotLayout.addLayout(hbox2)
        plotLayout.addLayout(hbox1)
        plotLayout.addLayout(hbox3)
        plotLayout.addWidget(toolbar)
        plotLayout.addLayout(hbox)
        qfigWidget.setLayout(plotLayout)
        

 

        
        

 

                        # prevent the canvas to shrink beyond a point
                        # original size looks like a good minimum size
        self.canvas.setMinimumSize(self.canvas.size())
                
        qscrollLayout.addWidget(qfigWidget)
        
        
        qscrollContents.setLayout(qscrollLayout)



### Function for the slider values ###


    def updateLabelx(self, value):
        self.labelx.setText(str(value))
        
        if ( value > 0):
                self.mf_actionButtonschaos.setEnabled(True)
        else:
                self.mf_actionButtonschaos.setEnabled(False)
             


    def updateLabely(self, value2):
        self.labely.setText(str(value2))
        if (value2 > 0):
                self.mf_actionButtonschaos.setEnabled(True)
        else:
                self.mf_actionButtonschaos.setEnabled(False)

    def updateLabelz(self, value3):
        self.labelz.setText(str(value3))
        if (value3 > 0):
                self.mf_actionButtonschaos.setEnabled(True)
        else:
                self.mf_actionButtonschaos.setEnabled(False)


    def updateLabelr(self, value4):
        self.labelr.setText(str(value4))
        if (value4 > 0):
                self.mf_actionButtonschaos.setEnabled(True)
        else:
                self.mf_actionButtonschaos.setEnabled(False)






######## Function for the base line ######################

    def checkboxStatus(self):
        if self.checkBox.isChecked():
#                self.tracking = 1
                self.disableSlider()
        ############################
                self.allObjects = list()

                for index in xrange(self.per_listBox.count()):
                        self.allObjects.append(self.per_listBox.item(index).text())
                
                print(self.allObjects)
                l= len(self.allObjects)
                for i in range (0, l):
                        mdlName = self.allObjects[i]
                        print(mdlName)
                        getLocation = GetModelLocation(mdlName)
                        print(getLocation)
                        getLoc = getLocation.showGazeboModels()
                        print(getLoc)

                        initial_x_pos = -1*float(getLoc.pose.position.y)
                        print(initial_x_pos)
                        initial_y_pos = float(getLoc.pose.position.x)
                        print(initial_y_pos)
                        initial_z_pos = float(getLoc.pose.position.z)

                        if i not in self.initial_pos:
                                self.initial_pos[i]=[initial_x_pos, initial_y_pos]
                                

        

                print("==>",self.tracking)
                self.removeallNode()
                for index in range (self.chaos_listBox_1.count()):
                        item = self.chaos_listBox_1.item(index)
                        item.setFlags(Qt.NoItemFlags)  
        else:
 #               self.tracking = 0
                self.enableSlider()
                print("==>",self.tracking)
                for index in range (self.chaos_listBox_1.count()):
                        item = self.chaos_listBox_1.item(index)
                        item.setFlags(Qt.ItemIsEnabled) 
                        

    def disableSlider(self):
            self.perturbation_X.setEnabled(False)
            self.labelx.setText(str(0))
            self.perturbation_Y.setEnabled(False)
            self.labely.setText(str(0))

          
            
            self.perturbation_Z.setEnabled(False)
            self.labelz.setText(str(0))


    def enableSlider(self):
            self.perturbation_X.setEnabled(True)
            self.perturbation_Y.setEnabled(True)
        #     self.rangeofAcceptance.setEnabled(True)
            self.perturbation_Z.setEnabled(True)   

      

                

        # qfWidget = QtWidgets.QWidget(qscrollContents)

        # self.canvas = Canvas( qfWidget, width=8, height=2)
        # # # self.canvas = Canvas(self. scrollBar, width=8, height=2)
        # self.canvas.move(0,0)
        # qscrollLayout.addWidget(qfWidget)
        # qscrollContents.setLayout(qscrollLayout)
        # # self.monitoringResultGrid.addWidget(self.canvas, 0,0,1,1)

        # # self.pertabgrid.addWidget(self.monitoringResultFrame, 0, 0, 1, 1)

        # self.gridLayout_5.addWidget(self.perturbationtabWidget, 4, 0, 1, 8)




#This is the bottom frame inside the main frame consisting of action buttons for the chaos robo#
    def actionButtons(self,MainWindow):
        self.mf_actionButtons = QtWidgets.QFrame(self.mainframe)
        self.mf_actionButtons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mf_actionButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mf_actionButtons.setObjectName("mf_actionButtons")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mf_actionButtons)
        self.gridLayout_2.setObjectName("gridLayout_2")

#terminal for packages and launch file
        self.terminal_label = QtWidgets.QLabel(self.mf_actionButtons)
        self.gridLayout_2.addWidget(self.terminal_label, 0, 0, 1, 2)
        
        self.terminal = QtWidgets.QLineEdit(self.mf_actionButtons)
        self.terminal.setStyleSheet("QLineEdit" "{background : lightblue;}")
        self.gridLayout_2.addWidget(self.terminal, 1, 0, 1, 2)

        # self.terminalBox = QtWidgets.QComboBox(self.mf_actionButtons)
        # # self.terminalBox.addItems(self.allGazeboObjects)
        # self.terminalBox.setEditable(True)
        # self.terminalBox.setEditText("Select Package")
        # self.terminalBox.setInsertPolicy(QComboBox.InsertAlphabetically)
        # policy =  self.terminalBox.insertPolicy()
        # self.gridLayout_2.addWidget(self.terminalBox, 0, 2, 1, 1)


        # self.terminalBox2 = QtWidgets.QComboBox(self.mf_actionButtons)
        # # self.terminalBox.addItems(self.allGazeboObjects)
        # self.terminalBox2.setEditable(True)
        # self.terminalBox2.setEditText("Select Launch File")
        # self.terminalBox2.setInsertPolicy(QComboBox.InsertAlphabetically)
        # policy =  self.terminalBox2.insertPolicy()
        # self.gridLayout_2.addWidget(self.terminalBox2, 0, 3, 1, 1)

#chaos button#
        self.mf_actionButtonschaos = QtWidgets.QPushButton(self.mf_actionButtons)
        self.mf_actionButtonschaos.setObjectName("mf_actionButtonschaos")
        self.mf_actionButtonschaos.clicked.connect(self.initChaos)
        self.mf_actionButtonschaos.setEnabled(False)
        self.gridLayout_2.addWidget(self.mf_actionButtonschaos, 2, 0, 1, 1)
# # rqt button #
        # self.mf_actionButtonsrqt = QtWidgets.QPushButton(self.mf_actionButtons)
        # self.mf_actionButtonsrqt.setObjectName("mf_actionButtonsrqt")
        # self.mf_actionButtonschaos.clicked.connect(self.initChao)
        # self.gridLayout_2.addWidget(self.mf_actionButtonsrqt, 0, 1, 1, 1)
#run button#
        self.mf_actionButtonsrun = QtWidgets.QPushButton(self.mf_actionButtons)
        self.mf_actionButtonsrun.setObjectName("mf_actionButtonsrun")
        self.mf_actionButtonsrun.clicked.connect(self.gear_controller)
        self.mf_actionButtonsrun.clicked.connect(self.recordNodes)
        self.gridLayout_2.addWidget(self.mf_actionButtonsrun, 2, 1, 1, 1)
#check box#        
        self.checkBox = QtWidgets.QCheckBox(self.mf_actionButtons)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.checkboxStatus)
        # self.restartButton = QtWidgets.QPushButton(self.mf_actionButtons)
        # self.restartButton.setObjectName("restartButton")
        # self.restartButton.clicked.connect(self.callBack)

        # self.gridLayout_2.addWidget(self.restartButton, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.checkBox, 2, 2, 1, 1)

        self.gridLayout_10.addWidget(self.mf_actionButtons, 2, 0, 1, 1)

    
    def chaosPanel(self, MainWindow):
  
      
        #Creating Frame for chaosPanel      
        self.chaosTabframe1 = QtWidgets.QFrame(self.chaosTab)
        self.chaosTabframe1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.chaosTabframe1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chaosGrid_2 = QtWidgets.QGridLayout(self.chaosTabframe1)

        
        # Create Chaos Button
        self.createChaosButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.createChaosButton.clicked.connect(self.killNodesRandomly)
        self.chaosGrid_2.addWidget(self.createChaosButton, 1, 4, 1, 1)
        self.createChaosButton.setEnabled(False)


        #Add Node Button

        self.addNodeButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.addNodeButton.clicked.connect(self.addNode)
        self.chaosGrid_2.addWidget(self.addNodeButton, 3, 2, 1, 1)


        #Clear Screen Button

        self.clearButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.clearButton.clicked.connect(self.clearScreen)
        self.chaosGrid_2.addWidget(self.clearButton, 15, 1, 1, 1)


        #Add All Node Button

        self.addallNodeButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.addallNodeButton.clicked.connect(self.addallNode)
        self.chaosGrid_2.addWidget(self.addallNodeButton, 4, 2, 1, 1)

        # Simulation time input box

        # self.simtimebox = QtWidgets.QLineEdit(self.chaosTabframe1)
        # self.simtimebox.setFixedSize(180,25)
        # self.onlyint = QIntValidator()
        # self.simtimebox.setValidator(self.onlyint)
        # self.simtimebox.setToolTip("This value determines parameter lambda for poisson distribution.\n It is calculated as follows:\nlambda =  no.of nodes to be killed/Entered sim time")
        # self.chaosGrid_1.addWidget(self.simtimebox, 1, 2, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_2.addItem(spacerItem, 13, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_2.addItem(spacerItem1, 17, 2, 1, 1)

        # Display Output Screen Label

        self.label3 = QtWidgets.QLabel(self.chaosTabframe1)
        self.chaosGrid_2.addWidget(self.label3, 15, 0, 1, 1)

        # Display active Nodes List Box 1

        self.chaos_listBox_1 = QtWidgets.QListWidget(self.chaosTabframe1)
        self.listWidgetItem_1 = QtWidgets.QListWidgetItem()
        self.chaosGrid_2.addWidget(self.chaos_listBox_1, 3, 0, 9, 2)

        # displayActivenodes button widget in chaos tab #s

        self.activeNodesButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.activeNodesButton.clicked.connect(self.displayActiveNodes)
        self.activeNodesButton.setToolTip("Red Nodes denote Nodes which became active during simulation \n Green Nodes denote Nodes which are active before simulation ")
        self.chaosGrid_2.addWidget(self.activeNodesButton, 1, 1, 1, 1)

        # Display Nodes to be Killed List Box 2
        self.chaos_listBox_2 = QtWidgets.QListWidget(self.chaosTabframe1)
        self.listWidgetItem_2 = QtWidgets.QListWidgetItem()
        self.chaosGrid_2.addWidget(self.chaos_listBox_2, 3, 3, 9, 2)

        # Display Output Screen List Box 3

        self.chaos_listBox_3 = QtWidgets.QListWidget(self.chaosTabframe1)
        self.chaos_listBox_3.adjustSize()
        self.listWidgetItem_3 = QtWidgets.QListWidgetItem()
        self.chaosGrid_2.addWidget(self.chaos_listBox_3, 18, 0, 1, 5)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_2.addItem(spacerItem2, 16, 2, 1, 1)
        
        #List of  active Nodes Label

        self.label1 = QtWidgets.QLabel(self.chaosTabframe1)
        self.chaosGrid_2.addWidget(self.label1, 1, 0, 1, 1)

        #List of of Nodes to be Killed Label

        self.label2 = QtWidgets.QLabel(self.chaosTabframe1)
        self.chaosGrid_2.addWidget(self.label2, 1, 3, 1, 1)

        
        
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_2.addItem(spacerItem3, 2, 2, 1, 1)

        #Enter sim time Label

        # self.label4 = QtWidgets.QLabel(self.chaosTabframe1)
        # self.chaosGrid_1.addWidget(self.label4, 0, 2, 1, 1)

        #Remove Node Button

        self.removeNodeButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.removeNodeButton.clicked.connect(self.removeNode)
        self.chaosGrid_2.addWidget(self.removeNodeButton, 5, 2, 1, 1)

        #Remove All Node Button

        self.removeallNodeButton = QtWidgets.QPushButton(self.chaosTabframe1)
        self.removeallNodeButton.clicked.connect(self.removeallNode)
        self.chaosGrid_2.addWidget(self.removeallNodeButton, 6, 2, 1, 1)


        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chaosGrid_2.addItem(spacerItem4, 7, 2, 2, 1)
        self.chaosGrid.addWidget(self.chaosTabframe1, 0, 0, 1, 1)



    def objectAdd(self, MainWindow):

        self.objectAddTabframe1 = QtWidgets.QFrame(self.objectAddTab)
        self.objectAddTabframe1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.objectAddTabframe1.setFrameShadow(QtWidgets.QFrame.Raised)

        self.gridlayout_13 = QtWidgets.QGridLayout(self.objectAddTabframe1)

        self.objectAddListLabel = QtWidgets.QLabel(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.objectAddListLabel, 0, 0, 1, 2)

        self.objectAddListBox = QtWidgets.QComboBox(self.objectAddTabframe1)
        self.objectAddListBox.setObjectName("objectAddListBox")
        
        self.objectAddListBox.addItems(objectList)
        self.objectAddListBox.setEditable(True)
        self.objectAddListBox.setEditText("Select Gazebo Objects")
        self.objectAddListBox.setInsertPolicy(QComboBox.InsertAlphabetically)
        policy = self.objectAddListBox.insertPolicy()

        


        self.gridlayout_13.addWidget(self.objectAddListBox, 1, 0, 1, 2)

        self.objectEditLabel = QtWidgets.QLabel(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.objectEditLabel, 0, 2, 1, 2)

        self.objectEdit = QtWidgets.QLineEdit(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.objectEdit, 1, 2, 1, 2)

        self.xPositionLabel = QtWidgets.QLabel(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.xPositionLabel, 2,0,1,2)

        self.xPosition = QtWidgets.QLineEdit(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.xPosition, 3, 0, 1, 2)

        self.yPositionLabel = QtWidgets.QLabel(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.yPositionLabel, 2, 2, 1, 2)

        self.yPosition = QtWidgets.QLineEdit(self.objectAddTabframe1)
        self.gridlayout_13.addWidget(self.yPosition, 3, 2, 1, 2)


        self.objectSelect = QtWidgets.QPushButton(self.objectAddTabframe1)
        self.objectSelect.clicked.connect(self.objectAddListItemSelect)
        self.gridlayout_13.addWidget(self.objectSelect, 4, 0, 1, 2)

        self.objectRemove = QtWidgets.QPushButton(self.objectAddTabframe1)
        self.objectRemove.clicked.connect(self.objectAddListItemRemove)
        self.gridlayout_13.addWidget(self.objectRemove, 4, 2, 1, 2)

        self.objectAddList = QtWidgets.QListWidget(self.objectAddTabframe1)
        self.objectAddListWidget = QtWidgets.QListWidgetItem()
        self.gridlayout_13.addWidget(self.objectAddList, 5, 0, 5, 5)





        self.objectAddGrid.addWidget(self.objectAddTabframe1, 0, 0, 1, 1)

       






if __name__ == "__main__":
    time.sleep(50)        
    rospy.init_node('gui_app')
    try:
        
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = GUI(MainWindow)
        ui.mainInterface(MainWindow)

        MainWindow.show()
        # MainWindow.showMaximized()
        # MainWindow.setFixedSize(1024,528)
        sys.exit(app.exec_())
    except rospy.ROSInterruptException:
        pass




