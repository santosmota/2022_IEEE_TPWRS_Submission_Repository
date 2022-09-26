# 2022_IEEE_TPWRS_Submission_Repository
Data repository for the manuscript "Coordination of Frequency Reserves in an Isolated Industrial Grid Equipped with Energy Storage and Dominated by Constant Power Loads" submitted to the IEEE Transations in Power Systems in October 2022.

The data is divided into folders:
  - Simplified rotating mass model
  - Detailed model
  - Power hardware in the loop (PHIL)
  - Python scripts
  
## Simplified rotating mass model
Simulations performed with Matlab R2018a Update 6.

The following files are stored in this folder: 
  - **FCR_sharing.slx**: simulink linearized rotating mass model with three primary power providers, two gas turbines and an energy storage system.
  - **FCR_sharing_Script.m**: runs linear analyzes of the the simulink model for 7 different gain sets for the FCR providers, stores the eigenvalues of each analyzis in a csv file.
  - **mateigen_run_1.csv ... mateigen_run_7.csv**: output files of the script FCR_sharing_Script.m.
    
## Detailed model
Simulations performed with DIgSILENT PowerFactory 2020 SP2A.

The following files are stored in this folder: 
  - **202208_RMS_Tests.pfd**: archive of the project.
  - **/Stability/**
      - **eigenvalues_00.csv ... eigenvalues_06.csv**: obtained after running **journal_powfact_charts_01.py**, used for plotting the 3 charts (side by side) with eigenvalues.
      - **timedomain_00.csv ... timedomain_06.csv**: time domain data with the steps of 1.2MW used for the eigenvalue analysis.
  - **/ThreeStepsForPHILvalidation/**
      - **simulationdata_00.csv**: case 3, ESS + FLX
      - **simulationdata_01.csv**: case 2, GTs + ESS
      - **simulationdata_02.csv**: case 1, GTs only
   
## Power hardware in the loop (PHIL)
The following files are stored in this folder: 
  - **opalPlotFile_5.mat**: case 1, GTs only
  - **opalPlotFile_6.mat**: case 2, GTs + ESS
  - **opalPlotFile_8.mat**: case 3, ESS + FLX

## Python Scripts
Anonymized version of the Python scripts used for controlling PowerFactory and for obtaining the figures in the manuscript. The scripts have not been tested after anonymization.

The following files are stored in this folder: 
  - *powerfactorycontrol.py*: custom made functions for controlling the model in 202208_RMS_Tests.pfd. Fuctions for open the project and study case, set gains, time for transients, run RMS simulations, run modal analyzis, etc.
  - *plothelp.py*: custom made help functions for plotting the figures in the manuscript.
  - *journal_powfact_charts_01.py*: controls 202208_RMS_Tests.pfd and runs the simulations for the detailed eigenvalue analysis. Runs also the RMS simulations for comparison with the PHIL setup. Functions have to be manually commented/uncommented inside the script.
  - *journal_PowFacRTLAB_charts_01.py*: plots the load steps with secondary power response from the PowerFactory and PHIL tests.
  - *journal_MATLAB_eigen_7csv.py*: for obtaining the figure in the manuscript with caption "Eigenvalues with linearized rotating mass model for a total gain of 12 MW/Hz and different sharing of FCRN between ESS and GTs". This file has not been tested after anonymization.
  


