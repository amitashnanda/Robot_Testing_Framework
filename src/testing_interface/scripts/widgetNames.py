from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from chaosState import GazeboModels, GetModelLocation


# This function consists of the naming declaration for all the widgets #

def widgetnames(self, MainWindow):
       global comBox
       _translate = QtCore.QCoreApplication.translate
       MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
       self.headingLabel.setText(_translate("MainWindow", "Chaos Robo Testing Platform"))
       self.mf_actionButtonschaos.setText(_translate("MainWindow", "Chaos Robo"))
       # self.mf_actionButtonsrqt.setText(_translate("MainWindow", "RQT Console"))
       self.mf_actionButtonsrun.setText(_translate("MainWindow", "RUN"))
       self.checkBox.setText(_translate("MainWindow", "Base Line"))
       # self.restartButton.setText(_translate("MainWindow", "Restart"))


       self.mf_subframe2tabWidget.setTabText(self.mf_subframe2tabWidget.indexOf(self.interactionTab), _translate("MainWindow", "Chaos_Perturbation"))
       self.mf_subframe2tabWidget.setTabText(self.mf_subframe2tabWidget.indexOf(self.objectAddTab), _translate("MainWindow", "Object_Addition"))
       self.mf_subframe2tabWidget.setTabText(self.mf_subframe2tabWidget.indexOf(self.objectdetailsTab), _translate("MainWindow", "Object_Properties"))
      
       self.mf_subframe2tabWidget.setTabText(self.mf_subframe2tabWidget.indexOf(self.chaosTab), _translate("MainWindow", "Chaos_NodeKill"))
       self.mf_subframe2tabWidget.setTabText(self.mf_subframe2tabWidget.indexOf(self.monitoringGraphtab), _translate("MainWindow", "Chaos_MonitoringGraph"))
      
      
       self.selectButton.setText(_translate("MainWindow", "Select"))
       self.resetButton.setText(_translate("MainWindow", "Reset"))
        
       self.getLocationLabel.setText(_translate("MainWindow", "      Object Positioning Details"))
       self.getMassLabel.setText(_translate("MainWindow", "    Object Mass and Inertia Details"))

       self.perturbationLabel.setText(_translate("MainWindow", "Select Object(s) for Perturbation"))
       self.monitoringLabel.setText(_translate("MainWindow", "Select Object(s) for Monitoring"))
       self.per_addButton.setText(_translate("MainWindow", "Add"))
       self.per_removeButton.setText(_translate("MainWindow", "Remove"))
       self.mon_addButton.setText(_translate("MainWindow", "Add"))
       self.mon_removeButton.setText(_translate("MainWindow", "Remove"))

       self.objectSelect.setText(_translate("MainWindow", "Add Object to Simulation World"))
       self.objectRemove.setText(_translate("MainWindow", "Remove Object from Simulation World"))
       self.objectAddListLabel.setText(_translate("MainWindow", "Select Object to be Added"))
       self.objectEditLabel.setText(_translate("MainWindow", "Enter the name of Object"))
       self.xPositionLabel.setText(_translate("MainWindow", "Enter X co-ordinate value"))
       self.yPositionLabel.setText(_translate("MainWindow", "Enter Y co-ordinate value"))
       self.refreshButton.setText(_translate("MainWindow", "Refresh"))


        
       self.interactionTabframe1label3.setText(_translate("MainWindow", "For the Selected Gazebo Objects location uncertanity range defination"))
       self.x_label.setText(_translate("MainWindow", "                                                 Perturbation in X direction"))
       self.y_label.setText(_translate("MainWindow", "                                                 Perturbation in Y direction"))
       self.z_label.setText(_translate("MainWindow", "                                                 Perturbation in Z direction"))
       self.rangeofAcceptanceLabel.setText(_translate("MainWindow", "                                         Acceptance of Deviation in Trajectory"))
       self.perturbationtabWidget.setTabText(self.perturbationtabWidget.indexOf(self.perturbationTab1), _translate("MainWindow", "Location Chaos"))
       # self.perturbationtabWidget.setTabText(self.perturbationtabWidget.indexOf(self.monitoringResultTab), _translate("MainWindow", "Monitoring Graph"))
       self.nextButtonForCanvas.setText(_translate("MainWindow", "Switch"))
       self.refreshButtonForCanvas.setText(_translate("MainWindow", "Redraw"))
       # self.percentage.setText(_translate("MainWindow", "%"))
       #self.Button.setText(_translate("MainWindow", "Click"))

       # self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
       # self.actionMaximize.setText(_translate("MainWindow", "Maximize"))

# #Create Chaos Tab Button Labels       
       self.activeNodesButton.setText(_translate("MainWindow", "All Nodes"))
       # self.activeNodesButton.setStyleSheet("background-color : green")
       self.addNodeButton.setText(_translate("MainWindow", "Add"))
       self.addallNodeButton.setText(_translate("MainWindow", "Add All-->"))
       self.removeNodeButton.setText(_translate("MainWindow", "Remove"))
       self.createChaosButton.setText(_translate("MainWindow", "Kill Nodes"))
       # self.createChaosButton.setStyleSheet("background-color : red")
       self.removeallNodeButton.setText(_translate("MainWindow", "<--Remove All"))
       self.clearButton.setText(_translate("MainWindow", "Clear"))

# #Create Chaos Tab List Box Labels
       self.label1.setText(_translate("MainWindow", "List of Active Nodes"))
       self.label2.setText(_translate("MainWindow", "List of of Nodes to be Killed"))
       self.label3.setText(_translate("MainWindow", "Output Log"))
       #self.label4.setText(_translate("MainWindow", "Enter sim time (in seconds)"))