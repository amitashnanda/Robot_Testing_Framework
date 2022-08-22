#!/usr/bin/env python

import rospy
import os
# import matplotlib.pyplot as plt
import numpy as np
from chaosState import GetModelLocation, SetModelLocation
import threading
from threading import *
import time
import cPickle

class PlotGraph:

    def __init__(self,listofObjects, index, rng, track):

        self.listofObjects = listofObjects
        self.returnQue = [None] * index
        self.rng = rng
        self.track = track

    def threadGetLoc(self,name,idx):
        data = []
        startTime = time.time()
        timeT = startTime
        while (timeT - startTime) <50.0:
            getLocation = GetModelLocation(name)
            getLoc = getLocation.showGazeboModels()
            x_pos = -1*float(getLoc.pose.position.y)
            y_pos = float(getLoc.pose.position.x)
            z_pos = float(getLoc.pose.position.z)
            timeT = time.time()
            data.append([(timeT - startTime),[x_pos,y_pos,z_pos]])
            time.sleep(0.01)
            # print ("---->",name,x_pos,(timeT - startTime),idx)
        
        self.returnQue[idx] = data

        if self.track == 1:
            with open(str(self.listofObjects[idx-1])+'.txt','w') as f:
                cPickle.dump(data,f)

    def plotGraphs(self,setData):
        idx = 1
        for each in setData:
            t = np.array([x[0] for x in each])
            x = np.array([i[1][0] for i in each])
            y = np.array([j[1][1] for j in each])
            z = np.array([k[1][2] for k in each])
            # plt.figure(str(self.listofObjects[idx-1]))
            try:
                with open(str(self.listofObjects[idx-1])+'.txt','rb') as f:
                    dataReload = cPickle.load(f)
                    t0 = np.array([x1[0] for x1 in dataReload])
                    x0 = np.array([i1[1][0] for i1 in dataReload])
                    y0 = np.array([j1[1][1] for j1 in dataReload])
                    z0 = np.array([k1[1][2] for k1 in dataReload])
                    lowerX = x0 - float(self.rng)/100.0
                    lowerY = y0 - float(self.rng)/100.0
                    lowerZ = z0 - float(self.rng)/100.0

                    upperX = x0 + float(self.rng)/100.0
                    upperY = y0 + float(self.rng)/100.0
                    upperZ = z0 + float(self.rng)/100.0
                    # plt.fill_between(t0,lowerX, upperX, facecolor='red',alpha=0.2)
                    # plt.fill_between(t0,lowerY, upperY, facecolor='blue',alpha=0.2)
                    # plt.fill_between(t0,lowerZ, upperZ, facecolor='green',alpha=0.2)

            except:
                pass

            
            # plt.plot(t,x, 'r')
            # plt.plot(t,y, 'b')
            # plt.plot(t,z, 'g')
            # plt.legend(labels = ('X', 'Y', 'Z'), loc= 'upper right')
            title = str(self.listofObjects[idx-1]) +': motion in x,y,z axis'
            # plt.xlabel('Time')
            # plt.ylabel('')
            idx += 1
        return [t,x,y,z,title]



        

        

        