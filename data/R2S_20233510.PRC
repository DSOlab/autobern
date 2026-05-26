================================================================================
RNX2SNX BPE PROCESSING SUMMARY FOR YEAR-SESSION 2023-3510
================================================================================


Summary file generated at 23-May-2026 00:23:42 by R2S_SUM

General and model files:
-----------------------
   Mean pole model:                             V_MEANPL = "IERS2010_v1.2.0"
   Subdaily pole model:                         V_SUBMOD = "DESAI2016"
   Nutation model:                              V_NUTMOD = "IAU2000R06"
   Antenna phase center (PCV) model:            V_PCV    = "I20"
   PCV information file:                        V_PCVINF = "ANTENNA"
   Satellite information file:                  V_SATINF = "SATELLIT"
   Satellite problem file:                      V_SATCRX = "SAT_2023"
   Directory with orbit prodcuts:               V_ORBDIR = "/home/bpe54/data/GPSDATA/DATAPOOL/COD0OPSFIN"
   Orbit/ERP, CLK, bias information:            V_ORB    = "COD0OPSFIN"
      Stochastic pulses (Orbit_midnight or Spacing):V_STOCH_NUMBER= "Orbit_midnight"

Reference frame and station related files:
-----------------------------------------
   Directory with basic Bernese files:          V_REFDIR = "/home/bpe54/data/GPSDATA/DATAPOOL/REF54"
   Master/reference CRD/VEL filename:           V_REFINF = "IGS20"
   PSD corrections (ITRF2014 or higher):        V_REFPSD = "IGS20"
   Merged CRD/VEL filename:                     V_CRDINF = "EPNB23"
      Station information file:                 V_STAINF = "CODE_EPN"
      Accepted station inform.inconsistencies:  V_CRXINF = ""
      BLQ file name, CMC corrections:           V_BLQINF = "FES2014b"
      ATL file name, CMC corrections:           V_ATLINF = ""
   Directory with basic Bernese files:          V_BSWDIR = "/home/bpe54/data/GPSDATA/DATAPOOL/BSW54"
      Ionosphere model for higher order iono:   V_HOIFIL = "HOI_20233510"
      OSB-file with GNSS satellite biases:      V_OSBFIL = "COD_20233510"

Data selection:
--------------
   Directory with the RINEX files:              V_RNXDIR = "/home/bpe54/data/GPSDATA/CAMPAIGN54/EPNB23/RAW"
   Station selection file (blank: all):         V_RNXSEL = ""
   Observation selection file:                  V_OBSSEL = "OBSERV"
   Data sampling interval (in seconds):         V_SAMPL  = "180"

   Select the GNSS (max. supported: GRECJ):     V_SATSYS = "GRE"

Ambiguity resolution:
--------------------
   Select the GNSS for amb. resolu. (GECJ):     V_GNSSAR = "GRE"
   Maximum baseline length for MW/L3 AR:        V_BL_AMB = "6000"
   Maximum baseline length for QIF AR:          V_BL_QIF = "2000"
   Maximum baseline length for L5/L3 AR:        V_BL_L53 = "200"
   Maximum baseline length for L1&L2 AR:        V_BL_L12 = "10"

Processing flow related variables:
---------------------------------
   Maximum number of files per cluster:         V_CLU    = "8"
   Same as V_CLU but for GPSEDT:                V_CLUEDT = "5"
   N: skip A: auto clustering in GPSCLU:        V_CLUFIN = "A"

   Session range begin (for COMPAR):            V_MINUS  = "-6"
   Session range end:                           V_PLUS   = "+0"

   Number of hourly sessions proc. together:    V_HOURLY = "8"
   PRC file: indicator to repeat the sess.:     V_SKIP   = "/home/bpe54/data/GPSDATA/SAVEDISK/RNX2SNX/2023/OUT/R2S_20233510.PRC_"

Storing the results:
-------------------
   Directory name for the RNX2SNX results:      V_RESULT = "/home/bpe54/data/GPSDATA/SAVEDISK/RNX2SNX/2023"
   Save results (Y/N)?:                         V_SAV    = "Y"
   Save observation files (Y/N)?:               V_SAVOBS = "Y"
      Final (ambiguity-fixed) results:          V_FIN    = "DSO"
      Size-reduced NEQ information:             V_RED    = "DSR"

Other solution IDs used in the BPE:
----------------------------------
   A priori information:                        V_APR    = "APR"
   Preliminary (ambiguity-float) results:       V_FLT    = "DSP"

Other variables:
---------------
   SINEX header file:                           V_SNXINF = "NTUA_DDP"
   ANTEX file for update (name incl. ext):      V_MYATX  = ""
   Delete result files in the campaign (Y/N)?:  V_DEL    = "N"



================================================================================
PART 0: RINEX INCONSISTENCIES
================================================================================

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/ADAR00GBR_S_20233510000_01D_30S_MO.RNX

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/ARIS00GBR_S_20233510000_01D_30S_MO.RNX

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/BOR100POL_R_20233510000_01D_30S_MO.RNX

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/KLOP00DEU_S_20233510000_01D_30S_MO.RNX

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/MOP200SVK_R_20233510000_01D_30S_MO.RNX

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  GLONASS COD/PHS/BIS
        RINEX file name: ${P}/EPNB23/RAW/SCIL00GBR_S_20233510000_01D_30S_MO.RNX

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### FN O_RNXBASE:chkConformRnxRecsFound, PG RNXSMT
        Mandatory header record is missing.
        Missing record:  SYS / PHASE SHIFT
        RINEX file name: ${P}/EPNB23/RAW/ZADA00HRV_S_20233510000_01D_30S_MO.RNX

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   GANP*            2002 09 04 00 00 00                     
      GANP 11515M001   GANP*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   IENG*            2001 10 04 09 00 00                     
      IENG 12724S001   IENG*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     
      KLOP 14214M002   KLOP*            1997 03 19 00 00 00                     

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   PTBB*            2000 03 29 00 00 00                     
      PTBB 14234M001   PTBB*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   SFER*            1995 12 18 00 00 00                     
      SFER 13402M004   SFER*                                                    

 ### SR D_STACRX:chkType001: Ambiguous data in TYPE 001, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   VILL*            1994 11 12 00 00 00                     
      VILL 13406M001   VILL*                                                    

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001                        2006 08 24 23 59 59 TRIMBLE 4700         TRM29659.00     NONE
      GANP 11515M001   2002 09 04 00 00 00  2006 08 24 11 29 00 TRIMBLE 4700         TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2006 08 24 16 09 00  2009 08 19 09 30 00 TRIMBLE NETR5        TRM55971.00     NONE
      GANP 11515M001   2006 08 25 00 00 00  2009 08 18 23 59 59 TRIMBLE NETR5        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2009 08 19 00 00 00  2012 04 19 23 59 59 TRIMBLE NETR8        TRM55971.00     NONE
      GANP 11515M001   2009 08 19 09 45 00  2012 04 19 08 00 00 TRIMBLE NETR8        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 19 08 10 00  2017 02 06 10 00 00 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2012 04 20 00 00 00  2017 02 06 11 59 59 TRIMBLE NETR9        TRM55971.00     NONE
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2017 02 06 10 01 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS
      GANP 11515M001   2017 02 06 12 00 00  2018 08 20 12 15 00 TRIMBLE NETR9        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS
      GANP 11515M001   2018 08 20 12 24 00                      TRIMBLE ALLOY        TRM59800.00     SCIS

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001                        2018 03 23 23 59 59 ASHTECH Z-XII3T      ASH701945C_M    NONE
      IENG 12724S001   2001 10 04 09 00 00  2018 03 23 23 59 00 ASHTECH Z-XII3T      ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE
      IENG 12724S001   2018 03 28 00 00 00  2019 04 11 06 00 00 SEPT POLARX4TR       ASH701945C_M    NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 30 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2019 04 11 07 05 00  2023 06 27 09 00 00 SEPT POLARX4TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE
      IENG 12724S001   2023 06 27 09 30 00                      SEPT POLARX5TR       SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 44 59 TRIMBLE 4000SSI      TRM22020.00+GP  DOME
      KLOP 14214M002   1997 03 19 00 00 00  2001 05 08 09 45 00 TRIMBLE 4000SSI      TRM22020.00+GP  DOME

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 08 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2001 05 08 09 45 00  2002 07 02 08 09 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 14 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      KLOP 14214M002   2002 07 02 09 55 00  2004 10 28 09 15 00 TRIMBLE 4000SSI      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 59 TRIMBLE NETRS        TRM29659.00     NONE
      KLOP 14214M002   2004 10 28 09 15 00  2007 04 26 12 44 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 59 TRIMBLE NETR5        TRM29659.00     NONE
      KLOP 14214M002   2007 04 26 12 45 00  2007 06 27 10 59 00 TRIMBLE NETR5        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 08 59 59 TRIMBLE NETR5        TRM55971.00     TZGD
      KLOP 14214M002   2007 06 27 11 00 00  2013 06 28 09 00 00 TRIMBLE NETR5        TRM55971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 27 59 TRIMBLE NETR5        TRM57971.00     TZGD
      KLOP 14214M002   2013 06 28 10 10 00  2013 12 11 07 28 00 TRIMBLE NETR5        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD
      KLOP 14214M002   2013 12 11 07 48 00  2018 10 31 07 28 00 TRIMBLE NETR9        TRM57971.00     TZGD

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM
      KLOP 14214M002   2018 10 31 11 00 00  2020 11 24 08 00 00 TRIMBLE NETR9        LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM
      KLOP 14214M002   2020 11 24 09 00 00                      LEICA GR50           LEIAR20         LEIM

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001                        2002 03 18 23 59 59 ROGUE SNR-8000       AOAD/M_T        NONE
      PTBB 14234M001   2000 03 29 00 00 00  2002 03 19 00 00 00 ROGUE SNR-8000       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 23 59 59 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2002 03 19 00 00 00  2006 07 25 08 35 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 25 08 35 00  2006 11 13 13 15 00 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 07 26 00 00 00  2006 11 13 23 59 59 SEPT POLARX2         ASH700936E      SNOW
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2006 11 13 13 15 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW
      PTBB 14234M001   2006 11 14 00 00 00  2019 03 26 08 00 00 ASHTECH Z-XII3T      ASH700936E      SNOW

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT
      PTBB 14234M001   2019 03 26 14 00 00                      SEPT POLARX5TR       LEIAR25.R4      LEIT

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004                        2002 03 04 23 59 59 TRIMBLE 4000SSI      TRM29659.00     NONE
      SFER 13402M004   1995 12 18 00 00 00  1997 12 31 00 00 00 TRIMBLE 4000SSE      TRM22020.00+GP  NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2002 03 05 00 00 00  2005 11 27 23 59 59 TRIMBLE 4000SSE      TRM29659.00     NONE
      SFER 13402M004   2002 03 05 00 00 00  2005 11 28 00 00 00 TRIMBLE 4000SSE      TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2005 11 28 00 00 00  2014 01 30 11 39 59 TRIMBLE NETRS        TRM29659.00     NONE
      SFER 13402M004   2005 11 28 00 00 00  2008 05 20 09 35 00 TRIMBLE NETRS        TRM29659.00     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 29 59 LEICA GR25           LEIAR20         NONE
      SFER 13402M004   2014 01 30 11 40 00  2019 01 17 10 30 00 LEICA GR25           LEIAR20         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE
      SFER 13402M004   2019 01 17 11 00 00  2023 02 15 09 00 00 LEICA GR25           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE
      SFER 13402M004   2023 02 15 10 00 00                      LEICA GR30           LEIAR25         NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001                        2000 07 18 11 29 59 ROGUE SNR-8100       AOAD/M_T        NONE
      VILL 13406M001   1994 11 12 00 00 00  2000 07 18 11 30 00 ROGUE SNR-8100       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2000 07 18 11 30 00  2001 04 22 23 59 59 AOA SNR-8100 ACT     AOAD/M_T        NONE
      VILL 13406M001   2000 07 18 11 30 00  2001 04 23 00 00 00 AOA SNR-8100 ACT     AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 04 23 00 00 00  2004 12 02 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2001 05 29 00 00 00  2004 12 03 08 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2004 12 03 00 00 00  2005 01 18 23 59 59 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2004 12 03 08 00 00  2005 01 18 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 18 10 00 00  2008 09 25 11 00 00 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2005 01 19 00 00 00  2008 09 25 23 59 59 ASHTECH Z-XII3       AOAD/M_T        NONE
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2008 09 25 12 00 00  2012 12 27 10 00 00 ASHTECH UZ-12        AOAD/M_T        NONE
      VILL 13406M001   2008 09 26 00 00 00  2012 12 27 10 14 59 ASHTECH UZ-12        AOAD/M_T        NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE
      VILL 13406M001   2012 12 27 10 15 00  2020 01 07 12 00 00 SEPT POLARX4         SEPCHOKE_MC     NONE

 ### SR D_STACRX:chkType002: Overlapping intervals in TYPE 002, file: ${P}/EPNB23/STA/CODE_EPN.STA    
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE
      VILL 13406M001   2020 01 07 12 30 00                      SEPT POLARX5         SEPCHOKE_B3E6   NONE

 ### SR updmea: Observations from system GLONASS excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          LEIAT504        LEIS
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ACOR3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          LEIAT504        LEIS
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ACOR3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          LEIAR25         LEIT
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ARIS3510.CZO    

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._R_20233510000_01D_30S_MO.SMT
                Station name : GANP 11515M001
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM115000.00    TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/GJML3510.CZO    

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._R_20233510000_01D_30S_MO.SMT
                Station name : IENG 12724S001
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          STXSA1500       STXG
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/IGMI3510.CZO    

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._S_20233510000_01D_30S_MO.SMT
                Station name : KLOP 14214M002
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR updmea: Observations from system GLONASS excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM41249.00     TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/KNJA3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM41249.00     TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/KNJA3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM115000.00    TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/NPAZ3510.CZO    

 ### SR updmea: Observations from system GLONASS excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          AOAD/M_B        OSOD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ONSA3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          AOAD/M_B        OSOD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ONSA3510.CZO    

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._R_20233510000_01D_30S_MO.SMT
                Station name : PTBB 14234M001
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._R_20233510000_01D_30S_MO.SMT
                Station name : SFER 13402M004
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM115000.00    TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/SID03510.CZO    

 ### SR updmea: Observations from system GLONASS excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM41249.00     NONE
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/SUBO3510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM41249.00     NONE
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/SUBO3510.CZO    

 ### SR RXOCRX: Equipment or antenna pos. change found (type 002)
                Bernese obs. files will not be written.
                Sta info file: ${P}/EPNB23/STA/CODE_EPN.STA
                List of flags: all entries
                Rinex file   : ..._R_20233510000_01D_30S_MO.SMT
                Station name : VILL 13406M001
                First epoch  : 2023-12-17 00:00:00
                Last epoch   : 2023-12-17 23:59:30

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          AOAD/M_T        OSOD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/VIS03510.CZO    

 ### SR updmea: Observations from system GALILEO excluded because
                the receiver antenna method was declared as insufficient
                Antenna type:          TRM115000.00    TZGD
                Antenna calib. method: ADOPTED from GPS
                Filename:              ${P}/EPNB23/OBS/ZADA3510.CZO    



================================================================================
PART 1: RINEX PSEUDO-GRAPHICS
================================================================================

 DATE : 2023-12-17

 PHASE OBSERVATIONS
 BOTH FREQUENCIES

    1 |5555555555555553-                   -23321-                        -1345
    2 |***************1-                -25***93-                    -11*******
    3 |*********************-                     -27**62-                  -1*
    4 |   -1*******************91-                       -5******83-           
    5 |                  -28****************31-          -4***********4-       
    6 |       -19****************21           -4***********5-                  
    7 |            -16*******************2-                        -8******984-
    8 |*********2-             -2********1-                       -16**********
    9 |      -16********************4-                      -38**742-          
   10 |******3-                         -7*********821-          -2************
   11 |           -3***************41-         --4*************1-              
   12 |       -26**63--                -11*********************3-              
   13 |                   -15********************-                 -13****61-  
   14 |********721-         -19****************52-                         -6**
   15 |                        -28******************2-            -28********1-
   16 |2-            --5********4-                         -6******************
   17 |-3***************21-         -4**************2-                         
   18 |                        -3*******841-            -1*******************2-
   19 |   -19*************21-         -3**************9-                       
   20 |              -4*****************81-            -3*********5-           
   21 |**************-                  -369*71-                    --3********
   22 |*********941-          -28*****************4-                         -7
   23 |*7--                         -4************21-          -***************
   24 |7884--                     -15********************8-                 -13
   25 |         -13792-                    -13*********************1-          
   26 |            -27*******5-                        -28******************1- 
   27 |*****-                -138****2-                      -18***************
   28 |  --9**********61-                        -28****************31-        
   29 |                 -6****942-              -12********************5-      
   30 |-              -17********************1-                       -6****962
   31 |    -2************5-                         -27***************21-      
   32 |**********3-                         -29*************411-         -*****
  101 |      ---*******************5-                  --5*****31              
  102 |            -19*******************-                 16*****71           
  103 |                  -38*****************2-              -3*******4-       
  104 |1-                      -3****************2-            -3*********4-   
  105 |*****1                        -5**************1-           -7***********
  107 |*****************2-                      1**********51-           -9****
  108 | -13******************6-                    -1********6-             -1*
  109 |        -2*********5-                     -28*****************2-        
  111 |*2-           -*************6-                        -7*************81-
  112 |****41-           -***************3-                       -3***********
  113 |*****71-             -1****************2-                       -9******
  114 |-1******72-              -16******************5-                    -2**
  115 |   -15*****5-                 -18*******************4-                  
  116 |      -3*******4-                  -13*******************2-             
  117 |            -************61-          -4*************2-                 
  118 |                -7**********41-           -***************1-            
  119 |                    -7*******73-             -1***************3-        
  120 |***9-                    -3*****51-               -1*****************5- 
  121 |**********-                 -6******2-                -13***************
  122 |**************2-              -2*******4-                  -14**********
  124 |      -3**************21-          -4***********1-                      
  125 |333333333-                  -1222211-                  --223333333333333
  126 |  -                                           -122221-                -1
  202 |         -148****61-                          -149**********************
  203 |****81-                               -28**************711-           -2
  204 |             -13**************************6-                -26*********
  205 |-                             -25*******************511-          -2****
  207 |*******************71-                             -58****952-          
  208 |***********91-                               -5**********841-           
  209 |                     -169**********************6--             -4*******
  210 |         -27*****************621-           -********************51-    
  211 |             -16***************411-           -2**********************11
  212 |     -24*******************511-            1*****************6-         
  213 |***********3-                    -13******61-                          -
  214 |               --2111-                -1232344444444444444432-          
  215 |***1-                         -15****94-                       -26******
  218 |44445641                   -122453333-                                -1
  219 |      -128*************************2-                     --26***83-    
  221 |***711-          -3******************2-                               -5
  224 | -18*******62-                 -15**************************9-          
  225 |      -15****62-                       12**************************1-   
  226 |******************-                 128*********3-                      
  227 |-             -2*************72-                               -2*******
  230 |            -28********3-                              -24**************
  231 |*********831-            -14*************************4-                 
  233 |***********************3-             -2**************3-                
  234 |                          16*******82-                  -15*************
  236 |                    -5************31-              -3*******************
 -----+-----------------+-----------------+-----------------+-----------------+
      0                                  12                                  24


 NUMBER OF SATELLITES INCLUDED IN DATA FILES:    80

 DATE : 2023-12-17

 PHASE OBSERVATIONS
 BOTH FREQUENCIES

 SATELLITE SYSTEM: GPS    

 ACOR |99**99*******98999888*9899*99*************89*88999899*8****9*99*9******9
 ADAR |****99********99*8*******9****************9999***99********99**8*******9
 ARIS |****8999******99997******799*******9*****99889*888998*******99989****9*9
 BOR1 |889****9999*99999***999*999****************988988999****99*98*9*9****998
 BRST |99*989******9*89*9877**9999*9****99***9**997788998999988**9999989*****98
 BUDD |****9*******************89*****************899***89*********89********89
 CLIB |99******9****99*9*******98*****************979*9999*********89**9****998
 CTAB |*99*************9********8******************99*8999**********9*******998
 DEVA |8889**88999****89999*998*9*****9**********998889899989***9**8999*999*877
 DLF1 |*************************9*****************9*****99*********9**9********
 GANP |97*9**9*999***89999*9889*8****9****9****9*99889889989*9*99*88999*99***88
 GJML |8899*99**99***9*98***88**999999*********9*99788889989**99*9*9*88989**987
 GLSV |9**----999***9**99***9*****************88***8*888**9********98- -99***99
 GRAZ |999*****9************99**9*****************978989**9****9***9*9******988
 IENG |999******9*****9****99**9*9**9**************9998999**********99******88*
 IGEO |9*99****999*****99***999********************87898**99*****99***9*9****99
 IGMI |677778**99999988667888769*98778*999**9889989987788689998799**886789*9887
 JOZE |99****8***9***9899989988988**998**89****9997878988987**99978889999999*78
 KLOP |799*98*99****9898*9***99*8**9****99****9*98879*898889****89989989***7898
 KNJA |8899*****99**97*979*988898*99999**********99989889899**988**9998989*9887
 LROC |89**89**99***98998988**899**9****9********98898898779*99***999989***9899
 MATE |877898999*999*9999899898**99*9*9**9***9***78997788899*9999****9889***889
 MLVL |*9************99*9*******9*****************9*9**999********999*9******9*
 MOP2 |88998889997*87888999*989777****9*98****98897878778887**9999767*9**877678
 NPAZ |-888989***99-*8*989**8898899999*********8989988888989*-9899*99788-8-*-87
 ONSA |9***9***9*****899**99***999****************77****89*********89******9*89
 PENC |777778789999*977898998887799889989*9*98876977787878879*88987898878887877
 POTS |****************9*****9999******************88998999****98*889**9*****99
 PTBB |99*999**9***99989*8***99889*****9*********9879*998889******98998****9899
 RIGA |**899*8899***8787***9**878****9***9*****8778989*8799******8778*****97988
 SCIL |9*************9**99**************9********9*99****99***********9********
 SFER |99*9*9******9**9***8*99*******************9***989999999*******9********9
 SID0 |8899*****99***9*98***8999899999***********99789889989**99*9*9988889**987
 SUBO |8899*89*9*9*****98**989998999*9*********9*99789889989**9999*8988889**988
 TLSE |899*99******9**99*997**99*9**************8*999889989***9*9*9*9*89***988*
 VILL |99**9**99****9*979877878899899999*99**9*988788889879976798*889779**98889
 VIS0 |****9**********9***************************89****89********989********9*
 WTZR |999*9********99*9***9*9**89******9**********7998999*9***99*989*******998
 ZADA |988******99*****99***89*9*9****************9989889*9****9****9998****988
 ZIM2 |****************9999*99899*999***9*****9**9989989988****99*999999***99**
 -----+-----------------+-----------------+-----------------+-----------------+
      0                                  12                                  24

 SATELLITE SYSTEM: GLONASS

 ACOR |666676556656676667788887898887668776675667688866787677766665586776567757
 ADAR |867766676777778768879888999988898788856767779878787897887777968878866677
 ARIS |667756666876578666877788788878988788766565777788777867877776667778766677
 BOR1 |676555656677776687878778888666779887785677688778788876768787776777778666
 BRST |866766556566667667868878998787679777766557768877787776765666567677867776
 BUDD |67866666667877787887898888*888899888767766778888888778786778787878887777
 CLIB |777755666687787677888989888987888887787676788889888886777687797778878676
 CTAB |777775666787777887888989988987889987787677788879888886778887797777888777
 DEVA |555645556867766777878777676676778977876776678777787875667877777677767665
 DLF1 |877776667678777778879988989888898988777667779789888777786778788777877677
 GANP |776555556767776687887778887556778877786576687776887755667767786677776665
 GJML |665544444567765777688768886666677877776577678767787655566577875677688766
 GLSV |776-  -6687777777889877787667788899788756678777888887777888788-  6777776
 GRAZ |677745656777776887788888988866779*77786677688779888775668877886777788666
 IENG |877555555867776877788879988986789977786677688878888877667767777777787767
 IGEO |656555566667775778788776666676788987887777677777777876677877888677776555
 IGMI |666344444445665676677776776555666556665677677564777545555355565676665545
 JOZE |788655666567766657877768887566888977776566677769998866666768887788878777
 KLOP |544334544565667667878877788766768677666667778778788775667676766666556565
 KNJA |664545556577775677788677676666678977686567688776676644667656776666756555
 LROC |545444454546655667767777766566666666655566677776666433333445545655555445
 MATE |766544456677766887688887877765678977876777678876777655567777887777676655
 MLVL |876765667777778777879877989976779887777677789878778867787777778777777777
 MOP2 |665554654666756656775577777556776887767555566667877656666667777666764564
 NPAZ |-34333333444-43554666555435445566676544445666444555544-4433333444-5-4-43
 ONSA |677655667677777878888988789877888888767766778888789766777778787878887677
 PENC |454433445446755666668755566546666667755555668765666555554467745666665543
 POTS |88877777767778778788888888888998**99787677778889889877768898898888988788
 PTBB |677655654677777767877688887877887888765666778688887776766677767778876677
 RIGA |667655565676677677876877787977888878677446766788788776777776687668776566
 SCIL |8767766768777786678889899*8998899888886666788888887887888677878778876777
 SFER |88866765465556766669889*99*988788766766677768787887778766555558766777676
 SID0 |776544455577765777688769887766677777776577678766887755566577776677678766
 SUBO |654444456477775777688767666666677877785577678766677655567577676677556654
 TLSE |776655556766777677788878999876679887766677688877888756557676667777667767
 VILL |986655555555544556667778996776665666554667757667898775544665556777678668
 VIS0 |788667677678777788888988789878888898777667777988989789797788888878886777
 WTZR |777655655667776777878888988987888987787677678878888787767677787777878667
 ZADA |776655555767776877688879988886677*77786777678877888754567867786777677556
 ZIM2 |765455565667776677878978987766678987777676688776888645567777687777767667
 -----+-----------------+-----------------+-----------------+-----------------+
      0                                  12                                  24

 SATELLITE SYSTEM: GALILEO

 ACOR |877767777777666776667889897789967666555557678788889889998777776676767888
 ADAR |888877788888788898788*999999988778887777789888**9*******9*89777779888899
 ARIS |7878778788988777887886999988978878786766688788789*999**9*999878777877788
 BOR1 |8987767765455678789899778898767765457667877889*999***9888778877788889*98
 BRST |88876777877666667677799999998987777755556667889******99*9997776668667998
 BUDD |99788777978788798*9899988989897788788777889889**9******99897888998999999
 CLIB |9977777778767678*8999998888888776887666789789*********99888887788989*998
 CTAB |9997777768866788999*99*88998*8776787767789889*********99888988899899**99
 DEVA |8888665555565688877*887788776556555567788667889889*999677777998898789988
 DLF1 |9988877889888879**989*989999*887898877778*9899*********99*9*88899999999*
 GANP |888777755665678898899988878777765556667788779**9*99**8877777778989889*98
 GJML |888666555545555788899877788876555545555677689*9889*9*8777777977898879*97
 GLSV |878-  -6666778899899*989887778867678987888779**9**99*998877788-  9989**9
 GRAZ |99976677667557888*9*9978889887666676767788999**9******8877799899*899**99
 IENG |99886777776556669*899888899*87877776555669989********9988789877778*99999
 IGEO |655554333336565565655666665456555555656666556566566656555555445566666565
 IGMI |786556665544455566778887777666655543445556776898898878777776566667778778
 JOZE |98987755554656786789888787767677655676677678999*9****9788887879998788988
 KLOP |8877777664457666568888888888777765666655568888*99**99*998777777767788898
 KNJA |444444544333333224445544433332233333333454445445655455546665444354455455
 LROC |222122333331111123222222211111122333323444432233222322233433332444443222
 MATE |778666555555455689788888777676655664445677876898999978877788766888878878
 MLVL |988778878887767688889898999889878878666688888988988989989889877778898999
 MOP2 |666787665465677877887787766577666456666777777779988878788777778896788777
 NPAZ |-89765555555-56788*99887788786555556555677789*9999*998-7777797778-8-9-98
 ONSA |99787777776678788998989988897877777776677898898*******99989788799*999998
 PENC |                                                                        
 POTS |**98988778777788**9999988998**88887897778*89*************98997999889**99
 PTBB |88787776667676778798999888988876666767677778898*99*89*988777878987798898
 RIGA |443443444434434434344333444434434443443444334433343444444443343443434433
 SCIL |888877888998879987788989999**98979977677887888*9*********9*987788*88889*
 SFER |87777779887766777768889*99999999**775556676778899**99**9**99776677788889
 SID0 |888766555554556787899877887876555555555677688*9899*9*877777797788887**98
 SUBO |655455554333333554555565554332344443335554557658886755677755557665565767
 TLSE |*998788868656666899**888899*88898*76555669*99***************777667*99999
 VILL |8888776656555666566678889888877764455555667789**9*******9877776667567888
 VIS0 |989888788889888999*9999988998788787788778889899**9***999889799999*989*89
 WTZR |997778876665677878989978899877788667666778789978898898899778878988888999
 ZADA |999766775555566779*99888889897666566556777988**99****99877789778888***98
 ZIM2 |9987677765445666798899788898988766666666698888*89***99989878877768889999
 -----+-----------------+-----------------+-----------------+-----------------+
      0                                  12                                  24

 ANTI-SPOOFING :

  202 |          11477752                            112378********************
  203 |***981                                 188**9********995311           15
  204 |             12369************************92                2367999***98
  205 |                               2389****************85111           6****
  207 |*****************9851                               135788631           
  208 |**********982                                 379899***985221           
  209 |                     123588*******************981              267******
  210 |          17899**************6321           35*****************8751     
  211 |               589***********975221           138******************98531
  212 |      2577*****************8211            59**************8862         
  213 |**********832                      14666663                            1
  214 |                                         132             111            
  215 |97532                           145664                        123479****
  218 |  222222                      1221 111                                  
  219 |     111489***********************952                       122243      
  220 |          122222 111   11                                               
  221 |***7311           4*****************82                                 3
  224 |   4788888742                  126**************************92          
  225 |        144443                       112479************************51   
  226 |******************2                 146799***9753                       
  227 |2             2569**********961                                 28999***
  230 |            136788988752                                 68*************
  231 |*******984221            116**********************87552                 
  233 |8********************9932             1458*********9854                 
  234 |                           36999988531                  125*************
  236 |                     5899******985321             1179******************
 -----+-----------------+-----------------+-----------------+-----------------+
      0                                  12                                  24



================================================================================
PART 2: ORBIT GENERATION SUMMARY
================================================================================

 NTUA_DDP_20233510: Generate GNSS standard orbit                  22-MAY-26 23:49
 TIME FROM DAY : 0 GPS WEEK: 2293
      TO   DAY : 1 GPS WEEK: 2293
 -------------------------------------------------------------------------------
 ORBIT REPEATABILITY FROM A 1-DAY FIT THROUGH DAILY ORBIT SOLUTIONS (MM)
 # ECLIPSING SATELLITES:   7 E /   0 M (  0 EM)
 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ECL  ..  ..  E.  ..  E.  ..  ..  ..  ..  E.  ..  ..  ..  ..  ..  ..  ..  ..  ..  E.  ..  ..  E.  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  E.  ..  E.  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..
 DOY   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32 101 102 103 104 105 107 108 109 111 112 113 114 115 116 117 118 119 120 121 122 124 125 126 202 203 204 205 207 208 209 210 211 212 213 214 215 218 219 221 224 225 226 227 230 231 233 234 236
 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 351   8   8  13  10  13   9  10  11   9  12   8  12  12   8  11  13  11  11  12  12   8   9  11   9  11  12  11   9   9   9   8  10  10  11  13  12   8  13  13   8  13  11   7  10  14  12   9   7  10  11   7   6  11   7  13  11  12  14  10  12  14  12  10  10   9  11  12  11  10  13  10  14  12  11  14  15  14  11  10  11
 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ALL   8   8  13  10  13   9  10  11   9  12   8  12  12   8  11  13  11  11  12  12   8   9  11   9  11  12  11   9   9   9   8  10  10  11  13  12   8  13  13   8  13  11   7  10  14  12   9   7  10  11   7   6  11   7  13  11  12  14  10  12  14  12  10  10   9  11  12  11  10  13  10  14  12  11  14  15  14  11  10  11
 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


================================================================================
PART 3: SINGLE-POINT-POSITIONING SUMMARY
================================================================================


 ===============================================================================
 Bernese GNSS Software, Version 5.4
 -------------------------------------------------------------------------------
 Program        : CODXTR
 Purpose        : Extract CODSPP program output
 -------------------------------------------------------------------------------
 Campaign       : ${P}/EPNB23
 Default session: 3510 year 2023
 Date           : 22-May-2026 23:56:55
 User name      : bpe54
 ===============================================================================


 NTUA_DDP_20233510: Extraction from CODSPP
 -------------------------------------------------------------------------------


 INPUT AND OUTPUT FILENAMES
 --------------------------

 -------------------------------------------------------------------------------
 List of good files              :  ---
 List of bad files               :  ---
 Program output                  : ${P}/EPNB23/OUT/SPP_20233510.OUT
 Error message                   : ${U}/WORK/ERROR.MSG
 Session table                   : ${P}/EPNB23/GEN/SESSIONS.SES
 -------------------------------------------------------------------------------


 -------------------------------------------------------------------------------
 File   Input files                      
 -------------------------------------------------------------------------------
    1   ...NB23/OUT/SPP_20233510_001.OUT 
    2   ...NB23/OUT/SPP_20233510_002.OUT 
    3   ...NB23/OUT/SPP_20233510_003.OUT 
    4   ...NB23/OUT/SPP_20233510_004.OUT 
    5   ...NB23/OUT/SPP_20233510_005.OUT 
 -------------------------------------------------------------------------------



  34 FILES, MAX. RMS:    1.42 M    FOR STATION: IGMI 12701M003  
            MAX. BAD:    5.06 %    FOR STATION: SCIL 19201M001  
            MAX. OFF:   -0.26 MSEC FOR STATION: JOZE 12204M001  


-----------------------------------------------------------------
>>> CPU/Real time for pgm "CODXTR": 0:00:00.020 / 0:00:00.020
>>> Program finished successfully



================================================================================
PART 4: PREPROCESS PHASE OBSERVATIONS
================================================================================

 SUMMARY OF THE MAUPRP OUTPUT FILE 
 *********************************

 SESS FIL OK?  ST1  ST2 L(KM)   #OBS.    RMS    DX     DY     DZ    #SL   #DL   #MA  MAXL3      MIN. SLIP
 --------------------------------------------------------------------------------------------------------
 3510   1 OK   ACOR BRST  634   23661     14    215    -35    238    38   741    51     50             11
 3510   2 OK   ADAR ARIS  464   45938     15    298    -42    435    18  1690   146     46             11
 3510   3 OK   ADAR SCIL  338   70390     13   -278    -23   -477    16  2088   172     50             11
 3510   4 OK   BOR1 CLIB  218   68142     13    -77    -23   -111    21  1252   167     49             11
 3510   5 OK   BOR1 JOZE  271   63695     12     61     62    106     4   799   131     51             12
 3510   6 OK   BRST LROC  350   46689     22   -244     -4   -238    63  1918   166     50             11
 3510   7 OK   BRST SCIL  215   67005     12     68      7     74    18   810   128     49             12
 3510   8 OK   BUDD ONSA  188   27832     11    -71    -64     77     3   568    84     13             12
 3510   9 OK   BUDD POTS  376   71223     13   -152   -122   -446     3  1166   188     34             11
 3510  10 OK   CLIB CTAB  154   71684     12     68     -7     27    21   977   177     43             12
 3510  11 OK   CLIB POTS  226   70763     12    -50    -21    -28    15  1217   204     49             11
 3510  12 OK   CTAB MOP2  222   62207     13     58     30     30     6  1196   158     34             11
 3510  13 OK   CTAB WTZR  134   70578     14    -24     -9    -20    19   912   166     43             11
 3510  14 OK   DEVA IGEO  473   58035     14   -102      1    -20    42   796   147     44             12
 3510  15 OK   DEVA SUBO  253   23395     12    -35     21    -33    17   225    74     42             13
 3510  16 OK   DLF1 MLVL  372   70290     10     21    -26    -19     9   961   122     31             12
 3510  17 OK   GJML NPAZ   98   36893     13    -52    -18    -58    21  1119   101     24             11
 3510  18 OK   GJML SID0  157   43992     13     77     18     95     6   310    94     38             22
 3510  19 OK   GLSV IGEO  390   56616     13     65     43    -17    50   650   150     50             11
 3510  20 OK   GRAZ MOP2  197   61153     12      7      7     50     5   970   143     31             12
 3510  21 OK   GRAZ ZADA  329   45722     13   -289   -164   -383     3   625    91     30             12
 3510  22 OK   IGMI ZADA  324   38467     14     39     55     64    40   696    99     50             11
 3510  23 OK   IGMI ZIM2  451   37280     15    163     96    218    40  1152   109     49             11
 3510  24 OK   KNJA NPAZ  149   23341     12    -88     -4    -69     6   348    53     44             11
 3510  25 OK   LROC MLVL  414   48369     21    336     69    371    74  1855   168     50             11
 3510  26 OK   LROC TLSE  359   47879     22    152     48    158    50  1956   163     50             11
 3510  27 OK   MATE ZADA  403   42550     13    -87    -39    -37    35   951   130     47             11
 3510  28 OK   MLVL ZIM2  425   65988     14     14     30    -24    32  2108   164     46             11
 3510  29 OK   MOP2 PENC  163   36458     14     -4    -23    -43     7  1063   114     40             14
 3510  30 OK   ONSA VIS0  387   27510     12   -286    -77   -389     8   490    79     44             12
 3510  31 OK   PENC SUBO  190   21480     13     19     52    -22     6   469    65     28             25
 3510  32 OK   RIGA VIS0  352   45871     14     81     36    159    63   954   133     49             11
 3510  33 OK   SID0 SUBO  113   25007     12     74     17    109     4   164    47     39             20
 --------------------------------------------------------------------------------------------------------
 Tot:  33                 297   71684     22   -278    -23   -477    74  2108   204     51             11



================================================================================
PART 5: DATA PREPROCESSING/SCREENING SUMMARY
================================================================================


 ===============================================================================
 Bernese GNSS Software, Version 5.4
 -------------------------------------------------------------------------------
 Program        : RESCHK
 Purpose        : Detect misbehaving stations/satellites
 -------------------------------------------------------------------------------
 Campaign       : ${P}/EPNB23
 Default session: 3510 year 2023
 Date           : 23-May-2026 00:02:55
 User name      : bpe54
 ===============================================================================


 NTUA_DDP_20233510: Check residual statistics for bad stations
 -------------------------------------------------------------------------------


 INPUT AND OUTPUT FILENAMES
 --------------------------

 -------------------------------------------------------------------------------
 Satellite problems              : ${CONFIG}/SAT_2023.CRX
 Abbreviation table              : ${P}/EPNB23/STA/EPNB23.ABB
 Files deletion list             : ${P}/EPNB23/OUT/CHK_20233510.DEL
 Short summary                   : ${P}/EPNB23/OUT/CHK_20233510.SUM
 Program output                  : ${P}/EPNB23/OUT/CHK_20233510.OUT
 Error message                   : ${U}/WORK/ERROR.MSG
 Session table                   : ${P}/EPNB23/GEN/SESSIONS.SES
 -------------------------------------------------------------------------------



RESRMS SUMMARY FILE NAME:  ${P}/EPNB23/OUT/RES_20233510.SUM


NO SPECIAL EVENTS FOUND IN THIS SOLUTION



-----------------------------------------------------------------
>>> CPU/Real time for pgm "RESCHK": 0:00:00.006 / 0:00:00.006
>>> Program finished successfully

--------------------------------------------------------------------------------
PRN | % Observations   Difference   | # Observations   Difference   | RMS       
    | before   after   abs      rel | before    after  abs      rel | bef    aft
----+-------------------------------+-------------------------------+-----------
  2 |   1.60    1.59   -0.00  -0.27 |   4479    4416     -63  -1.41 |  1.6   1.4
  3 |   1.53    1.54    0.01   0.73 |   4304    4286     -18  -0.42 |  1.4   1.3
  4 |   1.62    1.62    0.01   0.42 |   4540    4507     -33  -0.73 |  1.5   1.3
  5 |   1.90    1.90    0.01   0.49 |   5320    5285     -35  -0.66 |  1.6   1.4
  6 |   1.89    1.91    0.01   0.60 |   5317    5288     -29  -0.55 |  1.5   1.4
  7 |   1.70    1.71    0.01   0.44 |   4779    4745     -34  -0.71 |  1.4   1.3
  8 |   1.69    1.69    0.00   0.28 |   4736    4695     -41  -0.87 |  1.5   1.5
  9 |   1.55    1.55    0.00   0.29 |   4345    4308     -37  -0.85 |  1.5   1.3
 10 |   1.81    1.82    0.01   0.38 |   5092    5053     -39  -0.77 |  1.5   1.4
 11 |   1.92    1.93    0.01   0.65 |   5386    5359     -27  -0.50 |  1.5   1.4
 12 |   1.53    1.54    0.00   0.24 |   4305    4266     -39  -0.91 |  1.5   1.4
 13 |   1.50    1.50    0.01   0.36 |   4204    4171     -33  -0.78 |  1.5   1.3
 14 |   1.75    1.74   -0.01  -0.45 |   4916    4838     -78  -1.59 |  1.6   1.4
 15 |   1.72    1.73    0.01   0.53 |   4829    4799     -30  -0.62 |  1.6   1.4
 16 |   1.72    1.74    0.02   0.88 |   4831    4818     -13  -0.27 |  1.4   1.3
 17 |   1.94    1.95    0.00   0.17 |   5454    5401     -53  -0.97 |  1.5   1.4
 18 |   1.66    1.67    0.01   0.37 |   4664    4628     -36  -0.77 |  1.5   1.4
 19 |   1.87    1.89    0.01   0.60 |   5263    5234     -29  -0.55 |  1.5   1.4
 20 |   1.77    1.78    0.02   0.85 |   4965    4950     -15  -0.30 |  1.5   1.4
 21 |   1.57    1.57    0.01   0.33 |   4395    4359     -36  -0.82 |  1.4   1.3
 22 |   1.70    1.70   -0.00  -0.26 |   4785    4718     -67  -1.40 |  1.5   1.4
 23 |   1.88    1.88   -0.00  -0.26 |   5291    5217     -74  -1.40 |  1.6   1.4
 24 |   1.45    1.44   -0.01  -0.85 |   4080    3999     -81  -1.99 |  1.6   1.4
 25 |   1.51    1.50   -0.01  -0.70 |   4247    4169     -78  -1.84 |  1.6   1.5
 26 |   1.70    1.71    0.02   0.90 |   4761    4749     -12  -0.25 |  1.4   1.3
 27 |   1.55    1.55    0.01   0.53 |   4337    4310     -27  -0.62 |  1.4   1.3
 28 |   1.85    1.87    0.02   0.96 |   5205    5195     -10  -0.19 |  1.4   1.4
 29 |   1.57    1.57   -0.00  -0.20 |   4418    4359     -59  -1.34 |  1.5   1.4
 30 |   1.59    1.60    0.01   0.34 |   4471    4435     -36  -0.81 |  1.5   1.4
 31 |   1.90    1.91    0.02   0.83 |   5328    5311     -17  -0.32 |  1.4   1.4
 32 |   1.96    1.97    0.01   0.62 |   5495    5466     -29  -0.53 |  1.5   1.4
101 |   1.17    1.14   -0.03  -2.55 |   3280    3160    -120  -3.66 |  1.8   1.4
102 |   1.30    1.29   -0.00  -0.21 |   3638    3589     -49  -1.35 |  1.6   1.4
103 |   1.28    1.24   -0.04  -2.95 |   3595    3449    -146  -4.06 |  1.8   1.4
104 |   1.27    1.28    0.01   0.90 |   3568    3559      -9  -0.25 |  1.6   1.5
105 |   1.62    1.63    0.01   0.58 |   4558    4532     -26  -0.57 |  1.5   1.4
107 |   1.62    1.61   -0.01  -0.89 |   4561    4469     -92  -2.02 |  1.6   1.4
108 |   1.28    1.28    0.00   0.06 |   3593    3554     -39  -1.09 |  1.6   1.4
109 |   1.45    1.43   -0.02  -1.20 |   4073    3978     -95  -2.33 |  1.6   1.4
111 |   1.53    1.52   -0.01  -0.40 |   4281    4215     -66  -1.54 |  1.6   1.4
112 |   1.64    1.64    0.00   0.01 |   4595    4543     -52  -1.13 |  1.6   1.4
113 |   1.20    1.21    0.01   0.43 |   3368    3344     -24  -0.71 |  1.6   1.5
114 |   1.31    1.29   -0.02  -1.82 |   3678    3570    -108  -2.94 |  1.7   1.4
115 |   1.29    1.27   -0.02  -1.56 |   3619    3522     -97  -2.68 |  1.7   1.4
116 |   1.40    1.37   -0.03  -2.19 |   3932    3802    -130  -3.31 |  1.7   1.4
117 |   1.33    1.31   -0.02  -1.77 |   3738    3630    -108  -2.89 |  1.7   1.4
118 |   1.36    1.35   -0.01  -0.65 |   3809    3741     -68  -1.79 |  1.6   1.4
119 |   0.96    0.95   -0.01  -0.68 |   2696    2647     -49  -1.82 |  1.7   1.6
120 |   1.11    1.12    0.01   0.54 |   3129    3110     -19  -0.61 |  1.6   1.5
121 |   1.63    1.63    0.00   0.00 |   4569    4517     -52  -1.14 |  1.5   1.4
122 |   1.66    1.65   -0.01  -0.47 |   4658    4583     -75  -1.61 |  1.6   1.4
124 |   1.31    1.31    0.00   0.06 |   3689    3649     -40  -1.08 |  1.5   1.4
202 |   0.80    0.80    0.01   0.88 |   2232    2226      -6  -0.27 |  1.4   1.4
203 |   0.55    0.55   -0.00  -0.09 |   1542    1523     -19  -1.23 |  1.6   1.4
204 |   1.14    1.14    0.01   0.58 |   3189    3171     -18  -0.56 |  1.5   1.3
205 |   0.70    0.70   -0.01  -1.05 |   1977    1934     -43  -2.18 |  1.8   1.5
207 |   0.74    0.74    0.00   0.52 |   2075    2062     -13  -0.63 |  1.6   1.4
208 |   0.61    0.61    0.01   0.86 |   1705    1700      -5  -0.29 |  1.6   1.4
209 |   0.97    0.97   -0.00  -0.48 |   2722    2678     -44  -1.62 |  1.7   1.4
210 |   1.03    1.04    0.00   0.32 |   2898    2874     -24  -0.83 |  1.6   1.4
211 |   1.07    1.08    0.01   0.58 |   3011    2994     -17  -0.56 |  1.6   1.4
212 |   1.11    1.10   -0.01  -0.51 |   3106    3055     -51  -1.64 |  1.6   1.4
213 |   0.39    0.40    0.00   0.15 |   1108    1097     -11  -0.99 |  1.6   1.4
214 |   0.01    0.01    0.00   1.15 |     31      31       0   0.00 |  1.1   1.1
215 |   0.22    0.23    0.00   0.51 |    630     626      -4  -0.63 |  1.7   1.4
218 |   0.01    0.01    0.00   1.15 |     25      25       0   0.00 |  0.9   0.9
219 |   0.80    0.79   -0.01  -1.27 |   2251    2197     -54  -2.40 |  1.7   1.4
221 |   0.61    0.60   -0.01  -1.95 |   1724    1671     -53  -3.07 |  1.7   1.4
224 |   1.03    1.03    0.00   0.21 |   2883    2856     -27  -0.94 |  1.6   1.3
225 |   0.86    0.86    0.00   0.32 |   2417    2397     -20  -0.83 |  1.6   1.4
226 |   0.87    0.87    0.00   0.29 |   2448    2427     -21  -0.86 |  1.6   1.4
227 |   0.60    0.61    0.00   0.74 |   1690    1683      -7  -0.41 |  1.6   1.4
230 |   0.71    0.72    0.01   0.90 |   2007    2002      -5  -0.25 |  1.5   1.4
231 |   1.06    1.06    0.00   0.34 |   2974    2950     -24  -0.81 |  1.6   1.4
233 |   1.02    1.02    0.00   0.27 |   2860    2835     -25  -0.87 |  1.6   1.4
234 |   0.55    0.56    0.00   0.44 |   1556    1545     -11  -0.71 |  1.6   1.4
236 |   0.88    0.88   -0.00  -0.11 |   2478    2447     -31  -1.25 |  1.6   1.4
----+-------------------------------+-------------------------------+-----------
TOT | 100.00  100.00    0.00   0.00 | 280708  277503   -3205  -1.14 |  1.6   1.4
--------------------------------------------------------------------------------

 BASELINE  SESS     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32   101   102   103   104   105   107   108   109   111   112   113   114   115   116   117   118   119   120   121   122   124   202   203   204   205   207   208   209   210   211   212   213   214   215   218   219   221   224   225   226   227   230   231   233   234   236   TOT
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ACOR-BRST 3510   1.0   1.0   0.9   1.4   1.1   1.3   0.9   1.1   1.2   1.2   1.4   1.6   1.5   1.4   0.9   1.2   1.2   1.3   1.3   1.0   1.4   1.4   1.4   1.2   1.1   0.9   1.0   0.9   1.4   1.0   1.0                                                                                                                                                                                                                                                                                       1.2
 ADAR-ARIS 3510   1.7   1.6   1.6   1.7   1.7   1.5   1.7   1.6   1.6   1.6   1.6   1.6   1.6   1.6   1.6   1.7   1.7   1.7   1.6   1.5   1.5   1.7   1.5   1.6   1.7   1.6   1.7   1.6   2.3   1.6   1.8   1.7   1.5   1.6   1.5   1.5   1.8   1.7   1.8   1.7   1.5   1.6   1.7   1.5   1.6   1.7   1.6   1.9   1.5   1.7   1.5   1.6                                                                                                                                                         1.6
 ADAR-SCIL 3510   1.3   1.3   1.4   1.5   1.4   1.2   1.5   1.5   1.4   1.3   1.4   1.2   1.5   1.4   1.7   1.3   1.5   1.3   1.3   1.3   1.4   1.4   1.4   1.4   1.4   1.4   1.5   1.5   1.6   1.4   1.4   1.5   1.3   1.5   1.2   1.4   1.4   1.3   1.4   1.7   1.4   1.3   1.3   1.4   1.6   1.4   1.5   1.7   1.5   1.4   1.3   1.2   1.5   1.3   1.3   1.6   1.5   1.4   1.4   1.5   1.4   1.3   1.3         1.2         1.2   1.2   1.3   1.4   1.4   1.5   1.3   1.4   1.3   1.4   1.3   1.4
 BOR1-CLIB 3510   1.3   1.1   1.1   1.5   1.3   1.2   1.4   1.3   1.2   1.2   1.3   1.3   1.3   1.4   1.4   1.2   1.4   1.2   1.2   1.2   1.3   1.4   1.3   1.5   1.2   1.3   1.3   1.4   1.2   1.3   1.3   1.4   1.4   1.4   1.4   1.4   1.3   1.2   1.3   1.5   1.3   1.3   1.3   1.4   1.2   1.2   1.4   1.4   1.4   1.3   1.3   1.2   1.3   1.3   1.2   1.5   1.2   1.3   1.3   1.3   1.3   1.2   1.3         1.3         1.2   1.2   1.3   1.5   1.3   1.2   1.5   1.3   1.2   1.4   1.3   1.3
 BOR1-JOZE 3510   1.1   1.0   0.9   1.2   1.2   0.9   1.1   1.0   1.2   1.1   1.3   1.1   1.2   1.2   1.2   1.1   1.1   1.2   1.1   1.1   1.1   1.2   1.4   1.4   1.0   1.1   1.2   1.3   1.0   1.1   1.3   1.0   1.1   1.2   1.2   1.2   1.1   1.0   1.1   1.1   1.1   1.3   1.3   1.4   1.3   1.1   1.2   1.2   1.2   1.2   1.1   1.2   1.0   1.2   1.1   1.3   1.0   1.1   1.3   1.1   1.1   1.1   1.1   1.1   1.1   0.9   0.9   1.0   1.2   1.3   1.2   1.1   1.0   1.2   1.1   1.1   1.1   1.1
 BRST-LROC 3510   1.2   1.1   1.1   1.2   1.0   1.1   1.1   0.9   1.2   1.1   1.3   1.1   1.2   1.2   1.1   1.1   1.2   1.2   1.0   1.1   1.2   1.3   1.3   1.2   1.0   1.1   1.1   1.0   1.1   1.1   1.2   1.0   1.0   1.2   1.3   1.3   1.1   0.9   1.1   1.1   1.2   1.3   1.1   1.1   1.1   1.1   1.0         1.5   1.1   1.1   1.1   1.2   0.7   1.1   1.5   1.1         1.3   1.0         1.2   1.2                                 1.1   1.1   1.2         1.1   1.3   1.0   1.0   1.2   1.1
 BRST-SCIL 3510   1.4   1.2   1.3   1.3   1.2   1.2   1.3   1.2   1.5   1.2   1.3   1.2   1.5   1.3   1.3   1.3   1.5   1.3   1.2   1.3   1.4   1.4   1.2   1.5   1.3   1.5   1.3   1.3   1.2   1.3   1.3   1.3   1.2   1.3   1.4   1.3   1.4   1.3   1.3   1.6   1.4   1.4   1.2   1.5   1.3   1.2   1.3   1.7   1.6   1.3   1.3   1.3   1.2   1.4   1.2   1.4   1.3   1.4   1.4   1.2   1.3   1.3   1.4         1.3         1.2   1.2   1.3   1.3   1.3   1.4   1.3   1.3   1.3   1.4   1.3   1.3
 BUDD-ONSA 3510   0.9   0.8   1.1   1.0   1.1   0.9   1.0   1.1   0.9   1.1   1.0   1.1   0.9   1.0   0.9   0.9   1.2   0.9   1.0   0.9   0.9   0.8   0.9   1.0   0.9   0.8   0.9   0.9   0.9   0.9   1.0                                                                                                                                                                                                                                                                                       1.0
 BUDD-POTS 3510   3.2   2.7   2.4   2.8   2.6   2.4   2.4   2.6   3.2   2.7   2.8   2.9   3.6   2.9   2.2   3.1   2.4   3.0   2.5   3.1   3.6   3.4   3.9   2.6   2.2   2.5   2.4   3.1   3.1   2.3   2.4   4.2   2.6   4.0   2.7   2.9   3.3   3.0   3.4   3.0   2.9   2.9   3.8   4.0   3.4   3.9   2.9   2.7   2.6   2.7   3.0   3.0   2.2   2.6   2.8   3.3   2.7   2.6   2.9   2.3   2.5   2.5   2.8         2.9         2.4   2.8   2.9   2.2   2.8   2.6   2.1   2.8   2.7   2.1   2.4   2.9
 CLIB-CTAB 3510   1.6   1.4   1.3   1.8   1.4   1.5   1.8   1.5   1.6   1.4   1.4   1.6   1.8   1.7   1.4   1.5   1.6   1.4   1.4   1.5   1.6   1.8   1.5   1.6   1.3   1.6   1.4   1.5   1.7   1.3   1.5   1.4   1.5   1.6   1.8   1.6   1.4   1.3   1.3   1.6   1.7   1.4   1.5   1.4   1.6   1.4   1.4   1.5   1.5   1.5   1.5   1.4   1.3   1.3   1.4   1.6   1.4   1.3   1.6   1.4   1.4   1.4   1.4         1.4         1.4   1.4   1.4   1.2   1.5   1.4   1.4   1.4   1.4   1.5   1.5   1.5
 CLIB-POTS 3510   2.4   2.4   2.9   2.6   2.5   2.7   2.5   3.2   2.4   2.9   2.4   2.9   2.9   2.6   2.1   2.7   2.7   2.7   2.4   2.4   2.8   2.6   2.7   3.3   2.1   2.1   2.3   3.2   2.5   2.3   2.5   3.4   3.5   3.8   2.3   2.4   3.3   3.2   3.2   2.6   2.6   2.6   3.9   3.5   3.9   3.3   3.1   3.2   2.5   2.9   3.0   3.0   2.0   2.5   2.3   3.0   2.4   2.3   2.9   2.5   2.2   2.8   2.3         2.3         3.3   3.2   2.6   2.0   2.5   2.4   2.1   2.5   2.6   2.4   2.8   2.8
 CTAB-MOP2 3510   2.1   1.6   2.0   1.9   2.1   1.8   2.0   2.1   1.8   1.8   1.8   2.0   2.0   1.7   1.8   1.9   1.6   1.8   1.9   1.9   1.6   1.9   2.3   2.3   1.7   1.8   1.7   1.6   2.1   1.8   1.8   2.3   1.9   1.7   1.6   1.6   1.7   1.6   1.5   1.7   2.2   1.6   1.6   1.7   1.9   1.8   2.1   1.7   1.7   1.7   1.9   1.6   1.5   1.6   1.7   1.8   1.5   1.6   1.7   1.8   1.8   1.9   1.5         1.7         1.9   2.1   1.6   2.0   1.5   2.0   1.9   1.6   1.5   1.8   1.7   1.8
 CTAB-WTZR 3510   1.8   1.5   1.3   1.6   1.4   1.4   1.7   1.6   1.6   1.5   1.5   1.5   1.6   1.6   1.4   1.5   1.6   1.4   1.5   1.7   1.5   1.7   1.5   1.6   1.3   1.6   1.5   1.5   1.5   1.4   1.5   1.5   1.5   1.5   1.6   1.5   1.4   1.4   1.4   1.6   1.7   1.4   1.4   1.4   1.5   1.4   1.5   1.6   1.6   1.5   1.6   1.3   1.4   1.4   1.3   1.6   1.4   1.4   1.5   1.4   1.4   1.4   1.5         1.3         1.5   1.4   1.3   1.6   1.4   1.5   1.3   1.4   1.4   1.5   1.5   1.5
 DEVA-IGEO 3510   1.3   1.3   1.2   1.3   1.3   1.3   1.4   1.4   1.2   1.3   1.5   1.2   1.2   1.3   1.3   1.2   1.2   1.1   1.4   1.1   1.2   1.2   1.2   1.2   1.3   1.2   1.2   1.3   1.3   1.3   1.2   1.3   1.1   1.3   1.4   1.1   1.1   1.3   1.2   1.2   1.2   1.3   1.2   1.1   1.1   1.2   1.2   1.3   1.3   1.1   1.2   1.2   1.2   1.1   1.2   1.2   1.1   1.2   1.2         1.2   1.2                           1.2   1.3   1.2   1.3   1.1   1.2   1.1   1.2                     1.2
 DEVA-SUBO 3510   1.5   1.4   1.6   1.6   1.5   1.4   1.6   1.5   1.3   1.4   1.4   1.4   1.3   1.4   1.4   1.3   1.2   1.4   1.6   1.3   1.3   1.3   1.5   1.5   1.4   1.2   1.3   1.5   1.5   1.4   1.4                                                                                                                                                                                                                                                                                       1.4
 DLF1-MLVL 3510   1.3   1.3   1.1   1.3   1.2   1.2   1.2   1.1   1.3   1.1   1.0   1.2   1.3   1.3   1.2   1.1   1.3   1.2   1.1   1.2   1.1   1.3   1.2   1.3   1.1   1.2   1.1   1.2   1.1   1.1   1.2   1.2   1.2   1.2   1.3   1.1   1.2   1.1   1.2   1.3   1.2   1.2   1.1   1.1   1.1   1.1   1.2   1.3   1.3   1.2   1.1   1.2   1.0   1.2   1.1   1.2   1.1   1.1   1.2   1.1   1.1   1.2   1.2   0.8   1.1   0.8   1.1   1.1   1.1   1.1   1.2   1.1   1.1   1.1   1.2   1.3   1.1   1.2
 GJML-NPAZ 3510   1.3   1.2   1.2   1.3   1.3   1.3   1.3   1.2   1.2   1.3   1.4   1.2   1.4   1.4   1.3   1.3   1.2   1.3   1.4   1.3   1.2   1.4   1.3   1.3   1.2   1.3   1.2   1.3   1.3   1.2   1.3   1.3   1.2   1.2   1.4   1.2   1.1   1.1   1.2   1.3   1.4   1.4   1.3   1.2   1.2   1.3   1.4   1.2   1.1   1.1   1.3   1.3                                                                                                                                                         1.3
 GJML-SID0 3510   1.8   1.7   1.8   1.7   1.7   1.8   1.9   1.6   1.6   1.7   2.2   1.7   1.7   2.0   1.7   1.6   1.8   1.7   1.9   1.6   1.8   1.8   1.6   1.9   1.6   1.5   1.6   1.7   1.8   1.6   1.7   1.7   1.7   1.7   1.8   1.6   1.5   1.9   1.7   1.7   1.8   1.9   1.8   1.7   1.7   1.6   1.7   1.8   1.7   1.6   1.8   1.7                                                                                                                                                         1.7
 GLSV-IGEO 3510   1.6   1.3   1.3   1.4   1.5   1.3   1.5   1.3   1.5   1.3   1.6   1.6   1.5   1.6   1.3   1.4   1.2   1.2   1.4   1.5   1.5   1.4   1.4   1.4   1.2   1.4   1.4   1.6   1.4   1.3   1.3   1.6   1.2   1.6   1.6   1.3   1.3   1.2   1.3   1.4   1.4   1.8   1.6   1.4   1.2   1.2   1.2   1.7   1.6   1.3   1.5   1.3   1.4   1.3   1.4   1.4   1.4   1.2   1.5         1.3   1.2                           1.3   1.4   1.3   1.4   1.4   1.3   1.2   1.4                     1.4
 GRAZ-MOP2 3510   2.1   1.6   1.9   1.7   1.9   1.6   1.8   1.9   1.6   1.6   1.5   1.6   1.6   1.5   1.7   2.5   1.5   2.0   1.6   1.8   1.4   1.7   2.1   2.2   1.6   1.8   1.7   1.7   1.7   1.7   1.8   2.0   1.6   1.5   1.6   1.5   1.7   1.6   1.6   1.6   1.9   1.4   1.4   1.7   1.8   1.7   1.8   1.6   1.8   1.5   1.8   1.6   1.5   1.5   1.5   2.0   1.5   1.6   1.4   1.8   1.6   1.8   1.3         1.8         1.6   1.7   1.5   2.4   1.5   1.7   1.7   1.4   1.5   1.5   1.5   1.7
 GRAZ-ZADA 3510   1.3   1.3   1.3   1.3   1.4   1.2   1.3   1.3   1.3   1.3   1.5   1.3   1.3   1.4   1.4   1.4   1.4   1.4   1.4   1.1   1.3   1.4   1.5   1.6   1.3   1.2   1.3   1.4   1.3   1.2   1.3   1.4   1.4   1.4   1.4   1.4   1.1   1.3   1.4   1.4   1.4   1.3   1.4   1.3   1.3   1.3   1.3   1.3   1.4   1.2   1.3   1.3                                                                                                                                                         1.3
 IGMI-ZADA 3510   1.2   1.2   1.0   1.3   1.2   1.2   1.2   1.2   1.3   1.2   1.4   1.2   1.3   1.3   1.2   1.3   1.2   1.3   1.2   1.2   1.2   1.4   1.3   1.3   1.1   1.1   1.2   1.2   1.2   1.1   1.2   1.2   1.3   1.3   1.2   1.3   1.2   1.1   1.2   1.3   1.3   1.5   1.3   1.3   1.3   1.2   1.1   1.4   1.3   1.1   1.3   1.2                                                                                                                                                         1.2
 IGMI-ZIM2 3510   1.2   1.2   1.0   1.2   1.2   1.0   1.2   1.2   1.2   1.1   1.1   1.1   1.2   1.1   1.1   1.1   1.0   1.3   1.2   1.0   1.1   1.3   1.2   1.1   1.1   1.1   1.3   1.1   1.1   1.2   1.2   1.1   1.2   1.1   1.1   1.1   1.3   1.1   1.2   1.2   1.2   1.3   1.1   1.1   1.2   1.1   1.3   1.4   1.3   1.1   1.3   1.1                                                                                                                                                         1.2
 KNJA-NPAZ 3510   1.5   1.4   1.3   1.4   1.4   1.3   1.4   1.2   1.3   1.5   1.4   1.3   1.4   1.4   1.3   1.5   1.4   1.4   1.5   1.3   1.4   1.6   1.6   1.4   1.3   1.3   1.4   1.4   1.2   1.3   1.3                                                                                                                                                                                                                                                                                       1.4
 LROC-MLVL 3510   1.2   1.3   1.4   1.2   1.2   1.2   1.1   1.1   1.2   1.3   1.3   1.2   1.2   1.2   1.2   1.3   1.4   1.2   1.1   1.1   1.2   1.4   1.3   1.4   1.0   1.2   1.3   1.2   1.2   1.2   1.3   1.1   1.1   1.2   1.3   1.2   1.2   1.0   1.2   1.3   1.2   1.2   1.2   1.1   1.2   1.1   1.1         1.4   1.1   1.1   1.4   1.4   0.9   1.1   1.3   1.1         1.2   1.1         1.1   1.1                                 1.1   1.3   1.2         1.3   1.2   1.1   1.1   1.2   1.2
 LROC-TLSE 3510   1.0   1.0   1.0   1.0   1.0   1.1   1.1   0.9   1.0   1.0   1.1   1.0   1.1   1.0   1.1   1.1   1.3   1.1   1.1   0.9   1.2   1.1   1.1   1.1   1.0   1.0   1.0   0.9   1.0   1.1   1.1   1.0   1.0   1.1   1.1   1.1   1.0   0.9   1.0   1.1   1.0   1.3   1.1   1.0   1.0   1.0   1.0         1.3   1.0   1.0   1.1   1.1   0.7   1.0   1.3   1.0         1.1   1.0         1.1   0.9                                 1.0   1.1   1.1         1.1   1.0   1.0   1.0   1.1   1.1
 MATE-ZADA 3510   1.2   1.0   1.1   1.1   1.1   1.1   1.3   1.0   1.1   1.1   1.3   1.1   1.2   1.3   1.2   1.2   1.0   1.1   1.2   1.1   1.2   1.3   1.2   1.3   1.1   1.1   1.1   1.2   1.1   1.0   1.1   1.1   1.0   1.1   1.3   1.2   1.1   1.1   1.1   1.2   1.2   1.4   1.1   1.1   1.2   1.1   1.1   1.4   1.1   1.1   1.2   1.1                                                                                                                                                         1.2
 MLVL-ZIM2 3510   1.5   1.3   1.1   1.4   1.5   1.3   1.3   1.2   1.2   1.3   1.3   1.2   1.3   1.4   1.2   1.3   1.4   1.2   1.2   1.1   1.2   1.4   1.3   1.5   1.2   1.3   1.3   1.3   1.1   1.3   1.2   1.2   1.3   1.4   1.4   1.2   1.3   1.3   1.3   1.3   1.3   1.5   1.2   1.2   1.2   1.3   1.3   1.7   1.3   1.3   1.3   1.3   1.2   1.3   1.2   1.5   1.1   1.2   1.3   1.2   1.3   1.3   1.3         1.4   0.8   1.2   1.3   1.2   1.2   1.2   1.3   1.2   1.2   1.2   1.3   1.2   1.3
 MOP2-PENC 3510   2.1   1.7   1.9   1.6   1.8   1.9   1.6   1.8   1.5   1.9   1.6   2.0   1.4   1.7   1.8   2.3   1.6   2.0   1.8   1.9   1.4   1.8   2.3   2.2   1.9   2.0   1.8   1.6   1.8   1.8   1.8   2.0   2.0   1.6   1.5   1.6   1.8   1.9   1.6   1.8   1.9   1.5   1.5   1.7   1.9   2.1   2.0   1.5   1.6   1.6   1.9   1.5                                                                                                                                                         1.8
 ONSA-VIS0 3510   0.9   0.8   0.8   1.0   0.9   0.9   1.0   0.9   0.9   1.0   0.9   1.2   0.9   1.0   1.0   0.9   0.8   0.9   0.9   0.8   0.9   0.9   0.9   0.8   0.9   0.8   0.8   0.9   0.8   0.9   1.0                                                                                                                                                                                                                                                                                       0.9
 PENC-SUBO 3510   1.7   1.6   1.6   1.8   1.7   1.7   1.8   1.5   1.6   1.7   1.6   1.8   1.5   1.6   1.6   1.6   1.6   1.6   1.7   1.5   1.5   1.6   1.8   1.8   1.7   1.5   1.6   1.6   1.7   1.7   1.7                                                                                                                                                                                                                                                                                       1.6
 RIGA-VIS0 3510   1.2   1.1   1.2   1.2   1.2   1.2   1.4   1.1   1.0   1.1   1.1   1.2   1.2   1.2   1.1   1.2   1.2   1.2   1.2   1.1   1.2   1.1   1.1   1.2   1.1   1.1   1.1   1.2   1.1   1.3   1.1   1.2   1.2   1.3   1.3   1.2   1.1   1.1   1.2   1.1   1.2   1.1   1.2   1.2   1.1   1.2   1.1   1.4   1.2   1.1   1.1   1.2                                                                                                                                                         1.2
 SID0-SUBO 3510   1.8   1.7   1.8   2.0   1.9   1.8   2.1   1.7   1.6   1.8   2.1   1.9   1.7   2.0   1.8   1.8   2.0   1.6   1.8   1.7   1.7   1.8   1.8   2.3   1.9   1.7   1.8   1.8   1.9   1.8   1.8                                                                                                                                                                                                                                                                                       1.8
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOTAL RMS:       1.6   1.4   1.5   1.6   1.5   1.4   1.5   1.5   1.5   1.5   1.5   1.5   1.6   1.6   1.4   1.5   1.5   1.5   1.5   1.4   1.5   1.6   1.6   1.6   1.4   1.4   1.4   1.5   1.5   1.4   1.5   1.8   1.6   1.8   1.6   1.5   1.6   1.6   1.6   1.6   1.6   1.6   1.7   1.7   1.7   1.7   1.6   1.7   1.6   1.5   1.6   1.5   1.4   1.6   1.5   1.8   1.6   1.6   1.7   1.6   1.6   1.6   1.6   1.1   1.7   0.9   1.7   1.7   1.6   1.6   1.6   1.6   1.5   1.6   1.6   1.6   1.6   1.6
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOTAL OBS:       1.6   1.5   1.6   1.9   1.9   1.7   1.7   1.5   1.8   1.9   1.5   1.5   1.8   1.7   1.7   1.9   1.7   1.9   1.8   1.6   1.7   1.9   1.5   1.5   1.7   1.5   1.9   1.6   1.6   1.9   2.0   1.2   1.3   1.3   1.3   1.6   1.6   1.3   1.5   1.5   1.6   1.2   1.3   1.3   1.4   1.3   1.4   1.0   1.1   1.6   1.7   1.3   0.8   0.5   1.1   0.7   0.7   0.6   1.0   1.0   1.1   1.1   0.4   0.0   0.2   0.0   0.8   0.6   1.0   0.9   0.9   0.6   0.7   1.1   1.0   0.6   0.9
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOT OBS (1E0):  4479  4304  4540  5320  5317  4779  4736  4345  5092  5386  4305  4204  4916  4829  4831  5454  4664  5263  4965  4395  4785  5291  4080  4247  4761  4337  5205  4418  4471  5328  5495  3280  3638  3595  3568  4558  4561  3593  4073  4281  4595  3368  3678  3619  3932  3738  3809  2696  3129  4569  4658  3689  2232  1542  3189  1977  2075  1705  2722  2898  3011  3106  1108    31   630    25  2251  1724  2883  2417  2448  1690  2007  2974  2860  1556  2478
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 BASELINE  SESS     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32   101   102   103   104   105   107   108   109   111   112   113   114   115   116   117   118   119   120   121   122   124   202   203   204   205   207   208   209   210   211   212   213   214   215   218   219   221   224   225   226   227   230   231   233   234   236   TOT
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ACOR-BRST 3510   1.0   1.0   0.9   1.4   1.0   1.3   0.9   1.1   1.1   1.1   1.2   1.3   1.4   1.3   0.9   1.1   1.1   1.2   1.2   1.0   1.3   1.3   1.2   1.1   1.1   0.9   1.0   0.9   1.2   1.0   1.0                                                                                                                                                                                                                                                                                       1.1
 ADAR-ARIS 3510   1.7   1.6   1.6   1.6   1.7   1.6   1.6   1.6   1.5   1.5   1.6   1.6   1.5   1.6   1.5   1.6   1.7   1.7   1.5   1.4   1.4   1.6   1.5   1.6   1.6   1.5   1.6   1.6   1.7   1.6   1.7   1.7   1.5   1.6   1.5   1.5   1.7   1.7   1.7   1.6   1.5   1.5   1.7   1.5   1.6   1.7   1.5   1.8   1.5   1.6   1.4   1.6                                                                                                                                                         1.6
 ADAR-SCIL 3510   1.3   1.3   1.4   1.5   1.4   1.2   1.4   1.5   1.3   1.3   1.3   1.2   1.3   1.3   1.4   1.3   1.4   1.3   1.3   1.2   1.4   1.4   1.3   1.4   1.4   1.3   1.4   1.5   1.4   1.4   1.3   1.5   1.3   1.5   1.2   1.3   1.4   1.2   1.4   1.5   1.3   1.2   1.3   1.3   1.4   1.4   1.4   1.6   1.4   1.3   1.3   1.2   1.4   1.3   1.2   1.6   1.4   1.4   1.4   1.4   1.3   1.2   1.3         1.1         1.2   1.2   1.3   1.3   1.3   1.5   1.2   1.3   1.3   1.4   1.3   1.3
 BOR1-CLIB 3510   1.3   1.1   1.1   1.5   1.3   1.2   1.4   1.3   1.2   1.2   1.3   1.3   1.3   1.3   1.4   1.2   1.3   1.2   1.2   1.2   1.2   1.4   1.3   1.5   1.2   1.3   1.3   1.4   1.2   1.3   1.3   1.4   1.4   1.4   1.4   1.4   1.3   1.2   1.3   1.5   1.3   1.3   1.3   1.4   1.2   1.2   1.4   1.4   1.4   1.3   1.2   1.2   1.3   1.3   1.2   1.5   1.2   1.3   1.3   1.3   1.3   1.2   1.3         1.3         1.2   1.2   1.3   1.5   1.3   1.2   1.5   1.3   1.2   1.4   1.3   1.3
 BOR1-JOZE 3510   1.1   1.0   0.9   1.2   1.2   0.9   1.1   1.0   1.2   1.1   1.3   1.1   1.2   1.2   1.2   1.1   1.1   1.2   1.1   1.0   1.1   1.2   1.4   1.4   1.0   1.1   1.2   1.3   1.0   1.1   1.3   1.0   1.1   1.2   1.2   1.2   1.1   1.0   1.1   1.1   1.1   1.3   1.3   1.4   1.3   1.1   1.2   1.2   1.2   1.1   1.1   1.2   1.0   1.2   1.1   1.3   1.0   1.1   1.3   1.1   1.1   1.1   1.1   1.1   1.1   0.9   0.9   1.0   1.2   1.3   1.2   1.1   1.0   1.2   1.1   1.1   1.1   1.1
 BRST-LROC 3510   1.2   1.1   1.1   1.2   1.0   1.1   1.1   0.9   1.2   1.1   1.2   1.1   1.2   1.1   1.1   1.1   1.2   1.2   1.0   1.1   1.2   1.3   1.3   1.1   1.0   1.1   1.1   1.0   1.0   1.1   1.2   1.0   1.0   1.2   1.2   1.3   1.1   0.9   1.1   1.1   1.2   1.3   1.1   1.1   1.1   1.0   1.0         1.5   1.1   1.1   1.1   1.2   0.7   1.1   1.1   1.1         1.2   1.0         1.2   1.2                                 1.1   1.1   1.2         1.1   1.2   1.0   1.0   1.2   1.1
 BRST-SCIL 3510   1.4   1.2   1.3   1.3   1.2   1.2   1.3   1.2   1.4   1.2   1.3   1.1   1.4   1.2   1.3   1.3   1.5   1.3   1.2   1.3   1.4   1.4   1.2   1.4   1.3   1.5   1.3   1.3   1.1   1.3   1.3   1.3   1.2   1.3   1.3   1.3   1.3   1.3   1.3   1.6   1.4   1.4   1.2   1.3   1.2   1.2   1.2   1.6   1.6   1.2   1.2   1.3   1.2   1.3   1.2   1.3   1.3   1.4   1.3   1.2   1.3   1.3   1.4         1.3         1.2   1.2   1.2   1.3   1.2   1.4   1.3   1.2   1.2   1.4   1.3   1.3
 BUDD-ONSA 3510   0.9   0.8   0.9   1.0   1.0   0.9   1.0   1.1   0.9   1.0   0.9   1.0   0.9   1.0   0.9   0.9   1.1   0.9   1.0   0.9   0.9   0.8   0.9   1.0   0.9   0.8   0.9   0.9   0.9   0.9   0.9                                                                                                                                                                                                                                                                                       0.9
 BUDD-POTS 3510   1.9   2.0   1.9   2.0   2.0   2.0   2.0   2.1   1.8   1.9   1.7   1.8   2.1   1.9   1.8   1.8   2.1   1.9   2.1   1.9   2.1   1.9   2.0   2.1   1.8   1.9   1.8   2.1   2.1   1.8   1.8   2.6   2.6   2.4   2.2   2.2   2.2   2.5   2.5   2.4   2.4   2.1   2.3   2.7   2.3   2.4   2.2   2.4   2.3   2.1   2.1   2.5   1.7   1.8   1.9   1.9   2.1   1.8   2.0   1.8   1.8   1.8   1.7         1.8         1.9   2.1   1.7   1.7   2.0   2.1   1.7   1.8   2.0   1.7   1.9   2.0
 CLIB-CTAB 3510   1.6   1.4   1.3   1.7   1.3   1.4   1.7   1.5   1.6   1.4   1.4   1.6   1.7   1.6   1.4   1.5   1.6   1.4   1.4   1.5   1.6   1.7   1.5   1.6   1.3   1.6   1.4   1.4   1.7   1.3   1.5   1.4   1.5   1.5   1.7   1.6   1.4   1.3   1.3   1.6   1.7   1.4   1.5   1.4   1.6   1.4   1.4   1.5   1.5   1.5   1.4   1.4   1.3   1.3   1.4   1.6   1.4   1.3   1.5   1.4   1.4   1.3   1.4         1.4         1.4   1.4   1.4   1.2   1.5   1.4   1.4   1.4   1.4   1.5   1.5   1.5
 CLIB-POTS 3510   2.0   1.7   1.9   1.8   1.7   1.7   2.0   1.9   2.2   1.9   1.9   1.7   2.1   1.8   1.7   1.7   1.9   2.0   1.8   1.9   2.1   2.1   1.8   2.4   1.7   1.9   1.8   1.9   1.9   1.7   1.9   2.3   2.4   2.1   1.9   2.1   2.3   2.3   2.4   2.1   2.2   2.2   2.2   2.2   2.3   2.5   2.2   2.4   2.2   2.2   2.2   2.4   1.8   1.9   1.7   2.0   1.8   1.8   1.9   1.8   1.7   1.8   1.7         1.9         1.9   1.8   1.8   1.7   1.7   1.8   1.7   1.8   1.9   1.7   1.8   2.0
 CTAB-MOP2 3510   1.9   1.5   1.6   1.7   1.7   1.5   1.8   1.5   1.7   1.5   1.6   1.7   1.8   1.6   1.4   1.6   1.5   1.5   1.6   1.7   1.5   1.8   1.5   1.8   1.4   1.6   1.6   1.5   1.8   1.7   1.6   1.7   1.5   1.5   1.6   1.5   1.6   1.5   1.4   1.4   1.7   1.5   1.5   1.5   1.7   1.6   1.6   1.6   1.7   1.6   1.5   1.4   1.5   1.4   1.5   1.6   1.5   1.5   1.6   1.5   1.5   1.5   1.5         1.7         1.5   1.5   1.5   1.6   1.4   1.5   1.6   1.5   1.4   1.6   1.5   1.6
 CTAB-WTZR 3510   1.7   1.5   1.3   1.6   1.4   1.4   1.7   1.5   1.6   1.5   1.4   1.5   1.6   1.6   1.4   1.5   1.6   1.4   1.5   1.6   1.5   1.7   1.5   1.6   1.3   1.6   1.5   1.5   1.4   1.4   1.5   1.4   1.4   1.5   1.6   1.5   1.4   1.4   1.3   1.6   1.6   1.4   1.4   1.3   1.5   1.4   1.5   1.6   1.6   1.5   1.5   1.3   1.4   1.4   1.3   1.6   1.4   1.4   1.5   1.3   1.4   1.4   1.5         1.3         1.5   1.4   1.3   1.6   1.4   1.5   1.3   1.4   1.4   1.5   1.4   1.5
 DEVA-IGEO 3510   1.3   1.3   1.2   1.3   1.3   1.3   1.3   1.4   1.2   1.3   1.5   1.2   1.2   1.3   1.3   1.2   1.2   1.1   1.4   1.1   1.2   1.2   1.2   1.2   1.3   1.2   1.2   1.3   1.3   1.2   1.2   1.3   1.1   1.3   1.3   1.1   1.1   1.3   1.2   1.2   1.2   1.3   1.2   1.1   1.1   1.2   1.2   1.3   1.2   1.1   1.2   1.1   1.2   1.1   1.2   1.2   1.1   1.2   1.2         1.2   1.2                           1.2   1.3   1.2   1.3   1.1   1.2   1.1   1.2                     1.2
 DEVA-SUBO 3510   1.5   1.4   1.6   1.6   1.5   1.4   1.5   1.4   1.3   1.4   1.4   1.4   1.3   1.4   1.3   1.3   1.2   1.3   1.6   1.3   1.3   1.3   1.4   1.5   1.4   1.2   1.3   1.4   1.5   1.4   1.4                                                                                                                                                                                                                                                                                       1.4
 DLF1-MLVL 3510   1.3   1.3   1.1   1.3   1.2   1.2   1.2   1.1   1.3   1.1   1.0   1.2   1.3   1.3   1.2   1.1   1.3   1.2   1.1   1.2   1.1   1.3   1.2   1.3   1.1   1.2   1.1   1.2   1.1   1.1   1.2   1.2   1.2   1.2   1.3   1.1   1.2   1.1   1.2   1.3   1.2   1.2   1.1   1.1   1.1   1.1   1.2   1.3   1.3   1.2   1.1   1.2   1.0   1.2   1.1   1.2   1.1   1.1   1.2   1.1   1.1   1.2   1.2   0.8   1.1   0.8   1.1   1.1   1.1   1.1   1.2   1.1   1.1   1.1   1.2   1.3   1.1   1.2
 GJML-NPAZ 3510   1.3   1.2   1.2   1.3   1.3   1.3   1.3   1.2   1.2   1.3   1.4   1.2   1.4   1.4   1.3   1.3   1.2   1.3   1.4   1.3   1.2   1.4   1.3   1.3   1.2   1.3   1.2   1.3   1.3   1.2   1.3   1.3   1.2   1.2   1.4   1.2   1.1   1.1   1.2   1.3   1.4   1.4   1.3   1.2   1.2   1.3   1.4   1.2   1.1   1.1   1.3   1.3                                                                                                                                                         1.3
 GJML-SID0 3510   1.7   1.7   1.7   1.7   1.7   1.7   1.9   1.6   1.6   1.7   1.8   1.7   1.7   1.9   1.7   1.6   1.8   1.6   1.9   1.5   1.8   1.7   1.5   1.8   1.6   1.5   1.6   1.6   1.8   1.6   1.7   1.6   1.7   1.7   1.7   1.6   1.5   1.8   1.6   1.7   1.7   1.8   1.8   1.6   1.6   1.6   1.6   1.6   1.7   1.6   1.8   1.7                                                                                                                                                         1.7
 GLSV-IGEO 3510   1.6   1.3   1.3   1.4   1.5   1.3   1.5   1.3   1.5   1.3   1.6   1.6   1.5   1.6   1.3   1.4   1.2   1.2   1.4   1.5   1.5   1.4   1.4   1.4   1.2   1.4   1.4   1.6   1.4   1.3   1.3   1.5   1.2   1.5   1.6   1.3   1.2   1.2   1.3   1.4   1.4   1.7   1.6   1.4   1.2   1.2   1.2   1.7   1.5   1.3   1.5   1.3   1.4   1.3   1.4   1.4   1.4   1.2   1.5         1.3   1.2                           1.3   1.4   1.3   1.4   1.4   1.3   1.2   1.4                     1.4
 GRAZ-MOP2 3510   1.6   1.5   1.6   1.6   1.7   1.4   1.6   1.5   1.6   1.4   1.4   1.4   1.5   1.4   1.4   1.6   1.4   1.5   1.5   1.5   1.4   1.6   1.3   1.6   1.4   1.5   1.5   1.5   1.5   1.6   1.5   1.7   1.5   1.4   1.5   1.4   1.5   1.4   1.5   1.4   1.6   1.4   1.3   1.4   1.6   1.5   1.4   1.5   1.7   1.4   1.4   1.4   1.5   1.4   1.4   1.6   1.4   1.4   1.3   1.4   1.4   1.5   1.3         1.8         1.4   1.4   1.4   1.6   1.3   1.4   1.5   1.3   1.4   1.4   1.4   1.5
 GRAZ-ZADA 3510   1.3   1.3   1.3   1.3   1.3   1.2   1.3   1.3   1.2   1.3   1.4   1.3   1.3   1.3   1.4   1.4   1.4   1.3   1.4   1.1   1.2   1.4   1.4   1.4   1.2   1.2   1.3   1.4   1.3   1.2   1.3   1.3   1.4   1.4   1.4   1.3   1.1   1.3   1.3   1.4   1.3   1.3   1.3   1.2   1.3   1.3   1.3   1.3   1.3   1.2   1.3   1.3                                                                                                                                                         1.3
 IGMI-ZADA 3510   1.1   1.2   1.0   1.3   1.2   1.2   1.2   1.2   1.3   1.2   1.4   1.2   1.3   1.3   1.2   1.3   1.2   1.3   1.2   1.2   1.2   1.4   1.3   1.2   1.1   1.1   1.2   1.2   1.2   1.1   1.2   1.2   1.3   1.3   1.2   1.3   1.2   1.1   1.2   1.3   1.2   1.5   1.3   1.3   1.3   1.2   1.1   1.4   1.3   1.1   1.2   1.2                                                                                                                                                         1.2
 IGMI-ZIM2 3510   1.2   1.2   1.0   1.2   1.2   1.0   1.2   1.2   1.1   1.1   1.1   1.1   1.2   1.1   1.1   1.1   1.0   1.2   1.2   1.0   1.1   1.3   1.2   1.1   1.1   1.1   1.3   1.1   1.1   1.2   1.2   1.1   1.2   1.1   1.1   1.1   1.2   1.1   1.2   1.2   1.2   1.3   1.0   1.1   1.2   1.1   1.3   1.4   1.3   1.1   1.3   1.1                                                                                                                                                         1.2
 KNJA-NPAZ 3510   1.5   1.4   1.3   1.4   1.4   1.3   1.4   1.2   1.3   1.5   1.4   1.3   1.4   1.4   1.3   1.5   1.4   1.4   1.5   1.3   1.4   1.6   1.5   1.4   1.3   1.3   1.4   1.4   1.2   1.3   1.4                                                                                                                                                                                                                                                                                       1.4
 LROC-MLVL 3510   1.2   1.3   1.3   1.2   1.2   1.2   1.1   1.1   1.2   1.3   1.3   1.2   1.2   1.2   1.2   1.3   1.4   1.2   1.1   1.1   1.2   1.3   1.3   1.4   1.0   1.2   1.3   1.2   1.2   1.2   1.3   1.1   1.1   1.2   1.3   1.2   1.2   1.0   1.2   1.3   1.2   1.2   1.2   1.1   1.2   1.1   1.1         1.4   1.1   1.1   1.4   1.4   0.9   1.1   1.3   1.1         1.2   1.1         1.1   1.1                                 1.1   1.3   1.2         1.3   1.2   1.1   1.1   1.2   1.2
 LROC-TLSE 3510   1.0   1.0   1.0   1.0   1.0   1.1   1.1   0.9   1.0   1.0   1.1   1.0   1.1   1.0   1.1   1.1   1.2   1.1   1.1   0.9   1.2   1.1   1.1   1.1   1.0   1.0   1.0   0.9   1.0   1.1   1.1   1.0   1.0   1.1   1.1   1.1   1.0   0.9   1.0   1.1   1.0   1.3   1.1   1.0   1.0   1.0   1.0         1.3   1.0   1.0   1.1   1.1   0.7   1.0   1.3   1.0         1.1   1.0         1.1   0.9                                 1.0   1.1   1.1         1.1   1.0   1.0   1.0   1.1   1.1
 MATE-ZADA 3510   1.2   1.0   1.1   1.1   1.1   1.1   1.3   1.0   1.1   1.1   1.3   1.1   1.2   1.3   1.2   1.1   1.0   1.1   1.2   1.1   1.2   1.3   1.2   1.2   1.1   1.1   1.1   1.2   1.1   1.0   1.1   1.1   1.0   1.1   1.3   1.2   1.1   1.1   1.1   1.2   1.2   1.3   1.1   1.1   1.2   1.1   1.1   1.4   1.1   1.1   1.2   1.1                                                                                                                                                         1.1
 MLVL-ZIM2 3510   1.5   1.3   1.1   1.4   1.5   1.3   1.3   1.2   1.2   1.3   1.3   1.2   1.3   1.4   1.2   1.3   1.4   1.2   1.2   1.1   1.2   1.4   1.3   1.4   1.2   1.3   1.3   1.3   1.1   1.3   1.2   1.2   1.3   1.4   1.4   1.2   1.3   1.3   1.3   1.3   1.3   1.5   1.2   1.2   1.2   1.3   1.3   1.6   1.3   1.3   1.2   1.3   1.2   1.3   1.2   1.5   1.1   1.2   1.3   1.2   1.3   1.3   1.3         1.4   0.8   1.2   1.3   1.2   1.2   1.2   1.3   1.2   1.2   1.2   1.3   1.2   1.3
 MOP2-PENC 3510   1.4   1.5   1.4   1.5   1.5   1.4   1.4   1.4   1.3   1.7   1.4   1.4   1.3   1.5   1.4   1.6   1.4   1.7   1.5   1.4   1.3   1.6   1.4   1.5   1.5   1.3   1.6   1.5   1.4   1.7   1.5   1.4   1.3   1.4   1.4   1.4   1.5   1.4   1.5   1.4   1.5   1.4   1.3   1.5   1.6   1.4   1.5   1.4   1.4   1.4   1.4   1.3                                                                                                                                                         1.5
 ONSA-VIS0 3510   0.9   0.8   0.8   1.0   0.9   0.9   1.0   0.9   0.9   1.0   0.8   1.0   0.9   1.0   1.0   0.9   0.8   0.8   0.9   0.8   0.9   0.9   0.9   0.8   0.9   0.8   0.8   0.9   0.8   0.9   1.0                                                                                                                                                                                                                                                                                       0.9
 PENC-SUBO 3510   1.7   1.5   1.6   1.7   1.7   1.7   1.7   1.5   1.6   1.7   1.6   1.6   1.5   1.6   1.6   1.6   1.6   1.6   1.6   1.5   1.5   1.6   1.7   1.8   1.6   1.5   1.6   1.6   1.6   1.6   1.6                                                                                                                                                                                                                                                                                       1.6
 RIGA-VIS0 3510   1.2   1.1   1.2   1.2   1.2   1.1   1.3   1.1   1.0   1.1   1.1   1.1   1.2   1.2   1.1   1.2   1.2   1.2   1.2   1.1   1.2   1.1   1.1   1.2   1.1   1.1   1.1   1.2   1.1   1.3   1.1   1.2   1.2   1.3   1.3   1.2   1.1   1.1   1.2   1.1   1.2   1.1   1.2   1.2   1.1   1.2   1.1   1.4   1.2   1.1   1.1   1.2                                                                                                                                                         1.2
 SID0-SUBO 3510   1.7   1.6   1.7   1.8   1.7   1.8   2.0   1.7   1.6   1.7   2.0   1.8   1.7   1.9   1.7   1.7   1.8   1.5   1.7   1.6   1.7   1.7   1.7   1.9   1.8   1.6   1.7   1.7   1.8   1.7   1.7                                                                                                                                                                                                                                                                                       1.7
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOTAL RMS:       1.4   1.3   1.3   1.4   1.4   1.3   1.5   1.3   1.4   1.4   1.4   1.3   1.4   1.4   1.3   1.4   1.4   1.4   1.4   1.3   1.4   1.4   1.4   1.5   1.3   1.3   1.4   1.4   1.4   1.4   1.4   1.4   1.4   1.4   1.5   1.4   1.4   1.4   1.4   1.4   1.4   1.5   1.4   1.4   1.4   1.4   1.4   1.6   1.5   1.4   1.4   1.4   1.4   1.4   1.3   1.5   1.4   1.4   1.4   1.4   1.4   1.4   1.4   1.1   1.4   0.9   1.4   1.4   1.3   1.4   1.4   1.4   1.4   1.4   1.4   1.4   1.4   1.4
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOTAL OBS:       1.6   1.5   1.6   1.9   1.9   1.7   1.7   1.6   1.8   1.9   1.5   1.5   1.7   1.7   1.7   1.9   1.7   1.9   1.8   1.6   1.7   1.9   1.4   1.5   1.7   1.6   1.9   1.6   1.6   1.9   2.0   1.1   1.3   1.2   1.3   1.6   1.6   1.3   1.4   1.5   1.6   1.2   1.3   1.3   1.4   1.3   1.3   1.0   1.1   1.6   1.7   1.3   0.8   0.5   1.1   0.7   0.7   0.6   1.0   1.0   1.1   1.1   0.4   0.0   0.2   0.0   0.8   0.6   1.0   0.9   0.9   0.6   0.7   1.1   1.0   0.6   0.9
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 TOT OBS (1E0):  4416  4286  4507  5285  5288  4745  4695  4308  5053  5359  4266  4171  4838  4799  4818  5401  4628  5234  4950  4359  4718  5217  3999  4169  4749  4310  5195  4359  4435  5311  5466  3160  3589  3449  3559  4532  4469  3554  3978  4215  4543  3344  3570  3522  3802  3630  3741  2647  3110  4517  4583  3649  2226  1523  3171  1934  2062  1700  2678  2874  2994  3055  1097    31   626    25  2197  1671  2856  2397  2427  1683  2002  2950  2835  1545  2447
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



================================================================================
PART 6: AMBIGUITY RESOLUTION SUMMARY
================================================================================

================================================================================
 Code-Based Widelane (WL) Ambiguity Resolution (<6000 km)
================================================================================

 File     Sta1 Sta2    Length     Before     After    Res  Sys     Max/RMS L5    QCB FRQ Receiver 1           Receiver 2
                        (km)    #Amb (mm)  #Amb (mm)  (%)       (L5 Cycles)        
 ----------------------------------------------------------------------------------------------------------------------------------
 ACBR3510 ACOR BRST    634.078    71  0.1    14  0.4  80.3 G       0.145  0.080    I   - LEICA GR50           TRIMBLE ALLOY         #AR_WL
 ADAR3510 ADAR ARIS    464.061    97  0.0    28  0.4  71.1 G       0.150  0.089    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_WL
 ADSC3510 ADAR SCIL    337.602    93  0.0     6  0.1  93.5 G       0.149  0.060    I   - SEPT POLARX5         SEPT POLARX5          #AR_WL
 ADSC3510 ADAR SCIL    337.602    56  0.0     3  0.1  94.6   E     0.156  0.048    -   - SEPT POLARX5         SEPT POLARX5          #AR_WL
 ADSC3510 ADAR SCIL    337.602   149  0.0     9  0.1  94.0 G E     0.156  0.056    I   - SEPT POLARX5         SEPT POLARX5          #AR_WL
 BOCL3510 BOR1 CLIB    218.102    88  0.0    19  0.3  78.4 G       0.158  0.070    I   - TRIMBLE NETR9        LEICA GR30            #AR_WL
 BOCL3510 BOR1 CLIB    218.102    55  0.0    10  0.3  81.8   E     0.144  0.084    -   - TRIMBLE NETR9        LEICA GR30            #AR_WL
 BOCL3510 BOR1 CLIB    218.102   143  0.0    29  0.3  79.7 G E     0.158  0.076    I   - TRIMBLE NETR9        LEICA GR30            #AR_WL
 BOJO3510 BOR1 JOZE    271.387    66  0.0     4  0.4  93.9 G       0.148  0.082    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_WL
 BOJO3510 BOR1 JOZE    271.387    65  0.0     7  0.4  89.2   E     0.147  0.077    -   - TRIMBLE NETR9        SEPT POLARX5          #AR_WL
 BOJO3510 BOR1 JOZE    271.387   131  0.0    11  0.4  91.6 G E     0.148  0.079    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_WL
 BRLR3510 BRST LROC    349.903    69  0.0     9  0.4  87.0 G       0.149  0.082    I   - TRIMBLE ALLOY        LEICA GR25            #AR_WL
 BRLR3510 BRST LROC    349.903     1  0.0     1  0.4   0.0   E     0.000  0.000    -   - TRIMBLE ALLOY        LEICA GR25            #AR_WL
 BRLR3510 BRST LROC    349.903    70  0.0    10  0.4  85.7 G E     0.149  0.082    I   - TRIMBLE ALLOY        LEICA GR25            #AR_WL
 BRSC3510 BRST SCIL    215.237    76  0.0    11  0.3  85.5 G       0.149  0.063    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_WL
 BRSC3510 BRST SCIL    215.237    56  0.0    11  0.3  80.4   E     0.173  0.086    -   - TRIMBLE ALLOY        SEPT POLARX5          #AR_WL
 BRSC3510 BRST SCIL    215.237   132  0.0    22  0.3  83.3 G E     0.173  0.073    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_WL
 BUON3510 BUDD ONSA    187.791   111  0.0     9  0.2  91.9 G       0.148  0.063    I   - SEPT POLARX5         SEPT POLARX5TR        #AR_WL
 BUPO3510 BUDD POTS    375.723   100  0.0    24  0.3  76.0 G       0.149  0.081    I   - SEPT POLARX5         JAVAD TRE_3           #AR_WL
 BUPO3510 BUDD POTS    375.723    63  0.0    11  0.3  82.5   E     0.128  0.066    -   - SEPT POLARX5         JAVAD TRE_3           #AR_WL
 BUPO3510 BUDD POTS    375.723   163  0.0    35  0.3  78.5 G E     0.149  0.075    I   - SEPT POLARX5         JAVAD TRE_3           #AR_WL
 CLPO3510 CLIB POTS    226.025   102  0.0    27  0.3  73.5 G       0.185  0.088    I   - LEICA GR30           JAVAD TRE_3           #AR_WL
 CLPO3510 CLIB POTS    226.025    58  0.0    13  0.3  77.6   E     0.140  0.073    -   - LEICA GR30           JAVAD TRE_3           #AR_WL
 CLPO3510 CLIB POTS    226.025   160  0.0    40  0.3  75.0 G E     0.185  0.083    I   - LEICA GR30           JAVAD TRE_3           #AR_WL
 CTMO3510 CTAB MOP2    222.418    67  0.0     9  0.3  86.6 G       0.148  0.078    I   - LEICA GR30           TRIMBLE ALLOY         #AR_WL
 CTMO3510 CTAB MOP2    222.418    46  0.0     6  0.3  87.0   E     0.143  0.073    -   - LEICA GR30           TRIMBLE ALLOY         #AR_WL
 CTMO3510 CTAB MOP2    222.418   113  0.0    15  0.3  86.7 G E     0.148  0.076    I   - LEICA GR30           TRIMBLE ALLOY         #AR_WL
 DEIG3510 DEVA IGEO    473.005    68  0.1    17  0.3  75.0 G       0.146  0.066    I   - LEICA GR50           LEICA GR10            #AR_WL
 DEIG3510 DEVA IGEO    473.005    23  0.1     2  0.3  91.3   E     0.150  0.083    -   - LEICA GR50           LEICA GR10            #AR_WL
 DEIG3510 DEVA IGEO    473.005    91  0.1    19  0.3  79.1 G E     0.150  0.071    I   - LEICA GR50           LEICA GR10            #AR_WL
 DESU3510 DEVA SUBO    252.701    92  0.0    22  0.4  76.1 G       0.186  0.081    I   - LEICA GR50           TRIMBLE NETR9         #AR_WL
 DLML3510 DLF1 MLVL    372.424    73  0.0    12  0.3  83.6 G       0.147  0.078    I   - TRIMBLE ALLOY        LEICA GR50            #AR_WL
 DLML3510 DLF1 MLVL    372.424    44  0.0     5  0.3  88.6   E     0.172  0.092    -   - TRIMBLE ALLOY        LEICA GR50            #AR_WL
 DLML3510 DLF1 MLVL    372.424   117  0.0    17  0.3  85.5 G E     0.172  0.084    I   - TRIMBLE ALLOY        LEICA GR50            #AR_WL
 GLIG3510 GLSV IGEO    390.120    81  0.0    12  0.2  85.2 G       0.147  0.078    I   - TRIMBLE NETR9        LEICA GR10            #AR_WL
 GLIG3510 GLSV IGEO    390.120    33  0.0     8  0.2  75.8   E     0.142  0.084    -   - TRIMBLE NETR9        LEICA GR10            #AR_WL
 GLIG3510 GLSV IGEO    390.120   114  0.0    20  0.2  82.5 G E     0.147  0.080    I   - TRIMBLE NETR9        LEICA GR10            #AR_WL
 GRMO3510 GRAZ MOP2    197.265    76  0.0     7  0.3  90.8 G       0.164  0.078    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_WL
 GRMO3510 GRAZ MOP2    197.265    53  0.0     5  0.3  90.6   E     0.149  0.081    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_WL
 GRMO3510 GRAZ MOP2    197.265   129  0.0    12  0.3  90.7 G E     0.164  0.079    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_WL
 GRZA3510 GRAZ ZADA    328.946    70  0.0    10  0.4  85.7 G       0.147  0.081    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_WL
 IMZA3510 IGMI ZADA    324.039    74  0.1    10  0.4  86.5 G       0.149  0.084    I   - STONEX SC2200        TRIMBLE ALLOY         #AR_WL
 IMZI3510 IGMI ZIM2    451.084    78  0.1    16  0.4  79.5 G       0.177  0.086    I   - STONEX SC2200        TRIMBLE NETR9         #AR_WL
 LRML3510 LROC MLVL    413.570    60  0.0     7  0.4  88.3 G       0.144  0.083    I   - LEICA GR25           LEICA GR50            #AR_WL
 LRML3510 LROC MLVL    413.570     3  0.0     2  0.4  33.3   E     0.165  0.165    -   - LEICA GR25           LEICA GR50            #AR_WL
 LRML3510 LROC MLVL    413.570    63  0.0     9  0.4  85.7 G E     0.165  0.086    I   - LEICA GR25           LEICA GR50            #AR_WL
 LRTL3510 LROC TLSE    358.965    71  0.0     9  0.3  87.3 G       0.149  0.074    I   - LEICA GR25           TRIMBLE ALLOY         #AR_WL
 LRTL3510 LROC TLSE    358.965     4  0.0     2  0.3  50.0   E     0.102  0.075    -   - LEICA GR25           TRIMBLE ALLOY         #AR_WL
 LRTL3510 LROC TLSE    358.965    75  0.0    11  0.3  85.3 G E     0.149  0.074    I   - LEICA GR25           TRIMBLE ALLOY         #AR_WL
 MAZA3510 MATE ZADA    403.485    84  0.0    26  0.4  69.0 G       0.148  0.076    I   - LEICA GR30           TRIMBLE ALLOY         #AR_WL
 MLZI3510 MLVL ZIM2    425.163    72  0.0    15  0.2  79.2 G       0.146  0.079    I   - LEICA GR50           TRIMBLE NETR9         #AR_WL
 MLZI3510 MLVL ZIM2    425.163    51  0.0     8  0.2  84.3   E     0.150  0.061    -   - LEICA GR50           TRIMBLE NETR9         #AR_WL
 MLZI3510 MLVL ZIM2    425.163   123  0.0    23  0.2  81.3 G E     0.150  0.072    I   - LEICA GR50           TRIMBLE NETR9         #AR_WL
 ONVS3510 ONSA VIS0    386.828   106  0.0     7  0.1  93.4 G       0.131  0.042    I   - SEPT POLARX5TR       SEPT POLARX5          #AR_WL
 PESU3510 PENC SUBO    190.168    79  0.0    11  0.4  86.1 G       0.167  0.088    I   - LEICA GRX1200GGPRO   TRIMBLE NETR9         #AR_WL
 RIVS3510 RIGA VIS0    351.802    90  0.0    15  0.4  83.3 G       0.182  0.086    I   - LEICA GR25           SEPT POLARX5          #AR_WL
 ----------------------------------------------------------------------------------------------------------------------------------
 Tot:  26              339.304  2114  0.0   356  0.3  83.2 G       0.186  0.077                                                     #AR_WL
 Tot:  15              323.127   611  0.0    94  0.3  84.6   E     0.173  0.076                                                     #AR_WL
 Tot:  26              339.304  2725  0.0   450  0.3  83.5 G E     0.186  0.076                                                     #AR_WL


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Code-Based Narrowlane (NL) Ambiguity Resolution (<6000 km)
================================================================================

 File     Sta1 Sta2    Length     Before     After    Res  Sys     Max/RMS L1    QCB FRQ Receiver 1           Receiver 2
                        (km)    #Amb (mm)  #Amb (mm)  (%)       (L1 Cycles)        
 ----------------------------------------------------------------------------------------------------------------------------------
 ACBR3510 ACOR BRST    634.078    76  1.1    23  1.1  69.7 G       0.145  0.047    I   - LEICA GR50           TRIMBLE ALLOY         #AR_NL
 ADAR3510 ADAR ARIS    464.061   105  1.4    42  1.4  60.0 G       0.149  0.059    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_NL
 ADSC3510 ADAR SCIL    337.602   103  1.0    34  1.1  67.0 G       0.157  0.057    I   - SEPT POLARX5         SEPT POLARX5          #AR_NL
 ADSC3510 ADAR SCIL    337.602    56  1.0    14  1.1  75.0   E     0.142  0.061    -   - SEPT POLARX5         SEPT POLARX5          #AR_NL
 ADSC3510 ADAR SCIL    337.602   159  1.0    48  1.1  69.8 G E     0.157  0.058    I   - SEPT POLARX5         SEPT POLARX5          #AR_NL
 BOCL3510 BOR1 CLIB    218.102    93  1.0    32  1.1  65.6 G       0.168  0.043    I   - TRIMBLE NETR9        LEICA GR30            #AR_NL
 BOCL3510 BOR1 CLIB    218.102    58  1.0    16  1.1  72.4   E     0.160  0.044    -   - TRIMBLE NETR9        LEICA GR30            #AR_NL
 BOCL3510 BOR1 CLIB    218.102   151  1.0    48  1.1  68.2 G E     0.168  0.043    I   - TRIMBLE NETR9        LEICA GR30            #AR_NL
 BOJO3510 BOR1 JOZE    271.387    69  0.9     9  1.0  87.0 G       0.146  0.036    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_NL
 BOJO3510 BOR1 JOZE    271.387    64  0.9    11  1.0  82.8   E     0.135  0.047    -   - TRIMBLE NETR9        SEPT POLARX5          #AR_NL
 BOJO3510 BOR1 JOZE    271.387   133  0.9    20  1.0  85.0 G E     0.146  0.042    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_NL
 BRLR3510 BRST LROC    349.903    83  1.0    30  1.0  63.9 G       0.139  0.045    I   - TRIMBLE ALLOY        LEICA GR25            #AR_NL
 BRLR3510 BRST LROC    349.903    67  1.0    67  1.0   0.0   E     0.000  0.000    -   - TRIMBLE ALLOY        LEICA GR25            #AR_NL
 BRLR3510 BRST LROC    349.903   150  1.0    97  1.0  35.3 G E     0.139  0.045    I   - TRIMBLE ALLOY        LEICA GR25            #AR_NL
 BRSC3510 BRST SCIL    215.237    76  1.0    18  1.0  76.3 G       0.116  0.041    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_NL
 BRSC3510 BRST SCIL    215.237    56  1.0    16  1.0  71.4   E     0.141  0.042    -   - TRIMBLE ALLOY        SEPT POLARX5          #AR_NL
 BRSC3510 BRST SCIL    215.237   132  1.0    34  1.0  74.2 G E     0.141  0.042    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_NL
 BUON3510 BUDD ONSA    187.791   111  0.8    22  0.9  80.2 G       0.184  0.063    I   - SEPT POLARX5         SEPT POLARX5TR        #AR_NL
 BUPO3510 BUDD POTS    375.723   101  0.9    28  0.9  72.3 G       0.176  0.053    I   - SEPT POLARX5         JAVAD TRE_3           #AR_NL
 BUPO3510 BUDD POTS    375.723    63  0.9    17  0.9  73.0   E     0.132  0.042    -   - SEPT POLARX5         JAVAD TRE_3           #AR_NL
 BUPO3510 BUDD POTS    375.723   164  0.9    45  0.9  72.6 G E     0.176  0.049    I   - SEPT POLARX5         JAVAD TRE_3           #AR_NL
 CLPO3510 CLIB POTS    226.025   107  1.1    42  1.1  60.7 G       0.134  0.044    I   - LEICA GR30           JAVAD TRE_3           #AR_NL
 CLPO3510 CLIB POTS    226.025    66  1.1    24  1.1  63.6   E     0.132  0.045    -   - LEICA GR30           JAVAD TRE_3           #AR_NL
 CLPO3510 CLIB POTS    226.025   173  1.1    66  1.1  61.8 G E     0.134  0.045    I   - LEICA GR30           JAVAD TRE_3           #AR_NL
 CTMO3510 CTAB MOP2    222.418    80  1.4    25  1.4  68.8 G       0.168  0.050    I   - LEICA GR30           TRIMBLE ALLOY         #AR_NL
 CTMO3510 CTAB MOP2    222.418    65  1.4    30  1.4  53.8   E     0.088  0.028    -   - LEICA GR30           TRIMBLE ALLOY         #AR_NL
 CTMO3510 CTAB MOP2    222.418   145  1.4    55  1.4  62.1 G E     0.168  0.043    I   - LEICA GR30           TRIMBLE ALLOY         #AR_NL
 DEIG3510 DEVA IGEO    473.005   105  1.0    56  1.1  46.7 G       0.077  0.032    I   - LEICA GR50           LEICA GR10            #AR_NL
 DEIG3510 DEVA IGEO    473.005    40  1.0    20  1.1  50.0   E     0.037  0.020    -   - LEICA GR50           LEICA GR10            #AR_NL
 DEIG3510 DEVA IGEO    473.005   145  1.0    76  1.1  47.6 G E     0.077  0.029    I   - LEICA GR50           LEICA GR10            #AR_NL
 DESU3510 DEVA SUBO    252.701   101  1.3    39  1.3  61.4 G       0.143  0.049    I   - LEICA GR50           TRIMBLE NETR9         #AR_NL
 DLML3510 DLF1 MLVL    372.424    77  1.0    17  1.0  77.9 G       0.121  0.041    I   - TRIMBLE ALLOY        LEICA GR50            #AR_NL
 DLML3510 DLF1 MLVL    372.424    52  1.0    15  1.0  71.2   E     0.129  0.039    -   - TRIMBLE ALLOY        LEICA GR50            #AR_NL
 DLML3510 DLF1 MLVL    372.424   129  1.0    32  1.0  75.2 G E     0.129  0.040    I   - TRIMBLE ALLOY        LEICA GR50            #AR_NL
 GLIG3510 GLSV IGEO    390.120    93  1.1    31  1.2  66.7 G       0.141  0.051    I   - TRIMBLE NETR9        LEICA GR10            #AR_NL
 GLIG3510 GLSV IGEO    390.120    44  1.1    21  1.2  52.3   E     0.129  0.047    -   - TRIMBLE NETR9        LEICA GR10            #AR_NL
 GLIG3510 GLSV IGEO    390.120   137  1.1    52  1.2  62.0 G E     0.141  0.050    I   - TRIMBLE NETR9        LEICA GR10            #AR_NL
 GRMO3510 GRAZ MOP2    197.265    78  1.2    14  1.3  82.1 G       0.139  0.049    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_NL
 GRMO3510 GRAZ MOP2    197.265    55  1.2    15  1.3  72.7   E     0.138  0.036    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_NL
 GRMO3510 GRAZ MOP2    197.265   133  1.2    29  1.3  78.2 G E     0.139  0.045    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_NL
 GRZA3510 GRAZ ZADA    328.946    74  1.1    18  1.1  75.7 G       0.186  0.047    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_NL
 IMZA3510 IGMI ZADA    324.039    83  1.1    23  1.2  72.3 G       0.162  0.061    I   - STONEX SC2200        TRIMBLE ALLOY         #AR_NL
 IMZI3510 IGMI ZIM2    451.084    88  1.0    30  1.1  65.9 G       0.147  0.057    I   - STONEX SC2200        TRIMBLE NETR9         #AR_NL
 LRML3510 LROC MLVL    413.570    86  1.0    37  1.1  57.0 G       0.100  0.044    I   - LEICA GR25           LEICA GR50            #AR_NL
 LRML3510 LROC MLVL    413.570    69  1.0    68  1.1   1.4   E     0.003  0.003    -   - LEICA GR25           LEICA GR50            #AR_NL
 LRML3510 LROC MLVL    413.570   155  1.0   105  1.1  32.3 G E     0.100  0.043    I   - LEICA GR25           LEICA GR50            #AR_NL
 LRTL3510 LROC TLSE    358.965    81  0.9    23  0.9  71.6 G       0.133  0.045    I   - LEICA GR25           TRIMBLE ALLOY         #AR_NL
 LRTL3510 LROC TLSE    358.965    66  0.9    64  0.9   3.0   E     0.030  0.021    -   - LEICA GR25           TRIMBLE ALLOY         #AR_NL
 LRTL3510 LROC TLSE    358.965   147  0.9    87  0.9  40.8 G E     0.133  0.044    I   - LEICA GR25           TRIMBLE ALLOY         #AR_NL
 MAZA3510 MATE ZADA    403.485   107  1.0    52  1.0  51.4 G       0.147  0.042    I   - LEICA GR30           TRIMBLE ALLOY         #AR_NL
 MLZI3510 MLVL ZIM2    425.163    90  1.0    36  1.1  60.0 G       0.142  0.041    I   - LEICA GR50           TRIMBLE NETR9         #AR_NL
 MLZI3510 MLVL ZIM2    425.163    55  1.0    14  1.1  74.5   E     0.143  0.050    -   - LEICA GR50           TRIMBLE NETR9         #AR_NL
 MLZI3510 MLVL ZIM2    425.163   145  1.0    50  1.1  65.5 G E     0.143  0.045    I   - LEICA GR50           TRIMBLE NETR9         #AR_NL
 ONVS3510 ONSA VIS0    386.828   107  0.8    22  0.8  79.4 G       0.172  0.054    I   - SEPT POLARX5TR       SEPT POLARX5          #AR_NL
 PESU3510 PENC SUBO    190.168    85  1.5    26  1.6  69.4 G       0.183  0.058    I   - LEICA GRX1200GGPRO   TRIMBLE NETR9         #AR_NL
 RIVS3510 RIGA VIS0    351.802   100  1.0    32  1.0  68.0 G       0.141  0.045    I   - LEICA GR25           SEPT POLARX5          #AR_NL
 ----------------------------------------------------------------------------------------------------------------------------------
 Tot:  26              339.304  2359  1.1   761  1.1  67.7 G       0.186  0.049                                                     #AR_NL
 Tot:  15              323.127   876  1.0   412  1.1  53.0   E     0.160  0.044                                                     #AR_NL
 Tot:  26              339.304  3235  1.1  1173  1.1  63.7 G E     0.186  0.048                                                     #AR_NL


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Phase-Based Widelane (L5) Ambiguity Resolution (<200 km)
================================================================================

 File     Sta1 Sta2    Length     Before     After    Res  Sys     Max/RMS L5    QCB FRQ Receiver 1           Receiver 2
                        (km)    #Amb (mm)  #Amb (mm)  (%)       (L5 Cycles)        
 ----------------------------------------------------------------------------------------------------------------------------------
 BUON3510 BUDD ONSA    187.791   111 14.5    46 15.0  58.6 G       0.171  0.087    I   - SEPT POLARX5         SEPT POLARX5TR        #AR_L5
 CLCT3510 CLIB CTAB    153.910    95 10.0    34 10.3  64.2 G       0.165  0.071    I   - LEICA GR30           LEICA GR30            #AR_L5
 CLCT3510 CLIB CTAB    153.910    78 10.0    41 10.3  47.4  R      0.146  0.064    -   N LEICA GR30           LEICA GR30            #AR_L5
 CLCT3510 CLIB CTAB    153.910    60 10.0    22 10.3  63.3   E     0.144  0.068    -   - LEICA GR30           LEICA GR30            #AR_L5
 CLCT3510 CLIB CTAB    153.910   233 10.0    97 10.3  58.4 GRE     0.165  0.068    I   N LEICA GR30           LEICA GR30            #AR_L5
 CTWT3510 CTAB WTZR    134.366    85  7.3    22  7.6  74.1 G       0.144  0.054    I   - LEICA GR30           LEICA GR50            #AR_L5
 CTWT3510 CTAB WTZR    134.366    73  7.3    31  7.6  57.5  R      0.148  0.069    -   N LEICA GR30           LEICA GR50            #AR_L5
 CTWT3510 CTAB WTZR    134.366    64  7.3    25  7.6  60.9   E     0.144  0.060    -   - LEICA GR30           LEICA GR50            #AR_L5
 CTWT3510 CTAB WTZR    134.366   222  7.3    78  7.6  64.9 GRE     0.148  0.060    I   N LEICA GR30           LEICA GR50            #AR_L5
 GJNP3510 GJML NPAZ     98.439    84  6.7    21  7.0  75.0 G       0.145  0.051    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GJNP3510 GJML NPAZ     98.439    51  6.7    20  7.0  60.8  R      0.139  0.061    -   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GJNP3510 GJML NPAZ     98.439   135  6.7    41  7.0  69.6 GR      0.145  0.054    I   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GJSI3510 GJML SID0    157.036    80  9.3    22  9.5  72.5 G       0.135  0.051    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GJSI3510 GJML SID0    157.036    58  9.3    34  9.5  41.4  R      0.146  0.053    -   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GJSI3510 GJML SID0    157.036   138  9.3    56  9.5  59.4 GR      0.146  0.052    I   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 GRMO3510 GRAZ MOP2    197.265    78  9.3    19  9.7  75.6 G       0.139  0.060    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_L5
 GRMO3510 GRAZ MOP2    197.265    63  9.3    29  9.7  54.0  R      0.147  0.070    -   N SEPT POLARX5         TRIMBLE ALLOY         #AR_L5
 GRMO3510 GRAZ MOP2    197.265    55  9.3    15  9.7  72.7   E     0.181  0.075    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_L5
 GRMO3510 GRAZ MOP2    197.265   196  9.3    63  9.7  67.9 GRE     0.181  0.067    I   N SEPT POLARX5         TRIMBLE ALLOY         #AR_L5
 KNNP3510 KNJA NPAZ    148.523    76  6.6    19  7.1  75.0 G       0.169  0.067    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 MOPE3510 MOP2 PENC    163.036    88  9.3    22  9.5  75.0 G       0.169  0.065    I   - TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L5
 MOPE3510 MOP2 PENC    163.036    57  9.3    30  9.5  47.4  R      0.147  0.055    -   N TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L5
 MOPE3510 MOP2 PENC    163.036   145  9.3    52  9.5  64.1 GR      0.169  0.063    I   N TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L5
 PESU3510 PENC SUBO    190.168    85 12.3    28 12.8  67.1 G       0.149  0.079    I   - LEICA GRX1200GGPRO   TRIMBLE NETR9         #AR_L5
 SISU3510 SID0 SUBO    113.252    76  8.3    21  8.5  72.4 G       0.135  0.047    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L5
 ----------------------------------------------------------------------------------------------------------------------------------
 Tot:  10              154.379   858  9.7   254 10.0  70.4 G       0.171  0.065                                                     #AR_L5
 Tot:   6              150.676   380  8.7   185  9.0  51.3  R      0.148  0.063                                                     #AR_L5
 Tot:   3              161.847   179  8.9    62  9.3  65.4   E     0.181  0.068                                                     #AR_L5
 Tot:  10              154.379  1417  9.7   501 10.0  64.6 GRE     0.181  0.065                                                     #AR_L5


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Phase-Based Narrowlane (L3) Ambiguity Resolution (<200 km)
================================================================================

 File     Sta1 Sta2    Length     Before     After    Res  Sys     Max/RMS L1    QCB FRQ Receiver 1           Receiver 2
                        (km)    #Amb (mm)  #Amb (mm)  (%)       (L1 Cycles)        
 ----------------------------------------------------------------------------------------------------------------------------------
 BUON3510 BUDD ONSA    187.791   111  0.8    51  0.9  54.1 G       0.148  0.050    I   - SEPT POLARX5         SEPT POLARX5TR        #AR_L3
 CLCT3510 CLIB CTAB    153.910    96  1.2    36  1.2  62.5 G       0.129  0.039    I   - LEICA GR30           LEICA GR30            #AR_L3
 CLCT3510 CLIB CTAB    153.910    78  1.2    41  1.2  47.4  R      0.140  0.049    -   N LEICA GR30           LEICA GR30            #AR_L3
 CLCT3510 CLIB CTAB    153.910    59  1.2    21  1.2  64.4   E     0.098  0.033    -   - LEICA GR30           LEICA GR30            #AR_L3
 CLCT3510 CLIB CTAB    153.910   233  1.2    98  1.2  57.9 GRE     0.140  0.040    I   N LEICA GR30           LEICA GR30            #AR_L3
 CTWT3510 CTAB WTZR    134.366    85  1.2    23  1.2  72.9 G       0.123  0.037    I   - LEICA GR30           LEICA GR50            #AR_L3
 CTWT3510 CTAB WTZR    134.366    73  1.2    32  1.2  56.2  R      0.145  0.053    -   N LEICA GR30           LEICA GR50            #AR_L3
 CTWT3510 CTAB WTZR    134.366    64  1.2    26  1.2  59.4   E     0.081  0.033    -   - LEICA GR30           LEICA GR50            #AR_L3
 CTWT3510 CTAB WTZR    134.366   222  1.2    81  1.2  63.5 GRE     0.145  0.041    I   N LEICA GR30           LEICA GR50            #AR_L3
 GJNP3510 GJML NPAZ     98.439    84  1.2    25  1.2  70.2 G       0.145  0.043    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GJNP3510 GJML NPAZ     98.439    51  1.2    23  1.2  54.9  R      0.105  0.047    -   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GJNP3510 GJML NPAZ     98.439   135  1.2    48  1.2  64.4 GR      0.145  0.044    I   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GJSI3510 GJML SID0    157.036    80  1.5    24  1.5  70.0 G       0.129  0.048    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GJSI3510 GJML SID0    157.036    58  1.5    35  1.5  39.7  R      0.095  0.040    -   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GJSI3510 GJML SID0    157.036   138  1.5    59  1.5  57.2 GR      0.129  0.046    I   N TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 GRMO3510 GRAZ MOP2    197.265    78  1.3    22  1.3  71.8 G       0.132  0.036    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_L3
 GRMO3510 GRAZ MOP2    197.265    63  1.3    33  1.3  47.6  R      0.076  0.034    -   N SEPT POLARX5         TRIMBLE ALLOY         #AR_L3
 GRMO3510 GRAZ MOP2    197.265    55  1.3    19  1.3  65.5   E     0.087  0.027    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_L3
 GRMO3510 GRAZ MOP2    197.265   196  1.3    74  1.3  62.2 GRE     0.132  0.033    I   N SEPT POLARX5         TRIMBLE ALLOY         #AR_L3
 KNNP3510 KNJA NPAZ    148.523    76  1.3    22  1.3  71.1 G       0.112  0.036    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 MOPE3510 MOP2 PENC    163.036    88  1.4    26  1.4  70.5 G       0.112  0.039    I   - TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L3
 MOPE3510 MOP2 PENC    163.036    57  1.4    32  1.4  43.9  R      0.139  0.052    -   N TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L3
 MOPE3510 MOP2 PENC    163.036   145  1.4    58  1.4  60.0 GR      0.139  0.043    I   N TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_L3
 PESU3510 PENC SUBO    190.168    85  1.5    30  1.6  64.7 G       0.130  0.051    I   - LEICA GRX1200GGPRO   TRIMBLE NETR9         #AR_L3
 SISU3510 SID0 SUBO    113.252    76  1.6    21  1.7  72.4 G       0.128  0.053    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_L3
 ----------------------------------------------------------------------------------------------------------------------------------
 Tot:  10              154.379   859  1.3   280  1.3  67.4 G       0.148  0.044                                                     #AR_L3
 Tot:   6              150.676   380  1.3   196  1.3  48.4  R      0.145  0.047                                                     #AR_L3
 Tot:   3              161.847   178  1.2    66  1.2  62.9   E     0.098  0.031                                                     #AR_L3
 Tot:  10              154.379  1417  1.3   542  1.3  61.8 GRE     0.148  0.043                                                     #AR_L3


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Quasi-Ionosphere-Free (QIF) Ambiguity Resolution (<2000 km)
================================================================================

 File     Sta1 Sta2    Length     Before     After    Res  Sys     Max/RMS L5    Max/RMS L3    QCB FRQ Receiver 1           Receiver 2
                        (km)    #Amb (mm)  #Amb (mm)  (%)       (L5 Cycles)   (L3 Cycles)        
 ------------------------------------------------------------------------------------------------------------------------------------------------
 ACBR3510 ACOR BRST    634.078    46  1.3    44  1.4   4.3 G       0.060  0.042  0.016  0.011    I   - LEICA GR50           TRIMBLE ALLOY         #AR_QIF
 ADAR3510 ADAR ARIS    464.061    84  1.7    78  1.7   7.1 G       0.482  0.202  0.082  0.044    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 ADAR3510 ADAR ARIS    464.061   142  1.7   102  1.7  28.2  R      0.387  0.147  0.086  0.030    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 ADAR3510 ADAR ARIS    464.061   226  1.7   180  1.7  20.4 GR      0.482  0.156  0.086  0.032    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 ADSC3510 ADAR SCIL    337.602    68  1.3    66  1.3   2.9 G       0.355  0.251  0.098  0.069    I   - SEPT POLARX5         SEPT POLARX5          #AR_QIF
 ADSC3510 ADAR SCIL    337.602   136  1.3    84  1.3  38.2  R      0.493  0.172  0.091  0.031    -   - SEPT POLARX5         SEPT POLARX5          #AR_QIF
 ADSC3510 ADAR SCIL    337.602    30  1.3    30  1.3   0.0   E     0.000  0.000  0.000  0.000    -   - SEPT POLARX5         SEPT POLARX5          #AR_QIF
 ADSC3510 ADAR SCIL    337.602   234  1.3   180  1.3  23.1 GRE     0.493  0.176  0.098  0.033    I   - SEPT POLARX5         SEPT POLARX5          #AR_QIF
 BOCL3510 BOR1 CLIB    218.102    64  1.2    60  1.2   6.2 G       0.079  0.042  0.007  0.004    I   - TRIMBLE NETR9        LEICA GR30            #AR_QIF
 BOCL3510 BOR1 CLIB    218.102   138  1.2    72  1.2  47.8  R      0.403  0.087  0.088  0.025    -   - TRIMBLE NETR9        LEICA GR30            #AR_QIF
 BOCL3510 BOR1 CLIB    218.102    34  1.2    28  1.2  17.6   E     0.454  0.190  0.079  0.037    -   - TRIMBLE NETR9        LEICA GR30            #AR_QIF
 BOCL3510 BOR1 CLIB    218.102   236  1.2   160  1.2  32.2 GRE     0.454  0.098  0.088  0.025    I   - TRIMBLE NETR9        LEICA GR30            #AR_QIF
 BOJO3510 BOR1 JOZE    271.387    18  1.1    18  1.1   0.0 G       0.000  0.000  0.000  0.000    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_QIF
 BOJO3510 BOR1 JOZE    271.387   120  1.1    50  1.1  58.3  R      0.495  0.109  0.076  0.016    -   - TRIMBLE NETR9        SEPT POLARX5          #AR_QIF
 BOJO3510 BOR1 JOZE    271.387    24  1.1    18  1.1  25.0   E     0.150  0.075  0.025  0.010    -   - TRIMBLE NETR9        SEPT POLARX5          #AR_QIF
 BOJO3510 BOR1 JOZE    271.387   162  1.1    86  1.1  46.9 GRE     0.495  0.107  0.076  0.016    I   - TRIMBLE NETR9        SEPT POLARX5          #AR_QIF
 BRLR3510 BRST LROC    349.903    60  1.1    60  1.1   0.0 G       0.000  0.000  0.000  0.000    I   - TRIMBLE ALLOY        LEICA GR25            #AR_QIF
 BRLR3510 BRST LROC    349.903    96  1.1    50  1.1  47.9  R      0.364  0.087  0.050  0.018    -   - TRIMBLE ALLOY        LEICA GR25            #AR_QIF
 BRLR3510 BRST LROC    349.903   134  1.1    18  1.1  86.6   E     0.439  0.142  0.096  0.026    -   - TRIMBLE ALLOY        LEICA GR25            #AR_QIF
 BRLR3510 BRST LROC    349.903   290  1.1   128  1.1  55.9 GRE     0.439  0.129  0.096  0.024    I   - TRIMBLE ALLOY        LEICA GR25            #AR_QIF
 BRSC3510 BRST SCIL    215.237    36  1.2    32  1.2  11.1 G       0.238  0.129  0.023  0.012    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_QIF
 BRSC3510 BRST SCIL    215.237   118  1.2    52  1.2  55.9  R      0.407  0.117  0.098  0.032    -   - TRIMBLE ALLOY        SEPT POLARX5          #AR_QIF
 BRSC3510 BRST SCIL    215.237    34  1.2    30  1.2  11.8   E     0.116  0.079  0.091  0.046    -   - TRIMBLE ALLOY        SEPT POLARX5          #AR_QIF
 BRSC3510 BRST SCIL    215.237   188  1.2   114  1.2  39.4 GRE     0.407  0.116  0.098  0.032    I   - TRIMBLE ALLOY        SEPT POLARX5          #AR_QIF
 BUON3510 BUDD ONSA    187.791   102  1.0    80  1.0  21.6 G       0.447  0.209  0.099  0.039    I   - SEPT POLARX5         SEPT POLARX5TR        #AR_QIF
 BUPO3510 BUDD POTS    375.723    56  2.2    52  2.2   7.1 G       0.290  0.145  0.016  0.008    I   - SEPT POLARX5         JAVAD TRE_3           #AR_QIF
 BUPO3510 BUDD POTS    375.723   144  2.2   102  2.2  29.2  R      0.348  0.154  0.091  0.035    -   - SEPT POLARX5         JAVAD TRE_3           #AR_QIF
 BUPO3510 BUDD POTS    375.723    36  2.2    34  2.2   5.6   E     0.292  0.206  0.008  0.006    -   - SEPT POLARX5         JAVAD TRE_3           #AR_QIF
 BUPO3510 BUDD POTS    375.723   236  2.2   188  2.2  20.3 GRE     0.348  0.156  0.091  0.033    I   - SEPT POLARX5         JAVAD TRE_3           #AR_QIF
 CLCT3510 CLIB CTAB    153.910    72  1.3    68  1.3   5.6 G       0.383  0.260  0.071  0.042    I   - LEICA GR30           LEICA GR30            #AR_QIF
 CLCT3510 CLIB CTAB    153.910    82  1.3    70  1.3  14.6  R      0.419  0.213  0.088  0.033    -   - LEICA GR30           LEICA GR30            #AR_QIF
 CLCT3510 CLIB CTAB    153.910    44  1.3    36  1.3  18.2   E     0.437  0.235  0.047  0.025    -   - LEICA GR30           LEICA GR30            #AR_QIF
 CLCT3510 CLIB CTAB    153.910   198  1.3   174  1.3  12.1 GRE     0.437  0.229  0.088  0.032    I   - LEICA GR30           LEICA GR30            #AR_QIF
 CLPO3510 CLIB POTS    226.025    84  2.2    78  2.3   7.1 G       0.394  0.164  0.024  0.012    I   - LEICA GR30           JAVAD TRE_3           #AR_QIF
 CLPO3510 CLIB POTS    226.025   166  2.2   108  2.3  34.9  R      0.480  0.125  0.099  0.037    -   - LEICA GR30           JAVAD TRE_3           #AR_QIF
 CLPO3510 CLIB POTS    226.025    50  2.2    50  2.3   0.0   E     0.000  0.000  0.000  0.000    -   - LEICA GR30           JAVAD TRE_3           #AR_QIF
 CLPO3510 CLIB POTS    226.025   300  2.2   236  2.3  21.3 GRE     0.480  0.129  0.099  0.035    I   - LEICA GR30           JAVAD TRE_3           #AR_QIF
 CTMO3510 CTAB MOP2    222.418    48  1.5    38  1.5  20.8 G       0.234  0.116  0.038  0.014    I   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 CTMO3510 CTAB MOP2    222.418   130  1.5    66  1.5  49.2  R      0.484  0.093  0.081  0.026    -   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 CTMO3510 CTAB MOP2    222.418    62  1.5    52  1.5  16.1   E     0.319  0.141  0.053  0.022    -   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 CTMO3510 CTAB MOP2    222.418   240  1.5   156  1.5  35.0 GRE     0.484  0.103  0.081  0.024    I   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 CTWT3510 CTAB WTZR    134.366    44  1.3    44  1.3   0.0 G       0.000  0.000  0.000  0.000    I   - LEICA GR30           LEICA GR50            #AR_QIF
 CTWT3510 CTAB WTZR    134.366    64  1.3    56  1.3  12.5  R      0.377  0.201  0.079  0.039    -   - LEICA GR30           LEICA GR50            #AR_QIF
 CTWT3510 CTAB WTZR    134.366    54  1.3    48  1.3  11.1   E     0.287  0.137  0.018  0.008    -   - LEICA GR30           LEICA GR50            #AR_QIF
 CTWT3510 CTAB WTZR    134.366   162  1.3   148  1.3   8.6 GRE     0.377  0.176  0.079  0.030    I   - LEICA GR30           LEICA GR50            #AR_QIF
 DEIG3510 DEVA IGEO    473.005   112  1.2    96  1.2  14.3 G       0.394  0.138  0.100  0.036    I   - LEICA GR50           LEICA GR10            #AR_QIF
 DEIG3510 DEVA IGEO    473.005   106  1.2    50  1.2  52.8  R      0.433  0.145  0.068  0.020    -   - LEICA GR50           LEICA GR10            #AR_QIF
 DEIG3510 DEVA IGEO    473.005    42  1.2    28  1.2  33.3   E     0.458  0.218  0.092  0.032    -   - LEICA GR50           LEICA GR10            #AR_QIF
 DEIG3510 DEVA IGEO    473.005   260  1.2   174  1.2  33.1 GRE     0.458  0.158  0.100  0.026    I   - LEICA GR50           LEICA GR10            #AR_QIF
 DESU3510 DEVA SUBO    252.701    78  1.4    76  1.4   2.6 G       0.064  0.045  0.087  0.062    I   - LEICA GR50           TRIMBLE NETR9         #AR_QIF
 DLML3510 DLF1 MLVL    372.424    34  1.1    26  1.1  23.5 G       0.206  0.099  0.064  0.024    I   - TRIMBLE ALLOY        LEICA GR50            #AR_QIF
 DLML3510 DLF1 MLVL    372.424   122  1.1    70  1.1  42.6  R      0.446  0.148  0.092  0.029    -   - TRIMBLE ALLOY        LEICA GR50            #AR_QIF
 DLML3510 DLF1 MLVL    372.424    32  1.1    26  1.1  18.8   E     0.488  0.269  0.053  0.024    -   - TRIMBLE ALLOY        LEICA GR50            #AR_QIF
 DLML3510 DLF1 MLVL    372.424   188  1.1   122  1.1  35.1 GRE     0.488  0.158  0.092  0.028    I   - TRIMBLE ALLOY        LEICA GR50            #AR_QIF
 GJNP3510 GJML NPAZ     98.439    50  1.3    48  1.3   4.0 G       0.285  0.202  0.040  0.028    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GJNP3510 GJML NPAZ     98.439    46  1.3    46  1.3   0.0  R      0.000  0.000  0.000  0.000    -   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GJNP3510 GJML NPAZ     98.439    96  1.3    94  1.3   2.1 GR      0.285  0.202  0.040  0.028    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GJSI3510 GJML SID0    157.036    48  1.6    46  1.6   4.2 G       0.396  0.280  0.072  0.051    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GJSI3510 GJML SID0    157.036    70  1.6    64  1.6   8.6  R      0.469  0.234  0.094  0.054    -   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GJSI3510 GJML SID0    157.036   118  1.6   110  1.6   6.8 GR      0.469  0.247  0.094  0.053    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 GLIG3510 GLSV IGEO    390.120    64  1.3    58  1.3   9.4 G       0.148  0.068  0.097  0.040    I   - TRIMBLE NETR9        LEICA GR10            #AR_QIF
 GLIG3510 GLSV IGEO    390.120   136  1.3   102  1.3  25.0  R      0.417  0.140  0.099  0.044    -   - TRIMBLE NETR9        LEICA GR10            #AR_QIF
 GLIG3510 GLSV IGEO    390.120    44  1.3    30  1.3  31.8   E     0.483  0.244  0.070  0.024    -   - TRIMBLE NETR9        LEICA GR10            #AR_QIF
 GLIG3510 GLSV IGEO    390.120   244  1.3   190  1.3  22.1 GRE     0.483  0.168  0.099  0.039    I   - TRIMBLE NETR9        LEICA GR10            #AR_QIF
 GRMO3510 GRAZ MOP2    197.265    42  1.4    36  1.4  14.3 G       0.469  0.223  0.088  0.039    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRMO3510 GRAZ MOP2    197.265    66  1.4    56  1.4  15.2  R      0.470  0.247  0.090  0.036    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRMO3510 GRAZ MOP2    197.265    40  1.4    34  1.4  15.0   E     0.198  0.088  0.099  0.041    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRMO3510 GRAZ MOP2    197.265   148  1.4   126  1.4  14.9 GRE     0.470  0.208  0.099  0.038    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRZA3510 GRAZ ZADA    328.946    36  1.3    34  1.3   5.6 G       0.182  0.129  0.002  0.001    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRZA3510 GRAZ ZADA    328.946   122  1.3    68  1.3  44.3  R      0.432  0.125  0.071  0.020    -   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 GRZA3510 GRAZ ZADA    328.946   158  1.3   102  1.3  35.4 GR      0.432  0.125  0.071  0.019    I   - SEPT POLARX5         TRIMBLE ALLOY         #AR_QIF
 IMZA3510 IGMI ZADA    324.039    46  1.2    40  1.3  13.0 G       0.312  0.137  0.086  0.039    I   - STONEX SC2200        TRIMBLE ALLOY         #AR_QIF
 IMZA3510 IGMI ZADA    324.039   108  1.2    64  1.3  40.7  R      0.441  0.089  0.093  0.028    -   - STONEX SC2200        TRIMBLE ALLOY         #AR_QIF
 IMZA3510 IGMI ZADA    324.039   154  1.2   104  1.3  32.5 GR      0.441  0.096  0.093  0.029    I   - STONEX SC2200        TRIMBLE ALLOY         #AR_QIF
 IMZI3510 IGMI ZIM2    451.084    60  1.3    56  1.3   6.7 G       0.134  0.073  0.060  0.037    I   - STONEX SC2200        TRIMBLE NETR9         #AR_QIF
 IMZI3510 IGMI ZIM2    451.084   116  1.3    72  1.3  37.9  R      0.361  0.140  0.031  0.014    -   - STONEX SC2200        TRIMBLE NETR9         #AR_QIF
 IMZI3510 IGMI ZIM2    451.084   176  1.3   128  1.3  27.3 GR      0.361  0.136  0.060  0.017    I   - STONEX SC2200        TRIMBLE NETR9         #AR_QIF
 KNNP3510 KNJA NPAZ    148.523    44  1.4    44  1.4   0.0 G       0.000  0.000  0.000  0.000    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 LRML3510 LROC MLVL    413.570    74  1.2    64  1.2  13.5 G       0.454  0.153  0.099  0.052    I   - LEICA GR25           LEICA GR50            #AR_QIF
 LRML3510 LROC MLVL    413.570    96  1.2    52  1.2  45.8  R      0.330  0.107  0.067  0.025    -   - LEICA GR25           LEICA GR50            #AR_QIF
 LRML3510 LROC MLVL    413.570   136  1.2    22  1.2  83.8   E     0.394  0.119  0.093  0.030    -   - LEICA GR25           LEICA GR50            #AR_QIF
 LRML3510 LROC MLVL    413.570   306  1.2   138  1.2  54.9 GRE     0.454  0.118  0.099  0.031    I   - LEICA GR25           LEICA GR50            #AR_QIF
 LRTL3510 LROC TLSE    358.965    46  1.0    44  1.0   4.3 G       0.066  0.047  0.003  0.002    I   - LEICA GR25           TRIMBLE ALLOY         #AR_QIF
 LRTL3510 LROC TLSE    358.965    90  1.0    48  1.0  46.7  R      0.274  0.088  0.042  0.015    -   - LEICA GR25           TRIMBLE ALLOY         #AR_QIF
 LRTL3510 LROC TLSE    358.965   128  1.0    16  1.0  87.5   E     0.417  0.143  0.097  0.027    -   - LEICA GR25           TRIMBLE ALLOY         #AR_QIF
 LRTL3510 LROC TLSE    358.965   264  1.0   108  1.0  59.1 GRE     0.417  0.130  0.097  0.024    I   - LEICA GR25           TRIMBLE ALLOY         #AR_QIF
 MAZA3510 MATE ZADA    403.485   104  1.2   100  1.2   3.8 G       0.159  0.080  0.012  0.006    I   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 MAZA3510 MATE ZADA    403.485   120  1.2    70  1.2  41.7  R      0.386  0.124  0.076  0.022    -   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 MAZA3510 MATE ZADA    403.485   224  1.2   170  1.2  24.1 GR      0.386  0.121  0.076  0.021    I   - LEICA GR30           TRIMBLE ALLOY         #AR_QIF
 MLZI3510 MLVL ZIM2    425.163    72  1.2    60  1.2  16.7 G       0.307  0.128  0.072  0.028    I   - LEICA GR50           TRIMBLE NETR9         #AR_QIF
 MLZI3510 MLVL ZIM2    425.163   140  1.2    82  1.2  41.4  R      0.483  0.119  0.087  0.031    -   - LEICA GR50           TRIMBLE NETR9         #AR_QIF
 MLZI3510 MLVL ZIM2    425.163    30  1.2    24  1.2  20.0   E     0.085  0.041  0.086  0.036    -   - LEICA GR50           TRIMBLE NETR9         #AR_QIF
 MLZI3510 MLVL ZIM2    425.163   242  1.2   166  1.2  31.4 GRE     0.483  0.117  0.087  0.031    I   - LEICA GR50           TRIMBLE NETR9         #AR_QIF
 MOPE3510 MOP2 PENC    163.036    52  1.5    50  1.5   3.8 G       0.363  0.257  0.059  0.042    I   - TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_QIF
 MOPE3510 MOP2 PENC    163.036    64  1.5    58  1.5   9.4  R      0.388  0.212  0.032  0.013    -   - TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_QIF
 MOPE3510 MOP2 PENC    163.036   116  1.5   108  1.5   6.9 GR      0.388  0.224  0.059  0.024    I   - TRIMBLE ALLOY        LEICA GRX1200GGPRO    #AR_QIF
 ONVS3510 ONSA VIS0    386.828    44  1.0    44  1.0   0.0 G       0.000  0.000  0.000  0.000    I   - SEPT POLARX5TR       SEPT POLARX5          #AR_QIF
 PESU3510 PENC SUBO    190.168    60  1.7    58  1.7   3.3 G       0.434  0.307  0.016  0.011    I   - LEICA GRX1200GGPRO   TRIMBLE NETR9         #AR_QIF
 RIVS3510 RIGA VIS0    351.802    64  1.1    60  1.1   6.2 G       0.403  0.202  0.019  0.011    I   - LEICA GR25           SEPT POLARX5          #AR_QIF
 RIVS3510 RIGA VIS0    351.802   140  1.1    54  1.1  61.4  R      0.458  0.137  0.098  0.025    -   - LEICA GR25           SEPT POLARX5          #AR_QIF
 RIVS3510 RIGA VIS0    351.802   204  1.1   114  1.1  44.1 GR      0.458  0.141  0.098  0.024    I   - LEICA GR25           SEPT POLARX5          #AR_QIF
 SISU3510 SID0 SUBO    113.252    42  1.9    42  1.9   0.0 G       0.000  0.000  0.000  0.000    I   - TRIMBLE NETR9        TRIMBLE NETR9         #AR_QIF
 ------------------------------------------------------------------------------------------------------------------------------------------------
 Tot:  33              296.680  1954  1.4  1800  1.4   7.9 G       0.482  0.164  0.100  0.034                                                     #AR_QIF
 Tot:  26              302.966  2878  1.4  1768  1.4  38.6  R      0.495  0.129  0.099  0.027                                                     #AR_QIF
 Tot:  17              302.070   954  1.4   524  1.4  45.1   E     0.488  0.147  0.099  0.028                                                     #AR_QIF
 Tot:  33              296.680  5786  1.4  4092  1.4  29.3 GRE     0.495  0.138  0.100  0.028                                                     #AR_QIF


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Direct L1/L2 Ambiguity Resolution (<10 km)
================================================================================

 ----------------------------------------------------------------------------------------------------------------------------------


Legend:
 QCB  consider GPS quarter-cycle bias : - (not applicable) N (never) A (always) I (indicated) S (selected)
 FRQ  GLONASS resolution between freq.: - (not applicable) N (never) A (always) T (same rcvr. type) M (same rcvr. model)


================================================================================
 Station-wise Ambiguity Resolution Statistics
================================================================================


 ===============================================================================
 Bernese GNSS Software, Version 5.4
 -------------------------------------------------------------------------------
 Program        : OBSXTR
 Purpose        : Extract statistics from observation file header
 -------------------------------------------------------------------------------
 Campaign       : ${P}/EPNB23
 Default session: 3510 year 2023
 Date           : 23-May-2026 00:20:05
 User name      : bpe54
 ===============================================================================


 NTUA_DDP_20233510: Extraction from ambiguity resolution
 -------------------------------------------------------------------------------


 INPUT AND OUTPUT FILENAMES
 --------------------------

 -------------------------------------------------------------------------------
 General constants               : ${MODEL}/CONST.BSW
 Satellite information           : ${CONFIG}/SATELLIT_I20.SAT
 File with the list of selected R:  ---
 File with the list of unselected:  ---
 Summary file                    : ${P}/EPNB23/OUT/TMP_20233510.SUM
 Program output                  : ${P}/EPNB23/OUT/TMP_20233510.OUT
 Error message                   : ${U}/WORK/ERROR.MSG
 Session table                   : ${P}/EPNB23/GEN/SESSIONS.SES
 -------------------------------------------------------------------------------


                                                   numb.   ambiguity resolution statistics
 File   Station 1         Station 2            Sys  sat    total     L1           L2           L5        Filename
 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    1   ACOR 13434M001    BRST 10004M004       GPS   31       77     23 70.1%     23 70.1%     20 74.0%  ACBR3510.PSH  #AMB
    1   ACOR 13434M001    BRST 10004M004       tot   31       77     23 70.1%     23 70.1%     20 74.0%  ACBR3510.PSH  #AMB
    2   ADAR 19161M001    ARIS 19190M001       GPS   31      106     40 62.3%     40 62.3%     37 65.1%  ADAR3510.PSH  #AMB
    2   ADAR 19161M001    ARIS 19190M001       GLO   21       71     51 28.2%     51 28.2%     71  0.0%  ADAR3510.PSH  #AMB
    2   ADAR 19161M001    ARIS 19190M001       tot   52      177     91 48.6%     91 48.6%    108 39.0%  ADAR3510.PSH  #AMB
    3   ADAR 19161M001    SCIL 19201M001       GPS   31      103     34 67.0%     34 67.0%     17 83.5%  ADSC3510.PSH  #AMB
    3   ADAR 19161M001    SCIL 19201M001       GLO   21       68     42 38.2%     42 38.2%     68  0.0%  ADSC3510.PSH  #AMB
    3   ADAR 19161M001    SCIL 19201M001       GAL   23       57     15 73.7%     15 73.7%      4 93.0%  ADSC3510.PSH  #AMB
    3   ADAR 19161M001    SCIL 19201M001       tot   75      228     91 60.1%     91 60.1%     89 61.0%  ADSC3510.PSH  #AMB
    4   BOR1 12205M002    CLIB 11526M001       GPS   31       93     31 66.7%     31 66.7%     24 74.2%  BOCL3510.PSH  #AMB
    4   BOR1 12205M002    CLIB 11526M001       GLO   21       69     36 47.8%     36 47.8%     69  0.0%  BOCL3510.PSH  #AMB
    4   BOR1 12205M002    CLIB 11526M001       GAL   23       59     15 74.6%     15 74.6%     15 74.6%  BOCL3510.PSH  #AMB
    4   BOR1 12205M002    CLIB 11526M001       tot   75      221     82 62.9%     82 62.9%    108 51.1%  BOCL3510.PSH  #AMB
    5   BOR1 12205M002    JOZE 12204M001       GPS   31       69     10 85.5%     10 85.5%      7 89.9%  BOJO3510.PSH  #AMB
    5   BOR1 12205M002    JOZE 12204M001       GLO   21       60     26 56.7%     26 56.7%     60  0.0%  BOJO3510.PSH  #AMB
    5   BOR1 12205M002    JOZE 12204M001       GAL   25       65      9 86.2%      9 86.2%      8 87.7%  BOJO3510.PSH  #AMB
    5   BOR1 12205M002    JOZE 12204M001       tot   77      194     45 76.8%     45 76.8%     75 61.3%  BOJO3510.PSH  #AMB
    6   BRST 10004M004    LROC 10023M001       GPS   31       84     31 63.1%     31 63.1%     24 71.4%  BRLR3510.PSH  #AMB
    6   BRST 10004M004    LROC 10023M001       GLO   20       48     25 47.9%     25 47.9%     48  0.0%  BRLR3510.PSH  #AMB
    6   BRST 10004M004    LROC 10023M001       GAL   22       67      9 86.6%      9 86.6%     67  0.0%  BRLR3510.PSH  #AMB
    6   BRST 10004M004    LROC 10023M001       tot   73      199     65 67.3%     65 67.3%    139 30.2%  BRLR3510.PSH  #AMB
    7   BRST 10004M004    SCIL 19201M001       GPS   31       76     17 77.6%     17 77.6%     11 85.5%  BRSC3510.PSH  #AMB
    7   BRST 10004M004    SCIL 19201M001       GLO   21       59     26 55.9%     26 55.9%     59  0.0%  BRSC3510.PSH  #AMB
    7   BRST 10004M004    SCIL 19201M001       GAL   23       57     15 73.7%     15 73.7%     12 78.9%  BRSC3510.PSH  #AMB
    7   BRST 10004M004    SCIL 19201M001       tot   75      192     58 69.8%     58 69.8%     82 57.3%  BRSC3510.PSH  #AMB
    8   BUDD 10101S001    ONSA 10402M004       GPS   31      112     41 63.4%     41 63.4%     47 58.0%  BUON3510.PSH  #AMB
    8   BUDD 10101S001    ONSA 10402M004       tot   31      112     41 63.4%     41 63.4%     47 58.0%  BUON3510.PSH  #AMB
    9   BUDD 10101S001    POTS 14106M003       GPS   31      101     27 73.3%     27 73.3%     26 74.3%  BUPO3510.PSH  #AMB
    9   BUDD 10101S001    POTS 14106M003       GLO   21       72     52 27.8%     52 27.8%     72  0.0%  BUPO3510.PSH  #AMB
    9   BUDD 10101S001    POTS 14106M003       GAL   23       64     17 73.4%     17 73.4%     12 81.2%  BUPO3510.PSH  #AMB
    9   BUDD 10101S001    POTS 14106M003       tot   75      237     96 59.5%     96 59.5%    110 53.6%  BUPO3510.PSH  #AMB
   10   CLIB 11526M001    CTAB 11529M001       GPS   31       96     35 63.5%     35 63.5%     35 63.5%  CLCT3510.PSH  #AMB
   10   CLIB 11526M001    CTAB 11529M001       GLO   21       78     35 55.1%     35 55.1%     41 47.4%  CLCT3510.PSH  #AMB
   10   CLIB 11526M001    CTAB 11529M001       GAL   23       60     18 70.0%     18 70.0%     22 63.3%  CLCT3510.PSH  #AMB
   10   CLIB 11526M001    CTAB 11529M001       tot   75      234     88 62.4%     88 62.4%     98 58.1%  CLCT3510.PSH  #AMB
   11   CLIB 11526M001    POTS 14106M003       GPS   31      107     40 62.6%     40 62.6%     32 70.1%  CLPO3510.PSH  #AMB
   11   CLIB 11526M001    POTS 14106M003       GLO   21       83     55 33.7%     55 33.7%     83  0.0%  CLPO3510.PSH  #AMB
   11   CLIB 11526M001    POTS 14106M003       GAL   23       67     25 62.7%     25 62.7%     22 67.2%  CLPO3510.PSH  #AMB
   11   CLIB 11526M001    POTS 14106M003       tot   75      257    120 53.3%    120 53.3%    137 46.7%  CLPO3510.PSH  #AMB
   12   CTAB 11529M001    MOP2 11507M002       GPS   31       80     20 75.0%     20 75.0%     22 72.5%  CTMO3510.PSH  #AMB
   12   CTAB 11529M001    MOP2 11507M002       GLO   21       65     33 49.2%     33 49.2%     65  0.0%  CTMO3510.PSH  #AMB
   12   CTAB 11529M001    MOP2 11507M002       GAL   23       66     27 59.1%     27 59.1%     27 59.1%  CTMO3510.PSH  #AMB
   12   CTAB 11529M001    MOP2 11507M002       tot   75      211     80 62.1%     80 62.1%    114 46.0%  CTMO3510.PSH  #AMB
   13   CTAB 11529M001    WTZR 14201M010       GPS   31       85     23 72.9%     23 72.9%     22 74.1%  CTWT3510.PSH  #AMB
   13   CTAB 11529M001    WTZR 14201M010       GLO   21       73     28 61.6%     28 61.6%     31 57.5%  CTWT3510.PSH  #AMB
   13   CTAB 11529M001    WTZR 14201M010       GAL   23       65     25 61.5%     25 61.5%     26 60.0%  CTWT3510.PSH  #AMB
   13   CTAB 11529M001    WTZR 14201M010       tot   75      223     76 65.9%     76 65.9%     79 64.6%  CTWT3510.PSH  #AMB
   14   DEVA 11408M001    IGEO 15101M001       GPS   31      105     49 53.3%     49 53.3%     54 48.6%  DEIG3510.PSH  #AMB
   14   DEVA 11408M001    IGEO 15101M001       GLO   21       53     25 52.8%     25 52.8%     53  0.0%  DEIG3510.PSH  #AMB
   14   DEVA 11408M001    IGEO 15101M001       GAL   17       41     14 65.9%     14 65.9%     21 48.8%  DEIG3510.PSH  #AMB
   14   DEVA 11408M001    IGEO 15101M001       tot   69      199     88 55.8%     88 55.8%    128 35.7%  DEIG3510.PSH  #AMB
   15   DEVA 11408M001    SUBO 12116M001       GPS   31      102     39 61.8%     39 61.8%     32 68.6%  DESU3510.PSH  #AMB
   15   DEVA 11408M001    SUBO 12116M001       tot   31      102     39 61.8%     39 61.8%     32 68.6%  DESU3510.PSH  #AMB
   16   DLF1 13502M009    MLVL 10092M001       GPS   31       77     14 81.8%     14 81.8%     16 79.2%  DLML3510.PSH  #AMB
   16   DLF1 13502M009    MLVL 10092M001       GLO   21       61     35 42.6%     35 42.6%     61  0.0%  DLML3510.PSH  #AMB
   16   DLF1 13502M009    MLVL 10092M001       GAL   25       53     13 75.5%     13 75.5%     14 73.6%  DLML3510.PSH  #AMB
   16   DLF1 13502M009    MLVL 10092M001       tot   77      191     62 67.5%     62 67.5%     91 52.4%  DLML3510.PSH  #AMB
   17   GJML 12121M001    NPAZ 12110M001       GPS   31       85     25 70.6%     25 70.6%     22 74.1%  GJNP3510.PSH  #AMB
   17   GJML 12121M001    NPAZ 12110M001       GLO   21       51     23 54.9%     23 54.9%     20 60.8%  GJNP3510.PSH  #AMB
   17   GJML 12121M001    NPAZ 12110M001       tot   52      136     48 64.7%     48 64.7%     42 69.1%  GJNP3510.PSH  #AMB
   18   GJML 12121M001    SID0 12132M001       GPS   31       81     24 70.4%     24 70.4%     23 71.6%  GJSI3510.PSH  #AMB
   18   GJML 12121M001    SID0 12132M001       GLO   21       58     32 44.8%     32 44.8%     34 41.4%  GJSI3510.PSH  #AMB
   18   GJML 12121M001    SID0 12132M001       tot   52      139     56 59.7%     56 59.7%     57 59.0%  GJSI3510.PSH  #AMB
   19   GLSV 12356M001    IGEO 15101M001       GPS   31       95     30 68.4%     30 68.4%     26 72.6%  GLIG3510.PSH  #AMB
   19   GLSV 12356M001    IGEO 15101M001       GLO   21       69     53 23.2%     53 23.2%     69  0.0%  GLIG3510.PSH  #AMB
   19   GLSV 12356M001    IGEO 15101M001       GAL   17       45     15 66.7%     15 66.7%     20 55.6%  GLIG3510.PSH  #AMB
   19   GLSV 12356M001    IGEO 15101M001       tot   69      209     98 53.1%     98 53.1%    115 45.0%  GLIG3510.PSH  #AMB
   20   GRAZ 11001M002    MOP2 11507M002       GPS   31       78     19 75.6%     19 75.6%     19 75.6%  GRMO3510.PSH  #AMB
   20   GRAZ 11001M002    MOP2 11507M002       GLO   21       63     28 55.6%     28 55.6%     29 54.0%  GRMO3510.PSH  #AMB
   20   GRAZ 11001M002    MOP2 11507M002       GAL   23       56     18 67.9%     18 67.9%     16 71.4%  GRMO3510.PSH  #AMB
   20   GRAZ 11001M002    MOP2 11507M002       tot   75      197     65 67.0%     65 67.0%     64 67.5%  GRMO3510.PSH  #AMB
   21   GRAZ 11001M002    ZADA 11905M001       GPS   31       75     18 76.0%     18 76.0%     15 80.0%  GRZA3510.PSH  #AMB
   21   GRAZ 11001M002    ZADA 11905M001       GLO   21       61     35 42.6%     35 42.6%     61  0.0%  GRZA3510.PSH  #AMB
   21   GRAZ 11001M002    ZADA 11905M001       tot   52      136     53 61.0%     53 61.0%     76 44.1%  GRZA3510.PSH  #AMB
   22   IGMI 12701M003    ZADA 11905M001       GPS   31       84     21 75.0%     21 75.0%     20 76.2%  IMZA3510.PSH  #AMB
   22   IGMI 12701M003    ZADA 11905M001       GLO   21       54     32 40.7%     32 40.7%     54  0.0%  IMZA3510.PSH  #AMB
   22   IGMI 12701M003    ZADA 11905M001       tot   52      138     53 61.6%     53 61.6%     74 46.4%  IMZA3510.PSH  #AMB
   23   IGMI 12701M003    ZIM2 14001M008       GPS   31       89     29 67.4%     29 67.4%     27 69.7%  IMZI3510.PSH  #AMB
   23   IGMI 12701M003    ZIM2 14001M008       GLO   21       58     36 37.9%     36 37.9%     58  0.0%  IMZI3510.PSH  #AMB
   23   IGMI 12701M003    ZIM2 14001M008       tot   52      147     65 55.8%     65 55.8%     85 42.2%  IMZI3510.PSH  #AMB
   24   KNJA 12113M001    NPAZ 12110M001       GPS   31       77     23 70.1%     23 70.1%     20 74.0%  KNNP3510.PSH  #AMB
   24   KNJA 12113M001    NPAZ 12110M001       tot   31       77     23 70.1%     23 70.1%     20 74.0%  KNNP3510.PSH  #AMB
   25   LROC 10023M001    MLVL 10092M001       GPS   31       87     33 62.1%     33 62.1%     34 60.9%  LRML3510.PSH  #AMB
   25   LROC 10023M001    MLVL 10092M001       GLO   20       48     26 45.8%     26 45.8%     48  0.0%  LRML3510.PSH  #AMB
   25   LROC 10023M001    MLVL 10092M001       GAL   22       69     11 84.1%     11 84.1%     68  1.4%  LRML3510.PSH  #AMB
   25   LROC 10023M001    MLVL 10092M001       tot   73      204     70 65.7%     70 65.7%    150 26.5%  LRML3510.PSH  #AMB
   26   LROC 10023M001    TLSE 10003M009       GPS   31       82     23 72.0%     23 72.0%     20 75.6%  LRTL3510.PSH  #AMB
   26   LROC 10023M001    TLSE 10003M009       GLO   20       45     24 46.7%     24 46.7%     45  0.0%  LRTL3510.PSH  #AMB
   26   LROC 10023M001    TLSE 10003M009       GAL   22       66      8 87.9%      8 87.9%     64  3.0%  LRTL3510.PSH  #AMB
   26   LROC 10023M001    TLSE 10003M009       tot   73      193     55 71.5%     55 71.5%    129 33.2%  LRTL3510.PSH  #AMB
   27   MATE 12734M008    ZADA 11905M001       GPS   31      108     51 52.8%     51 52.8%     50 53.7%  MAZA3510.PSH  #AMB
   27   MATE 12734M008    ZADA 11905M001       GLO   21       60     36 40.0%     36 40.0%     60  0.0%  MAZA3510.PSH  #AMB
   27   MATE 12734M008    ZADA 11905M001       tot   52      168     87 48.2%     87 48.2%    110 34.5%  MAZA3510.PSH  #AMB
   28   MLVL 10092M001    ZIM2 14001M008       GPS   31       90     31 65.6%     31 65.6%     33 63.3%  MLZI3510.PSH  #AMB
   28   MLVL 10092M001    ZIM2 14001M008       GLO   21       70     41 41.4%     41 41.4%     70  0.0%  MLZI3510.PSH  #AMB
   28   MLVL 10092M001    ZIM2 14001M008       GAL   24       56     12 78.6%     12 78.6%     13 76.8%  MLZI3510.PSH  #AMB
   28   MLVL 10092M001    ZIM2 14001M008       tot   76      216     84 61.1%     84 61.1%    116 46.3%  MLZI3510.PSH  #AMB
   29   MOP2 11507M002    PENC 11206M006       GPS   31       89     26 70.8%     26 70.8%     23 74.2%  MOPE3510.PSH  #AMB
   29   MOP2 11507M002    PENC 11206M006       GLO   21       57     29 49.1%     29 49.1%     30 47.4%  MOPE3510.PSH  #AMB
   29   MOP2 11507M002    PENC 11206M006       tot   52      146     55 62.3%     55 62.3%     53 63.7%  MOPE3510.PSH  #AMB
   30   ONSA 10402M004    VIS0 10423M001       GPS   31      108     23 78.7%     23 78.7%      9 91.7%  ONVS3510.PSH  #AMB
   30   ONSA 10402M004    VIS0 10423M001       tot   31      108     23 78.7%     23 78.7%      9 91.7%  ONVS3510.PSH  #AMB
   31   PENC 11206M006    SUBO 12116M001       GPS   31       86     30 65.1%     30 65.1%     29 66.3%  PESU3510.PSH  #AMB
   31   PENC 11206M006    SUBO 12116M001       tot   31       86     30 65.1%     30 65.1%     29 66.3%  PESU3510.PSH  #AMB
   32   RIGA 12302M002    VIS0 10423M001       GPS   31      101     31 69.3%     31 69.3%     26 74.3%  RIVS3510.PSH  #AMB
   32   RIGA 12302M002    VIS0 10423M001       GLO   21       70     27 61.4%     27 61.4%     70  0.0%  RIVS3510.PSH  #AMB
   32   RIGA 12302M002    VIS0 10423M001       tot   52      171     58 66.1%     58 66.1%     96 43.9%  RIVS3510.PSH  #AMB
   33   SID0 12132M001    SUBO 12116M001       GPS   31       77     22 71.4%     22 71.4%     22 71.4%  SISU3510.PSH  #AMB
   33   SID0 12132M001    SUBO 12116M001       tot   31       77     22 71.4%     22 71.4%     22 71.4%  SISU3510.PSH  #AMB
 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   33   files do contain                       GPS   31     2965    933 68.5%    933 68.5%    844 71.5%
   26   files do contain                       GLO   21     1624    891 45.1%    891 45.1%   1429 12.0%
   17   files do contain                       GAL   25     1013    266 73.7%    266 73.7%    431 57.5%
   33   files do contain                       tot   77     5602   2090 62.7%   2090 62.7%   2704 51.7%


-----------------------------------------------------------------
>>> CPU/Real time for pgm "OBSXTR": 0:00:00.016 / 0:00:00.016
>>> Program finished successfully

================================================================================
 Satellite-wise Ambiguity Resolution Statistics
================================================================================

-------------------------------------------------------------
PRN |   Amb   |  L1 & L2 ambiguities  |     L5 ambiguities   
    |  total  |  solved  #/clu    rel |  solved  #/clu    rel
----+---------+-----------------------+----------------------
  2 |      90 |      72   24.5   76.7 |      74   22.0   78.5
  3 |      74 |      38   20.7   48.9 |      44   33.5   57.7
  4 |      93 |      47   20.9   48.1 |      52   22.9   53.5
  5 |      80 |      68   37.4   82.7 |      68   37.9   82.8
  6 |     102 |      79   17.6   73.1 |      77   19.8   71.7
  7 |      78 |      55   27.5   68.0 |      60   31.0   74.4
  8 |     132 |      98   19.6   70.4 |      99   17.1   70.6
  9 |      50 |      40   24.7   76.8 |      41   21.3   78.1
 10 |     125 |     105   17.9   79.3 |     107   20.5   81.4
 11 |      98 |      74   22.2   72.1 |      75   23.6   73.3
 12 |      72 |      45   14.7   58.2 |      47   14.5   60.8
 13 |      83 |      45   24.4   52.0 |      48   23.5   55.4
 14 |     135 |      93   14.2   64.0 |      99   13.7   68.0
 15 |      93 |      65   23.2   66.9 |      69   24.6   71.2
 16 |     108 |      72   18.0   63.0 |      79   31.4   70.8
 17 |     118 |      88   22.3   71.2 |      92   26.2   75.0
 18 |      78 |      54   17.7   65.3 |      56   17.3   67.6
 19 |     126 |      98   17.4   73.3 |      99   23.2   75.2
 20 |      92 |      68   37.3   71.9 |      71   31.0   74.7
 21 |      88 |      73   27.5   79.9 |      75   31.7   82.5
 22 |     129 |      82   20.1   60.4 |      90   24.3   66.9
 23 |     119 |      90   15.7   70.8 |      90   15.9   70.9
 24 |      75 |      39   24.9   49.9 |      45   27.4   57.8
 25 |      67 |      41   20.0   58.1 |      42   19.2   59.4
 26 |      99 |      76   21.9   73.3 |      81   24.1   78.4
 27 |     104 |      76   20.1   69.4 |      77   19.9   70.3
 28 |     102 |      77   22.9   72.2 |      80   25.6   75.4
 29 |      69 |      44   21.0   60.7 |      49   19.5   67.4
 30 |      65 |      44   16.6   63.6 |      46   25.2   68.0
 31 |      97 |      75   25.9   74.3 |      77   25.1   76.2
 32 |     124 |     114   23.9   88.1 |     113   19.3   86.4
101 |      63 |      31    4.2   37.5 |      12    5.2   15.4
102 |      63 |      10    2.0    7.9 |       6    2.0    4.8
103 |      62 |      41    4.2   50.4 |      10    4.3   12.4
104 |      52 |      46    3.1   59.9 |      11    3.5   15.1
105 |      86 |      75    4.0   65.6 |      18    4.9   16.6
107 |     114 |      76    4.4   51.5 |      16    4.3   10.8
108 |      85 |      35    3.1   28.0 |      10    3.5    8.4
109 |      72 |      50    3.9   51.6 |      14    4.4   15.0
111 |      78 |      58    3.4   52.4 |      14    3.7   13.1
112 |      99 |      70    4.2   53.7 |      18    4.6   14.3
113 |      80 |      55    4.2   52.3 |      13    4.6   12.7
114 |     100 |      20    2.2   11.0 |       5    2.5    3.0
115 |      68 |      31    3.5   32.5 |       8    3.6    8.5
116 |      68 |      39    4.3   43.9 |      10    4.7   11.6
117 |      72 |      55    4.4   59.1 |      13    4.3   13.9
118 |      71 |      51    3.8   53.0 |      10    4.0   10.6
119 |      50 |      19    2.1   20.0 |       6    2.0    6.0
120 |      79 |      49    4.1   47.0 |      13    4.9   13.1
121 |      88 |      63    4.7   56.2 |      19    4.8   17.1
122 |      89 |      63    4.0   53.2 |      16    3.5   12.9
124 |      85 |      57    4.0   50.4 |      17    5.1   16.1
202 |      42 |      29   25.7   66.4 |      21   18.0   47.2
203 |      44 |      36   34.3   79.4 |      29   15.4   61.6
204 |      54 |      38   11.6   64.3 |      31   17.2   54.1
205 |      41 |      36   36.4   85.4 |      28   28.0   65.9
207 |      48 |      42   24.6   83.9 |      21   30.4   42.3
208 |      38 |      28   32.1   71.4 |      23   16.0   56.7
209 |      44 |      36   20.1   77.7 |      30   25.0   65.5
210 |      65 |      58   16.1   83.7 |      27   21.7   39.6
211 |      36 |      30   32.6   80.8 |      31   13.0   79.5
212 |      46 |      41   17.2   84.0 |      29   22.8   60.3
213 |      33 |      20   26.1   58.3 |      19   16.1   54.0
214 |      10 |       9   14.0   83.6 |       9   29.4   86.9
215 |      43 |      21    7.0   41.8 |      21   15.5   45.7
218 |       8 |       8   51.5   98.1 |       8    8.1   87.7
219 |      31 |      16   22.1   49.3 |      16   35.9   50.2
221 |      34 |      28   23.8   78.9 |      28   10.6   74.6
224 |      59 |      36   15.0   56.9 |      27   28.8   44.2
225 |      44 |      25   28.2   54.8 |      22   18.9   47.4
226 |      54 |      40   13.9   68.7 |      31   23.8   55.0
227 |      32 |      29   24.0   86.8 |      28   24.5   83.9
230 |      49 |      41   37.6   81.4 |      27   32.5   53.4
231 |      50 |      45   37.1   87.6 |      31   32.0   60.1
233 |      44 |      37   45.7   82.3 |      26   28.0   57.0
234 |      29 |      22   13.7   70.3 |      24   11.2   75.4
236 |      35 |      33   45.2   92.2 |      27   16.9   72.6
----+---------+-----------------------+----------------------
GPS |    2965 |    2135   20.7   68.5 |    2222   22.0   71.5
GLO |    1624 |     994    3.8   45.1 |     259    4.0   12.0
GAL |    1013 |     784   21.2   73.7 |     614   19.2   57.5
----+---------+-----------------------+----------------------


================================================================================
PART 7: GNSS COORDINATE/TROPOSPHERE SOLUTION STATISTICS
================================================================================


================================================================================
Preliminary (ambiguity-float) results
================================================================================

 DSP_20233510.OUT    Rms:  1.28 , # fil.:  33 , # obs.:  262234 , # par.:  6211
 (DOY: 2023-351)


================================================================================
Final (ambiguity-fixed) results
================================================================================

Stations have been processed in clusters:
  Cluster: 20233510__.CLB with 33 baselines

 DSO_20233510.OUT    Rms:  1.32 , # fil.:  33 , # obs.:  262609 , # par.:  3073
 (DOY: 2023-351)


================================================================================
Size-reduced NEQ information
================================================================================

 DSR_20233510.OUT    Rms:  1.32 , # fil.:  33 , # obs.:  261725 , # par.:  3073
 (DOY: 2023-351)




================================================================================
PART 8: VERIFICATION OF DATUM DEFINITION
================================================================================


 ===============================================================================
 Bernese GNSS Software, Version 5.4
 -------------------------------------------------------------------------------
 Program        : HELMR1
 Purpose        : Helmert Transformation
 -------------------------------------------------------------------------------
 Campaign       : ${P}/EPNB23
 Default session: 3510 year 2023
 Date           : 23-May-2026 00:23:39
 User name      : bpe54
 ===============================================================================


 NTUA_DDP_20233510: Verification of fiducial stations
 -------------------------------------------------------------------------------


 FILE 1: APR_20233510.CRD: NTUA_DDP_20233510: Extrapolate coordinates           
 FILE 2: DSO_20233510.CRD: NTUA_DDP_20233510: Final coordinate/troposphere resul

 LOCAL GEODETIC DATUM: IGS20           
 RESIDUALS IN LOCAL SYSTEM (NORTH, EAST, UP)


 LIST OF REMOVED STATIONS: 

 OUTLIER CRITERIA:                    10.00     10.00     30.00



 ---------------------------------------------------------------------
 | NUM |      NAME        | FLG |     RESIDUALS IN MILLIMETERS   |   |
 ---------------------------------------------------------------------
 |     |                  |     |                                |   |
 |   1 | BOR1 12205M002   | I W |       0.93     -1.14     -0.21 |   |
 |   2 | BRST 10004M004   | I W |       1.24     -0.91     -4.41 |   |
 |   3 | DLF1 13502M009   | I W |      -1.74     -0.50      0.96 |   |
 |   4 | GLSV 12356M001   | I W |      -1.91      0.69      5.70 |   |
 |   5 | GRAZ 11001M002   | I W |       0.88      0.05     -0.51 |   |
 |   6 | JOZE 12204M001   | I W |      -0.56      0.07      5.04 |   |
 |   7 | LROC 10023M001   | I W |       0.29      0.51      0.56 |   |
 |   8 | MATE 12734M008   | I W |      -2.21      0.32      4.57 |   |
 |   9 | ONSA 10402M004   | I W |      -1.41      0.38    -11.79 |   |
 |  10 | PENC 11206M006   | I W |      -0.27      3.30     -7.01 |   |
 |  11 | POTS 14106M003   | I W |       1.15      0.32     -1.45 |   |
 |  12 | RIGA 12302M002   | I W |       2.42     -1.49      0.63 |   |
 |  13 | TLSE 10003M009   | I W |       1.53      0.25      3.04 |   |
 |  14 | VIS0 10423M001   | I W |       0.33     -2.49     -6.61 |   |
 |  15 | WTZR 14201M010   | I W |       0.68      1.19      5.44 |   |
 |  16 | ZIM2 14001M008   | I W |      -1.37     -0.56      6.03 |   |
 |     |                  |     |                                |   |
 ---------------------------------------------------------------------
 |     | RMS / COMPONENT  |     |       1.39      1.28      5.22 |   |
 |     | IQR              |     |       2.43      1.18      7.74 |   |
 |     | MEAN             |     |       0.00     -0.00      0.00 |   |
 |     | MEDIAN           |     |       0.31      0.16      0.60 |   |
 |     | MIN              |     |      -2.21     -2.49    -11.79 |   |
 |     | MAX              |     |       2.42      3.30      6.03 |   |
 ---------------------------------------------------------------------
         OVERALL RMS/IQR/MAX(3D)        3.21      2.31     11.88       ONSA 10402M004      #SUM
 ---------------------------------------------------------------------
 | ALL | RMS / COMPONENT  |     |       1.39      1.28      5.22 |   |
 | ALL | IQR              |     |       2.43      1.18      7.74 |   |
 | ALL | MEAN             |     |       0.00     -0.00      0.00 |   |
 | ALL | MEDIAN           |     |       0.31      0.16      0.60 |   |
 | ALL | MIN              |     |      -2.21     -2.49    -11.79 |   |
 | ALL | MAX              |     |       2.42      3.30      6.03 |   |
 ---------------------------------------------------------------------
   ALL   OVERALL RMS/IQR/MAX(3D)        3.21      2.31     11.88       ONSA 10402M004      #SUM_ALL


 NUMBER OF PARAMETERS  :     3
 NUMBER OF STATIONS    :    16
 NUMBER OF COORDINATES :    48
 RMS OF TRANSFORMATION :    3.21 MM 

 BARYCENTER COORDINATES:

 LATITUDE              :    50 24 54.57
 LONGITUDE             :    12 41  9.23
 HEIGHT                :         -54.848 KM


 PARAMETERS:

 TRANSLATION IN  N     :           0.00     +-  0.80    MM 
 TRANSLATION IN  E     :           0.00     +-  0.80    MM 
 TRANSLATION IN  U     :           0.00     +-  0.80    MM 


 NUMBER OF ITERATIONS  :     1


 ACCEPTED STATIONS     :    16
 REJECTED STATIONS     :     0
 VERIFIED STATIONS     :     0
 


-----------------------------------------------------------------
>>> CPU/Real time for pgm "HELMR1": 0:00:00.006 / 0:00:00.006
>>> Program finished successfully



