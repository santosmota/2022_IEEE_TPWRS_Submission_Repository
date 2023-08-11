##############################################################################################
# Several Python functions (not very well organized)
###############################################################################################
# By: Daniel dos Santos Mota, 2023-01-05
# 	This file has been copied from a private repository into this public one.
#       Some comments have been added only to the copied file.
#	It has not been tested after copying.
###############################################################################################

##############################################################################
# LIST OF FUNCTIONS
##############################################################################
# def run_sim_3xstepload_Z2(Z2_plini = 3.0):
# -----------------------------------------
#    runs three step loads with different FCR gains, saves CSVs of time and eigenvalues
#
#    if 3MW step: ../Powerfactory/simdata/20220824_3steps/ # The one used for FIGURE
#
#    gts_normal_k = [0.0, 1.217532468, 2.435064935]
#    btc_kp_gain = [55.65862709, 55.65862709, 0.0]
#    flex_kp_gain = [10.1503759399, 0.0, 0.0]  
#
#    creates csvs for eigenvalues: 
#        csvfolder + "eigenvalues_0" + str(simcount) + "_tini" +".csv"
#        csvfolder + "eigenvalues_0" + str(simcount) + "_tmid" +".csv"
#        csvfolder + "eigenvalues_0" + str(simcount) + "_tend" +".csv"
#    creates csvs for time domain:
#        csvfolder + "simulationdata_0" + str(simcount) + ".csv"
####################################
# def plot_3xstepload_Z2():
#--------------------------
#    Leftover - not used in the manuscript
####################################
# def run_sim_steps_load_Z2_eigen(Z2_plini=1.0):
#-----------------------------------------------
#    7 steps (creates the data for FIGURES 5 and 6)
#
#    proj_name = '202208_RMS_Tests'
#
#    csvfolder = "../Powerfactory/simdata/20220824/"
#
#    figstepname = csvfolder + '/figsteps_needsretouching.eps'
#    figeigename = csvfolder + '/figeigen_needsretouching.eps'
#    figstep11kVname = csvfolder + '/figsteps11kV_needsretouching.eps'
#
#    csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
#    csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'
#    csveigentotfolder = '\\\\!REDACTED!\\2022_Journal_Data\\Powerfactory\\simdata\\20220824\\'
#
#    simcount_total = 7
#    cores = ['red', 'gray', 'gray', 'gray', 'gray', 'gray', 'blue']
####################################
# def plot_eigen_fmeas_from_csvs(simcount_total=7...plotvpcc=True,...
#------------------------------------------------
#    Creates FIGURES 5 and 6
####################################
# def plot_eigen_charts_from_3_csvs():
# def plot_eigen_chart_from_1_csvs():
#   LEFTOVERS - not used in the manuscript

# def main():

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np

import powerfactorycontrol as pfc
import plothelp as pth

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'cmr10'  # 'https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/font_file.html
# plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
# ... https://matplotlib.org/stable/tutorials/introductory/customizing.html#matplotlibrc-sample
# DejaVu is shipped with Matplotlib and is thus guaranteed
# to be available; the other entries are
# left as examples of other possible values.
# https://stackoverflow.com/questions/58361594/matplotlib-glyph-8722-missing-from-current-font-despite-being-in-font-manager
# avoids RuntimeWarning: Glyph 8722 missing from current font. font.set_text(s, 0.0, flags=flags)
plt.rc('axes', unicode_minus=False)
#https://stackoverflow.com/questions/29188757/matplotlib-specify-format-of-floats-for-tick-labels

#############
# solves a warning with a previous syntax for using the package
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

##############################################################################
#  run_sim_3xstepload_3MW()
##############################################################################
def run_sim_3xstepload_Z2(Z2_plini = 3.0):
    print("#####################")
    print("Function name: ", run_sim_3xstepload_Z2.__name__)
    
    ##########################################################################
    # Open Power Factory
    ##########################################################################
    import sys
    sys.path.append(r"C:\programs\DIgSILENT\PowerFactory-2020\Python\3.7")
    # Path to PowerFactory Python Module
    #for name in sys.path:
        #    print(name)
    import powerfactory as pf

    ##########################################################################
    # Get Power Factory Application
    ##########################################################################
    # try:
    #     app = pf.GetApplicationExt()
    # except pf.ExitError as error:
    #     print(error)
    #     print('error.code = %d' % error.code)
    
    app = pf.GetApplication()
    if app is None:
        raise Exception('getting Powerfactory application failed')

    proj_name = '202208_RMS_Tests'
    study_case = 'Study Case'
    project, proj = pfc.open_project_study_case(app=app,
                                                proj_name=proj_name,
                                                study_case=study_case)

    ##########################################################################
    # Figures for plotting
    ##########################################################################
    figsizex = 9
    figsizey = 5
    fig_steps, axs_steps = plt.subplots(3, 3, sharex=True,
                                           figsize=(figsizex, figsizey),
                                           num='Step3')

    ##########################################################################
    # folder for saving the csv files
    ##########################################################################
    if Z2_plini == 3.0:
        csvfolder = "../Powerfactory/simdata/20220824_3steps/"
    if Z2_plini == 6.0:
        csvfolder = "../Powerfactory/simdata/20221028_3steps_6MW/"

    ##########################################################################
    # Figures for plotting
    ##########################################################################
    cores = ['blue', 'red', 'olive']
    estilos = ['-', ':', '-.']
    grossuras = [0.75, 1.0, 0.75]
    legendas = ['case 1', 'case 2', 'case 3']

    gts_normal_k = [0.0, 1.217532468, 2.435064935]
    gts_max_normal_droop_power = [0.0, 0.021307, 0.042614]
    gts_min_normal_droop_power = [0.0, -0.021307, -0.042614]

    btc_kp_gain = [55.65862709, 55.65862709, 0.0]

    # flex_kp_gain = [11.27819549, 0.0, 0.0]  # wrong gain I got by dividing by 7.6MW, forgot the cos phi = 0.9
    flex_kp_gain = [10.1503759399, 0.0, 0.0]  # 1.5 / (1 - 0.125) * 50 / 7.6 / 0.9

    ##########################################################################
    # Rated values / pu values
    ##########################################################################
    vn_pcc = 11.0       # pcc rated voltage in kV

    ##########################################################################
    # Set transient : connection of Load Z2 at time 155s
    ##########################################################################
    t_to_steady_state = 150 #150
    t_transient = t_to_steady_state + 10
    t_middle_eigen = t_transient + 20
    t_stop = t_to_steady_state + 150 # 150

    pfc.set_load_param(app, load_name='Z2.ElmLod',
                       input_mode='PC',  # DEF: default, PC: P, cos(phi)
                       plini=Z2_plini,  # active power in MW
                       coslini=0.95,  # cosinus phi
                       pf_recap=0,  # 0: ind          1: cap
                       u0=1.0)  # rated voltage in pu

    pfc.set_switch_transient_param(app, trans_name='PCC11kVZ2',
                                   outserv=0,   # 0: in service       1: out of service
                                   time=t_transient, # time of the transient in seconds
                                   i_switch=1,  # 0:open              1: close
                                   i_allph=1)   # 0:not all phases    1: all phases

    for simcount in range(0, 3):
    
        ##########################################################################
        # droops
        ##########################################################################
        pfc.set_iactrefgen_droop(app, controller_name='BCiactref.ElmDsl',
                                 kp=btc_kp_gain[simcount],
                                 pdroopmax=1.5/1.54,
                                 pdroopmin=-1.5/1.54)
    
        pfc.set_iactrefgen_droop(app, controller_name='FLEX_iact_ref_gen.ElmDsl',
                                 kp=flex_kp_gain[simcount],
                                 pdroopmax=1.5/7.6*0.9,
                                 pdroopmin=-1.5/7.6*0.9)
    
        pfc.set_govdb_N_droop(app, controller_name='GT1govdb.ElmDsl',
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power[simcount],
                              deltaP_normal_min=gts_min_normal_droop_power[simcount])
    
        pfc.set_govdb_N_droop(app, controller_name='GT2govdb.ElmDsl',
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power[simcount],
                              deltaP_normal_min=gts_min_normal_droop_power[simcount])
        
        ##########################################################################
        # run 150s for steady state and run model analysis ACOLA
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.run_rms(app=app, tstop=t_to_steady_state)
        pfc.save_snapshot(app=app)
        
        pfc.run_modal(app=app)
        eigen_real, eigen_imag, eigen_part_names = pfc.get_eigen_real_imag_participation(app=app,
                                                                                         part_threshold=0.5,
                                                                                         include_states_in_names=True,
                                                                                         add_partfact_to_name=True)
        
        
        df_eigen = pd.DataFrame({"real": eigen_real,
                                 "imag": eigen_imag,
                                 "names": eigen_part_names})
        
        csvname =  csvfolder + "eigenvalues_0" + str(simcount) + "_tini" +".csv"
        df_eigen.to_csv(csvname, index=False)
        
        
        ##########################################################################
        # purposefully re-initiate, load snapshot, run simulation, to drop the first 150s of the results
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.load_snapshot(app=app)
        
        
        ##########################################################################
        # middle point for eigen values
        ##########################################################################
        pfc.run_rms(app=app, tstop=t_middle_eigen)
        pfc.run_modal(app=app)
        eigen_real, eigen_imag, eigen_part_names = pfc.get_eigen_real_imag_participation(app=app,
                                                                                         part_threshold=0.5,
                                                                                         include_states_in_names=True,
                                                                                         add_partfact_to_name=True)
                
        df_eigen = pd.DataFrame({"real": eigen_real,
                                 "imag": eigen_imag,
                                 "names": eigen_part_names})
        
        csvname =  csvfolder + "eigenvalues_0" + str(simcount) + "_tmid" +".csv"
        df_eigen.to_csv(csvname, index=False)
        
        ##########################################################################
        # all the way to the end
        ##########################################################################
        pfc.run_rms(app=app, tstop=t_stop)
        pfc.run_modal(app=app)
        eigen_real, eigen_imag, eigen_part_names = pfc.get_eigen_real_imag_participation(app=app,
                                                                                         part_threshold=0.5,
                                                                                         include_states_in_names=True,
                                                                                         add_partfact_to_name=True)
                
        df_eigen = pd.DataFrame({"real": eigen_real,
                                 "imag": eigen_imag,
                                 "names": eigen_part_names})
        
        csvname =  csvfolder + "eigenvalues_0" + str(simcount) + "_tend" +".csv"
        df_eigen.to_csv(csvname, index=False)
        
        ##########################################################################
        # simulation results
        ##########################################################################
        #PLATPmeas.ElmDsl s:pfixed, s:pflex, s:pwf, c:pbt, c:pel, c:pfc (MW)
        #PLATPsecctrl.ElmDsl s:Fmeas (Hz)
        #GT1pqmeasMVA.StaPqmea s:p (MW)
        #GT2pqmeasMVA.StaPqmea s:p (MW)
        #PCC11kvmeas.StaVmea s:u (pu)
    
        ##################################
        elmRes = app.GetFromStudyCase('*.ElmRes')   # get the result file
        elmRes.Load()                               # load the result file in memory
        n_row = elmRes.GetNumberOfRows()            # get the number of samples

        time = pfc.get_res_time(app=app, elmres=elmRes)
        time = pth.time_offset(time, offset=-t_transient)
    
        
        fmeas = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                    element_name='PLATPsecctrl.ElmDsl',
                                    signal_name='s:Fmeas')
    
        vpcc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PCC11kvmeas.StaVmea',
                                   signal_name='s:u')
    
    
        pwf = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                  element_name='PLATPmeas.ElmDsl',
                                  signal_name='s:pwf')
        
        pgt1 = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='GT1pqmeasMVA.StaPqmea',
                                   signal_name='s:p')
    
        pgt2 = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='GT2pqmeasMVA.StaPqmea',
                                   signal_name='s:p')
    
        pfixed = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                     element_name='PLATPmeas.ElmDsl',
                                     signal_name='s:pfixed')
        
        pflex = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                    element_name='PLATPmeas.ElmDsl',
                                    signal_name='s:pflex')
    
        pbtc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PLATPmeas.ElmDsl',
                                   signal_name='c:pbt')
    
        pelc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PLATPmeas.ElmDsl',
                                   signal_name='c:pel')
    
        pfcc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PLATPmeas.ElmDsl',
                                   signal_name='c:pfc')
    
    
        ##########################################################################
        # PLOT
        ##########################################################################
        # selecting the figure
        plt.figure('Step3')
        # select the figure
        
        axs_steps[0][0].plot(time, vpcc*vn_pcc,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount]) #label='GTs+ESS+FLX'
        axs_steps[0][1].plot(time, fmeas,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[0][2].plot(time, pwf,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[1][0].plot(time, pgt1 + pgt2,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[1][1].plot(time, pfixed,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[1][2].plot(time, pflex,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[2][0].plot(time, pfcc,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[2][1].plot(time, pbtc,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        axs_steps[2][2].plot(time, pelc,
                                linestyle=estilos[simcount],
                                linewidth=grossuras[simcount],
                                color=cores[simcount],
                                label=legendas[simcount])
        
        ##########################################################################
        # SAVING CSV OF SIMULATION
        ##########################################################################
        df_timedata = pd.DataFrame({"time": time,
                           "vpcc": vpcc*vn_pcc,
                           "fmeas": fmeas,
                           "pwf": pwf,
                           "pgts": pgt1 + pgt2,
                           "pfixed": pfixed,
                           "pflex": pflex,
                           "pfcc": pfcc,
                           "pbtc": pbtc,
                           "pelc": pelc})
        
        csvname = csvfolder + "simulationdata_0" + str(simcount) + ".csv"
        
        df_timedata.to_csv(csvname, index=False)
        
    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps[2][0].set_xlabel(r'Time (s)')
    axs_steps[2][1].set_xlabel(r'Time (s)')
    axs_steps[2][2].set_xlabel(r'Time (s)')
    
    axs_steps[0][0].set_ylabel(r'PCC volt. (kV)')
    axs_steps[0][1].set_ylabel(r'PCC freq. (Hz)')
    axs_steps[0][2].set_ylabel(r'WF power (MW)')
    
    axs_steps[1][0].set_ylabel(r'GTs power (MW)')
    axs_steps[1][1].set_ylabel(r'Load power (MW)')
    axs_steps[1][2].set_ylabel(r'FLEX pow. (MW)')
    
    axs_steps[2][0].set_ylabel(r'FCC power (MW)')
    axs_steps[2][1].set_ylabel(r'BTC power (MW)')
    axs_steps[2][2].set_ylabel(r'ELC power (MW)')
    
    axs_steps[2][2].set_xticks(np.arange(-20,180,20))
    axs_steps[2][2].set_xlim([-10, 110])
            
    axs_steps[2][2].legend(loc='best', frameon=True)
    
    fig_steps.align_ylabels(axs_steps[:, :])
    fig_steps.tight_layout()
    fig_steps.show()

    plt.show()
    # plt.savefig('sim_3xstepload_3MW.eps', format='eps')


##########################################################################
# Plo 3 step loads of Z2
##########################################################################
def plot_3xstepload_Z2():
    print("#####################")
    print("Function name: ", plot_3xstepload_Z2.__name__)
    
    ##########################################################################
    # folder for saving the csv files
    ##########################################################################
    csvfolder = "../Powerfactory/simdata/"
    csvfolder = csvfolder + "20220816/"
    print("        csvfolder: ", csvfolder)
    
    ##########################################################################
    # Figures for plotting
    ##########################################################################
    cores = ['blue', 'red', 'olive']
    estilos = ['solid', 'dashed', 'dashdot']
    grossuras = [0.75, 0.75, 0.75] # if using dotted, better to use 1.0 linewidth
    legendas = ['case 1', 'case 2', 'case 3']
    
    #########################################################################
    # Figures for plotting
    ##########################################################################
    figsizex = 9
    figsizey = 5
    fig_steps, axs_steps = plt.subplots(3, 3, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step3xXMW')
    
    for simcount in range(0, 3):
        ##########################################################################
        # PLOT
        ##########################################################################
        # selecting the figure
        plt.figure('Step3x3MW')                       # select the figure
     
        df = pd.read_csv(csvfolder + 'simulationdata_0' + str(simcount) + '.csv')    
     
        axs_steps[0][0].plot(df["time"], df["vpcc"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[0][1].plot(df["time"], df["fmeas"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[0][2].plot(df["time"], df["pwf"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[1][0].plot(df["time"], df["pgts"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[1][1].plot(df["time"], df["pfixed"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[1][2].plot(df["time"], df["pflex"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[2][0].plot(df["time"], df["pfcc"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[2][1].plot(df["time"], df["pbtc"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
        axs_steps[2][2].plot(df["time"], df["pelc"],
                             linestyle=estilos[simcount],
                             linewidth=grossuras[simcount],
                             color=cores[simcount],
                             label=legendas[simcount])
        
    # ##########################################################################
    # # chart identification - legend - abcdefghi
    # ##########################################################################
    corlegenda = 'whitesmoke'

    axs_steps[0][0].annotate(r'a', xy=(100, 10.9), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][1].annotate(r'b', xy=(100, 49.2), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][2].annotate(r'c', xy=(100, 11.6), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][0].annotate(r'd', xy=(100, 35), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][1].annotate(r'e', xy=(100, 37), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][2].annotate(r'f', xy=(100, 4.5), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][0].annotate(r'g', xy=(100, 0.3), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][1].annotate(r'h', xy=(100, 0.3), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][2].annotate(r'i', xy=(100, -1.2), xycoords='data',
                             # va='center', ha='center',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps[2][0].set_xlabel(r'Time (s)')
    axs_steps[2][1].set_xlabel(r'Time (s)')
    axs_steps[2][2].set_xlabel(r'Time (s)')
    
    axs_steps[0][0].set_ylabel(r'Busbar volt. (kV)')
    axs_steps[0][1].set_ylabel(r'Busbar freq. (Hz)')
    axs_steps[0][2].set_ylabel(r'WF power (MW)')
    
    axs_steps[1][0].set_ylabel(r'GTs power (MW)')
    axs_steps[1][1].set_ylabel(r'Load power (MW)')
    axs_steps[1][2].set_ylabel(r'FLX power (MW)')
    
    axs_steps[2][0].set_ylabel(r'FCC power (MW)')
    axs_steps[2][1].set_ylabel(r'BTC power (MW)')
    axs_steps[2][2].set_ylabel(r'ELC power (MW)')
    
    
    ##########################################################################
    # axis limits
    ##########################################################################
    axs_steps[2][2].set_xticks(np.arange(-20, 180, 20))
    axs_steps[2][2].set_xlim([-10, 130])

    axs_steps[0][0].set_yticks(np.arange(-10.900, 12.000, 0.1))
    axs_steps[0][0].set_ylim([10.8, 11.1])
    axs_steps[0][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[0][1].set_yticks(np.arange(48.000, 51, 0.5))
    axs_steps[0][1].set_ylim([48.9, 50.1])
    axs_steps[0][1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[0][2].set_yticks(np.arange(11, 13, 0.1))
    axs_steps[0][2].set_ylim([11.5, 12])
    axs_steps[0][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[1][0].set_yticks(np.arange(29, 40, 1))
    axs_steps[1][0].set_ylim([31, 36])
    axs_steps[1][0].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    axs_steps[1][1].set_yticks(np.arange(35, 45, 1))
    axs_steps[1][1].set_ylim([36, 41])
    axs_steps[1][1].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    axs_steps[1][2].set_yticks(np.arange(3, 7, 0.5))
    axs_steps[1][2].set_ylim([4, 6.5])
    axs_steps[1][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][0].set_yticks(np.arange(0, 3, 0.5))
    axs_steps[2][0].set_ylim([-0.05, 1.55])
    axs_steps[2][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][1].set_yticks(np.arange(0, 3, 0.5))
    axs_steps[2][1].set_ylim([-0.05, 1.55])
    axs_steps[2][1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][2].set_yticks(np.arange(-3, 1, 0.5))
    axs_steps[2][2].set_ylim([-1.55, 0.05])
    axs_steps[2][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ##########################################################################
    # axis legends
    ##########################################################################
    axs_steps[2][2].legend(loc='best', frameon=False)
    
    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig_steps.align_ylabels(axs_steps[:, :])
    fig_steps.tight_layout()
    fig_steps.show()
    plt.savefig(csvfolder + 'sim_3xstepload_3MW.eps', format='eps')


##############################################################################
#  run_sim_steps_load_Z2_eigen
##############################################################################
def run_sim_steps_load_Z2_eigen(Z2_plini=1.0):
    print("#####################")
    print("Function name: ", run_sim_steps_load_Z2_eigen.__name__)

    ##########################################################################
    # Open Power Factory
    ##########################################################################
    import sys
    sys.path.append(r"C:\programs\DIgSILENT\PowerFactory-2020\Python\3.7")
    # Path to PowerFactory Python Module
    # for name in sys.path:
    #    print(name)
    import powerfactory as pf

    app = pf.GetApplication()
    if app is None:
        raise Exception('getting Powerfactory application failed')

    proj_name = '202208_RMS_Tests'
    study_case = 'Study Case'
    project, proj = pfc.open_project_study_case(app=app,
                                                proj_name=proj_name,
                                                study_case=study_case)
    ##########################################################################
    # folder for saving the csv files
    ##########################################################################
    csvfolder = "../Powerfactory/simdata/20220824/"
    csveigentotfolder = '\\\\!REDACTED!\\2022_Journal_Data\\Powerfactory\\simdata\\20220824\\'

    figstepname = csvfolder + '/figsteps_needsretouching.eps'
    figeigename = csvfolder + '/figeigen_needsretouching.eps'
    figstep11kVname = csvfolder + '/figsteps11kV_needsretouching.eps'

    ##########################################################################
    # Figures for plotting
    ##########################################################################
    figsizex = 4
    figsizey = 2
    fig_steps, axs_steps = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step')

    fig_steps_BTC, axs_steps_BTC = plt.subplots(1, 1, sharex=True,
                                                figsize=(figsizex, figsizey),
                                                num='StepBTC')

    fig_steps_11kV, axs_steps_11kV = plt.subplots(1, 1, sharex=True,
                                                  figsize=(figsizex, figsizey),
                                                  num='Step11kV')

    figsizex = 5
    figsizey = 9
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')
        
    cores = ['red', 'gray', 'gray', 'gray', 'gray', 'gray', 'blue']
    estilos = ['-', ':', ':', ':', ':', ':', '-.']
    legendas = ['GTs only', '', '', '', '', '', 'ESS only']
    
    grossuras = 0.75
    marker = 'x'
    markersize = 5

    ##########################################################################
    # parameters for each run
    ##########################################################################
    N_db = 0.0

    gts_normal_k = np.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]) * 50.0 / 35.2
    gts_max_normal_droop_power = 1.5 / 35.2
    gts_min_normal_droop_power = -1.5 / 35.2

    btc_kp_gain = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) * 50.0 / 1.54
    btc_max_normal_droop_power = 1.5/1.54
    btc_min_normal_droop_power = -1.5/1.54

    flex_kp_gain = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) * 50.0 / (7.6 / 0.9)
    flex_max_normal_droop_power = 1.5 / (7.6 / 0.9)
    flex_min_normal_droop_power = -1.5 / (7.6 / 0.9)

    simcount_total = 7

    ##########################################################################
    # Set transient : connection of Load Z2 at time 155s
    ##########################################################################
    t_to_steady_state = 30 
    t_transient = t_to_steady_state + 10 
    t_middle_eigen = t_transient + 20  

    pfc.set_load_param(app, load_name='Z2.ElmLod',
                       input_mode='PC',  # DEF: default, PC: P, cos(phi)
                       plini=Z2_plini,  # active power in MW
                       coslini=0.95,  # cosinus phi
                       pf_recap=0,  # 0: ind          1: cap
                       u0=1.0)  # rated voltage in pu

    pfc.set_switch_transient_param(app, trans_name='PCC11kVZ2',
                                   outserv=0,  # 0: in service       1: out of service
                                   time=t_transient,  # time of the transient in seconds
                                   i_switch=1,  # 0:open              1: close
                                   i_allph=1)  # 0:not all phases    1: all phases

    for simcount in range(0, simcount_total, 1):
        print("######################################################")
        print("Simulation run: ", simcount, "of ", simcount_total - 1)
        ##########################################################################
        # droops
        ##########################################################################
        pfc.set_iactrefgen_droop(app, controller_name='BCiactref.ElmDsl',
                                 ferrdb=N_db,
                                 kp=btc_kp_gain[simcount],
                                 pdroopmax=btc_max_normal_droop_power,
                                 pdroopmin=btc_min_normal_droop_power)

        pfc.set_iactrefgen_droop(app, controller_name='FLEX_iact_ref_gen.ElmDsl',
                                 ferrdb=N_db,
                                 kp=flex_kp_gain[simcount],
                                 pdroopmax=flex_max_normal_droop_power,
                                 pdroopmin=flex_min_normal_droop_power)

        pfc.set_govdb_N_droop(app, controller_name='GT1govdb.ElmDsl',
                              db_normal=N_db,
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power,
                              deltaP_normal_min=gts_min_normal_droop_power)

        pfc.set_govdb_N_droop(app, controller_name='GT2govdb.ElmDsl',
                              db_normal=N_db,
                              kN=gts_normal_k[simcount],
                              deltaP_normal_max=gts_max_normal_droop_power,
                              deltaP_normal_min=gts_min_normal_droop_power)

        ##########################################################################
        # run for steady state and run model analysis
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.run_rms(app=app, tstop=t_to_steady_state)
        pfc.save_snapshot(app=app)

        ##########################################################################
        # purposefully re-initiate, load snapshot, run simulation, to drop the first 150s of the results
        ##########################################################################
        pfc.calc_ini_rms(app=app)
        pfc.load_snapshot(app=app)

        ##########################################################################
        # names for the csv and for the columns of the dataframe (time domain, to be created later) 
        ##########################################################################
        
        if simcount < 10:
            csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
            csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'

            # colname = "fmeas_0" + str(simcount)
            csveigentotname = csveigentotfolder + 'eigenvalues_total_0' + str(simcount) + '.csv'  #  
        else:
            csvname = csvfolder + "/eigenvalues_" + str(simcount) + '.csv'
            csvtimedomainname = csvfolder + "/timedomain_" + str(simcount) + '.csv'
            
            # colname = "fmeas_" + str(simcount)
            csveigentotname = csveigentotfolder + 'eigenvalues_total_' + str(simcount) + '.csv'


        ##########################################################################
        # run step, calculate modal, create dataframe (eigen values)
        ##########################################################################
        pfc.run_rms(app=app, tstop=t_middle_eigen)
        pfc.run_modal(app=app)
        eigen_real, eigen_imag, eigen_part_names = pfc.get_eigen_real_imag_participation(app=app,
                                                                                         part_threshold=0.5,
                                                                                         include_states_in_names=False,
                                                                                         add_partfact_to_name=True,
                                                                                         savetotaleigen=True,
                                                                                         csveigentotname=csveigentotname)
                
        df_eigen = pd.DataFrame({"real": eigen_real,
                                 "imag": eigen_imag,
                                 "names": eigen_part_names})
        
        ##########################################################################
        # erase eigen values from AM_loads, saves csv for post processing of charts
        ##########################################################################
        df_eigen = df_eigen[~df_eigen['names'].str.contains("AM_")]  # deletes eigenvalues with AM_ loads which are not active
        df_eigen.to_csv(csvname, index=False)


        ##########################################################################
        # plots eigen values, aux lines, and names
        ##########################################################################
        axs_eigen.plot(df_eigen['real'], df_eigen['imag'],
                       color=cores[simcount],
                       label=legendas[simcount],
                       linestyle='None',
                       linewidth=grossuras,
                       marker=marker,
                       markersize=markersize)
        
        if simcount == 0:
            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen, nzetalines=31)
        
        if simcount == 0 or simcount == simcount_total - 1:
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=0.98)
    
        ##########################################################################
        # retrieve time domain data
        ##########################################################################
        elmRes = app.GetFromStudyCase('*.ElmRes')   # get the result file
        elmRes.Load()                               # load the result file in memory
        n_row = elmRes.GetNumberOfRows()            # get the number of samples

        time = pfc.get_res_time(app=app, elmres=elmRes)
        time = pth.time_offset(time, offset=-t_transient)
    
        df_td = pd.DataFrame({"time": time})

        fmeas = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                    element_name='PLATPsecctrl.ElmDsl',
                                    signal_name='s:Fmeas')

        fmeasBTC = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                       element_name='BCiactref.ElmDsl',
                                       signal_name='s:Fmeas')

        vpcc = pfc.get_res_element(app=app, elmres=elmRes, n_row=n_row,
                                   element_name='PCC11kvmeas.StaVmea',
                                   signal_name='s:u')
    
        df_td['fmeasSEC'] = fmeas
        df_td['fmeasBTC'] = fmeasBTC
        df_td['vpcc'] = vpcc * 11.0

        axs_steps.plot(df_td['time'],
                       df_td['fmeasSEC'],
                       linestyle=estilos[simcount],
                       linewidth=grossuras,
                       color=cores[simcount],
                       label=legendas[simcount])

        axs_steps_BTC.plot(df_td['time'],
                           df_td['fmeasBTC'],
                           linestyle=estilos[simcount],
                           linewidth=grossuras,
                           color=cores[simcount],
                           label=legendas[simcount])

        axs_steps_11kV.plot(df_td['time'],
                            df_td['vpcc'],
                            linestyle=estilos[simcount],
                            linewidth=grossuras,
                            color=cores[simcount],
                            label=legendas[simcount])



        df_td.to_csv(csvtimedomainname, index=False)

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps.set_xlabel(r'Time (s)')
    axs_steps.set_ylabel(r'Frequency (Hz)')

    axs_steps_BTC.set_xlabel(r'Time (s)')
    axs_steps_BTC.set_ylabel(r'Frequency (Hz)')

    axs_steps.set_xticks(np.arange(-20, 180, 5))
    axs_steps.set_xlim([-10, 20])

    axs_steps_BTC.set_xticks(np.arange(-20, 180, 5))
    axs_steps_BTC.set_xlim([-10, 20])

    axs_steps.legend(loc='best', frameon=True)
    axs_steps_BTC.legend(loc='best', frameon=True)

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    fig_steps.tight_layout()
    fig_steps_BTC.tight_layout()
    fig_steps_11kV.tight_layout()

    fig_steps_11kV.show()
    fig_steps_11kV.savefig(figstep11kVname, format='eps')  

    fig_steps.show()
    fig_steps.savefig(figstepname, format='eps')  

    fig_eigen.tight_layout()
    fig_eigen.show()
    fig_eigen.savefig(figeigename, format='eps')

    plt.show()

#####################################################
# plot eigen value charts and the frequency measurement from a set of csv files
#####################################################
def plot_eigen_fmeas_from_csvs(simcount_total=3,
                               csvfolder="//REDACTED/2022_Journal_Data/Powerfactory/simdata/20220729",
                               offsetfrequency=False,
                               Fn=50.0,
                               plotFmeasBTC=False,
                               plotvpcc=True,
                               timeoffset=0.0,
                               detailplot=True):
    print("#####################")
    print("Function name: ", plot_eigen_fmeas_from_csvs.__name__)

    if detailplot:
        figeigename = csvfolder + '/figeigen.eps'
    else:
        figeigename = csvfolder + '/figeigenGeral.eps'
        
    if plotFmeasBTC:
        figstepsname = csvfolder + '/figstepsBTC.eps'
    else:
        figstepsname = csvfolder + '/figsteps.eps'
    
    
    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 4.5
    figsizey = 5.5
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')
    figsizex = 4
    figsizey = 2
    fig_steps, axs_steps = plt.subplots(1, 1, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step')

    if plotvpcc:
        figsizex = 4.5
        figsizey = 3
        figstepsnamevpcc = csvfolder + '/figstepsfvpcc.eps'
        fig_steps_vpcc, axs_steps_vpcc = plt.subplots(2, 1, sharex=True,
                                                      figsize=(figsizex, figsizey),
                                                      num='StepFVpcc')


    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total,1):
        if simcount == 0:
            cores.append('red')
            legendas.append('GTs')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append('gray')
            legendas.append('GTs+BTC+FLX')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append('blue')
            legendas.append('BTC+FLX')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append('gray')
            legendas.append('')
            marker.append('+')
            estilos.append(':')
            
    grossuras = 0.75
    markersize = 5

    # if plotFmeasBTC:
    #     csvname = csvfolder + '/timedomainBTC.csv'
    # else:
    #     csvname = csvfolder + '/timedomain.csv'

    #

    # if plotvpcc:
    #     csvname = csvfolder + '/timedomain11kV.csv'
    #     figstepsnamevpcc = csvfolder + '/figstepsnamevpcc.eps'
    #     df_td_vpcc = pd.read_csv(csvname)

    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        if simcount < 10:
            csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
            colname = "fmeas_0" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'
        else:
            csvname = csvfolder + "/eigenvalues_" + str(simcount) + '.csv'
            colname = "fmeas_" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_" + str(simcount) + '.csv'

        df_eigen = pd.read_csv(csvname)
        df_td = pd.read_csv(csvtimedomainname)

        ##########################################################################
        # name replacements, erasing
        ##########################################################################
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXpll','FLXfmeas ')
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXctrl', 'FLXctrl')

        df_eigen['names'] = df_eigen['names'].str.replace('BCpll','BTCfmeas')
        df_eigen['names'] = df_eigen['names'].str.replace('BCiactref','BTCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('BATLR','BTL ')

        df_eigen['names'] = df_eigen['names'].str.replace('FCictrl', 'FCCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('FCLR', 'FCL ')

        df_eigen['names'] = df_eigen['names'].str.replace('ELictrl', 'ELCctrl')
        df_eigen['names'] = df_eigen['names'].str.replace('ELLR', 'ELL ')

        df_eigen['names'] = df_eigen['names'].str.replace('GT2', 'GT2 ')

        df_eigen['names'] = df_eigen['names'].str.replace('GT2 exc', 'GT2exc ')

        df_eigen['names'] = df_eigen['names'].str.replace('WT1', 'WT')
        df_eigen['names'] = df_eigen['names'].str.replace('WT2', 'WT')
        df_eigen['names'] = df_eigen['names'].str.replace('WT3', 'WT')

        # df_eigen['names'] = df_eigen['names'].str.replace('FCpll','')
        # df_eigen['names'] = df_eigen['names'].str.replace('ELpll','')

        # df_eigen['names'] = df_eigen['names'].str.replace('ESSDC+', '')
        # df_eigen['names'] = df_eigen['names'].str.replace('ESSDC-', '')

        #df_eigen['names'] = df_eigen['names'].str.replace('PLATpll','')
        df_eigen['names'] = df_eigen['names'].str.replace('PLAT','SEC')
        
        df_eigen['names'] = df_eigen['names'].str.replace('pll','fmeas')
        
        df_eigen['names'] = df_eigen['names'].str.replace('govdb','gov')
        
        df_eigen['names'] = df_eigen['names'].str.replace('udcquacctrl','ctrl')

        df_eigen['names'] = df_eigen['names'].str.replace('ESSGC', 'ESSGC ')
        df_eigen['names'] = df_eigen['names'].str.replace('ESSGC ctrl', 'ESSGCctrl')

        ##########################################################################
        # plots ei gen values, aux lines, and names
        ##########################################################################
        axs_eigen.plot(df_eigen['real'], df_eigen['imag'],
                       color=cores[simcount],
                       label=legendas[simcount],
                       linestyle='None',
                       linewidth=grossuras,
                       marker=marker[simcount],
                       markersize=markersize)
        
        if detailplot:
            maxrealred = 8.0
            maximagred = 4.5
            
            namesrealminred = -6.0
            namesimagminred = 0.0
            namesimagmaxred = 3.0
            
            eigenxticks = 1.0
            eigenyticks = 0.5
            
            namesrealminblue = -5.1
            namesrealmaxblue = -0.5
            namesimagminblue = -0.5
            namesimagmaxblue = 4
            
            mindampforaddnumbers=0.55
            
            legendx = 0.52
            legendy = 0.6
            
            namesvertorientred = 'bottom'
            namesvertorientblue = 'top'
            
        else:
            # maxrealred = 70
            # maximagred = 25

            maxrealred = 300
            maximagred = 200

            namesrealminred = -10
            
            namesimagminred = 1.2
            namesimagmaxred = 1.5
            
            eigenxticks = 10.0
            eigenyticks = 2.0

            # eigenxticks = 100.0
            # eigenyticks = 100.0

            namesrealminblue = -maximagred
            namesrealmaxblue = -0.5
            namesimagminblue = 3.0
            namesimagmaxblue = maximagred
            
            mindampforaddnumbers=0.1

            legendx = 0.55
            legendy = 0.85

            namesvertorientred = 'center'
            namesvertorientblue = 'center'

        if simcount == 0:

            if detailplot:
                n_segments = 1
            else:
                n_segments = 200

            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen, #nzetalines=31,
                                              nzetalines=19,
                                              max_real=maxrealred, max_imag=maximagred,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=mindampforaddnumbers,
                                              n_segments=n_segments)
        
            # red
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=1,
                                          real_min=namesrealminred,
                                          real_max=0.0,
                                          imag_min=namesimagminred,
                                          imag_max=namesimagmaxred,
                                          vert_orient=namesvertorientred)
            
        if simcount == simcount_total - 1: # blue
            pth.add_root_locus_part_names(eigen_real=df_eigen['real'],
                                          eigen_imag=df_eigen['imag'],
                                          eigen_part_names=df_eigen['names'],
                                          axis=axs_eigen,
                                          zeta_threshold=1,
                                          real_min=namesrealminblue,
                                          real_max=namesrealmaxblue,
                                          imag_min=namesimagminblue,
                                          imag_max=namesimagmaxblue,
                                          vert_orient=namesvertorientblue)
            
        if offsetfrequency:
             df_td[colname] = df_td[colname] - (df_td[colname][0] - Fn)
        
        axs_steps.plot(df_td['time'] + timeoffset,
                       df_td['fmeasSEC'],
                       linestyle=estilos[simcount],
                       linewidth=grossuras,
                       color=cores[simcount],
                       label=legendas[simcount])

        if plotvpcc:
            axs_steps_vpcc[0].plot(df_td['time'] + timeoffset,
                                   df_td['fmeasSEC'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])
            axs_steps_vpcc[1].plot(df_td['time'] + timeoffset,
                                   df_td['vpcc'],
                                   linestyle=estilos[simcount],
                                   linewidth=grossuras,
                                   color=cores[simcount],
                                   label=legendas[simcount])

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps.set_xlabel(r'Time (s)')
    axs_steps.set_ylabel(r'Frequency (Hz)')
        
    axs_steps.set_xticks(np.arange(-20, 180, 5))
    axs_steps.set_xlim([0, 30])

    # axs_steps.set_yticks(np.arange(49.90, 50.10, 0.025))
    # axs_steps.set_ylim([49.95, 50.075])

    axs_steps.legend(loc='best', frameon=False)
    
    if plotvpcc:
        axs_steps_vpcc[0].set_ylabel(r'Frequency (Hz)')

        axs_steps_vpcc[1].set_xlabel(r'Time (s)')
        axs_steps_vpcc[1].set_ylabel(r'Voltage (kV)')
        
        axs_steps_vpcc[1].set_xticks(np.arange(-20, 180, 1))
        axs_steps_vpcc[1].set_xlim([0, 8])
    
        axs_steps_vpcc[1].set_yticks(np.arange(10.0, 11.1, 0.01))
        axs_steps_vpcc[1].set_ylim([10.97, 11.0])

        corlegenda = 'whitesmoke'

        axs_steps_vpcc[0].annotate(r'a', xy=(0.0625, 0.2), xycoords='axes fraction',
                              bbox=dict(boxstyle='circle', fc=corlegenda))

        axs_steps_vpcc[1].annotate(r'b', xy=(0.0625, 0.2), xycoords='axes fraction',
                              bbox=dict(boxstyle='circle', fc=corlegenda))

        axs_steps_vpcc[1].legend(loc='lower right', frameon=False)
    
        fig_steps_vpcc.tight_layout()
        fig_steps_vpcc.show()
        
        fig_steps_vpcc.savefig(figstepsnamevpcc, format='eps')
        

    if detailplot:
        axs_eigen.set_xticks(np.arange(-maxrealred, 10, eigenxticks))
        axs_eigen.set_xlim([-maxrealred, 0])

        axs_eigen.set_yticks(np.arange(- eigenyticks, maximagred + eigenyticks, eigenyticks))
        axs_eigen.set_ylim([-0.25, maximagred])

        axs_eigen.legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))

    else:
        axs_eigen.grid(which='major', axis='both', linestyle=':', linewidth=0.5, color='gray')

        axs_eigen.set_xscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=0.75)
        axs_eigen.set_xlim([-maxrealred, 0])
        axs_eigen.set_xticks([-maxrealred, -100, -10, -8, -6, -4, -2, 0])
        axs_eigen.set_xticklabels([-maxrealred, -100, -10, -8, -6, -4, -2, 0])

        axs_eigen.set_yscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=1)
        axs_eigen.set_yticks([0, 2, 4, 8, 6, 8, 10, 100, maximagred])
        axs_eigen.set_yticklabels([0, 2, 4, 8, 6, 8, 10, 100, maximagred])
        axs_eigen.set_ylim([-2.0, maximagred])

        axs_eigen.legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))







    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    fig_steps.tight_layout()
    fig_steps.show()
    fig_steps.savefig(figstepsname, format='eps')

    fig_eigen.tight_layout()
    fig_eigen.savefig(figeigename, format='eps')

    
    plt.show()


#####################################################
# plot eigen value charts and the frequency measurement from a set of csv files
#####################################################
def plot_eigen_fmeas_from_csvs_3charts(simcount_total=7,
                               csvfolder="//REDACTED/2022_Journal_Data/Powerfactory/simdata/20220824"
                               ):
    print("#####################")
    print("Function name: ", plot_eigen_fmeas_from_csvs_3charts.__name__)

    figeigename = csvfolder + '/figeigen_3charts.eps'

    ##########################################################################
    # figure
    ##########################################################################
    figsizex = 9.25
    figsizey = 2.75
    fig_eigen, axs_eigen = plt.subplots(1, 3, sharex=False,
                                        figsize=(figsizex, figsizey),
                                        num='Eigen')

    fig_eigen.show()

    # gs = axs_eigen[0, 0].get_gridspec()

    # for ax in axs_eigen[0:, 0]:
    #     ax.remove()

    # axs_eigen_big = fig_eigen.add_subplot(gs[0:, 0])

    ##########################################################################
    # style of the plots
    ##########################################################################
    cores = []
    legendas = []
    marker = []
    estilos = []
    for simcount in range(0, simcount_total, 1):
        if simcount == 0:
            cores.append('red')
            legendas.append('GTs')
            marker.append('x')
            estilos.append('-')  # , ':', '-.']
        elif simcount == 1:
            cores.append('gray')
            legendas.append('GTs+BTC+FLX')
            marker.append('+')
            estilos.append(':')
        elif simcount == simcount_total - 1:
            cores.append('blue')
            legendas.append('BTC+FLX')
            marker.append('*')
            estilos.append('-.')
        else:
            cores.append('gray')
            legendas.append('')
            marker.append('+')
            estilos.append(':')

    grossuras = 0.75
    markersize = 5

    # chart_gov_modes = [[17], [17], [17], [17], [20], [20], [26], [26]]


    ##########################################################################
    # plotting the eigen values
    ##########################################################################
    for simcount in range(0, simcount_total, 1):

        if simcount < 10:
            csvname = csvfolder + "/eigenvalues_0" + str(simcount) + '.csv'
            colname = "fmeas_0" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_0" + str(simcount) + '.csv'
        else:
            csvname = csvfolder + "/eigenvalues_" + str(simcount) + '.csv'
            colname = "fmeas_" + str(simcount)
            csvtimedomainname = csvfolder + "/timedomain_" + str(simcount) + '.csv'

        df_eigen = pd.read_csv(csvname)

        ##########################################################################
        # plots ei gen values, aux lines, and names
        ##########################################################################
        axs_eigen[0].plot(df_eigen['real'], df_eigen['imag'],
                           color=cores[simcount],
                           label=legendas[simcount],
                           linestyle='None',
                           linewidth=grossuras,
                           marker=marker[simcount],
                           markersize=markersize)

        axs_eigen[1].plot(df_eigen['real'], df_eigen['imag'],
                             color=cores[simcount],
                             label=legendas[simcount],
                             linestyle='None',
                             linewidth=grossuras,
                             marker=marker[simcount],
                             markersize=markersize)

        axs_eigen[2].plot(df_eigen['real'], df_eigen['imag'],
                          color=cores[simcount],
                          label=legendas[simcount],
                          linestyle='None',
                          linewidth=grossuras,
                          marker=marker[simcount],
                          markersize=markersize)

        maxrealred = 100
        maximagred = 150

        mindampforaddnumbers = 0.1
        legendx = 0.55
        legendy = 0.85


        ##########################################################################
        # name replacements, erasing
        ##########################################################################
        df_eigen['names'] = df_eigen['names'].str.replace('GT1govdb,GT2govdb,GT1,GT2', 'Govs,GTs')
        df_eigen['names'] = df_eigen['names'].str.replace('GT1exc,GT2exc,GT1,GT2', 'Excs,GTs')

        df_eigen['names'] = df_eigen['names'].str.replace('BCpll', 'BTCpll')
        df_eigen['names'] = df_eigen['names'].str.replace('FLEXpll', 'FLXpll')
        df_eigen['names'] = df_eigen['names'].str.replace('PLATpll', 'SECpll')

        df_eigen['names'] = df_eigen['names'].str.replace('GT1exc,GT2exc', 'Excs')
        df_eigen['names'] = df_eigen['names'].str.replace('GT1,GT2', 'GTs')
        df_eigen['names'] = df_eigen['names'].str.replace('WT1udcquacctrl,WT1GC', 'WTs')
        df_eigen['names'] = df_eigen['names'].str.replace('ELictrl,ELLR', 'ELC,ELL')
        df_eigen['names'] = df_eigen['names'].str.replace('FCictrl,FCLR', 'FCC,FCL')
        df_eigen['names'] = df_eigen['names'].str.replace('BCiactref,BATLR', 'BTC,BTL')
        df_eigen['names'] = df_eigen['names'].str.replace('ESSGCudcquacctrl,ESSGC', 'ESSGC')


        if simcount == 0:

            ################################################################
            # overview chart
            ################################################################
            n_segments = 200

            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[0],  # nzetalines=31,
                                              nzetalines=13,
                                              max_real=maxrealred, max_imag=maximagred,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=mindampforaddnumbers,
                                              n_segments=n_segments)

            axs_eigen[0].annotate('',
                                  xy=(-45, 15), xycoords='data',
                                  xytext=(-45, 5), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple', # '"->",
                                  connectionstyle="arc3", color='gray'),
                                  )


            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[24], # GTs
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.05,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[37],  # Exc
                                                  xanot_offset=0.25,
                                                  yanot_offset=0.25,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[39], # WTs
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.5,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[67],  # ESSGC
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.25,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[93], # ELC
                                                  xanot_offset=5,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='center',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[95],  # FCC
                                                  xanot_offset=5,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            # annotation for detail (c)
            axs_eigen[0].text(x=df_eigen.iloc[17, df_eigen.columns.get_loc('real')] + 0.0,
                              y=df_eigen.iloc[17, df_eigen.columns.get_loc('imag')] + 0.1,
                              s='(c)',
                              ha='center',
                              va='bottom',
                              color='black')

            ################################################################
            # PLL chart
            ################################################################
            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[1],
                                              nzetalines=19,
                                              max_real=5.25, max_imag=3.75,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=0.76,
                                              max_damp_for_adding_numbers=0.88,
                                              n_segments=1)

            # auxmodes = [[33], [31]]
            # auxyoffsets = [0.05, 0.2]  #
            auxmodes = [[35], [33], [31]]
            auxyoffsets = [0.05, 0.2, 0.35]

            for [auxmod, auxoffset] in zip(auxmodes, auxyoffsets):
                pth.add_root_locus_participation_name(df=df_eigen,
                                                      axis=axs_eigen[1],
                                                      modes=auxmod,
                                                      xanot_offset=0.0,
                                                      yanot_offset=auxoffset,
                                                      hor_orient='center',
                                                      vert_orient='bottom',
                                                      text_color=cores[simcount]
                                                      )

            axs_eigen[1].annotate('',
                                  xy=(-4.25, 3.025), xycoords='data',
                                  xytext=(-4.5, 2.75), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            axs_eigen[1].annotate('',
                                  xy=(-4.65, 2.37), xycoords='data',
                                  xytext=(-4.8, 2.34), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            ################################################################
            # Governor chart
            ################################################################
            pth.plot_root_locus_damping_lines(eigen_real=df_eigen['real'],
                                              eigen_imag=df_eigen['imag'],
                                              axis=axs_eigen[2],
                                              nzetalines=7,
                                              max_real=2.5, max_imag=2,
                                              add_pos_damping_numbers=True,
                                              max_axis='manual',
                                              min_damp_for_adding_numbers=0.3,
                                              max_damp_for_adding_numbers=0.9,
                                              n_segments=1)

            axs_eigen[2].annotate('',
                                  xy=(-1.75, 1.0), xycoords='data',
                                  xytext=(-1.5, 1.45), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )

            axs_eigen[2].annotate('',
                                  xy=(-1.75, -1.1), xycoords='data',
                                  xytext=(-1.5, -1.55), textcoords='data',
                                  arrowprops=dict(arrowstyle='simple',  # '"->",
                                                  connectionstyle="arc3", color='gray'),
                                  )


            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[0, 5],
                                                  xanot_offset=0.0,
                                                  yanot_offset=0.04,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color='black'
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[17],
                                                  xanot_offset=-0.03,
                                                  yanot_offset=0.04,
                                                  hor_orient='right',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )


            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[18],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[1, 6],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='center',
                                                  vert_orient='top',
                                                  text_color='black'
                                                  )

        if simcount == 5:
            ################################################################
            # Governor chart
            ################################################################
            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[20],
                                                  xanot_offset=0.025,
                                                  yanot_offset=0.04,
                                                  hor_orient='right',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[2],
                                                  modes=[21],
                                                  xanot_offset=0.025,
                                                  yanot_offset=-0.05,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

        if simcount == 6:
            ################################################################
            # Overview Chart
            ################################################################
            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[0],
                                                  modes=[94],  # BTC
                                                  xanot_offset=0,
                                                  yanot_offset=1,
                                                  hor_orient='center',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            axs_eigen[0].text(x=df_eigen.iloc[29, df_eigen.columns.get_loc('real')] + 0.025,
                              y=df_eigen.iloc[29, df_eigen.columns.get_loc('imag')] + 0.0,
                              s='(b)',
                              ha='left',
                              va='bottom',
                              color='black')


            ################################################################
            # PLL chart
            ################################################################
            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[29], # BTCpll FLXpll, less damped
                                                  xanot_offset=-0.025,
                                                  yanot_offset=0.0,
                                                  hor_orient='right',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[31],
                                                  xanot_offset=0.025,
                                                  yanot_offset=0.0,
                                                  hor_orient='left',
                                                  vert_orient='bottom',
                                                  text_color=cores[simcount]
                                                  )

            pth.add_root_locus_participation_name(df=df_eigen,
                                                  axis=axs_eigen[1],
                                                  modes=[35],
                                                  xanot_offset=0.0,
                                                  yanot_offset=-0.05,
                                                  hor_orient='center',
                                                  vert_orient='top',
                                                  text_color=cores[simcount]
                                                  )

    ##########################################################################
    # axis big
    ##########################################################################
    # axs_eigen[0].grid(which='major', axis='both', linestyle=':', linewidth=0.5, color='gray')

    axs_eigen[0].set_xscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=0.75)
    axs_eigen[0].set_xlim([-maxrealred, 0])
    axs_eigen[0].set_xticks([-maxrealred, -100, -10, -8, -6, -4, -2, 0])
    axs_eigen[0].set_xticklabels([-maxrealred, -100, -10, -8, -6, -4, -2, 0])

    axs_eigen[0].set_yscale('symlog',
                             linthresh=10,
                             subs=np.arange(2, 10),
                             linscale=1)
    axs_eigen[0].set_yticks([-2, 0, 2, 4, 8, 6, 8, 10, 100, maximagred])
    axs_eigen[0].set_yticklabels([-2, 0, 2, 4, 8, 6, 8, 10, 100, maximagred])
    axs_eigen[0].set_ylim([-2.0, maximagred])

    # axs_eigen[0].legend(loc=(legendx, legendy), frameon=True)  # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))

    axs_eigen[0].set_xlabel(r'Real (Np/s)' '\n\n' r'(a) Overview')
    axs_eigen[0].set_ylabel(r'Imaginary (rad/s)')


    ##########################################################################
    # axis middle
    ##########################################################################
    axs_eigen[1].set_xticks(np.arange(-6, -3, 0.25))
    axs_eigen[1].set_xlim([-5.25, -3.75])

    axs_eigen[1].set_yticks(np.arange(1, 4, 0.25))
    axs_eigen[1].set_ylim([2, 3.75])

    axs_eigen[1].set_xlabel(r'Real (Np/s)' '\n\n' r'(b) Detail frequency measurement')
    axs_eigen[1].set_ylabel(r'Imaginary (rad/s)')

    ##########################################################################
    # axis right
    ##########################################################################
    axs_eigen[2].set_xlim([-2.5, 0])
    axs_eigen[2].set_ylim([-2, 2])

    axs_eigen[2].set_xlabel(r'Real (Np/s)' '\n\n' r'(c) Detail governors')
    axs_eigen[2].set_ylabel(r'Imaginary (rad/s)')

    fig_eigen.tight_layout()

    fig_eigen.savefig(figeigename, format='eps')

    plt.show()


#####################################################
# plot single chart with eigen values stored in a csv file
#####################################################
def plot_eigen_charts_from_3_csvs():
    print("#####################")
    print("Function name: ", plot_eigen_charts_from_3_csvs.__name__)

    ###############################################################
    # DATA FILE - CSV FILE
    ###############################################################
    # FOLDER LOCATION
    data_folder = '//REDACTED/2022_Journal_Data/PowerFactory/simdata/20220723/step3MW'
    # TKINTER TO OPEN THE FILE
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    data_full_path_01 = askopenfilename(initialdir=data_folder)
    data_full_path_02 = askopenfilename()
    data_full_path_03 = askopenfilename()

    if data_full_path_01 == '' or data_full_path_02 == '' or data_full_path_03 == '':
        print('No csv data file chosen')
        return

    df_01 = pd.read_csv(data_full_path_01)
    print('Chosen file: ', data_full_path_01)
    df_02 = pd.read_csv(data_full_path_02)
    print('Chosen file: ', data_full_path_02)
    df_03 = pd.read_csv(data_full_path_03)
    print('Chosen file: ', data_full_path_03)

    # deletes the rows whose column "names" contains "AM_", the "AM_" loads are not enabled in the Power Factory Model
    df_01 = df_01[~df_01['names'].str.contains("AM_")]
    df_02 = df_02[~df_02['names'].str.contains("AM_")]
    df_03 = df_03[~df_03['names'].str.contains("AM_")]

    ###############################################################################################
    # Figures for plotting
    ###############################################################################################
    figsizex = 5
    figsizey = 7
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True, figsize=(figsizex, figsizey), num='Eigen')

    linewidth = 0.75
    color = ['blue', 'red', 'olive']
    marker = 'x'
    markersize = 5

    axs_eigen.plot(df_01['real'], df_01['imag'],
                   color=color[0],
                   #label=label,
                   linestyle='None',
                   linewidth=linewidth,
                   marker=marker,
                   markersize=markersize)

    #pth.add_root_locus_part_names(eigen_real=df_01['real'],
    #                              eigen_imag=df_01['imag'],
    #                              eigen_part_names=df_01['names'],
    #                              axis=axs_eigen,
    #                              zeta_threshold=0.95)

    axs_eigen.plot(df_02['real'], df_02['imag'],
                   color=color[1],
                   # label=label,
                   linestyle='None',
                   linewidth=linewidth,
                   marker=marker,
                   markersize=markersize)

    # pth.add_root_locus_part_names(eigen_real=df_02['real'],
    #                               eigen_imag=df_02['imag'],
    #                               eigen_part_names=df_02['names'],
    #                               axis=axs_eigen,
    #                               zeta_threshold=0.95)

    axs_eigen.plot(df_03['real'], df_03['imag'],
                   color=color[2],
                   # label=label,
                   linestyle='None',
                   linewidth=linewidth,
                   marker=marker,
                   markersize=markersize)

    #pth.add_root_locus_part_names(eigen_real=df_03['real'],
    #                              eigen_imag=df_03['imag'],
    #                              eigen_part_names=df_03['names'],
    #                              axis=axs_eigen,
    #                              zeta_threshold=0.95)

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    #fig_eigen.tight_layout()
    fig_eigen.show()


#####################################################
# plot single chart with eigen values stored in a csv file
#####################################################
def plot_eigen_chart_from_1_csvs():
    print("#####################")
    print("Function name: ", plot_eigen_chart_from_1_csvs.__name__)

    ###############################################################
    # DATA FILE - CSV FILE
    ###############################################################
    # FOLDER LOCATION
    data_folder = '//REDACTED/2022_Journal_Data/PowerFactory/simdata/'
    # TKINTER TO OPEN THE FILE
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    data_full_path_01 = askopenfilename(initialdir=data_folder)
    
    if data_full_path_01 == '':
        print('No csv data file chosen')
        return

    df_01 = pd.read_csv(data_full_path_01)
    print('Chosen file: ', data_full_path_01)
    
    # deletes the rows whose column "names" contains "AM_", the "AM_" loads are not enabled in the Power Factory Model
    df_01 = df_01[~df_01['names'].str.contains("AM_")]
    
    ###############################################################################################
    # Figures for plotting
    ###############################################################################################
    figsizex = 5
    figsizey = 7
    fig_eigen, axs_eigen = plt.subplots(1, 1, sharex=True, figsize=(figsizex, figsizey), num='Eigen')

    linewidth = 0.75
    color = ['blue', 'red', 'olive']
    marker = 'x'
    markersize = 5

    pth.plot_root_locus_damping_lines(df_01['real'], df_01['imag'],
                                      axis=axs_eigen, #nzetalines=31,
                                      nzetalines=19,
                                      add_pos_damping_numbers=True,
                                      min_damp_for_adding_numbers=0.3)
        

    axs_eigen.plot(df_01['real'], df_01['imag'],
                   color=color[0],
                   #label=label,
                   linestyle='None',
                   linewidth=linewidth,
                   marker=marker,
                   markersize=markersize)

    pth.add_root_locus_part_names(eigen_real=df_01['real'],
                                  eigen_imag=df_01['imag'],
                                  eigen_part_names=df_01['names'],
                                  axis=axs_eigen,
                                  zeta_threshold=0.99)

    axs_eigen.set_xlabel(r'Real (Np/s)')
    axs_eigen.set_ylabel(r'Imaginary (rad/s)')

    #fig_eigen.tight_layout()
    fig_eigen.show()

#####################################################
# main
#####################################################
def main():
    print("#####################")
    print("Function name: ", main.__name__)

    # 3 STEPS OF 3MW THAT MADE INTO FIRST DRAFT TO IEEE TPWRS
    # run_sim_3xstepload_Z2(Z2_plini=3.0)

    # 3 STEPS OF 6MW JUST IN CASE
    # run_sim_3xstepload_Z2(Z2_plini=6.0)
    # plot_3xstepload_Z2()

    # run_sim_steps_load_Z2_eigen(Z2_plini=1.2)
        # ON the day 20220818
            # PLATPsecctrl kg = 1, Toff = 60s    

    #plot_eigen_fmeas_from_csvs(simcount_total=7,
    #                           csvfolder="//...Desktop/2022_Journal_Data/Powerfactory/simdata/20220824",
    #                           offsetfrequency=False,
    #                           plotFmeasBTC=False,
    #                           plotvpcc=True,
    #                           timeoffset=1.0,
    #                           detailplot=False) # False, True

    # EIGENVALUES FIGURE THAT MADE INTO FIRST DRAFT TO IEEE TPWRS
    # plot_eigen_fmeas_from_csvs_3charts()  # False, True


    # plot_eigen_charts_from_3_csvs()
    # plot_eigen_chart_from_1_csvs()
    # print("Nothing else done")    


if __name__ == '__main__':
    main()

