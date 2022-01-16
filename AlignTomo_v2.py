import sys
import csv
import glob
import cv2
import os
import qimage2ndarray
import numpy as np
import matplotlib.pyplot as plt
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

qtCreatorFile = "interfaceAlignTomov2.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
  
        
        self.liste_blanc_plot1 = []
        self.liste_blanc_batonnets = []
        self.liste_blanc_plot2 = []
        self.liste_blanc_plot = []
        self.liste_image1 = []
        self.liste_image2 = []
        self.liste_image3 = []
        
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        
        
        
        self.vignette_plot11 = None
        self.vignette_plot12 = None
        self.vignette_batonnets1 = None
        self.vignette_batonnets2 = None
        self.vignette_plot21 =  None
        self.vignette_plot22 = None
        self.fileName_img_test_plots = None
        self.fileName_img_test_batonnets = None
        self.valeur_seuil_plots = 110
        self.valeur_seuil_batonnets = 110
        self.progressBar.setProperty("value", 0) 
        self.progressBar.hide()
        self.dossier_de_travail_texte =''
        

        self.actionOpen.triggered.connect(self.dossier_de_travail)
        self.actionQuit.triggered.connect(self.quit)
        self.actionSave.triggered.connect(self.save)
        self.actionApropos.triggered.connect(self.apropos)
        self.pushButton.clicked.connect(self.debut_plot1)
        self.pushButton_2.clicked.connect(self.fin_plot1)
        self.pushButton_3.clicked.connect(self.debut_batonnets)
        self.pushButton_4.clicked.connect(self.fin_batonnets)
        self.pushButton_5.clicked.connect(self.debut_plot2)
        self.pushButton_6.clicked.connect(self.fin_plot2)
        self.pushButton_calcul_ratio.clicked.connect(self.calculRatio)
        self.pushButton_7.clicked.connect(self.ouvrir_test_plots)
        self.pushButton_8.clicked.connect(self.ouvrir_test_batonnets)
        self.pushButton_9.clicked.connect(self.ouvrir_roi)
        self.pushButton_10.clicked.connect(self.crop)
        
        self.horizontalSlider.valueChanged.connect(self.slider_value_plots)
        self.horizontalSlider.valueChanged.connect(self.afficher_test_plots)
        
        self.horizontalSlider_2.valueChanged.connect(self.slider_value_batonnets)
        self.horizontalSlider_2.valueChanged.connect(self.afficher_test_batonnets)
        
        self.flag = 0
    
    def dossier_de_travail(self):
          
        self.dossier_de_travail = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dossier_de_travail_texte = str(self.dossier_de_travail)
        self.label_23.setText('Folder: '+self.dossier_de_travail_texte)
        if os.path.exists(self.dossier_de_travail+'/crop'):
            shutil.rmtree(self.dossier_de_travail+'/crop')
          
    def crop(self):
      
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            self.progressBar.setProperty("value", 0) 
            creation_dossier = 'crop'
            self.chemin_crop  = os.path.join(self.dossier_de_travail, creation_dossier)  
            if os.path.exists(self.chemin_crop ):  
                shutil.rmtree(self.chemin_crop)
            os.mkdir(self.chemin_crop)       
            i=0
            self.progressBar.show()
            self.progressBar.setMaximum(len (glob.glob(self.dossier_de_travail+"/*.tif")))
            for image in glob.glob(self.dossier_de_travail+"/*.tif"):
                img = cv2.imread(image)          
                img = img[int(self.y1):int(self.y2), int(self.x1):int(self.x2)]
                cv2.imwrite(self.chemin_crop+"/crop%04i.tif"%i, img)
                i+= 1
                self.progressBar.setProperty("value", i)

            self.progressBar.hide()
            self.tabWidget.setCurrentIndex(1)
        
        
    def non_crop(self):
            

        self.progressBar.show()
        self.progressBar.setProperty("value", 0) 
        creation_dossier = 'no_crop'
        self.chemin_crop  = os.path.join(self.dossier_de_travail, creation_dossier)
    
        if os.path.exists(self.chemin_crop ):
          
            shutil.rmtree(self.chemin_crop)
        os.mkdir(self.chemin_crop)       
        i=0
        self.progressBar.setMaximum(len (glob.glob(self.dossier_de_travail+"/*.tif")))
        
        for image in glob.glob(self.dossier_de_travail+"/*.tif"):
            img = cv2.imread(image)          
            cv2.imwrite(self.chemin_crop+"/crop%04i.tif"%i, img)
            i+= 1
            self.progressBar.setProperty("value", i)
            
        self.progressBar.hide()
        self.tabWidget.setCurrentIndex(1)
  
    def ouvrir_roi(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            self.fileName_img_test_roi = QFileDialog.getOpenFileName(self,"Open image",self.dossier_de_travail, "*.tif")         
            self.afficher_test_plots()        
            self.afficher_test_roi()
        
        
        
   
    def ouvrir_test_plots(self):
        '''
        On selectionne une image pour faire des tests de seuil
        '''  
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop'):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
                
            self.fileName_img_test_plots = QFileDialog.getOpenFileName(self,"Open image",dossier_a_ouvrir,"*.tif") 
            self.afficher_test_plots()
        
    def ouvrir_test_batonnets(self):
        '''
        On selectionne une image pour faire des tests de seuil
        '''
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
          
            self.fileName_img_test_batonnets = QFileDialog.getOpenFileName(self,"Open image", dossier_a_ouvrir,"*.tif")
            self.afficher_test_batonnets()
        
        
            
    def afficher_test_plots(self): 
        '''
        on affiche dans les graphics view l'image selectionnée et son image seuillée avec self.valeur_seuil ajustable'

        '''
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if self.fileName_img_test_plots is not None:
                self.img_test_orig_plots = cv2.imread(self.fileName_img_test_plots[0])            
                self.img_test_plots = qimage2ndarray.array2qimage(self.img_test_orig_plots)  
                self.pixmap_7 = QtGui.QPixmap.fromImage(self.img_test_plots.scaled(400,400, QtCore.Qt.KeepAspectRatio))
                self.scene7 = QtWidgets.QGraphicsScene()
                self.pixmap_item7 = self.scene7.addPixmap(self.pixmap_7) 
                self.graphicsView_7.setScene(self.scene7)          
                self.img_test_orig_plots = cv2.cvtColor(self.img_test_orig_plots, cv2.COLOR_BGR2GRAY)
                self.img_test_orig_plots = cv2.blur(self.img_test_orig_plots,(3,3))
                ret, self.thresh_plots = cv2.threshold(self.img_test_orig_plots, self.valeur_seuil_plots, 255, cv2.THRESH_BINARY)
                self.thresh_plots  = qimage2ndarray.array2qimage(self.thresh_plots )
                self.pixmap_8 = QtGui.QPixmap.fromImage(self.thresh_plots.scaled(400,400, QtCore.Qt.KeepAspectRatio))
                self.scene8 = QtWidgets.QGraphicsScene()
                self.pixmap_item8 = self.scene8.addPixmap(self.pixmap_8) 
                self.graphicsView_8.setScene(self.scene8)
        
    def afficher_test_batonnets(self): 
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            
            if self.fileName_img_test_batonnets is not None:
                self.img_test_orig_batonnets = cv2.imread(self.fileName_img_test_batonnets[0])               
                self.img_test_batonnets = qimage2ndarray.array2qimage(self.img_test_orig_batonnets)
                self.pixmap_9 = QtGui.QPixmap.fromImage(self.img_test_batonnets.scaled(400,400, QtCore.Qt.KeepAspectRatio))
                self.scene9 = QtWidgets.QGraphicsScene()
                self.pixmap_item9 = self.scene9.addPixmap(self.pixmap_9) 
                self.graphicsView_9.setScene(self.scene9) 
                self.img_test_orig_batonnets = cv2.cvtColor(self.img_test_orig_batonnets, cv2.COLOR_BGR2GRAY)
                self.img_test_orig_batonnets = cv2.blur(self.img_test_orig_batonnets,(3,3))
                ret, self.thresh_batonnets = cv2.threshold(self.img_test_orig_batonnets, self.valeur_seuil_batonnets, 255, cv2.THRESH_BINARY)
                self.thresh_batonnets  = qimage2ndarray.array2qimage(self.thresh_batonnets )
                self.pixmap_10 = QtGui.QPixmap.fromImage(self.thresh_batonnets.scaled(400,400, QtCore.Qt.KeepAspectRatio))
                self.scene10 = QtWidgets.QGraphicsScene()
                self.pixmap_item10 = self.scene10.addPixmap(self.pixmap_10) 
                self.graphicsView_10.setScene(self.scene10)   
        
    def afficher_test_roi(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
             if self.fileName_img_test_roi is not None:
                self.img_test_roi = cv2.imread(self.fileName_img_test_roi[0])      
                self.img_test_roi = qimage2ndarray.array2qimage(self.img_test_roi)
                self.pixmap_11 = QtGui.QPixmap.fromImage(self.img_test_roi)
                self.scene11 = QtWidgets.QGraphicsScene()
                self.pixmap_item11 = self.scene11.addPixmap(self.pixmap_11) 
                self.graphicsView_11.setScene(self.scene11)
                self.scene11.installEventFilter(self) 
            
    def afficher_graph(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            self.img_graph = cv2.imread(self.dossier_de_travail+'/graph.png')
            self.img_graph = qimage2ndarray.array2qimage(self.img_graph)
            self.pixmap_12 = QtGui.QPixmap.fromImage(self.img_graph)
            self.scene12 = QtWidgets.QGraphicsScene()
            self.pixmap_item12 = self.scene12.addPixmap(self.pixmap_12) 
            self.graphicsView_12.setScene(self.scene12)
          
    def quit(self):
        '''
        Quitter
        '''
        reply = QMessageBox.question(self, 'Close Window', 'Are you sure you want to close?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes :
  
            if self.dossier_de_travail_texte =='':
                 pass
            else: 
                if os.path.exists(self.dossier_de_travail+'/crop'):
                    shutil.rmtree(self.dossier_de_travail+'/crop')
                if os.path.exists(self.dossier_de_travail+'/no_crop'):
                    shutil.rmtree(self.dossier_de_travail+'/no_crop')
                    
                if os.path.exists(self.dossier_de_travail+'/seuil'):
                    shutil.rmtree(self.dossier_de_travail+'/seuil')
           
            QtCore.QCoreApplication.instance().quit()
            QtWidgets.QMainWindow.close(self)
   
    def open_image(self):
           
        '''
        affichage des vignettes correspondant aux differentes images selectionner pour délimiter plots et batonnets
        '''    
        if self.vignette_plot11 is not None:
           self.pixmap = QtGui.QPixmap.fromImage(self.vignette_plot11.scaled(200,200, QtCore.Qt.KeepAspectRatio))
           self.scene = QtWidgets.QGraphicsScene()
           self.pixmap_item = self.scene.addPixmap(self.pixmap) 
           self.graphicsView.setScene(self.scene)
        
        if self.vignette_plot12 is not None:
            self.pixmap_2 = QtGui.QPixmap.fromImage(self.vignette_plot12.scaled(200,200, QtCore.Qt.KeepAspectRatio))
            self.scene2 = QtWidgets.QGraphicsScene()
            self.pixmap_item2 = self.scene2.addPixmap(self.pixmap_2) 
            self.graphicsView_2.setScene(self.scene2)
               
        if self.vignette_batonnets1 is not None:
            self.pixmap_3 = QtGui.QPixmap.fromImage(self.vignette_batonnets1.scaled(200,200, QtCore.Qt.KeepAspectRatio))
            self.scene3 = QtWidgets.QGraphicsScene()
            self.pixmap_item3 = self.scene3.addPixmap(self.pixmap_3) 
            self.graphicsView_3.setScene(self.scene3)
                  
        if self.vignette_batonnets2 is not None:
            self.pixmap_4 = QtGui.QPixmap.fromImage(self.vignette_batonnets2.scaled(200,200, QtCore.Qt.KeepAspectRatio))
            self.scene4 = QtWidgets.QGraphicsScene()
            self.pixmap_item4 = self.scene4.addPixmap(self.pixmap_4) 
            self.graphicsView_4.setScene(self.scene4)
            
        if self.vignette_plot21 is not None:
           self.pixmap_5 = QtGui.QPixmap.fromImage(self.vignette_plot21.scaled(200,200, QtCore.Qt.KeepAspectRatio))
           self.scene5 = QtWidgets.QGraphicsScene()
           self.pixmap_item5 = self.scene5.addPixmap(self.pixmap_5) 
           self.graphicsView_5.setScene(self.scene5)
           
        if self.vignette_plot22 is not None:
           self.pixmap_6 = QtGui.QPixmap.fromImage(self.vignette_plot22.scaled(200,200, QtCore.Qt.KeepAspectRatio))
           self.scene6 = QtWidgets.QGraphicsScene()
           self.pixmap_item6 = self.scene6.addPixmap(self.pixmap_6) 
           self.graphicsView_6.setScene(self.scene6)
           
       
    def slider_value_plots(self):
        '''
        Recuperer les valeurs de la slide bar de seuil , actualiser l'image seuillée, afficher la valeur de seuil dans le label '''
        self.valeur_seuil_plots = self.horizontalSlider.value() 
        self.open_image()
        self.Text_seuil_plots = str(self.valeur_seuil_plots)
        self.label_20.setText(self.Text_seuil_plots)
        
    def slider_value_batonnets(self):
        '''
        Recuperer les valeurs de la slide bar de seuil , actualiser l'image seuillée, afficher la valeur de seuil dans le label '''
        self.valeur_seuil_batonnets= self.horizontalSlider_2.value() 
        self.open_image()
        self.Text_seuil_batonnets = str(self.valeur_seuil_batonnets)
        self.label_22.setText(self.Text_seuil_batonnets)    
      
    def debut_plot1(self):
        
        '''
        Selectionner les images pour les limites plots et batonnets
        '''
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            
            self.plot11 = QFileDialog.getOpenFileName(self,"Selectionner debut plot1", dossier_a_ouvrir,"*.tif")
            self.Text_plot11 = str(self.plot11[0])  
            self.image_plot11 = cv2.imread(self.plot11[0])
            self.vignette_plot11 = qimage2ndarray.array2qimage(self.image_plot11)
            self.label_14.setText(self.Text_plot11[-8:-4])
            self.num_plot11 = int(self.Text_plot11[-8:-4])
             
        self.open_image()
         
         

    
    def fin_plot1(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
        
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            self.plot12 = QFileDialog.getOpenFileName(self,"Selectionner fin plot1", dossier_a_ouvrir,"*.tif")
            self.Text_plot12 = str(self.plot12[0])
            self.image_plot12 = cv2.imread(self.plot12[0])
            self.vignette_plot12 = qimage2ndarray.array2qimage(self.image_plot12)
            self.label_15.setText(self.Text_plot12[-8:-4])
            self.num_plot12 = int(self.Text_plot12[-8:-4])
            self.open_image()
          
        
    def debut_batonnets(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            self.batonnets1 = QFileDialog.getOpenFileName(self,"Selectionner debut batonnets", dossier_a_ouvrir,"*.tif")
            self.Text_batonnets1 = str(self.batonnets1[0])
            self.image_batonnets1= cv2.imread(self.batonnets1[0])
            self.vignette_batonnets1 = qimage2ndarray.array2qimage(self.image_batonnets1)
            self.label_16.setText(self.Text_batonnets1[-8:-4])
            self.num_batonnets1 = int(self.Text_batonnets1[-8:-4])
        
        self.open_image()

    def fin_batonnets(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            self.batonnets2 = QFileDialog.getOpenFileName(self,"Selectionner fin batonnets",  dossier_a_ouvrir,"*.tif")
            self.Text_batonnets2 = str(self.batonnets2[0])
            self.image_batonnets2= cv2.imread(self.batonnets2[0])
            self.vignette_batonnets2 = qimage2ndarray.array2qimage(self.image_batonnets2)
            self.label_17.setText(self.Text_batonnets2[-8:-4])
            self.num_batonnets2 = int(self.Text_batonnets2[-8:-4])
            self.open_image()

    def debut_plot2(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            self.plot21 = QFileDialog.getOpenFileName(self,"Selectionner debut plot2",  dossier_a_ouvrir,"*.tif")
            self.Text_plot21 = str(self.plot21[0])
            self.image_plot21 = cv2.imread(self.plot21[0])
            self.vignette_plot21 = qimage2ndarray.array2qimage(self.image_plot21)
            self.label_18.setText(self.Text_plot21[-8:-4])
            self.num_plot21 = int(self.Text_plot21[-8:-4])
            self.open_image()
         
    
    def fin_plot2(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
            else: 
                dossier_a_ouvrir = self.dossier_de_travail
            self.plot22 = QFileDialog.getOpenFileName(self,"Selectionner fin plot2", dossier_a_ouvrir,"*.tif")
            self.Text_plot22 = str(self.plot22[0])
            self.image_plot22 = cv2.imread(self.plot22[0])
            self.vignette_plot22 = qimage2ndarray.array2qimage(self.image_plot22)
            self.label_19.setText(self.Text_plot22[-8:-4])
            self.num_plot22 = int(self.Text_plot22[-8:-4])
            self.open_image()
        
        
    def calculRatio(self):
        
        if self.dossier_de_travail_texte =='':
            QMessageBox.about(self, "Info", "Select Working Folder File-> Open Folder ")
        else:
            if os.path.exists(self.dossier_de_travail+'/crop' ):
                dossier_a_ouvrir = self.chemin_crop
                
            else: 
                
                self.non_crop()
                dossier_a_ouvrir = self.dossier_de_travail+'/no_crop'

            self.progressBar.show()
            self.progressBar.setProperty("value", 0) 
            creation_dossier = 'seuil'
            self.chemin_seuil  = os.path.join(self.dossier_de_travail, creation_dossier)
       
            if os.path.exists(self.chemin_seuil ):
                
                shutil.rmtree(self.chemin_seuil)
            os.mkdir(self.chemin_seuil)          
            self.liste_blanc_plot1 = []
            self.liste_blanc_batonnets = []
            self.liste_blanc_plot2 = []
            self.liste_i = []
            self.liste_image = []
            self.progressBar.setProperty("value", 0) 
            self.progressBar.setMaximum(self.num_plot12-self.num_plot11)
            
            for i in range (self.num_plot11,self.num_plot12):
                             
                img = cv2.imread(dossier_a_ouvrir+"/crop%04i.tif"%i)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.blur(img,(3,3))
                ret, seuil = cv2.threshold(img, self.valeur_seuil_plots, 255, cv2.THRESH_BINARY)
                cv2.imwrite(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i, seuil)
                seuil = cv2.imread(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i)
                white_pix_plot1_ratio = np.sum(seuil == 255)
                self.liste_blanc_plot1.append(white_pix_plot1_ratio)
                self.progressBar.setProperty("value", i+1)
                self.liste_i.append(i)
                self.liste_image1.append(i)
            self.moyenne_plot1= np.mean(self.liste_blanc_plot1)
            self.mediane_plot1= np.median(self.liste_blanc_plot1)
            #fig=plt.figure()
            plt.ioff()
            plt.plot(self.liste_i,self.liste_blanc_plot1)
            plt.ylabel('nbre pixels blancs')
            plt.xlabel('image #')
            
            #plt.show ()
            self.liste_i = []    
            self.progressBar.setProperty("value", 0)
            self.progressBar.setMaximum(self.num_batonnets2-self.num_batonnets1)
          
            for i in range (self.num_batonnets1,self.num_batonnets2):
                
                img = cv2.imread(dossier_a_ouvrir+"/crop%04i.tif"%i)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.blur(img,(3,3))
                ret, seuil = cv2.threshold(img, self.valeur_seuil_batonnets, 255, cv2.THRESH_BINARY)
                cv2.imwrite(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i, seuil)
                seuil = cv2.imread(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i)
                white_pix_batonnets_ratio = np.sum(seuil == 255)
                self.liste_blanc_batonnets.append(white_pix_batonnets_ratio)
                self.progressBar.setProperty("value", i+1)
                self.liste_i.append(i)
                self.liste_image2.append(i)
            self.moyenne_batonnets= np.mean(self.liste_blanc_batonnets)
            self.mediane_batonnets= np.median(self.liste_blanc_batonnets)
            
            #fig=plt.figure()
            plt.ioff()
            plt.plot(self.liste_i,self.liste_blanc_batonnets)
            plt.ylabel('nbre pixels blancs')
            plt.xlabel('image #')
            #plt.close(fig)
            #plt.show ()
            self.liste_i = []   
            self.progressBar.setProperty("value", 0)  
            self.progressBar.setMaximum(self.num_plot22-self.num_plot21)
          
            for i in range (self.num_plot21, self.num_plot22):
                
                img = cv2.imread(dossier_a_ouvrir+"/crop%04i.tif"%i)
                ret, seuil = cv2.threshold(img, self.valeur_seuil_plots, 255, cv2.THRESH_BINARY)
                cv2.imwrite(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i, seuil)
                seuil = cv2.imread(self.dossier_de_travail+"/seuil/seuil%04i.tif"%i)
                white_pix_plot2_ratio = np.sum(seuil == 255)
                self.liste_blanc_plot2.append(white_pix_plot2_ratio)
                self.progressBar.setProperty("value", i+1)
                self.liste_i.append(i)
                self.liste_image3.append(i)
                
            self.moyenne_plot2= np.mean(self.liste_blanc_plot2)
            self.mediane_plot2= np.median(self.liste_blanc_plot2)
            
            #fig=plt.figure()
            plt.ioff()
            plt.plot(self.liste_i,self.liste_blanc_plot2)
            plt.ylabel('nbre pixels blancs')
            plt.xlabel('image #')
            # plt.close(fig)
            #plt.show ()
            ##############
            self.liste_i = []
            self.progressBar.hide()
            self.moyenne_plot1_plot2 = (self.moyenne_plot1 + self.moyenne_plot2)/2
            self.liste_blanc_plot = self.liste_blanc_plot1 + self.liste_blanc_plot2
            self.liste_blanc_plot.sort()
            self.mediane_plot1_plot2 = np.median(self.liste_blanc_plot)
            self.ratio = 100*(self.moyenne_batonnets / self.moyenne_plot1_plot2)
            self.ratio_mediane = 100*(self.mediane_batonnets / self.mediane_plot1_plot2)
            
            
            #conversion en texte et ne garder que le 6 premiers caracteres
            self.Text_moyenne_plot1 = str(self.moyenne_plot1)
            self.Text_moyenne_batonnets = str(self.moyenne_batonnets)
            self.Text_moyenne_plot2 = str(self.moyenne_plot2)
            self.Text_moyenne_plot1_plot2 = str(self.moyenne_plot1_plot2)
            self.Text_mediane_plot1 = str(self.mediane_plot1)
            self.Text_mediane_batonnets = str(self.mediane_batonnets)
            self.Text_mediane_plot2 = str(self.mediane_plot2)
            self.Text_mediane_plot1_plot2 = str(self.mediane_plot1_plot2)
            self.Text_ratio = str(self.ratio)
            self.Text_ratio = self.Text_ratio[0:5] 
            self.Text_ratio_mediane = str(self.ratio_mediane)
            self.Text_ratio_mediane = self.Text_ratio_mediane[0:5]          
            self.label_21.setText('Nano Rod Filling Ration'+self.Text_ratio+'%') 
            self.fichier_resultats()       
            plt.savefig(self.dossier_de_travail+'/graph.png')  
            self.afficher_graph()
            self.tabWidget.setCurrentIndex(3)
        
        
    def fichier_resultats(self):
        
        
        
        liste_image = self.liste_image1      
        liste_image.extend(self.liste_image2)
        liste_image.extend(self.liste_image3)
        liste_valeur = self.liste_blanc_plot1
        liste_valeur.extend(self.liste_blanc_batonnets)
        liste_valeur.extend(self.liste_blanc_plot2)     
        donnees=zip(liste_image, liste_valeur)
        
     
        with open("resultat.txt", "w") as fichier:
            fichier.write('####### Calcul Remplissage entre les plots #######')
            fichier.write('\n')
            fichier.write('Taux de remplissage = '+self.Text_ratio+'%')
            fichier.write('\n')
            fichier.write('Taux de remplissage en fonction de la mediane = '+self.Text_ratio_mediane+'%')
            fichier.write('\n')
            fichier.write('Moyenne pixels blancs dans plot 1 = '+self.Text_moyenne_plot1)
            fichier.write('\n')
            fichier.write('Mediane du plot 1 = '+self.Text_mediane_plot1)
            fichier.write('\n')
            fichier.write('Moyenne pixels blancs dans plot 2 = '+self.Text_moyenne_plot2)
            fichier.write('\n')
            fichier.write('Mediane du plot 2 = '+self.Text_mediane_plot2)
            fichier.write('\n')
            fichier.write('Moyenne des pixels blanc dans les 2 plots = '+self.Text_moyenne_plot1_plot2)
            fichier.write('\n')
            fichier.write('Mediane des 2 plots = '+self.Text_mediane_plot1_plot2)
            fichier.write('\n')
            fichier.write('Moyenne pixels blancs dans les batonnets = '+self.Text_moyenne_batonnets)
            fichier.write('\n')
            fichier.write('Mediane des batonnets = '+self.Text_mediane_batonnets)
            fichier.write('\n')
            fichier.write('###########################################################')
            fichier.write('\n')
            fichier.write('image#')
            fichier.write("pixels blancs")
            fichier.write('\n')
            writer = csv.writer(fichier)
            for row in donnees: 
                 writer.writerow(row)
            
                       
            
            
    def save(self):
        file_filter = 'Data File (*.txt)'
        sauvegarde = QFileDialog.getSaveFileName(parent=self,caption='Select a data file', directory= 'resultat.txt', filter=file_filter,initialFilter='Excel File (*.txt) ')
        
        shutil.copyfile('resultat.txt', sauvegarde[0])
        
    def apropos(self):
        QMessageBox.about(self, "A propos", "Réalisé par Simon Cayez et Héliam Klein \nINSA et Paul Sab' 2021")
             
    
    def eventFilter(self, object, event):
        '''cette fonction permet de récupérer les positions du curseur souris sur la QGraphicsScene lorsque l'on clique dessus
           de plus lorqu'on relâche le clic la fonction mémorise la position et trace un trait entre les deux points du clic 
           et du relâchement de celui-ci tout en affichant la distance entre ces deux points
           un nettoyage de la scene est effectué lorque l'on retrace un trait ou lorque l'on change les paramètres d'acquisition'''
       
        if object is self.scene11 and event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            
            
            spf = event.scenePos()
            lpf = self.pixmap_item11.mapFromScene(spf)
            brf = self.pixmap_item11.boundingRect()
            if brf.contains(lpf):
                lp = lpf.toPoint()

                self.x1 = int(lp.x())
                self.y1 = int(lp.y())
                self.x1 = str(lp.x())
                self.y1 = str(lp.y())
                        
                
        if object is self.scene11 and event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
          
            spf = event.scenePos()
            lpf = self.pixmap_item11.mapFromScene(spf)
            brf = self.pixmap_item11.boundingRect()
            if brf.contains(lpf):
                lp = lpf.toPoint()
                pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red))
                p1x=float(self.x1)
                p1y=float(self.y1)
                
                if self.flag ==1:
                    self.scene11.removeItem(self.rect)
                    self.flag = 0

                p2x=float(str(lp.x()))
                p2y=float(str(lp.y()))
                self.x2 = int(lp.x())
                self.y2 = int(lp.y())
                self.rect = self.scene11.addRect(p1x,p1y,p2x-p1x,p2y-p1y,pen)
                self.flag = 1
      
                
        if object is self.scene11 and event.type() == QtCore.QEvent.GraphicsSceneMouseMove:

                spf = event.scenePos()
                lpf = self.pixmap_item11.mapFromScene(spf)
                brf = self.pixmap_item11.boundingRect()
                if brf.contains(lpf):
                    lp = lpf.toPoint()
                    pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red))
                    p1x=float(self.x1)
                    p1y=float(self.y1)
                    p2x=float(str(lp.x()))
                    p2y=float(str(lp.y()))
                    #pour le premier tracé
                    if (self.flag==0):  
                        self.rect = self.scene11.addRect(p1x,p1y,p2x-p1x,p2y-p1y,pen)
                        self.flag=1

                     #pour les tracés suivants
                    if (self.flag ==1):
                        self.scene11.removeItem(self.rect)
                        self.flag=0 
                        self.rect = self.scene11.addRect(p1x,p1y,p2x-p1x,p2y-p1y,pen)
                        self.flag=1
      
                        
  
                
        return super().eventFilter(object, event)             
            


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
