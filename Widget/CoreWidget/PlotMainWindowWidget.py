import pyqtgraph as pg
# from pyqtgraph import ColorMap
from pyqtgraph.Qt import QtGui,QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scipy import optimize
from PyQt5.QtGui import *
from Model.DataAnalysis.CaculateAtoms import *
# from decimal import *
from PyQt5.QtGui import QFont
from copy import deepcopy
from matplotlib import cm
# import matplotlib.pyplot as plt
import numpy as np
# getcontext().prec = 4#Set significant number



class PlotMainWindow(QWidget):

    atom_number = pyqtSignal(object)  #from PyQt5.QtCore
    Pxatom_num = pyqtSignal(object)
    atom_numberF = pyqtSignal(object)
    Pxatom_numF = pyqtSignal(object)
    # TotalPhotons_num = pyqtSignal(object)
    fittingdata = pyqtSignal(dict)
    roipos = pyqtSignal(list)
    tempnum = pyqtSignal(object)
    HOD = pyqtSignal(object)
    VOD = pyqtSignal(object)
    # temcula = pyqtSignal(list)

    def __init__(self):
        super(PlotMainWindow, self).__init__()
        self.layout = QGridLayout(self)

        # win = pg.GraphicsView()
        l = pg.GraphicsLayout(border=(100, 100, 100))   #创建一个图形布局对象 l，它用于容纳和管理各种图形项（item）
        win = pg.GraphicsLayoutWidget()                 #创建一个图形布局窗口部件 win，它是一个图形界面组件，可以用来显示和交互图形布局
        win.setCentralItem(l)                           #将图形布局 l 设置为图形布局窗口部件 win 的中心项，以便图形布局能够填充整个窗口
        pg.setConfigOptions(imageAxisOrder='row-major') #设置全局配置选项，指定图像的坐标轴顺序为行优先（row-major）。这样设置后，在使用 pg.ImageItem 显示图像时，默认会按照行优先的方式进行显示和索引
        # pg.setConfigOptions(leftButtonPan=False)
        self.viewBox = l.addPlot()                      #在图形布局 l 中添加一个绘图视图 viewBox，它将用于显示各种图形项
        # self.viewBox.hideAxis('left')                   #hide the left and right
        # self.viewBox.hideAxis('bottom')                 #隐藏坐标轴
        self.img = pg.ImageItem()                       #创建一个图像项 img，它是 pyqtgraph 库中用于显示图像数据的项（item）
        y1 = np.arange(-10, 10, 0.1)                    #生成x值
        x1 = np.zeros(len(y1))                          #生成y值

        # self.curve = pg.PlotCurveItem(x1, y1)           #创建一个 PlotCurveItem 对象，并将数据设置为x1和y1
        # self.viewBox.addItem(self.curve)
        # # self.layout.addWidget(self.curve,0,0,1,8)  #设置主窗口位置
        
        # self.viewBox1 = l.addPlot() 
        # self.viewBox2 = l.addPlot()

        colormap = cm.get_cmap("jet")  # cm.get_cmap("CMRmap")
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
        self.img.setLookupTable(lut)

        self.viewBox.setMouseEnabled(x=False, y=False)#make image can not move
        # pg.setConfigOptions(leftButtonPan=False)
        # self.viewBox.addItem(self.img)
        # self.layout.addWidget(win,0,0,20,20)  #设置主窗口位置0088
        # self.img_label = QLabel()
        # self.img_label.setFont(QFont("Roman times", 10))  #10
        # self.img_label1 = QLabel('| Temperature/K')
        # self.img_label1.setFont(QFont("Roman times", 10))  #10
        # self.img_label2 = QLabel('| HpeakOD')
        # self.img_label2.setFont(QFont("Roman times", 10))  #10
        # self.img_label3 = QLabel()
        # self.img_label3.setFont(QFont("Roman times", 10))  #10
        # self.img_label4 = QLabel('| VpeakOD')
        # self.img_label4.setFont(QFont("Roman times", 10))  #10
        # self.img_label5 = QLabel()
        # self.img_label5.setFont(QFont("Roman times", 10))  #10

        self.viewBox.addItem(self.img)
        self.layout.addWidget(win,0,0,20,20)  #设置主窗口位置0088
        self.img_label = QLabel("")
        self.img_label.setFont(QFont("Roman times", 10))  #10
        self.img_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label.setMinimumSize(100, 25)
        self.img_label.setMaximumSize(100, 25)
        self.img_label1 = QLabel('| Temperature/K')
        self.img_label1.setFont(QFont("Roman times", 10))  #10
        self.img_label1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label1.setMinimumSize(100, 25)
        self.img_label1.setMaximumSize(100, 25)
        self.img_label2 = QLabel('| HpeakOD')
        self.img_label2.setFont(QFont("Roman times", 10))  #10
        self.img_label2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label2.setMinimumSize(100, 25)
        self.img_label2.setMaximumSize(100, 25)
        self.img_label3 = QLabel("")
        self.img_label3.setFont(QFont("Roman times", 10))  #10
        self.img_label3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label3.setMinimumSize(100, 25)
        self.img_label3.setMaximumSize(100, 25)
        self.img_label4 = QLabel('| VpeakOD')
        self.img_label4.setFont(QFont("Roman times", 10))  #10
        self.img_label4.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label4.setMinimumSize(100, 25)
        self.img_label4.setMaximumSize(100, 25)
        self.img_label5 = QLabel("")
        self.img_label5.setFont(QFont("Roman times", 10))  #10
        self.img_label5.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.img_label5.setMinimumSize(100, 25)
        self.img_label5.setMaximumSize(100, 25)

        # 通过修改棋盘格的数量和位置来修改窗口部件位置
        self.layout.addWidget(self.img_label,16,18,1,2)#1,0,1,2，PicName
        self.layout.addWidget(self.img_label1,17,18,1,2)#1,2,1,2 '| Temperature/K'
        self.layout.addWidget(self.img_label2,18,18,1,1)#1,4,1,1 '| HpeakOD'
        self.layout.addWidget(self.img_label3,18,19,1,1)#1,5  ((HpeakOD))
        self.layout.addWidget(self.img_label4,19,18)#1,6 '| VpeakOD'
        self.layout.addWidget(self.img_label5,19,19)#1,7 ((VpeakOD))
        ###########################################
        # self.layout.addWidget(self.img_label,17,19,1,2)#1,0,1,2，PicName
        # self.layout.addWidget(self.img_label1,18,19,1,2)#1,2,1,2 '| Temperature/K'
        # self.layout.addWidget(self.img_label2,19,19,1,1)#1,4,1,1 '| HpeakOD'
        # self.layout.addWidget(self.img_label3,19,20,1,1)#1,5  ((HpeakOD))
        # self.layout.addWidget(self.img_label4,20,19,1,1)#1,6 '| VpeakOD'
        # self.layout.addWidget(self.img_label5,20,20,1,1)#1,7 ((VpeakOD))
        ###########################################
        self.img_label.setStyleSheet("background-color: #000000;color: #ffffff")
        self.img_label1.setStyleSheet("background-color: #000000;color: #ffffff")
        self.img_label2.setStyleSheet("background-color: #000000;color: #ffffff")
        self.img_label3.setStyleSheet("background-color: #000000;color: #ffffff")
        self.img_label4.setStyleSheet("background-color: #000000;color: #ffffff")
        self.img_label5.setStyleSheet("background-color: #000000;color: #ffffff")
        # self.img_label.setStyleSheet("background-color: #ffffff;color: #000000")
        # self.img_label1.setStyleSheet("background-color: #ffffff;color: #000000")
        # self.img_label2.setStyleSheet("background-color: #ffffff;color: #000000")
        # self.img_label3.setStyleSheet("background-color: #ffffff;color: #000000")
        # self.img_label4.setStyleSheet("background-color: #ffffff;color: #000000")
        # self.img_label5.setStyleSheet("background-color: #ffffff;color: #000000")

        # ############################################
        # 方法一：模仿原版add_raw的方法，直接使用l.addPlot().plot()，
        # 使得self.img_pixelplot_v = l.addPlot().plot()
        # 优点：接下来的画笔参数以及数据更新的语法可以直接搬用原版
        # 缺点：没有找到确定位置的方法
        # 通过对原来函数的仿写，发现原先的绘图函数与图片是放在同一窗口部件中的（展示的图像实质上也就是个矩阵），
        # 也就是说两者的数轴是共用的，可以通过另开一窗口绘制图像比对得出
        # 需要注意的是，虽然self.viewBox = l.addPlot()但是
        # 如果用self.img_pixelplot_v = self.viewBox.plot()，函数图像会与照片重合。即plot在了viewBox里
        # 而如果用self.img_pixelplot_h = l.addPlot().plot()，函数图像会在部件中的另一区域，即实例化了一个新item
        # 该段改动效果为：在原来的窗口右边添加了两列窗口用于绘制函数
        
        # self.img_pixelplot_v = l.addPlot().plot()
        # self.img_pixelplot_h = l.addPlot().plot()
        # y1 = np.arange(-10, 10, 0.1)   # 生成x值
        # x1 = np.zeros(len(y1))   # 生成y值
        # # 在子图中绘制函数图像
        # self.img_pixelplot_v.setPen(color='b', width=3)
        # self.img_pixelplot_v.setData(x1, y1)
        # self.img_pixelplot_h.setPen(color='b', width=3)
        # self.img_pixelplot_h.setData(y1, x1)

        # subLayout = pg.GraphicsLayout(border=(0, 0, 0))    # 创建一个子区域的图形布局对象
        # l.addItem(subLayout)                               # 将子区域的图形布局添加到主图形布局中
        # subLayout.nextRow()                                # 在子区域中创建新的行
        # # 将 img_pixelplot_h 添加到子区域中
        # self.img_pixelplot_h.setParentItem(subLayout)
        # # 设置子区域在主图形布局中的位置
        # subLayout.setPos(10, 10)

        # self.layout.addWidget(self.subLayout,1,7)

        # self.layout.addWidget(self.img_pixelplot_h,1,1,1,8)
        # 显示图形窗口
        # win.show()
        # ############################################
        # self.img_pixelplot_v = l.addPlot()
        # self.img_pixelplot_h = l.addPlot()
        # y1 = np.arange(-10, 10, 0.1)
        # x1 = np.zeros(len(y1))
        # #############################################
        
        # # 使用 pg.plot() 创建2个单独的窗口，并返回一个 PlotWidget 对象
        # win1 = pg.plot(title='Function Plot')
        # win2 = pg.plot(title='Function Plot2')
        # win2.close
        # # 在窗口中绘制函数的图像
        # win1.plot(x1, y1, pen='b')
        # win2.plot(x1, y1, pen='b')
        # win1.close
        # self.layout.addWidget(win1,0,8,1,8)
        # self.layout.addWidget(win2,8,0,8,1)

        ###############################################
        # 外侧像素值函数
        # add plot 内侧添加函数
        self.img_pixelplot_v = l.addPlot(row=0, col=1)
        self.img_pixelplot_h = l.addPlot(row=1, col=0)

        # 绘制函数图像
        y1 = np.arange(-10, 10, 0.1)  # 生成x值
        x1 = np.zeros(len(y1))  # 生成y值

        self.img_pixelplot_v2 = self.img_pixelplot_v.plot()
        self.img_pixelplot_h2 = self.img_pixelplot_h.plot()
        self.img_pixelplot_v.plot().setPen(color='b', width=3)
        self.img_pixelplot_v.plot().setData(x1, y1)
        self.img_pixelplot_h.plot().setPen(color='b', width=3)
        self.img_pixelplot_h.plot().setData(y1, x1)

        self.img_pixelplot_v.plot(x1, y1, pen={'color': 'y', 'width': 3})
        self.img_pixelplot_h.plot(y1, x1, pen={'color': 'y', 'width': 3})

        # self.h_axes = self.viewBox.plot()
        # ?
        # self.img_pixelplot_v.plot.setPen(color='r', width=2)#x
        # # TODO: vertical axes hasn't finisheviewBox.plot() 
        # # self.v_axes = self.viewBox.plot()
        # self.img_pixelplot_h.plot.setPen(color='r', width=2)
        # ?
        
        self.img_pixelplot_v.setFixedWidth(180)   # 设置 img_pixelplot_v 的宽度
        self.img_pixelplot_v.setFixedHeight(500)  # 设置 img_pixelplot_v 的高度

        self.img_pixelplot_h.setFixedWidth(600)   # 设置 img_pixelplot_h 的宽度
        self.img_pixelplot_h.setFixedHeight(150)  # 设置 img_pixelplot_h 的高度

        # 将窗口部件添加到布局中
        # self.layout.addWidget(self.img_pixelplot_h,1,7)

        # # 设置子图大小和位置
        # self.img_pixelplot_v.setGeometry(0, 0, 100, 600) #100, 0, 100, 600
        # self.img_pixelplot_h.setGeometry(0, 0, 800, 100) #0, 1, 800, 100

        ##############################################

        # # 在子图中绘制函数图像
        # # self.img_pixelplot_v.setPen(color='b', width=3)
        # self.img_pixelplot_v.plot(x1, y1)

        # # self.img_pixelplot_h.setPen(color='b', width=3)
        # self.img_pixelplot_h.plot(y1, x1)

        # # 将窗口部件添加到布局中
        # self.layout.addWidget(win)

        ############################################
        self.setLayout(self.layout)      #将自定义窗口部件的布局设置为self.layout,其中self.layout是一个布局对象(如 QtGui.QVBoxLayout 或 QtGui.QHBoxLayout)
        self.h_axes = None               #初始化了一个属性 self.h_axes，并将其设置为 None
        self.v_axes = None
        self.data = None
        self.data_shape = None
        #获取当前屏幕的几何信息
        screen = QtGui.QDesktopWidget().screenGeometry()   
        #将自定义窗口部件的大小设置为根据屏幕宽度计算得到的固定值
        self.setFixedSize(screen.width()*44/100,screen.width()*(9/16)*63/100) 
        # print(self.width(), self.height())
        
    def change_HpeakOD(self, HpeakOD):
        self.img_label3.setText(str('%.3e' % HpeakOD))

    def change_VpeakOD(self, VpeakOD):
        self.img_label5.setText(str('%.3e' % VpeakOD))

    def change_TEM(self, TEM):
        self.img_label1.setText(str('| '+'%.3e' % TEM + '/K  '))

    def colormapsel(self, colormapname):
        colormapname = cm.get_cmap(settings.colorlist[colormapname])  # cm.get_cmap("CMRmap")
        colormapname._init()
        lut = (colormapname._lut * 255).view(np.ndarray)     # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
        self.img.setLookupTable(lut)

    def add_roi(self, roi_cbk_state, line_cbk_state):
        if roi_cbk_state.isChecked():
            # video mode doesn't have roi statistics
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have roi statistics, please choose another mode.")
                    # 0 doesn't check, 2 means check
                    roi_cbk_state.setCheckState(0)
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                roi_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                return
            roisize = int(settings.widget_params["Analyse Data Setting"]["roisize"])
            self.roi = pg.ROI([300, 300], [roisize, roisize], maxBounds=QtCore.QRect(0, 0, self.data_shape[1], self.data_shape[0]))
            # self.roi.setPen(color=QColor(42, 130, 218), width=3)  # set roi width and color
            self.roi.setPen(color=QColor(255, 255, 0), width=4)  # set roi width and color(225, 225, 225)浅灰色

            self.viewBox.addItem(self.roi)
            # make sure ROI is drawn above image
            self.roi.setZValue(10)
            self.goto_pos()
            self.calculate_roi()
            # if settings.widget_params["Analyse Data Setting"]["add_ten"]:
            # self.vLine = pg.InfiniteLine(angle=90, movable=False)
            # self.hLine = pg.InfiniteLine(angle=0, movable=False)
            # self.vLine.setPen(color='r', width=3)
            # self.hLine.setPen(color='r', width=3)
            # self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
            # self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
            # self.viewBox.addItem(self.vLine, ignoreBounds=True)
            # self.viewBox.addItem(self.hLine, ignoreBounds=True)
            if settings.widget_params["Analyse Data Setting"]["realtime"] == True:
                self.roi.sigRegionChanged.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChanged.connect(self.calculate_roi)
            else:
                self.roi.sigRegionChangeFinished.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChangeFinished.connect(self.calculate_roi)

            self.roi.sigRegionChanged.connect(self.changetenpos)


            settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
        else:
            roi_cbk_state.setCheckState(0)
            # axes_cbk_state.setCheckState(0)
            line_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
            settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
            # remove viewBox's items
            # self.viewBox.clear()
            # add image item
            try:
                self.viewBox.removeItem(self.roi)
            except AttributeError:
                pass

###############################################
    def add_roi2(self):
        if 1:
            # video mode doesn't have roi statistics
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have roi statistics, please choose another mode.")
                    # 0 doesn't check, 2 means check
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                return
            roisize = int(settings.widget_params["Analyse Data Setting"]["roisize"])
            self.roi = pg.ROI([300, 300], [roisize, roisize], maxBounds=QtCore.QRect(0, 0, self.data_shape[1], self.data_shape[0]))
            # self.roi.setPen(color=QColor(42, 130, 218), width=3)  # set roi width and color
            self.roi.setPen(color=QColor(225, 225, 225), width=3)  # set roi width and color

            self.viewBox.addItem(self.roi)
            # make sure ROI is drawn above image
            self.roi.setZValue(10)
            self.goto_pos()
            self.calculate_roi()
            # if settings.widget_params["Analyse Data Setting"]["add_ten"]:
            # self.vLine = pg.InfiniteLine(angle=90, movable=False)
            # self.hLine = pg.InfiniteLine(angle=0, movable=False)
            # self.vLine.setPen(color='r', width=3)
            # self.hLine.setPen(color='r', width=3)
            # self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
            # self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
            # self.viewBox.addItem(self.vLine, ignoreBounds=True)
            # self.viewBox.addItem(self.hLine, ignoreBounds=True)
            if settings.widget_params["Analyse Data Setting"]["realtime"] == True:
                self.roi.sigRegionChanged.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChanged.connect(self.calculate_roi)
            else:
                self.roi.sigRegionChangeFinished.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChangeFinished.connect(self.calculate_roi)

            self.roi.sigRegionChanged.connect(self.changetenpos)


            settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
        # else:
        #     roi_cbk_state.setCheckState(0)
        #     # axes_cbk_state.setCheckState(0)
        #     line_cbk_state.setCheckState(0)
        #     settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
        #     settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
        #     # remove viewBox's items
        #     # self.viewBox.clear()
        #     # add image item
        #     try:
        #         self.viewBox.removeItem(self.roi)
        #     except AttributeError:
        #         pass

###############################################

    def setroichange(self):
        try:
            if settings.widget_params["Analyse Data Setting"]["realtime"] == True:
                self.roi.sigRegionChangeFinished.disconnect(self.update_ch_fitting_cs)
                self.roi.sigRegionChangeFinished.disconnect(self.calculate_roi)
                self.roi.sigRegionChanged.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChanged.connect(self.calculate_roi)
            else:
                self.roi.sigRegionChanged.disconnect(self.update_ch_fitting_cs)
                self.roi.sigRegionChanged.disconnect(self.calculate_roi)
                self.roi.sigRegionChangeFinished.connect(self.update_ch_fitting_cs)
                self.roi.sigRegionChangeFinished.connect(self.calculate_roi)
        except AttributeError:
            pass


    def change_roisize(self):
        try:
            self.roi.setSize(int(settings.widget_params["Analyse Data Setting"]["roisize"]))
        except AttributeError:
            pass

    def goto_pos(self):
        try:
            xp = deepcopy(settings.widget_params["Analyse Data Setting"]["xpos"])
            yp = deepcopy(settings.widget_params["Analyse Data Setting"]["ypos"])
            if xp > int(self.data_shape[1] - self.roi.size()[0]/2):
                xp = int(self.data_shape[1] - self.roi.size()[0]/2)-1
            elif xp < int(self.roi.size()[0]/2):
                xp = int(self.roi.size()[0])/2
            if yp > int(self.data_shape[0] - self.roi.size()[1]/2):
                yp = int(self.data_shape[0] - self.roi.size()[1]/2)-1
            elif yp < int(self.roi.size()[0]/2):
                yp = int(self.roi.size()[1])/2
            self.roi.setPos(float(xp - int(self.roi.size()[0]/2)), float(yp - int(self.roi.size()[1]/2)))
        except TypeError:
            print('add ROI')
        except AttributeError:
            print('add ROI')

    def add_rawdata(self, cbk_state):
        if cbk_state.isChecked():
            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = True
                print('add horizontal axes')
                # add horizontal axes and vertical axes
                # 内侧像素值函数图像
                # self.h_axes = self.viewBox.plot()
                # self.h_axes.setPen(color='y', width=2)#x
                # TODO: vertical axes hasn't finisheviewBox.plot()
                # self.v_axes = self.viewBox.plot()
                # self.v_axes.setPen(color='y', width=2)
                # end 内侧像素值函数图像
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = True
                self.vLine = pg.InfiniteLine(angle=90, movable=False)
                self.hLine = pg.InfiniteLine(angle=0, movable=False)
                self.vLine.setPen(color='r', width=2, style=QtCore.Qt.DashLine) #设置画线的笔
                self.hLine.setPen(color='r', width=2, style=QtCore.Qt.DashLine)
                self.vLine.setPos(self.roi.pos()[0] + self.roi.size()[0] / 2)
                self.hLine.setPos(self.roi.pos()[1] + self.roi.size()[1] / 2)
                self.viewBox.addItem(self.vLine, ignoreBounds=True)
                self.viewBox.addItem(self.hLine, ignoreBounds=True)
                self.update_ch_fitting_cs()

            else:
                print("please add roi first.")
                # 0 doesn't check, 2 means check
                cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
                return
        else:
            cbk_state.setCheckState(0)
            self.viewBox.removeItem(self.h_axes)
            self.viewBox.removeItem(self.v_axes)
            try:
                self.viewBox.removeItem(self.vLine)
                self.viewBox.removeItem(self.hLine)
            except AttributeError:
                pass

            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                self.viewBox.addItem(self.roi)
            settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
            # remove plotItem if cross axes has added
            if self.h_axes is not None and self.v_axes is not None:
                self.viewBox.removeItem(self.h_axes)
                self.viewBox.removeItem(self.v_axes)
############################################
    def add_rawdata2(self):
        if 1:
            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = True
                print('add horizontal axes')
                # add horizontal axes and vertical axes
                # 内侧像素值函数图像
                self.h_axes = self.viewBox.plot()
                self.h_axes.setPen(color='y', width=2)#x
                # TODO: vertical axes hasn't finisheviewBox.plot()
                self.v_axes = self.viewBox.plot()
                self.v_axes.setPen(color='y', width=2)
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = True
                self.vLine = pg.InfiniteLine(angle=90, movable=False)
                self.hLine = pg.InfiniteLine(angle=0, movable=False)
                self.vLine.setPen(color='r', width=2, style=QtCore.Qt.DashLine) #设置画线的笔
                self.hLine.setPen(color='r', width=2, style=QtCore.Qt.DashLine)
                self.vLine.setPos(self.roi.pos()[0] + self.roi.size()[0] / 2)
                self.hLine.setPos(self.roi.pos()[1] + self.roi.size()[1] / 2)
                self.viewBox.addItem(self.vLine, ignoreBounds=True)
                self.viewBox.addItem(self.hLine, ignoreBounds=True)
                self.update_ch_fitting_cs()

            else:
                print("please add roi first.")
                # 0 doesn't check, 2 means check
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
                return
            
        # else:
        #     self.viewBox.removeItem(self.h_axes)
        #     self.viewBox.removeItem(self.v_axes)
        #     try:
        #         self.viewBox.removeItem(self.vLine)
        #         self.viewBox.removeItem(self.hLine)
        #     except AttributeError:
        #         pass

        #     if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
        #         self.viewBox.addItem(self.roi)
        #     settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
        #     # remove plotItem if cross axes has added
        #     if self.h_axes is not None and self.v_axes is not None:
        #         self.viewBox.removeItem(self.h_axes)
        #         self.viewBox.removeItem(self.v_axes)
#####################################
        # end modi

    def add_fitting(self, mode):
        # if mode.isChecked():
        if settings.widget_params["Fitting Setting"]["mode"] == 1:
            # pass
            try:
                self.viewBox.removeItem(self.h_axes2)
                self.viewBox.removeItem(self.v_axes2)
            except AttributeError:
                pass
            self.h_axes2 = self.viewBox.plot()
            self.h_axes2.setPen(color='r', width=2)  # x
            self.v_axes2 = self.viewBox.plot()
            self.v_axes2.setPen(color='r', width=2)
            self.update_ch_fitting_cs()
            # print(111)
        else:
            try:
                self.viewBox.removeItem(self.h_axes2)
                self.viewBox.removeItem(self.v_axes2)
            except AttributeError:
                pass
        # else:
        #     try:
        #         self.viewBox.removeItem(self.h_axes2)
        #         self.viewBox.removeItem(self.v_axes2)
        #     except AttributeError:
        #         pass

    # def add_cross_axes(self, cbk_state):
    #     if cbk_state.isChecked():
    #         if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
    #             settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = True
    #             self.vLine = pg.InfiniteLine(angle=90, movable=False)
    #             self.hLine = pg.InfiniteLine(angle=0, movable=False)
    #             self.vLine.setPen(color='r', width=3)
    #             self.hLine.setPen(color='r', width=3)
    #             self.vLine.setPos(self.roi.pos()[0] + self.roi.size()[0] / 2)
    #             self.hLine.setPos(self.roi.pos()[1] + self.roi.size()[1] / 2)
    #             self.viewBox.addItem(self.vLine, ignoreBounds=True)
    #             self.viewBox.addItem(self.hLine, ignoreBounds=True)
    #         else:
    #             settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
    #             print("please add roi first.")
    #             cbk_state.setCheckState(0)
    #             return
    #     else:
    #         cbk_state.setCheckState(0)
    #         try:
    #             self.viewBox.removeItem(self.vLine)
    #             self.viewBox.removeItem(self.hLine)
    #         except AttributeError:
    #             pass
    def changetenpos(self):
        try:
            if settings.widget_params["Analyse Data Setting"]["add_cross_axes"]:
                self.vLine.setPos(self.roi.pos()[0] + self.roi.size()[0] / 2)
                self.hLine.setPos(self.roi.pos()[1] + self.roi.size()[1] / 2)
        except AttributeError:
            pass

    def update_ch_fitting_cs(self):
    #更新十字上的像素坐标值
        # if settings.cameraON == False:
        if 1:
            try:
                # if settings.widget_params["Analyse Data Setting"]["add_cross_axes"]:
                #     self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
                #     self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
                if settings.widget_params["Analyse Data Setting"]["add_rawdata"] or settings.widget_params["Fitting Setting"]["mode"] == 1:

                    self.datals = self.data
                    h_dataraw = self.datals[int(self.roi.pos()[1] + self.roi.size()[1] / 2), :] #取了矩阵中的一行
                    h_data = copy.deepcopy(h_dataraw) #深度复制
                    num_h = range(len(h_data))  #创建一个从0开始、小于len(h_data)的整数序列
                    num_h_data = list(num_h)  #水平横坐标范围
                    # print("#水平横坐标范围",num_h_data)

                    v_dataraw = self.datals[:, int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                    v_data = v_dataraw
                    num_v = range(len(v_data))
                    num_v_data = list(num_v)#竖直横坐标范围
                    ##
                    # print('#设置横轴标签')
                    # self.h_fit_data = num_h_data2, self.Modify_data_size(h_data2, self.datals.shape[0])
                    # self.v_fit_data = self.Modify_data_size(v_data2, self.datals.shape[1]), num_v_data2
                    # self.h_fit_data = None
                    # self.v_fit_data = None
                    # if self.h_fit_data is not None:
                    #     self.h_fit_line = pg.PolyLineROI(self.h_fit_data[0], self.h_fit_data[1], closed=False, pen='y')
                    #     self.plot_widget.addItem(self.h_fit_line)

                    # if self.v_fit_data is not None:
                    #     self.v_fit_line = pg.PolyLineROI(self.v_fit_data[0], self.v_fit_data[1], closed=False, pen='y')
                    #     self.plot_widget.addItem(self.v_fit_line)

                    # vlen = np.ones(len(v_data))# make it at right
                    # vlenlist = list(len(h_data) * vlen)
                    # v_data = list(map(lambda x: x[0] - x[1], zip(vlenlist, v_data)))
                    # print(self.roi.pos())
                    # num_v_data = list([x*len(h_data) for x in num_v_data])
                    ##
                    if settings.widget_params["Fitting Setting"]["mode"] == 1:
                        # num_h_data2 = num_h_data[int(self.roi.pos()[0]): int(self.roi.pos()[0] + self.roi.size()[0])]
                        num_h_data2 = np.array(num_h_data)
                        import warnings
                        warnings.filterwarnings("ignore")#撤销runtimewarning提醒
                        avalue = (h_data[int(self.roi.pos()[0])] + h_data[int(self.roi.pos()[0])-1] + h_data[int(self.roi.pos()[0])+1])/3
                        p0 = [avalue, int(self.roi.pos()[0] + self.roi.size()[0] / 2), 100, 0]
                        plesq = optimize.leastsq(residuals, p0, args=(h_data, num_h_data2))
                        list1 = [plesq[0][0],plesq[0][1],plesq[0][2],plesq[0][3]]
                        settings.data3 = round(plesq[0][2],2)
                        # list1[3] = 0  #tuple cannot change, so list it
                        # if list1[0] < 0 or list1[0] > 1500 or list1[1] > 2000 or abs(list1[2]) > 100:
                        #     list1 = [0,0,0,0]       #When the fitting data deviates too much, do not draw, Same thing down here.
                        list1 = np.array(tuple(list1))
                        h_data2 = peval(num_h_data, list1)

                        num_v_data2 = np.array(num_v_data)
                        # v_data2 = self.datals[: , int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                        # v_data2 = self.data[int(self.roi.pos()[1]): int(self.roi.pos()[1] + self.roi.size()[1]), int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                        # v_data2 = np.array(v_data2)
                        avalue2 = (v_data[int(self.roi.pos()[1])] + v_data[int(self.roi.pos()[1]) - 1] + v_data[int(self.roi.pos()[1]) + 0]) / 3
                        p1 = [avalue2, int(self.roi.pos()[1] + self.roi.size()[1] / 2), 100, 0]
                        plesq2 = optimize.leastsq(residuals, p1, args=(v_data, num_v_data2))
                        list2 = [plesq2[0][0], plesq2[0][1], plesq2[0][2], plesq2[0][3]]
                        settings.data6 = round(plesq2[0][2],2)
                        # if list2[2] > 1500:
                        # list2[3] = 0
                        # if list2[0] < 0 or list2[0] > 1500 or list2[1] > 2000 or abs(list2[2]) > 100:
                        #     list2 = [0, 0, 0, 0]   #

                        list2 = np.array(tuple(list2))
                        v_data2 = peval(num_v_data, list2)
                        data7 = abs(2*np.pi*np.sqrt(plesq[0][0]*plesq2[0][0])*plesq[0][2]*plesq2[0][2])
                        CCDPlSize = [3.75, 3.75]
                        Magnification = float(settings.widget_params["Analyse Data Setting"]["magValue"])
                        data8 = plesq[0][2]*CCDPlSize[0]*Magnification*1E-3
                        data9 = plesq2[0][2]*CCDPlSize[1]*Magnification*1E-3
                        self.fittingdata.emit({'data1': plesq[0][0] , 'data2': plesq[0][1], 'data3': plesq[0][2], 'data4': plesq2[0][0],'data5': plesq2[0][1], 'data6': plesq2[0][2],'data7': data7, 'data8': data8,'data9': data9})
                        # h_data2[h_data2 < 0] = 0
                        # v_data2[v_data2 < 0] = 0
                        self.h_axes2.setData(num_h_data2, self.Modify_data_size(h_data2, self.datals.shape[0]))
                        self.v_axes2.setData(self.Modify_data_size(v_data2, self.datals.shape[1]), num_v_data2)
                        # print("num_h_data2",num_h_data2)


                    if settings.widget_params["Analyse Data Setting"]["add_rawdata"]:
                    # if settings.widget_params[1]:
                        #用于修改的像素值实时更新
                        # h_data[h_data < 0] = 0
                        # v_data[v_data < 0] = 0
                        # 原版像素值函数显示
                        # self.h_axes.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                        # self.v_axes.setData(self.Modify_data_size(v_data, self.datals.shape[1]), num_v_data)
                        # end原版像素值函数显示
                        # x2 = np.arange(-10, 10, 0.1)
                        # y2 = np.cos(x2)
                        # 更新外围像素值函数图
                        self.img_pixelplot_h2.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                        self.img_pixelplot_v2.setData(self.Modify_data_size(v_data, self.datals.shape[1]), num_v_data)


                        #################################
                        # # 创建一个应用程序对象和主窗口
                        # app = QtGui.QApplication([])
                        # win = pg.GraphicsWindow(title="Plot Example")
                        # win.resize(800, 600)

                        # # 创建一个绘图部件和一个 PlotItem 对象
                        # plot = win.addPlot()
                        # curve = plot.plot()

                        # # 创建数据
                        # x_data = [1, 2, 3, 4, 5]
                        # y_data = [10, 20, 30, 40, 50]

                        # # 设置坐标轴数据
                        # curve.setData(x_data, y_data)
                        # curve.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                        
                        # self.h_axes.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                        # self.v_axes.setData(self.Modify_data_size(v_data, self.datals.shape[1]), num_v_data)
                        
                        # 运行应用程序
                        # QtGui.QApplication.instance().exec_()

                        #####################################

                        # index_h = h_data.argmax()
                        # index_h_num = h_data.max()
                        # print("水平最大值坐标为：",index_h,"其值为：",index_h_num)
                        # index_v = v_data.argmax()
                        # index_v_num = v_data.max()
                        # print("垂直最大值坐标为：",index_v,"其值为：",index_v_num)
            except AttributeError:
                pass
        else:
            print('It is recommended to turn off the camera first')

    def update_ch_fitting_cs4(self):
    #更新十字上的像素坐标值
        try:
            if settings.widget_params["Analyse Data Setting"]["add_rawdata"] or settings.widget_params["Fitting Setting"]["mode"] == 1:

                self.datals = self.data
                h_dataraw = self.datals[int(self.roi.pos()[1] + self.roi.size()[1] / 2), :] #取了矩阵中的一行
                h_data = copy.deepcopy(h_dataraw) #深度复制
                num_h = range(len(h_data))  #创建一个从0开始、小于len(h_data)的整数序列
                num_h_data = list(num_h)  #水平横坐标范围
                # print("#水平横坐标范围",num_h_data)

                v_dataraw = self.datals[:, int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                v_data = v_dataraw
                num_v = range(len(v_data))
                num_v_data = list(num_v)#竖直横坐标范围
                
                if settings.widget_params["Fitting Setting"]["mode"] == 1:
                    # num_h_data2 = num_h_data[int(self.roi.pos()[0]): int(self.roi.pos()[0] + self.roi.size()[0])]
                    num_h_data2 = np.array(num_h_data)
                    import warnings
                    warnings.filterwarnings("ignore")#撤销runtimewarning提醒
                    avalue = (h_data[int(self.roi.pos()[0])] + h_data[int(self.roi.pos()[0])-1] + h_data[int(self.roi.pos()[0])+1])/3
                    p0 = [avalue, int(self.roi.pos()[0] + self.roi.size()[0] / 2), 100, 0]
                    plesq = optimize.leastsq(residuals, p0, args=(h_data, num_h_data2))
                    list1 = [plesq[0][0],plesq[0][1],plesq[0][2],plesq[0][3]]
                    settings.data3 = round(plesq[0][2],2)
                    
                    list1 = np.array(tuple(list1))
                    h_data2 = peval(num_h_data, list1)

                    num_v_data2 = np.array(num_v_data)
                    
                    avalue2 = (v_data[int(self.roi.pos()[1])] + v_data[int(self.roi.pos()[1]) - 1] + v_data[int(self.roi.pos()[1]) + 0]) / 3
                    p1 = [avalue2, int(self.roi.pos()[1] + self.roi.size()[1] / 2), 100, 0]
                    plesq2 = optimize.leastsq(residuals, p1, args=(v_data, num_v_data2))
                    list2 = [plesq2[0][0], plesq2[0][1], plesq2[0][2], plesq2[0][3]]
                    settings.data6 = round(plesq2[0][2],2)

                    list2 = np.array(tuple(list2))
                    v_data2 = peval(num_v_data, list2)
                    data7 = abs(2*np.pi*np.sqrt(plesq[0][0]*plesq2[0][0])*plesq[0][2]*plesq2[0][2])
                    CCDPlSize = [3.75, 3.75]
                    Magnification = float(settings.widget_params["Analyse Data Setting"]["magValue"])
                    data8 = plesq[0][2]*CCDPlSize[0]*Magnification*1E-3
                    data9 = plesq2[0][2]*CCDPlSize[1]*Magnification*1E-3
                    self.fittingdata.emit({'data1': plesq[0][0] , 'data2': plesq[0][1], 'data3': plesq[0][2], 'data4': plesq2[0][0],'data5': plesq2[0][1], 'data6': plesq2[0][2],'data7': data7, 'data8': data8,'data9': data9})
                    # h_data2[h_data2 < 0] = 0
                    # v_data2[v_data2 < 0] = 0
                    self.h_axes2.setData(num_h_data2, self.Modify_data_size(h_data2, self.datals.shape[0]))
                    self.v_axes2.setData(self.Modify_data_size(v_data2, self.datals.shape[1]), num_v_data2)
                    # print("num_h_data2",num_h_data2)


                # if settings.widget_params["Analyse Data Setting"]["add_rawdata"]:
                if settings.widget_params[1]:
                    #用于修改的像素值实时更新
                    # h_data[h_data < 0] = 0
                    # v_data[v_data < 0] = 0
                    self.h_axes.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                    self.v_axes.setData(self.Modify_data_size(v_data, self.datals.shape[1]), num_v_data)
                    # x2 = np.arange(-10, 10, 0.1)
                    # y2 = np.cos(x2)
                    # 更新外围像素值函数图
                    self.img_pixelplot_h2.setData(num_h_data, self.Modify_data_size(h_data, self.datals.shape[0]))
                    self.img_pixelplot_v2.setData(self.Modify_data_size(v_data, self.datals.shape[1]), num_v_data)
        except AttributeError:
            pass

    def Modify_data_size(self, data, PictureMax):
        #修改数据的大小，确保数据不超出图像范围
        Modify = max(data) / (PictureMax*0.2)

        return data/Modify

    def calculate_roi(self):
        # calculate atom number
        try:
            if self.roi.pos()[0] < 0 or self.roi.pos()[1] < 0 or self.roi.size()[1] > self.data_shape[1] or self.roi.size()[0] > self.data_shape[0]:
                return
            
            #print('before TotalPhotons is ',(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1] + self.roi.size()[0]), 
            #                                 int(self.roi.pos()[0]):int(self.roi.pos()[0] + self.roi.size()[1])])))

            TotalPhotons = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1] + self.roi.size()[0]), 
                                             int(self.roi.pos()[0]):int(self.roi.pos()[0] + self.roi.size()[1])]))
            #modi
            # print('TotalPhotons is ',TotalPhotons)
            ROIsize = self.roi.size()[0]*self.roi.size()[1]

            #以吸收成像的参数计算原子数
            calculatedata = calculateAtom(TotalPhotons, ROIsize, 1)
            self.atom_number.emit(calculatedata[0])
            self.Pxatom_num.emit(calculatedata[1])

            #以荧光成像的参数计算原子数
            calculatedataF = calculateAtom(TotalPhotons, ROIsize, 0)
            self.atom_numberF.emit(calculatedataF[0])
            self.Pxatom_numF.emit(calculatedataF[1])

            xpos = self.roi.pos()[1] + self.roi.size()[1]/2
            ypos = self.roi.pos()[0] + self.roi.size()[0]/2
            position = [ypos, xpos]
            self.roipos.emit(position)
        except:
            pass

    def judrcf(self, mode1, mode2, mode3):
        if settings.widget_params["Analyse Data Setting"]["roiStatus"] == True:

            self.add_roi(mode1, mode2)
            if settings.widget_params["Analyse Data Setting"]["add_rawdata"] == True:
                self.add_rawdata(mode2)
            if settings.widget_params["Fitting Setting"]["mode"] == 1:
                # print(1)
                self.add_fitting(mode3)

    def measureT(self):
        h_data = self.data[int(settings.ceny), :]
        num_h = range(len(h_data))
        num_h_data = list(num_h)
        num_h_data2 = np.array(num_h_data)
        h_data2 = self.data[int(settings.ceny), :]
        h_data2 = np.array(h_data2)
        import warnings
        warnings.filterwarnings("ignore")  # 撤销runtimewarning提醒
        avalue01 = (h_data[int(settings.cenx)] + h_data[int(settings.cenx) - 1] + h_data[int(settings.cenx) + 1]) / 3
        # p0 = [avalue, int(self.roi.pos()[0] + self.roi.size()[0] / 2), 100, 0]
        p00 = [avalue01, int(settings.cenx), int(200 / 2), 0]
        plesq3 = optimize.leastsq(residuals, p00, args=(h_data2, num_h_data2))
        h = [0, abs(round(plesq3[0][2], 2)) ** 2]
        list3 = [plesq3[0][0], plesq3[0][1], plesq3[0][2], plesq3[0][3]]
        list3 = np.array(tuple(list3))
        h_peakOD = max(peval(num_h_data2, list3))
        self.HOD.emit(h_peakOD)

        v_data = self.data[:, int(settings.cenx)]
        num_v = range(len(v_data))
        num_v_data = list(num_v)
        num_v_data2 = np.array(num_v_data)
        v_data2 = self.data[:, int(settings.cenx)]
        v_data2 = np.array(v_data2)
        avalue02 = (h_data[int(settings.ceny)] + h_data[int(settings.ceny) - 1] + h_data[int(settings.ceny) + 1]) / 3
        p11 = [avalue02, int(settings.ceny), int(200 / 2), 0]
        plesq4 = optimize.leastsq(residuals, p11, args=(v_data2, num_v_data2))
        v = [0, abs(round(plesq4[0][2], 2)) ** 2]
        list4 = [plesq4[0][0], plesq4[0][1], plesq4[0][2], plesq4[0][3]]
        list4 = np.array(tuple(list4))
        v_peakOD = max(peval(num_v_data2, list4))
        self.VOD.emit(v_peakOD)

        t = [0,(float(settings.widget_params["Analyse Data Setting"]["TOF"]) / 1000) ** 2]

        temp_fit = np.polyfit(t, h, 1)
        temp_fit2 = np.polyfit(t, v, 1)
        mass = 85.4678 * 1.66053886 * 10 ** (-27)
        kbol = 1.38 * 1e-23
        CCDPlSize = [3.75, 3.75]
        pixelArea = CCDPlSize[0] * CCDPlSize[1] * 1e-12  # μm**2
        M = float(settings.widget_params["Analyse Data Setting"]["magValue"])
        # tem = (temp_fit[0] ** 2 * M ** 2 * mass / kbol / pixelArea + temp_fit2[0] ** 2 * M ** 2 * mass / kbol / pixelArea) / 2
        tem = (temp_fit[0] * mass / M**2 / kbol * pixelArea + temp_fit2[0] * mass / M**2 / kbol * pixelArea) / 2

        # self.tempnum.connect(self.result_dock.change_temp)
        self.tempnum.emit(tem)

    def img_plot(self, img_dict):
        """
        design for software mode and hardware mode, choose image from image stack to display in main window
        :param img_dict:
        :return:
        """
        self.viewBox.clear()
        self.viewBox.addItem(self.img)
        self.img.clear()
        self.img.setImage(img_dict['img_data'])
        # print(img_dict['img_data'][794,420:450])
        self.data = img_dict['img_data']
        print('self.data_shape is',self.data_shape)
        # print(img_dict) #改了还未运行
        # print('self.data is',self.data)


        import cv2
        # gray_image = cv2.cvtColor(img_dict['img_data'], cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(img_dict['img_data'], 0, 255, 3)
        # image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 旧版本返回三个参数，新版本返回2个
        # contours, hierarchy = cv2.findContours(img_dict['img_data'], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cnt = contours[0]
        m = cv2.moments(img_dict['img_data'])
        #modi
        # plt.imshow(m)
        # plt.show()
        # print(m)
        x = int(m['m10'] / m['m00'])
        y = int(m['m01'] / m['m00'])
        mp = cv2.moments(img_dict['img_data'][y-200:y+200, x-200:x+200])
        xp = int(mp['m10'] / mp['m00'])
        yp = int(mp['m01'] / mp['m00'])
        mp2 = cv2.moments(img_dict['img_data'][yp+y-200-200:yp+y-200+200, xp+x-200-200:xp+x-200+200])
        xp2 = int(mp2['m10'] / mp2['m00'])
        yp2 = int(mp2['m01'] / mp2['m00'])
        mp3 = cv2.moments(img_dict['img_data'][yp+y-200+yp2-200-200:yp+y-200+yp2-200+200, xp+x-200+xp2-200-200:xp+x-200+xp2-200+200])
        xp3 = mp3['m10'] / mp3['m00']
        yp3 = mp3['m01'] / mp3['m00']
        # print('x=', xp+x-200, 'y=', yp+y-200)
        settings.widget_params["Analyse Data Setting"]["xpos"] = x+xp-200+xp2-200+xp3-200
        settings.widget_params["Analyse Data Setting"]["ypos"] = y+yp-200+yp2-200+yp3-200
        settings.cenx = x+xp-200+xp2-200+xp3-200
        settings.ceny = y+yp-200+yp2-200+yp3-200

        self.data_shape = self.data.shape
        self.img_label.setText(img_dict['img_name'])
        #Set the initial axis so that the size of the image remains the same when the axis is added
        numh = range(self.data_shape[1])
        numh = list(numh)
        numhd = np.zeros(self.data_shape[1])
        numv = range(self.data_shape[0])
        numv = list(numv)
        numvd = np.zeros(self.data_shape[0])
        self.h_axesm = self.viewBox.plot()
        self.h_axesm.setPen(color='k', width=2)  # x
        self.h_axesm.setData(numh, numhd)
        self.v_axesm = self.viewBox.plot()
        self.v_axesm.setPen(color='k', width=2)
        self.v_axesm.setData(numvd, numv)
        # if settings.widget_params["Analyse Data Setting"]["roiStatus"] == True:
            # roi_cbk_state.setCheckState(1)
        if settings.cameraON == False:
            self.measureT()


    def img_plot2(self):
        if settings.imgData["BkgImg"] !=[] and settings.imgData["Img_data"] !=[]:
            self.viewBox.clear()
            self.viewBox.addItem(self.img)
            self.img.clear()
            # Reloading improves operational efficiency
            subt = deepcopy(settings.imgData["Img_data"])
            # print(settings.imgData["Img_data"][0, 0:10])
            # print(settings.imgData["BkgImg"][0, 0:10])
            settings.imgData["Img_data"] = settings.imgData["Img_data"] - settings.imgData["BkgImg"]
            settings.imgData["Img_data"][settings.imgData["Img_data"] > subt] = 0
            self.img.setImage(settings.imgData["Img_data"])
            self.data = settings.imgData["Img_data"]
            self.data_shape = settings.imgData["Img_data"].shape
            self.update_ch_fitting_cs()
            try:
                self.calculate_roi()
            except AttributeError:
                pass
        elif settings.imgData["Img_data"] ==[]:
            print('No image')
        elif settings.imgData["BkgImg"] ==[]:
            print('No background image')

    def img_plot3(self, img_dict):
        if settings.imgData["Img_data"] != [] or 1:
            self.viewBox.clear()
            self.viewBox.addItem(self.img)
            self.img.clear()
            # Reloading improves operational efficiency
            settings.imgData["Img_photon_range"] = deepcopy(settings.imgData["Img_data"])
            try:
                settings.imgData["Img_photon_range"][settings.imgData["Img_data"] <= float(settings.widget_params["Image Display Setting"]["pfMin"])] = settings.widget_params["Image Display Setting"]["pfMin"]
                # print('imgDatamax',max(settings.imgData))
                # print('Img_photon_range',settings.imgData["Img_photon_range"])
                settings.imgData["Img_photon_range"][settings.imgData["Img_data"] >= float(settings.widget_params["Image Display Setting"]["pfMax"])] = settings.widget_params["Image Display Setting"]["pfMax"]
            except ValueError:
                print('The edit box cannot be empty')
            self.img.setImage(settings.imgData["Img_photon_range"])
            self.data = settings.imgData["Img_photon_range"]
            self.data_shape = settings.imgData["Img_photon_range"].shape
            self.update_ch_fitting_cs()
            try:
                self.calculate_roi()
            except AttributeError:
                pass
            # print('photon filter ： finish.')
        else:
            print('No image')

    def img_plot4(self, img_dict):
        #可以自动更新到大窗口且ROI位置不变
        if settings.imgData["Img_data"] != [] or 1:
            self.viewBox.clear()
            self.viewBox.addItem(self.img)
            self.img.clear()
            # modi add
            self.img.setImage(img_dict['img_data'])
            self.data = img_dict['img_data']
            # end modi
            print('implot4')
            # self.add_roi()
            # self.setroichange()
            self.add_rawdata2()
            self.add_roi2()
            self.update_ch_fitting_cs()
            try:
                self.calculate_roi()
                print("calculate_roi")
            except AttributeError:
                pass
            # print('photon filter ： finish.')
        else:
            print('No image')


    def clear_win(self):
        self.viewBox.clear()
        # add image item
        self.viewBox.addItem(self.img)
        if self.img is None:
            return
        self.img.clear()
        #modi 使清空大窗口后不刷新右下角标签变量
        self.img_label.setText('')
        self.img_label1.setText('| Tem/K')
        self.img_label2.setText('| HpeakOD')
        self.img_label3.setText('')
        self.img_label4.setText('| VpeakOD')
        self.img_label5.setText('')
        self.data = None
        self.data_shape = None

    def ClearPlotwin(self):
        self.viewBox.clear()
        # add image item
        self.viewBox.addItem(self.img)
        self.img.clear()
        self.img_label.setText('Waiting for the trigger')
        self.data = None
        self.data_shape = None

def func(xx, aa, bb, cc, dd):
    return aa * np.e ** (-((xx - bb) ** 2) / 2 / cc ** 2) + dd

# def logistic4(x, A, B, C, D):
#     return (A-D)/(1+(x/C)**B)+D

def residuals(p, y, x):
    [A, B, C, D] = p
    return y - func(x, A, B, C, D)

def peval(x, p):
    [A, B, C, D] = p
    return func(x, A, B, C, D)
