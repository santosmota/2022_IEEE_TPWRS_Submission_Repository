# Data Repository for Manuscript Submission to IEEE TPWRS - 2022

Data repository for the manuscript "Coordination of Frequency Reserves in an Isolated Industrial Grid Equipped with Energy Storage and Dominated by Constant Power Loads" submitted to the IEEE Transations in Power Systems:

  - Original manuscript: October 2022
  - First revision after comments: January 2023
  - Second revision after comments: June 2023
  - Final submission (after approval): August 2023

The models and other files that have been used for writing this manuscript are listed in the next sections. The list is made on a "per figure of the manuscript" basis. Some auxiliary python files are not explicitly listed, but it should be possible to indentify them by reading the python scripts that were used to control PowerFactory, to make the figures (matplotlib), and to parameterize the Simulink file.

The files are provided without any warranty. Use at your own risk. And cite if you use them.

## Software Tools

### MatLab (Linearized rotating mass model)

  - MATLAB R2018a Update 6 (9.4.0.949201) 64-bit (win64)
  - Windows 10 - Version 21H2 (OS Build 190144.2364): for MATLAB.

### PowerFactory

  - DIgSILENT PowerFactory 2020 SP2a (x64) Build 20.0.4.1 (10037) / Rev. 73397
  - Windows Server 2016 Version 1607 (OS Build 14393.5582): for running PowerFactory

### PHIL tests

  - RT-LAB (Workbench) Version: v2020.4.1.166: for compiling and uploading the electrical model into the real time simulator.
  - MATLAB R2016a (9.0.0341360) 64-bit (win64): the model compiled and loaded up to the real-time simulator
  - Windows 10 - Version 21H2 (OS Build 190144.2364): for running RT-LAB and MATLAB.
  - OPAL-RT OPAL-RT Linux (x86-based) version	2.6.29.6-opalrt-6.1: real time simulator.

## Figures 4 and 5
  - Figure 4: Frequency during a step load of 1.2MW with different sharing of FCRN between ESS and GTs.
  - Figure 5: Eigenvalues with linearized rotating mass model for a total gain of 12 MW/Hz and different sharing of FCRN between ESS and GTs.

Matlab + Simulink + CSV + eps: 

    at ./Matlab/
    - FCR_sharing.slx: Simulink Model
    - FCR_sharing_steps_Script.m: runs the step responses
    - FCR_sharing_eigen_Script.m: runs the eigenvalue analysis
    - matstep_run_1.csv: step response for Kgt=12MW/Hz, Kess = 0MW/Hz.
    - matstep_run_2.csv: step response for Kgt=10MW/Hz, Kess = 2MW/Hz.
    - matstep_run_3.csv: step response for Kgt=8MW/Hz, Kess = 4MW/Hz.
    - matstep_run_4.csv: step response for Kgt=6MW/Hz, Kess = 6MW/Hz.
    - matstep_run_5.csv: step response for Kgt=4MW/Hz, Kess = 8MW/Hz.
    - matstep_run_6.csv: step response for Kgt=2MW/Hz, Kess = 10MW/Hz.
    - matstep_run_7.csv: step response for Kgt=0MW/Hz, Kess = 12MW/Hz.
    - mateigen_run_1.csv: eigenvalues for Kgt=12MW/Hz, Kess = 0MW/Hz.
    - mateigen_run_2.csv: eigenvalues for Kgt=10MW/Hz, Kess = 2MW/Hz.
    - mateigen_run_3.csv: eigenvalues for Kgt=8MW/Hz, Kess = 4MW/Hz.
    - mateigen_run_4.csv: eigenvalues for Kgt=6MW/Hz, Kess = 6MW/Hz.
    - mateigen_run_5.csv: eigenvalues for Kgt=4MW/Hz, Kess = 8MW/Hz.
    - mateigen_run_6.csv: eigenvalues for Kgt=2MW/Hz, Kess = 10MW/Hz.
    - mateigen_run_7.csv: eigenvalues for Kgt=0MW/Hz, Kess = 12MW/Hz.

Python script: 

    at ./Python/
    - the python script for creating figure 4 has been ``lost in translations'' 
    - Eigen_MATLAB_7csv.py: creates figure 5

## Figure 8
Voltage and frequency at the main busbar during a step load of 1.2 MW.

PowerFactory Project:

    - ./PowerFactory/20220824/202208_RMS_Tests.pfd

PowerFactory running and data creation:
    
    - ./Python/PowerFactory_charts.py:
        Uncomment line in main "run_sim_steps_load_Z2_eigen(Z2_plini=1.2)"
        for running PowerFactory and creating the data.
        Uncomment line in main "plot_eigen_fmeas_from_csvs(simcount_total=7,.."
        for creating the figure and set "plotvpcc=True".

Raw Data and eps figure:

    at ./PowerFactory/20220824/
    - figstepsfvpcc.eps: created with function plot_eigen_fmeas_from_csvs in PowerFactory_charts.py.
    - timedomain_00.csv: GTs 6MW/Hz, BTC 0MW/Hz, FLX 0MW/Hz.
    - timedomain_01.csv: GTs 5MW/Hz, BTC 1MW/Hz, FLX 1MW/Hz.
    - timedomain_02.csv: GTs 4MW/Hz, BTC 2MW/Hz, FLX 2MW/Hz.
    - timedomain_03.csv: GTs 3MW/Hz, BTC 3MW/Hz, FLX 3MW/Hz.
    - timedomain_04.csv: GTs 2MW/Hz, BTC 4MW/Hz, FLX 4MW/Hz.
    - timedomain_05.csv: GTs 1MW/Hz, BTC 5MW/Hz, FLX 5MW/Hz.
    - timedomain_06.csv: GTs 0MW/Hz, BTC 6MW/Hz, FLX 6MW/Hz.

## Figure 9
Complex plane with eigenvalues.

PowerFactory Project (same as in Figure 5):

    - ./PowerFactory/20220824/202208_RMS_Tests.pfd

PowerFactory running and data creation:

    - ./Python/PowerFactory_charts.py:
       Uncomment line in main "run_sim_steps_load_Z2_eigen(Z2_plini=1.2)"
       for running PowerFactory and creating the data.
       Uncomment line in main "plot_eigen_fmeas_from_csvs_3charts()"
       for creating the figure. 

Raw Data and eps figure:

    at ./PowerFactory/20220824/
    - figstepsfvpcc.eps: created with function plot_eigen_fmeas_from_csvs_3charts in PowerFactory_charts.py.
    - eigenvalues_00.csv: GTs 6MW/Hz, BTC 0MW/Hz, FLX 0MW/Hz.
    - eigenvalues_01.csv: GTs 5MW/Hz, BTC 1MW/Hz, FLX 1MW/Hz.
    - eigenvalues_02.csv: GTs 4MW/Hz, BTC 2MW/Hz, FLX 2MW/Hz.
    - eigenvalues_03.csv: GTs 3MW/Hz, BTC 3MW/Hz, FLX 3MW/Hz.
    - eigenvalues_04.csv: GTs 2MW/Hz, BTC 4MW/Hz, FLX 4MW/Hz.
    - eigenvalues_05.csv: GTs 1MW/Hz, BTC 5MW/Hz, FLX 5MW/Hz.
    - eigenvalues_06.csv: GTs 0MW/Hz, BTC 6MW/Hz, FLX 6MW/Hz.

## Figure 10
Steps of 3 MW used for comparing the PowerFactory model and the PHIL test bed.

PowerFactory Project:

    - ./PowerFactory/20230105/202208_RMS_Tests.pfd
    Last back-up of this project.

PowerFactory running and data creation:
    
    - ./Python/PowerFactory_charts.py:
        Uncomment line in main "run_sim_3xstepload_Z2(Z2_plini=3.0)"
        for running PowerFactory and creating the data.

Python script / matplotlib and figure file: 
  
    - ./Python/Steps_PowerFactory_vs_RTLAB.py: creates the figure
    - ./RTLab/simdata/20220816/PlotSignalList.mat: mat file signal list
    - ./RTLab/simdata/20220816/figsteps_PowFact_RTLAB.pdf: the figure
   
PowerFactory data:

    at ./PowerFactory/20220824_3steps/
    - simulationdata_00.csv : Case 3 - FCRN: BTC+FLEX
    - simulationdata_01.csv : Case 2 - FCRN: BTC+GTs
    - simulationdata_02.csv : Case 1 - FCRN: GTs

PHIL data:
  
    at ./RTLab/simdata/20220816/
    - signal_list.txt: mat file signal list in text format
    - PHILconfig.png: reminder of how to set the PHIL test
    - PHIL_3MW_FCRN_BTCFLEX.mat : Case 3 - FCRN: BTC+FLEX
    - PHIL_3MW_FCRN_BTCGTs.mat : Case 2 - FCRN: BTC+GTs
    - PHIL_3MW_FCRN_GTs.mat : Case 1 - FCRN: GTs

The .mat fies with the PHIL data had to be zipped into several files smaller than 100MB due to Git Hub restrictions.

## Figure 10
Loss of 11MW from the wind farm for comparing the FCR vs Traditional.

Python script: 
  
    - ./PyCharts/WindChange_FCR_vs_Traditional.py
  
PHIL data:
      
    - ./RTLab/simdata/20220820/PlotSignalList.mat
    - ./RTLab/simdata/20230106/PHIL_Wind_12_6m_s_FCR.mat: Case 3 - FCRN: BTC+FLEX
    - ./RTLab/simdata/20230106/PHIL_Wind_12_6m_s_Trad.mat: Traditional droop GTs=BTC=FLX=1MW/Hz
    
The .mat fies with the PHIL data had to be zipped into several files smaller than 100MB due to Git Hub restrictions.

## OLD README

The data is divided into folders:
  - Simplified rotating mass model
  - Detailed model
  - Power hardware in the loop (PHIL)
  - Python scripts
  
## Simplified rotating mass model

Simulations performed with Matlab R2018a Update 6.

The following files are stored in this folder: 
  - **FCR_sharing.slx**:
      - Simulink linearized rotating mass model with three primary power providers, two gas turbines and an energy storage system.
  - **FCR_sharing_Script.m**:
      - Runs linear analyzes of the simulink model for 7 different gain sets for the FCR providers, stores the eigenvalues of each analyzis in a csv file.
  - **mateigen_run_1.csv ... mateigen_run_7.csv**:
      - Output files of the script FCR_sharing_Script.m.
    
## Detailed model

Simulations performed with DIgSILENT PowerFactory 2020 SP2A.

The following files are stored in this folder: 
  - **202208_RMS_Tests.pfd**: archive of the project.
  - **/Stability/**
      - **eigenvalues_00.csv ... eigenvalues_06.csv**: obtained after running **journal_powfact_charts_01.py**, used for plotting the 3 charts (side by side) with eigenvalues.
      - **timedomain_00.csv ... timedomain_06.csv**: time domain data with the steps of 1.2MW used for the eigenvalue analysis.
  - **/ThreeStepsForPHILvalidation/** simulation files with 3MW steps used for validation with the PHIL results. 
      - **simulationdata_00.csv**: case 3, ESS + FLX
      - **simulationdata_01.csv**: case 2, GTs + ESS
      - **simulationdata_02.csv**: case 1, GTs only
   
## Power hardware in the loop (PHIL)

The following files are stored in this folder: 
  - **opalPlotFile_5.mat**: case 1, GTs only
  - **opalPlotFile_6.mat**: case 2, GTs + ESS
  - **opalPlotFile_8.mat**: case 3, ESS + FLX

 For data storage purposes, the three files were stored in a split zip file. Use 7zip to unpack the three mat files from the six "7z.00x" files.

## Python Scripts

Anonymized version of the Python scripts used for controlling PowerFactory and for obtaining the figures in the manuscript. The scripts have not been tested after anonymization.

The following files are stored in this folder: 
  - **powerfactorycontrol.py**:
      - Custom made functions for controlling the model in **202208_RMS_Tests.pfd**. Fuctions for open the project and study case, set gains, time for transients, run RMS simulations, run modal analyzis, etc.
  - **plothelp.py**:
      - Custom made help functions for plotting the figures in the manuscript.
  - **journal_powfact_charts_01.py**:
      - Controls **202208_RMS_Tests.pfd** and runs the simulations for the detailed eigenvalue analysis. Runs also the RMS simulations for comparison with the PHIL setup. Functions have to be manually commented/uncommented inside the script.
  - **journal_PowFacRTLAB_charts_01.py**:
      - Plots the load steps with secondary power response from the PowerFactory and PHIL tests.
  - **journal_MATLAB_eigen_7csv.py**:
      - For obtaining the figure in the manuscript with caption "Eigenvalues with linearized rotating mass model for a total gain of 12 MW/Hz and different sharing of FCRN between ESS and GTs".
  


