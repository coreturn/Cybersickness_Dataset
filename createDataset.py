# -*- coding: utf-8 -*-
from scipy import interpolate
import numpy as np
import pandas as pd


class Questionnaire:
    def __init__(self, SSQ, Nausea, Oculomotor,Disorientation):
        self.SSQ=SSQ # 整体眩晕
        self.Nausea=Nausea
        self.Oculomotor=Oculomotor
        self.Disorientation=Disorientation


class steamVR:
    def __init__(self, rawHead, rawSpeed, rawRotation):
        self.rawHead=rawHead
        self.resampledHead=None
        
        self.rawSpeed=rawSpeed
        self.resampledSpeed=None
        
        self.rawRotation=rawRotation
        self.resampledRotation=None
        self.fs_speed=200
        self.fs_rotation=200
        self.fs_head=200

class E4:
    def __init__(self, GSR, BVP, HR, TEM ):
        self.GSR=GSR
        self.BVP=BVP
        self.HR=HR
        self.TEM=TEM


# 数据集的最终形式
class oneTest:
    def __init__(self, Name, Order, SicknessLevel, Steam, Empatica):
        self.Name=Name
        self.Order=Order
        self.SicknessLevel=SicknessLevel
        self.Steam= Steam
        self.Empatica= Empatica
    
    def resampleSteam(self,fs=200):
        self.resampleSpeed(fs)
        self.resampleRotation(fs)
        self.resampleHead(fs)
                   
    
# 重新采集speed    
    def resampleSpeed(self,fs=200):
        self.Steam.resampledSpeed=self.reSamplingDataFrame(self.Steam.rawSpeed,fs)
        self.Steam.fs_speed=fs
        
# 重新采集rotation    
    def resampleRotation(self,fs=200):
        self.Steam.resampledRotation=self.reSamplingDataFrame(self.Steam.rawRotation,fs)
        self.Steam.fs_rotation=fs
    
# 对头信号重新采集    
    def resampleHead(self,fs=200):
        self.Steam.resampledHead=self.reSamplingDataFrame(self.Steam.rawHead,fs)
        self.Steam.fs_head=fs


# 对dataframe 重新取样
    def reSamplingDataFrame(self,df,fs):    
        # get the shape of the old dataframe
        df_shape=df.shape
        
        # create an empty container
        new_df=pd.DataFrame(columns=df.columns)   
        x=df[['Time']].values
        xnew = np.arange(x[0], x[-1], 1/fs)
        new_df.iloc[:,0]=xnew
        
        for id in range(1,df_shape[1]):
            y=df.iloc[:,id].values
            _, ynew=self.reSampling(x,y,fs)        
            new_df.iloc[:,id]=ynew
        return new_df

# 分片插值函数，resamplng 时进行调用
    def reSampling(self,x,y,fs):
        xnew = np.arange(x[0], x[-1], 1/fs)    
        #tck = interpolate.splrep(x, y, s=0)
        #ynew = interpolate.splev(xnew, tck, der=0)
        x = np.squeeze(x)
        f = interpolate.interp1d(x,  y, kind='quadratic',fill_value="extrapolate")
        ynew=f(xnew)
        return xnew, ynew
    
    
    
    
    