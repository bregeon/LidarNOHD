#!/bin/env python
from math import sqrt, cos, sin

BeamDiv=2 # >2 mrad
Freq=20    # 20 Hz
PulseWidth=10*1e-9 # 10 ns
EyeClosed = 0.25 # 0.25 s
NPulses = Freq*EyeClosed # Pulses Within EyeClosed
Feet2Meters=0.3048 # 1 foot = 30.48 cm
MinElevationAngle = 85 # 85 degrees
MaxElevationAngle = 90 # 85 degrees

wl_list=[355,532,1064]

mpe_list=[]


def getEPulse(wl):
  if wl==355:
    Epulse=90 # 90 mJ
  elif wl==532:
    Epulse=230 # 230 mJ
  elif wl==1064:
    Epulse=400 # 400 mJ
  else:
    print("wl %d unknown for E pulse"%wl)
  return Epulse/1000.

def getPower(wl):
  POW=getEPulse(wl)*Freq
  return POW
  
def getMPEPulse(wl):
  """ MPE for one pulse in J.m**-2
   http://www.optique-ingenieur.org/fr/cours/OPI_fr_M01_C02/res/annexe1_2.jpg
  """
  mpeP=0
  if wl==355:
    mpeP=5.6*1e3*(PulseWidth**(1/4.))  # J/m2
  elif wl==532:
    mpeP=5*1e-3 # J/m2
  elif wl==1064:
    mpeP=5*1e-2 # J/m2
  else:
    print("wl %d unknown"%wl)
  return mpeP*1e-4 # J/cm2

def getMPEEye(wl):
  """ MPE for 0.25 s seconds
  """
  mpe=getMPEPulse(wl)*(NPulses**(-1./4.)) # J/cm2 for t=EyeClosed
  return mpe/EyeClosed # W/cm2

def getMPEEyeFromTable(wl):
  mpe=0
  if wl==355:
    mpe=getMPEEye(355) # not known
    #print('MPE Unknown for 355 nm')
  elif wl==532:
    mpe=6.69e-6 # W/cm2 (Table 3, p.74)
  elif wl==1064:
    mpe=11.2e-6 # W/cm2 (Table 2 p.73 ; Table 4, p.75 )
  else:
    print("wl %d unknown for MPE"%wl)
  return mpe

def getNOHDSlant(wl):
  """ NOHD Equation 6.1
  """
  nohd=sqrt( (1366*getEPulse(wl)) / ((BeamDiv**2)*getMPEPulse(wl)) )  
  return nohd*Feet2Meters # m

def getNOHDSlantPow(wl):
  """ NOHD Equation 6.2
  """
  nohd=sqrt( (1366*getPower(wl)) / ((BeamDiv**2)*getMPEEyeFromTable(wl)) )  
  return nohd*Feet2Meters # m

def getNOHDHorizontal(wl):
  """ NOHD Equation 6.2
  """
  nohd=getNOHDSlant(wl)*cos(MinElevationAngle*3.14159/180.)
  return nohd # m

def getNOHDVertical(wl):
  """ NOHD Equation 6.2
  """
  nohd=getNOHDSlant(wl)*sin(MaxElevationAngle*3.14159/180.)
  return nohd # m

def getNOHDHorizontalPow(wl):
  """ NOHD Equation 6.2
  """
  nohd=getNOHDSlantPow(wl)*cos(MinElevationAngle*3.14159/180.)
  return nohd # m

def getNOHDVerticalPow(wl):
  """ NOHD Equation 6.2
  """
  nohd=getNOHDSlantPow(wl)*sin(MaxElevationAngle*3.14159/180.)
  return nohd # m

def getSZEDSlant(wl):
  """ SZED Equation 6.3
  """
  szed=0
  if wl==532:
    szed=3700./BeamDiv*sqrt(getPower(wl))
  return szed*Feet2Meters # m

def getSZEDHorizontal(wl):
  """ NOHD Equation 6.2
  """
  nohd=getSZEDSlant(wl)*cos(MinElevationAngle*3.14159/180.)
  return nohd # m

def getSZEDVertical(wl):
  """ NOHD Equation 6.2
  """
  nohd=getSZEDSlant(wl)*sin(MaxElevationAngle*3.14159/180.)
  return nohd # m

def getCZEDSlant(wl):
  """ CZED  = SZED*4.5
  """
  return getSZEDSlant(wl)*4.5 # m

def getCZEDHorizontal(wl):
  """ CZED  = SZED*4.5
  """
  return getSZEDHorizontal(wl)*4.5 # m

def getCZEDVertical(wl):
  """ CZED  = SZED*4.5
  """
  return getSZEDVertical(wl)*4.5 # m

def getLFEDSlant(wl):
  """ LFED  = SZED*45
  """
  return getSZEDSlant(wl)*45 # m

def getLFEDHorizontal(wl):
  """ LFED  = SZED*45
  """
  return getSZEDHorizontal(wl)*45 # m

def getLFEDVertical(wl):
  """ LFED  = SZED*4.5
  """
  return getSZEDVertical(wl)*45 # m


for wl in wl_list:
  print("wl=%d nm"%wl)
  print("MPE(W/cm2) = %.2e"%getMPEEye(wl))
  print("MPE Pulse(J/cm2) = %.2e"%getMPEPulse(wl))
  print("NOHD from Pulse Slant/Horizontal/Vertical (m) = %.1f / %.1f / %.1f"%
         (getNOHDSlant(wl), getNOHDHorizontal(wl), getNOHDVertical(wl)))
  print("NOHD from Power Slant/Horizontal/Vertical (m) = %.1f / %.1f / %.1f"%
         (getNOHDSlantPow(wl), getNOHDHorizontalPow(wl), getNOHDVerticalPow(wl)))
  print("SZED Slant/Horizontal/Vertical (m) = %.1f / %.1f / %.1f"%
         (getSZEDSlant(wl), getSZEDHorizontal(wl), getSZEDVertical(wl)))
  print("CZED Slant/Horizontal/Vertical (m) = %.1f / %.1f / %.1f"%
         (getCZEDSlant(wl), getCZEDHorizontal(wl), getCZEDVertical(wl)))
  print("LFED Slant/Horizontal/Vertical (m) = %.1f / %.1f / %.1f"%
         (getLFEDSlant(wl), getLFEDHorizontal(wl), getLFEDVertical(wl)))

  print("\n")

