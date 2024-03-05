import sys
import SimpleITK as sitk
import cupy as cp

import cucim.skimage as cusk
from cucim.skimage.morphology import (cube,ball,square)

def MyReadDICOM(dataset):

  print("\n###############################")
  print("### DICOM INFO")
  print("###############################")
  print("\nReading Dicom directory:", dataset)
  reader = sitk.ImageSeriesReader()

  dicom_names = reader.GetGDCMSeriesFileNames(dataset)
  reader.SetFileNames(dicom_names)
  reader.MetaDataDictionaryArrayUpdateOn()
  reader.LoadPrivateTagsOn()

  Vorig = reader.Execute()
  w = Vorig.GetWidth()
  h = Vorig.GetHeight()
  d = Vorig.GetDepth()
  spacing = Vorig.GetSpacing()
 
  name = reader.GetMetaData(0,"0010|0010")
  print(f"\n\nPatient Name: {name}")

  patient_id = reader.GetMetaData(0,"0010|0020")
  print(f"Patient ID: {patient_id}")  

  Study_ID = reader.GetMetaData(0,"0020|0010")
  print(f"Study ID: {Study_ID}")

  Study_UID = reader.GetMetaData(0,"0020|000e")
  print(f"Series Instance UID: {Study_UID}")  

  Study_date = reader.GetMetaData(0,"0008|0020")
  print(f"Study Date: {Study_date}") 

  Study_time = reader.GetMetaData(0,"0008|0030")
  print(f"Study Time: {Study_time}") 

  Accession_Number = reader.GetMetaData(0,"0008|0050")
  print(f"Accession Number: {Accession_Number}") 

  Modality = reader.GetMetaData(0,"0008|0060")
  print(f"Modality: {Modality}") 





  Ori= Vorig.GetDirection()
  Vorig = sitk.GetArrayFromImage(Vorig)

  print("Dicom shape:",Vorig.shape)

  Ori = tuple([int(round(x,2)) if isinstance(x, float) else x for x in Ori])

  if (Ori[0]): #Coronal or Axial
    if (Ori[4]): #Axial
      print("MRI type: Axial")
      Vorig = cp.rot90(Vorig, k=2,axes=(2,0))
      w,h,d = h,d,w
      VS = cp.flipud(cp.rot90(cp.transpose(Vorig,[0,2,1])))
      V=VS #Voglio sempre la Sagittal
      

    else: #%Coronal
      print("MRI type: Coronal")
      Vorig = cp.rot90(cp.rot90(Vorig,axes=(2,1)),axes=(0,1))
      w,h,d = d,h,w
      VS=cp.fliplr(cp.transpose(Vorig,[0,2,1]))
      V=VS #Voglio sempre la Sagittal    
    
    StrelRotula = cusk.morphology.cube(3,dtype=cp.bool_) 
    #StrelRotula = cusk.morphology.cube(2,dtype=cp.bool_) 

  else: #Sagittal
          print("MRI type: Sagittal")
          StrelRotula = cusk.morphology.cube(4,dtype=cp.bool_)
          #StrelRotula = cusk.morphology.cube(3,dtype=cp.bool_)
          V=Vorig
          
  V = cp.asarray(V)

  return V, StrelRotula, w, h, d,spacing,name
