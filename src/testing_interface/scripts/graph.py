#!/usr/bin/env python2

import rospy
import os,sys
# import matplotlib.pyplot as plt
import numpy as np
from chaosState import GetModelLocation, SetModelLocation
import threading
from threading import *
import time
import cPickle
from decimal import Decimal,getcontext
class PlotGraph:

    def __init__(self,listofObjects, index, rng, track , monitoringtime):

        self.listofObjects = listofObjects
        self.returnQue = [None] * 10
        self.rng = rng
        self.track = track
        self.monitoringtime = monitoringtime

    def threadGetLoc(self,name,idx):
        data = []
        startTime = time.time()
        timeT = startTime
        while (timeT - startTime) < self.monitoringtime:
            getLocation = GetModelLocation(name)
            getLoc = getLocation.showGazeboModels()
            #getLoc = getLocation.showObjectMass()
            x_pos = -1*float(getLoc.pose.position.y)
            y_pos = float(getLoc.pose.position.x)
            z_pos = float(getLoc.pose.position.z)
            # x_pos = -1*float(getLoc.link_state.pose.y)
            # y_pos = float(getLoc.link_state.pose.x)
            # z_pos = float(getLoc.link_state.pose.z)
            
            timeT = time.time()
            data.append([(timeT - startTime),[x_pos,y_pos,z_pos]])
            time.sleep(0.01)
            # print ("---->",name,x_pos,(timeT - startTime),idx)
        
        self.returnQue[idx] = data

        if self.track == 1:
            # print("----------->",self.track,str(self.listofObjects[idx-1])+'.txt')
            os.system('pwd')
            with open(str(self.listofObjects[idx-1])+'.txt','w') as f:
                cPickle.dump(data,f)

    def plotGraphs(self,setData):
        idx = 1
        listOfAllGraphs = []
        
        for each in setData:
            t = np.array([x[0] for x in each])
            x = np.array([i[1][0] for i in each])
            y = np.array([j[1][1] for j in each])
            z = np.array([k[1][2] for k in each])
        
            try:
                
                with open(str(self.listofObjects[len(self.listofObjects) - idx])+'.txt','rb') as f:
                    dataReload = cPickle.load(f)
                    t0 = np.array([x1[0] for x1 in dataReload])
                    x0 = np.array([i1[1][0] for i1 in dataReload])
                    y0 = np.array([j1[1][1] for j1 in dataReload])
                    z0 = np.array([k1[1][2] for k1 in dataReload])

                    # mean = (x0 + y0 + z0) / 3                    
                    lowerX = x0 - (self.rng)/100.0
                    lowerY = y0 - (self.rng)/100.0
                    lowerZ = z0 - (self.rng)/100.0

                    upperX = x0 + (self.rng)/100.0
                    upperY = y0 + (self.rng)/100.0
                    upperZ = z0 + (self.rng)/100.0
                    
                    # plt.fill_between(t0,lowerX, upperX, facecolor='red',alpha=0.2)
                    # plt.fill_between(t0,lowerY, upperY, facecolor='blue',alpha=0.2)
                    # plt.fill_between(t0,lowerZ, upperZ, facecolor='green',alpha=0.2)
                    

            except Exception as error:
                print("Error ",error)
                

            title = str(self.listofObjects[idx-1]) +': motion in x,y,z axis'
            idx += 1
            listOfAllGraphs.append([t,x,y,z,title,t0,lowerX,upperX,lowerY,upperY,lowerZ,upperZ])
            
            
        return listOfAllGraphs



        

        

        