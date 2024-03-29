import sys
import os
import argparse
import atexit
import signal
from pynput import keyboard

import SimpleITK as sitk
import pyvista as pv

import cupy as cp
import numpy as np

import cucim.skimage as cusk
from cucim.skimage.morphology import (cube,ball,square)
import cupyx.scipy.ndimage as cuSci
import scipy.io as sciio
from cucim.skimage import filters,measure,feature,segmentation
from cucim.skimage.exposure import rescale_intensity


#my functions
from MRIcropCoordsRev import MRIcropCoordsRev
from VolumeViewer import VolumeViewer
from MyReadDICOM import MyReadDICOM
from EdgeBySlice import EdgeBySlice
from CHImage import CHImage
import Gui2 as g

import timeit
import tkinter as tk
from tkinter import filedialog,PhotoImage,Canvas
from PIL import Image, ImageTk
import subprocess
from subprocess import run,check_output,Popen
import time


# Esegui il comando "nvcc --version" e cattura l'output
output = check_output(["nvcc", "--version"])
# Decodifica l'output dalla codifica di byte alla stringa
output_str = output.decode("utf-8")
# Cerca la stringa "release" nell'output
release_line = [line for line in output_str.split("\n") if "release" in line][0]
# Estrai il sesto token (la versione) e i caratteri secondi e terzi della versione
version = release_line.split(" ")[5][1:3]

if int(version) < 11:
    from cupyx.scipy.ndimage import morphology as morphology
else:
    from cupyx.scipy.ndimage import _morphology as morphology 

import ctypes
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    handle = ctypes.CDLL(dir_path + "/smoothPatch.so")
elif sys.platform == "win32":
    # Windows...
    handle = ctypes.CDLL(dir_path + "\\smoothPatch.dll")

    
handle.smoothPatch.argtypes = [np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags='C_CONTIGUOUS'),ctypes.c_int,
                                np.ctypeslib.ndpointer(dtype=np.int64, ndim=1, flags='C_CONTIGUOUS'),ctypes.c_int]
handle.smoothPatch.restype = ctypes.c_void_p

import tempfile


#Functions

def smoothPatch(K,c,K1,c1):
    return handle.smoothPatch(K,c,K1,c1) 


#Define global var
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        #user = os.environ.get('USER')
        #if(locale.getdefaultlocale()[0] == "it_IT"):
    dataset = "./Datasets/"

elif sys.platform == "win32":
        # Windows...
        #import getpass
        # get your username
        #user = getpass.getuser()
    dataset =".\\Datasets\\"

elif sys.platform == "darwin":
        # OS X
    dataset = "./Datasets/"

SogliaCrop = 600
CHadd = 6
FinalClosing = 8
Protrus = 3
Edges = 1
STL_model_path= ""

first = True
fin = True
process= None

def on_press_exit(key):
    if key == keyboard.Key.esc:
        kill_visualizer_process()
        os._exit(0)
        


def kill_visualizer_process():
    global process
    if (process != None):
        print("exiting visualizer")
        os.kill(process.pid,signal.SIGTERM)


def main():

    
    global dataset, SogliaCrop, CHadd, FinalClosing, Protrus, Edges, flags,fin,data1,name,process
    
    first_render_is_not_done= True
    while(first_render_is_not_done):
        sG()
  

        global Tstart
        Tstart = timeit.default_timer()
        try:
            for f in flags:
                f()
            first_render_is_not_done = False
        except:
            print("                        ################")
            print("                        #### ERROR! ####")
            print("                        ################")
            g.GuiError()
            first_render_is_not_done = True
        

    # for f in flags:
    #     f()
    #temp_output_file = tempfile.NamedTemporaryFile()
    #temp_output_file_path=temp_output_file.name
    temp_output_file_path=tempfile.gettempdir() + "\\pipetest"
    if (not os.path.exists(temp_output_file_path)):
        temp_output_file = open(temp_output_file_path, "x")
        temp_output_file.close()
    #creates the file,if it doesn't exist
    temp_output_file =open(temp_output_file_path, "r+")
    temp_output_file.close()
    command = f"py Visualizer\\STLVisualizer.py " + " " + "\"" +  STL_model_path + "\"" + " " + "\"" + dataset + "\"" + " " + "\"" + temp_output_file_path + "\"" # the shell command
    process = Popen(command, stdout=None, stderr=None, shell=False)
        
    #process = Popen(command, stdout=subprocess.PIPE, stderr=None, shell=False)

    
    #print("visualizer is open")
    


    #re-render cycle, does not use the GUI
    exec_without_gui= True
    while(exec_without_gui):
        #visualizer outputs new parameters on this file
        time_modified_at_exec =  os.path.getmtime(temp_output_file_path)
        while(time_modified_at_exec == os.path.getmtime(temp_output_file_path)):
            #this is actually necessary 
            #python uses buffers to write to files
            #this interval of waiting gives the visualizer enough time to use the file buffers properly and actually write to it
            time.sleep(0.1)
            continue
            time.sleep(0.1)
        temp_output_file =open(temp_output_file_path, "r+")
        outputString = temp_output_file.readline()
        #print("aspetto di leggere dal visualizzatore")
        
        temp_output_file.close()
        print("Segmentation software has read from file")
        
        if (outputString):
            print("parameters have been loaded and parsed")
            params_dict= convert_string_into_param_dict(outputString)
            

            #parametri provenienti dal visualizzatore
            SogliaCropG = params_dict['intensity_threshold'] 
            CHaddG = params_dict['convex_hull_dilation'] 
            FinalClosingG = params_dict['final_closing'] 
            ProtrusG = params_dict['protrusion_removal'] 
            EdgesG = params_dict['final_dilation']

            print("\n\n###############################")
            print("### Re-rendering Input Data")
            print("###############################\n")
            print("Dataset:", dataset)
            print("SogliaCrop:", SogliaCropG)
            print("CHadd:", CHaddG)
            print("FinalClosing:", FinalClosingG)
            print("Protrus:", ProtrusG)
            print("Edges:", EdgesG)
            #rende possibile la parzializzazione del rerendering
            flags = np.asarray([s0,s1,s2,s3,s4,s5,s6,s7,s8])
            if(SogliaCropG != SogliaCrop):
                flags = np.asarray([s1,s2,s3,s4,s5,s6,s7,s8])
                print("\n\n###############################")
                print("### Restart from state 1")
                print("###############################\n")
            elif(CHaddG != CHadd):
                flags = np.asarray([s2,s3,s4,s5,s6,s7,s8])
                print("\n\n###############################")
                print("### Restart from state 2")
                print("###############################\n")
            elif(FinalClosingG != FinalClosing):
                flags = np.asarray([s3,s4,s5,s6,s7,s8])
                print("\n\n###############################")
                print("### Restart from state 3")
                print("###############################\n")   
            elif(ProtrusG != Protrus):
                flags = np.asarray([s4,s5,s6,s7,s8])
                print("\n\n###############################")
                print("### Restart from state 4")
                print("###############################\n")
            elif(EdgesG != Edges):
                flags = np.asarray([s5,s6,s7,s8])
                print("\n\n###############################")
                print("### Restart from state 5")
                print("###############################\n")

            SogliaCrop = SogliaCropG
            CHadd = CHaddG
            FinalClosing = FinalClosingG 
            Protrus = ProtrusG
            Edges = EdgesG
            try:
                Tstart = timeit.default_timer()
                for f in flags:
                    f()
            except:
                print("                        ################")
                print("                        #### ERROR! ####")
                print("                        ################")
                g.GuiError()
                return
                

            #empty modification to the temporary file, so that the visualizer knows we are done with the rerendering
            temp_output_file =open(temp_output_file_path, "w")
            temp_output_file.write("")
            temp_output_file.close()


        else:
            print("Error: nothing was read from file.")
        #catch KeyboardInterrupt:
            #process.kill()


        





def sG():

    global dataset, SogliaCrop, CHadd, FinalClosing, Protrus, Edges,flags,first
    datasetG, SogliaCropG, CHaddG, FinalClosingG, ProtrusG, EdgesG = g.Gui(dataset, SogliaCrop, CHadd, FinalClosing, Protrus, Edges)
    
    ##############################################################################
    ###  START MAIN and PARAMETERS
    ###############################################################################
    print("\n\n###############################")
    print("### Input Data")
    print("###############################\n")
    print("Dataset:", dataset)
    print("SogliaCrop:", SogliaCropG)
    print("CHadd:", CHaddG)
    print("FinalClosing:", FinalClosingG)
    print("Protrus:", ProtrusG)
    print("Edges:", EdgesG)

    if(first == False):
        if(datasetG != dataset):
            flags = np.asarray([s0,s1,s2,s3,s4,s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 0")
            print("###############################\n")
        elif(SogliaCropG != SogliaCrop):
            flags = np.asarray([s1,s2,s3,s4,s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 1")
            print("###############################\n")
        elif(CHaddG != CHadd):
            flags = np.asarray([s2,s3,s4,s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 2")
            print("###############################\n")
        elif(FinalClosingG != FinalClosing):
            flags = np.asarray([s3,s4,s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 3")
            print("###############################\n")   
        elif(ProtrusG != Protrus):
            flags = np.asarray([s4,s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 4")
            print("###############################\n")
        elif(EdgesG != Edges):
            flags = np.asarray([s5,s6,s7,s8])
            print("\n\n###############################")
            print("### Restart from state 5")
            print("###############################\n")
                
    
    else:
        first = False
        flags = np.asarray([s0,s1,s2,s3,s4,s5,s6,s7,s8])

    global SEbordiScuri,SEseparaOssa,SS3s
    SEbordiScuri = cusk.morphology.cube(2,dtype=cp.bool_) # El. Strutt. per aumentare i Edges scuri intorno alle ossa
    SEseparaOssa = cusk.morphology.ball(7,dtype=cp.bool_)  #El. Strutt. per separare le ossa dalle restanti strutture (es. legamenti e grasso)
    SS3s = cusk.morphology.square(3,dtype=cp.bool_) #Versione originaria
    global SEpp1  #El. strutt. per il Post-Processing 1 (imclose) per riempire i buchi intern
    global SEpp2 # El. Strutt. Post-Processing 2 (imopen) per eliminare protrusioni finali (calcificazioni) 
    global SEpp3  #El. Strutt. per Post-Processing 3 (imdilate) per riempire i Edges finali

    dataset, SogliaCrop, CHadd, FinalClosing, Protrus, Edges = datasetG, SogliaCropG, CHaddG, FinalClosingG, ProtrusG, EdgesG


    ##########################################################################



def s0():
    ##############################################################################
    ###  1) Read DICOM
    ###############################################################################
    t0 = timeit.default_timer()
    global V, StrelRotula, w, h, d, dataset,spacing,name
    V, StrelRotula, w, h, d,spacing,name = MyReadDICOM(dataset)
    t1 = timeit.default_timer()
    print("\n\n###############################")
    print("### SEGMENTATION TIMES")
    print("###############################")
    print(f"\nTime for reading MRI file: {t1 - t0}s")
    #g.worker("### SEGMENTATION TIMES")


def s1():
    global V,SogliaCrop,w,h,d
    ##############################################################################
    ###  2) Pre-processing
    ###############################################################################   
    ######################################################################
    # 2.1) Fa il crop eliminando zone scure intorno
    Vcrop,x1,x2,y1,y2,z1,z2 = MRIcropCoordsRev(V,SogliaCrop,w,h,d)
    Vcrop = cp.rot90(Vcrop,axes=(2,0))

    ######################################################################
    # 2.2)Aumenta i Edges scuri intorno alle ossa
    structCube0 = cp.asarray(SEbordiScuri)
    #erode = cuSci._morphology.grey_erosion(Vcrop, footprint=structCube0)
    erode = morphology.grey_erosion(Vcrop, footprint=structCube0)
    Img3D = cp.asarray(cp.double(erode.get()))
    # Normalize in 0 to 1 range
    Img3D = rescale_intensity(Img3D, out_range=(0, 1))

    ##############################################################################
    ###  3) Calcolo segmentazione ed estrazione delle 3 ossa (--> CCa2, CCb2, CCc2):
    ###############################################################################


    ######################################################################
    # 3.1) Segmentazione con Otsu thresholding  

    t0 = timeit.default_timer() 

    T = filters.threshold_otsu(Img3D)
    global OutSeg
    OutSeg = Img3D>T

    print(f"Time for segmentation: {timeit.default_timer() - t0}s")


    ######################################################################
    # 3.2) Estrazione di una versione "rough" di tibia e femore (--> CCa, CCb)
    #print("Tibia and Femur:******************************************\n")


    ######################################################################
    # 3.2.1) "Forte" erosione, per separare le ossa dalle restanti strutture (es. legamenti e grasso)
    t0 = timeit.default_timer() 

    #OutSeg_1 = cuSci._morphology.binary_erosion(OutSeg, structure=SEseparaOssa)    
    OutSeg_1 = morphology.binary_erosion(OutSeg, structure=SEseparaOssa)    

    print(f"Time for erosion: {timeit.default_timer() - t0}s")


    ######################################################################
    # 3.2.2) Ci sono casi (es. la mia coronale) in cui l'erosione non basta, 
    #        per cui elimino anche gli edge, individuati mediante Canny 2D (su ogni slice)
    t0 = timeit.default_timer() 

    #print(Img3D[:,:,150])
    global edge3D
    edge3D = EdgeBySlice(Img3D) #Calcolo degli edge

    print(f"Time for computing edges: {timeit.default_timer() - t0}s")

    OutSeg_2 = OutSeg_1*np.logical_not(edge3D)#Eliminazione degli edge


    ######################################################################
    #3.2.3) Calcolo di tutte le CC in OutSeg_2
    L0,nr_objects0 = cusk.measure.label(OutSeg_2,return_num=True, connectivity=1) #Connectivity below 1 or above 3 is illegal. 6 non va bene


    ######################################################################   
    # 3.2.4) Selezione delle 3 CC più voluminose
    t0 = timeit.default_timer() 

    stats0 = (measure.regionprops(L0))

    print(f"Time for computing the 3 widest CCs: {timeit.default_timer() - t0}s")

    # ordinamento per volume/area e ricerca prime 3
    stats0.sort(key=lambda x: x.area, reverse=True)

    #Cerco tibia e femore in quelle con volume fra il primo ed il terzo posto
    cc012 = cp.zeros(L0.shape, dtype=cp.bool_)
    for i in range(0,3):
      cc012[L0.get() == stats0[i].label] = True
    Vol13 = cp.asarray(cc012)


    ###################################################################### 
    # 3.2.5) Selezione delle 2 CC con maggior Extent (richiede tempo, per questo
    #        lo calcolo solo sulle 3 più estese) --> CCa, CCb

    L1,nr_objects1 = cusk.measure.label(Vol13,return_num=True, connectivity=1)
    stats1 = (measure.regionprops(L1))

    # ordinamento per extent e ricerca prime 3
    stats1.sort(key=lambda x: x.extent, reverse=True)

    CCa= cp.zeros(L1.shape, dtype=cp.bool_)
    CCa[L1.get() == stats1[0].label] = True
    CCb= cp.zeros(L1.shape, dtype=cp.bool_)
    CCb[L1.get() == stats1[1].label] = True
    CCa = cp.asarray(CCa)
    CCb = cp.asarray(CCb)

    #CC_AB = CCa + CCb


    ######################################################################     
    # 3.2.6) Calcolo CH di tibia e femore (servono in 3.3 per la rotula)

    #BBa = round(stats1.BoundingBox(idx(1),:));
    BBa = cp.zeros(6)
    for i in range(6):
      BBa[i] = round(stats1[0].bbox[i])

    t0 = timeit.default_timer()
    CIa = CHImage(CCa, BBa)
    print(f"Time for computing convex image: {timeit.default_timer() - t0}s")

    global Mtfa
    Mtfa = cp.zeros(Vol13.shape,dtype="bool")
    Mtfa[BBa[0]:BBa[3], BBa[1]:BBa[4], BBa[2]:BBa[5]]=CIa


    BBb = cp.zeros(6)
    for i in range(6):
      BBb[i] = round(stats1[1].bbox[i])

    t0 = timeit.default_timer()
    CIb = CHImage(CCb, BBb)
    print(f"Time for computing convex image CIb: {timeit.default_timer() - t0}s")
    global Mtfb
    Mtfb = cp.zeros(Vol13.shape,dtype="bool")
    Mtfb[BBb[0]:BBb[3], BBb[1]:BBb[4], BBb[2]:BBb[5]]=CIb

    #M12 = Mtfa + Mtfb



    ###############################################################################
    # 3.3) Estrazione di una versione "rough" della rotula (--> CCcs, nel sottovolume)

    #print('Rotula:**************************************************\n')


    ################################################################################   
    # 3.3.1) Costruzione maschera in cui cercare la rotula (escludendo tibia e femore)

    BW1CCab = cp.logical_xor(OutSeg, Mtfa | Mtfb)

    ##################################################################################################
    # 3.3.2) Estrazione sottovolume SubVol per cercare la rotula (a sx e in alto rispetto a CCa, CCb)  

    if (BBa[1]<BBb[1]):
      BBtibia = BBb
      BBfemore = BBa
    else:
      BBtibia = BBa
      BBfemore = BBb;

    SubVol = Img3D[0:BBfemore[0],0:BBtibia[1],:]

    ## Rotula: operazioni sul SubVol %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #  (tutte le variabili che finiscono con 's')

    BW1s = BW1CCab[0:BBfemore[0],0:BBtibia[1],:] #Restringo al sottovolume di interesse


    ######################################################################    
    #3.3.3) Forza la separazione fra le CC per la rotula (come fatto per tibia e femore)   

    t0 = timeit.default_timer()
    edge3Ds = EdgeBySlice(SubVol); #Calcolo degli edge nel SubVol
    print(f"Time for computing edges in SubVol: {timeit.default_timer() - t0}s")
      
    BW2s = BW1s*cp.logical_not(edge3Ds) #Segmentazione con separazione fra CC
    BW2s = cp.asarray(BW2s, dtype="float64")
    #BW2es = cuSci._morphology.binary_erosion(BW2s, structure=StrelRotula) #Ulteriore separazione delle CC
    BW2es = morphology.binary_erosion(BW2s, structure=StrelRotula)
       
    # VolumeViewer(BW2es.get()*1)
    # exit()

    ###########################################################################
    # 3.3.4) Selezione della CC più voluminosa (per TUTTE E 4 LE SST, la rotula e' 
    #        la CC piu' estesa, senza poter contare su Solidity ne' Extent)

    L0s,nr_objects_cc0 = cusk.measure.label(BW2es,return_num=True, connectivity=1)
    stats0s = (measure.regionprops(L0s))

    # ordinamento per area/volume e ricerca prime 3
    stats0s.sort(key=lambda x: x.area, reverse=True)
    CCcs = cp.zeros(L0s.shape, dtype=cp.bool_)
    CCcs[L0s.get() == stats0s[0].label] = True
       
    #Rotula: fine operazioni sul SubVol %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    ###########################################################################
    # 3.3.5) Calcolo CH della rotula (serve in 3.4)

    Ls,nr_objects_cc0 = cusk.measure.label(CCcs,return_num=True, connectivity=1)
    Propsc = (measure.regionprops(Ls))
    BBc = cp.zeros(6)
    for i in range(6):
      BBc[i] = round(Propsc[0].bbox[i])

    t0 = timeit.default_timer()
    CIc = CHImage(CCcs, BBc)
    print(f"Time for computing convex image CIc: {timeit.default_timer() - t0}s")
    global Mtfc
    Mtfc = cp.zeros(Vol13.shape,dtype="bool")
    Mtfc[BBc[0]:BBc[3], BBc[1]:BBc[4], BBc[2]:BBc[5]]=CIc

    #M123 = M12 + Mtfc


def s2():

    global CHadd,Mtfa,Mtfb,Mtfc
    ###########################################################################
    # 3.4) Estrazione della versione "raffinata" delle 3 ossa (--> CCa2, CCb2, CCc2)

    # 3.4.1) Dilatazione dei convex hull delle 3 ossa
    sphMT = cusk.morphology.ball(CHadd)
    Mtfa2 = cusk.morphology.binary_dilation(Mtfa,footprint=sphMT)
    Mtfb2 = cusk.morphology.binary_dilation(Mtfb,footprint=sphMT)
    Mtfc2 = cusk.morphology.binary_dilation(Mtfc,footprint=sphMT)

    ###########################################################################
    # 3.4.2) Ri-calcolo della versione erosa della OutSeg senza edge, OutSeg_4, 
    #        usando il "vecchio SS3" (piu' "densa" della OutSeg_2):

    #edge3D = cusk.morphology.binary_dilation(edge3D,footprint=SEpp4)
    OutSeg_3 = cp.asarray(OutSeg*cp.logical_not(edge3D),dtype="float64")
    OutSeg_4 = OutSeg_3

    #fig, ax = plt.subplots(1,1)
    ## create an IndexTracker and make sure it lives during the whole
    ## lifetime of the figure by assigning it to a variable
    #tracker = IndexTracker(ax, OutSeg_3.get())
    #
    #fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    #plt.show()

    for slice in range(0,OutSeg_3.shape[2]):
      #OutSeg_4[:,:,slice] = cuSci._morphology.grey_erosion(OutSeg_3[:,:,slice], footprint=SS3s)
      OutSeg_4[:,:,slice] = morphology.grey_erosion(OutSeg_3[:,:,slice], footprint=SS3s)

    OutSeg_4 = cp.asarray(OutSeg_4,dtype="bool")
    ###########################################################################
    #3.4.3) Estrae tibia e femore, eliminando altre CC re-introdotte in OutSeg_4

    BonesNotCloseabCH = OutSeg_4 & (Mtfa2 | Mtfb2)
    #VolumeViewer(BonesNotCloseabCH.get()*1)


    L02,nr_objects_cc02 = cusk.measure.label(BonesNotCloseabCH,return_num=True, connectivity=1)
    stats02 = (measure.regionprops(L02))
    # ordinamento per area/volume e ricerca prime 3
    stats02.sort(key=lambda x: x.area, reverse=True)

    global CCa2, CCb2
    CCa2 = cp.zeros(L02.shape, dtype=cp.bool_)
    CCa2[L02.get() == stats02[0].label] = True
    CCb2 = cp.zeros(L02.shape, dtype=cp.bool_)
    CCb2[L02.get() == stats02[1].label] = True



    ###########################################################################
    #3.4.4) Estrae la rotula, eliminando altre CC re-introdotte in OutSeg_4

    BonesNotClosecCH = OutSeg_4 & Mtfc2; 
    L03,nr_objects_cc03 = cusk.measure.label(BonesNotClosecCH,return_num=True, connectivity=1)
    stats03 = (measure.regionprops(L03))
    # ordinamento per area/volume e ricerca prime 3
    stats03.sort(key=lambda x: x.area, reverse=True)

    global CCc2
    CCc2 = cp.zeros(L03.shape, dtype=cp.bool_)
    CCc2[L03.get() == stats03[0].label] = True



    CCa2 = np.pad(CCa2,15, 'constant', constant_values=0)
    CCb2 = np.pad(CCb2,15, 'constant', constant_values=0)
    CCc2 = np.pad(CCc2,15, 'constant', constant_values=0)


    ####################################################################
    #4) Post-processing delle 3 ossa CCa2, CCb2, CCc2 (--> BonesClose):

    print('\nPost-processing:**************************************************')





def s3():
    global FinalClosing
    ########################################################################################
    # 4.1) Chiusura delle 3 CC separate per riempire i buchi interni, di ampiezza FinalClosing
    SEpp1 = cusk.morphology.ball(FinalClosing,dtype=cp.bool_)
    t0 = timeit.default_timer()
    global CCa2close,CCb2close,CCc2close
    CCa2close = cusk.morphology.binary_closing(CCa2,footprint=SEpp1)
    CCb2close = cusk.morphology.binary_closing(CCb2,footprint=SEpp1)
    CCc2close = cusk.morphology.binary_closing(CCc2,footprint=SEpp1)
    print(f"Time for Post-Processing 1 (imclose): {timeit.default_timer() - t0}s")



def s4():
    global Protrus
    ####################################################################   
    # 4.2) Opening per eliminare protrusioni (la calcificazione), di ampiezza Protrus  
    SEpp2 = cusk.morphology.ball(Protrus,dtype=cp.bool_) 
    t0 = timeit.default_timer()
    global Sopena
    Sopena = cusk.morphology.binary_opening(CCa2close,footprint=SEpp2)
    global Sopenb
    Sopenb = cusk.morphology.binary_opening(CCb2close,footprint=SEpp2)
    global Sopenc
    Sopenc = cusk.morphology.binary_opening(CCc2close,footprint=SEpp2)
    #Sopenc = CCc2close
    print(f"Time for Post-Processing 2 (imopen): {timeit.default_timer() - t0}s")


def s5():
    global BonesClose,Sopena,Sopenb,Sopenc
    #####################################################################
    # 4.3) Dilatazione finale per riempire i Edges, di ampiezza Edges
    SEpp3 = cusk.morphology.ball(Edges,dtype=cp.bool_)
    t0 = timeit.default_timer()
    SopenDila = cusk.morphology.binary_dilation(Sopena,footprint=SEpp3)
    SopenDilb = cusk.morphology.binary_dilation(Sopenb,footprint=SEpp3)
    SopenDilc = cusk.morphology.binary_dilation(Sopenc,footprint=SEpp3)
    
    BonesClose = SopenDila | SopenDilb | SopenDilc
    print(f"Time for Post-Processing 3 (imdilate): {timeit.default_timer() - t0}s")
    print("\n\n###############################")
    print("### SEGMENTATION COMPLETED")
    print("###############################")

def s6():
    global data1,spacing,BonesClose
    ##############################################################################
    ###  X) Volume Viewer with PyVista
    ###############################################################################

    #BonesClose = cp.asarray(np.asarray(MFC.get()))
    BonesClose2 = cp.zeros([BonesClose.shape[0] +2, BonesClose.shape[1],BonesClose.shape[2]],dtype="bool")
    BonesClose2[1:BonesClose2.shape[0]-1,:,:]=BonesClose
    #VolumeViewer(BonesClose2.get()*1)

    #########################################
    ###  6) Calcolo Isosuperfice
    #########################################
    
    data1 = np.invert(np.asarray(BonesClose2.get()*1))

    # del BonesClose,BonesClose2
    # cp._default_memory_pool.free_all_blocks()

    data1 = pv.wrap(data1)
    data1.spacing=spacing

    #triangolazione
    t0 = timeit.default_timer()
    data1 = data1.contour(isosurfaces = 3)
    print(f"\nTime for computing contour (triangulation): {timeit.default_timer() - t0}s")


def s7():
    global data1
    #########################################
    ###  7) Smoothpatch
    #########################################

    vertices = data1.points.flatten()
    faces = data1.faces.flatten()

    t0 = timeit.default_timer()
    data1Smoothed = smoothPatch(vertices,len(vertices),faces,len(faces))
    print(f"Time for computing smootPatch: {timeit.default_timer() - t0}s")

    data1.points = vertices.reshape(-1,3)
    data1.faces = faces.reshape(-1,4)


def s8():
    #########################################
    ###  8) STL View & Save
    #########################################
    global Tstart,dataset,data1,process,STL_model_path
    #TIME
    print(f"\nTime for total execution: {timeit.default_timer() - Tstart}s")


    data1.flip_normals()
    data1.compute_normals(cell_normals=True, point_normals=False, split_vertices=False, 
                          flip_normals=True, consistent_normals=True, auto_orient_normals=True, 
                          non_manifold_traversal=True,feature_angle=30.0, inplace=False, progress_bar=False)

    
    #STL save...
    # if( str(dataset)[-1] == '/' or str(dataset)[-1] == '\\'):
    #     nm = str(f"{dataset[:-1]}.stl")
    # else:
    #     nm = str(f"{dataset}.stl")
    # data1.save(nm)
    print("\nSaving...")
    STL_model_path = tempfile.gettempdir() +"\\MRI.stl"
    data1.save(STL_model_path)
    print("\nSaved in " + STL_model_path)

    # esecuzione = os.popen("Slicer.exe --minimized --no-splash --python-script .\\SegOscanSlicer.py")
    # risultato = esecuzione.read()
    # esecuzione.close()
    print("dataset:")
    print(dataset)
    print("\nOpening VR visualization... (Press Esc to exit the entire program)")
    #command = f"py ..\\STLVisualizer.py " + " " + "\"" +  STL_model_path + "\"" + " " + "\"" + dataset + "\"" # the shell command
    #process = Popen(command, stdout=None, stderr=None, shell=False)
    #process = Popen(command, stdout=subprocess.PIPE, stderr=None, shell=False)
    # print("\n\n###############################")
    # print("### Reprinting Input Data")
    # print("###############################\n")
    # print("Dataset:", dataset)
    # print("SogliaCrop:", SogliaCrop)
    # print("CHadd:", CHadd)
    # print("FinalClosing:", FinalClosing)
    # print("Protrus:", Protrus)
    # print("Edges:", Edges)
    
def convert_string_into_param_dict(output_string):
    parameters_from_string=output_string.split("%")
    param_dict = {}
    param_dict['intensity_threshold'] = int(parameters_from_string[1])
    param_dict['convex_hull_dilation'] = int(parameters_from_string[2])
    param_dict['final_closing'] = int(parameters_from_string[3])
    param_dict['protrusion_removal'] = int(parameters_from_string[4])
    param_dict['final_dilation'] = int(parameters_from_string[5])

    return param_dict




flags = np.asarray([s0,s1,s2,s3,s4,s5,s6,s7,s8])

atexit.register(kill_visualizer_process)
signal.signal(signal.SIGABRT,kill_visualizer_process)
signal.signal(signal.SIGTERM,kill_visualizer_process)
exit_listener= keyboard.Listener(on_press=on_press_exit)
exit_listener.start() 
if os.name == "nt":
    import win32api
    win32api.SetConsoleCtrlHandler(kill_visualizer_process, True)

main()
