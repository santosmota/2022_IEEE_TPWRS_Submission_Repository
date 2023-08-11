#################################################################
# Generates figure ??
# which contains steps of 3MW for comparing PowerFactory and PHIL RT LAB
#################################################################

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import scipy.io

import matplotlib.pyplot as plt
# plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
plt.rcParams['mathtext.fontset'] = 'cm'  # 'cm' Computer modern # 'dejavuserif', 'dejavusans'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'cmr10'
plt.rc('axes', unicode_minus=False)

#############
# solves a warning with a previous syntax for using the package
#https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
from matplotlib.ticker import FormatStrFormatter
# from matplotlib.offsetbox import AnchoredText

def plot_charts_from_csv_mat():
    print("#####################")
    print("Function name: ", plot_charts_from_csv_mat.__name__)

    gambiarratempo = +10.0

    ###############################################################
    # hardcoded choices - FOR RT LAB - RT LAB - RTLAB
    ###############################################################
    transient_type = 'Load3'

    # sampling_time = 0.001

    plot_complete_time = False  # True  # False
    start_time = -10  # -5.0
    end_time = 130  # 20.0

    BTC_pow_pu_base = 1.54  # 1.54 MW
    FCC_pow_pu_base = 4.0
    ELC_pow_pu_base = 6.0

    WF_pow_pu_base = 12.0 / 0.8
    FLEX_pow_pu_base = -7.6 / 0.9

    GT_w_pu_base = 50.0  # Hz

    #####################################
    # SIGNAL LIST
    #####################################
    # FOLDER LOCATION
    signal_list_folder = '../RTLab/simdata/20220816/'
    siglist_fullpath = signal_list_folder + 'PlotSignalList.mat'
    mat = scipy.io.loadmat(siglist_fullpath)
    siglist = mat['signalList']
    # CREATES AN ARRAY WITH THE SIGNAL NAMES
    signal_names = []
    for name in siglist:
        for element in name:
            # print(element[0])
            signal_names.append(element[0])

    ###############################################################
    # DATA FILE - MAT FILE
    ###############################################################
    # FOLDER LOCATION
    data_folder = '../RTLab/simdata/20220816/'

    # TKINTER TO OPEN THE FILE
    # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # data_full_path_01 = askopenfilename(initialdir=data_folder)  # show an "Open" dialog box and return the path to the selected file
    data_full_path_01 = '../RTLab/simdata/20220816/PHIL_3MW_FCRN_BTCFLEX.mat'

    print('###########################')
    print('# RT LAB')
    print('Chosen file: ', data_full_path_01)
    # FROM MAT FILE TO A DICT NAMED mat
    mat01 = scipy.io.loadmat(data_full_path_01)

    # data_full_path_02 = askopenfilename(initialdir=data_folder)  # show an "Open" dialog box and return the path to the selected file
    data_full_path_02 = '../RTLab/simdata/20220816/PHIL_3MW_FCRN_BTCGTs.mat'

    print('Chosen file: ', data_full_path_02)
    mat02 = scipy.io.loadmat(data_full_path_02)

    # data_full_path_03 = askopenfilename(initialdir=data_folder)  # show an "Open" dialog box and return the path to the selected file
    data_full_path_03 = '../RTLab/simdata/20220816/PHIL_3MW_FCRN_GTs.mat'
    print('Chosen file: ', data_full_path_03)
    mat03 = scipy.io.loadmat(data_full_path_03)

    ###############################################################
    # CREATING THE NAME OF THE FIGURE, FROM THE NAME OF THE MAT FILE
    index = data_full_path_01.rfind('/')  # index to last character '/'
    figure_folder = data_full_path_01[0:index + 1]  # selects figure folder
    figure_full_path = figure_folder + 'figsteps_PowFact_RTLAB.pdf'  # adds the 'eps

    #####################################
    # EXTRACTS DATA FROM MAT FILE AND PUT IN A DATAFRAME
    # There is a dumb dict in the mat file with a 2-D table with nameless data
    for key in mat01.keys():
        dados01 = np.transpose(np.array(mat01[key]))

    for key in mat02.keys():
        dados02 = np.transpose(np.array(mat02[key]))

    for key in mat03.keys():
        dados03 = np.transpose(np.array(mat03[key]))

    df_rt_01 = pd.DataFrame(dados01, columns=signal_names)
    df_rt_02 = pd.DataFrame(dados02, columns=signal_names)
    df_rt_03 = pd.DataFrame(dados03, columns=signal_names)

    #####################################
    # TRANSIENT TYPE, TIME, AND OTHER CHOICES
    #####################################
    if transient_type == 'Load3':
        # df_rt_01.at[100000, 'Load3_connect[on/off]'] = 1.0
        trig_01 = df_rt_01['495: sig.model.gui_commands.load3_connect'].gt(0.5).idxmax()
        trig_02 = df_rt_02['495: sig.model.gui_commands.load3_connect'].gt(0.5).idxmax()
        trig_03 = df_rt_03['495: sig.model.gui_commands.load3_connect'].gt(0.5).idxmax()

    else:
        trig_01 = df_rt_01['2: Trigg signal'].gt(0.5).idxmax()
        trig_02 = df_rt_02['2: Trigg signal'].gt(0.5).idxmax()
        trig_03 = df_rt_03['2: Trigg signal'].gt(0.5).idxmax()

    print('Making array of time')
    df_rt_01['time'] = df_rt_01['1: Time'].values - df_rt_01.at[trig_01, '1: Time'] + gambiarratempo
    df_rt_02['time'] = df_rt_02['1: Time'].values - df_rt_02.at[trig_02, '1: Time'] + gambiarratempo
    df_rt_03['time'] = df_rt_03['1: Time'].values - df_rt_03.at[trig_03, '1: Time'] + gambiarratempo

    if not plot_complete_time:
        start_time_idx = df_rt_01['time'].ge(start_time).idxmax()
        end_time_idx = df_rt_01['time'].ge(end_time).idxmax()
        df_rt_01 = df_rt_01.iloc[start_time_idx:end_time_idx]

        start_time_idx = df_rt_02['time'].ge(start_time).idxmax()
        end_time_idx = df_rt_02['time'].ge(end_time).idxmax()
        df_rt_02 = df_rt_02.iloc[start_time_idx:end_time_idx]

        start_time_idx = df_rt_03['time'].ge(start_time).idxmax()
        end_time_idx = df_rt_03['time'].ge(end_time).idxmax()
        df_rt_03 = df_rt_03.iloc[start_time_idx:end_time_idx]

    ###############################################################
    # size of the figure (in inches), and linestyles
    ###############################################################
    figsizex = 10
    figsizey = 5
    fig_steps, axs_steps = plt.subplots(3, 3, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='Step3MW')
    # stiles for the RTLAB plots
    aux = 'solid'  # (0, (1, 5))  # 'dotted'   # (0, (1, 10))
    cor_rt = ['blue', 'gray', 'red']
    linstyle_rt = [aux, aux, aux]
    linewidth_rt = [0.5, 0.5, 0.5]  # if using dotted, better to use 1.0 linewidth
    labeltext_rt = ['Case 3:PHIL:BTC+FLX', 'Case 2:PHIL:BTC+GTs', 'Case 1:PHIL:GTs']

    # styles for the power factory plots
    aux = (0, (6, 4))  # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    cor_pf = ['blue', 'gray', 'red']
    linestyle_pf = [(0, (7, 3)), (0, (6, 3)), (0, (7, 4))]
    linewidth_pf = [0.75, 0.75, 0.75]  # if using dotted, better to use 1.0 linewidth
    labeltext_pf = ['Case 3:SW:BTC+FLX', 'Case 2:SW:BTC+GTs', 'Case 1:SW:GTs']

    ##########################################################################
    # PLOT
    #########################################################################
    axs_steps[0, 0].plot(df_rt_03['time'],
                         df_rt_03['325: sig.model.sm_gemMeas.Vgen_filt [rms]'] / 1000.0,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    axs_steps[0, 0].plot(df_rt_02['time'],
                         df_rt_02['325: sig.model.sm_gemMeas.Vgen_filt [rms]'] / 1000.0,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[0, 0].plot(df_rt_01['time'],
                         df_rt_01['325: sig.model.sm_gemMeas.Vgen_filt [rms]'] / 1000.0,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])


    ##########################################
    axs_steps[0, 1].plot(df_rt_01['time'],
                         df_rt_01['340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_w_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[0, 1].plot(df_rt_02['time'],
                         df_rt_02['340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_w_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[0, 1].plot(df_rt_03['time'],
                         df_rt_03['340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_w_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[0, 2].plot(df_rt_01['time'],
                         df_rt_01['355: sig.model.windfarm_meas.COL.Pavg_pu'] * WF_pow_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[0, 2].plot(df_rt_02['time'],
                         df_rt_02['355: sig.model.windfarm_meas.COL.Pavg_pu'] * WF_pow_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[0, 2].plot(df_rt_03['time'],
                         df_rt_03['355: sig.model.windfarm_meas.COL.Pavg_pu'] * WF_pow_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[1, 0].plot(df_rt_01['time'],
                         df_rt_01['336: sig.model.sm_gemMeas.Pgen_W'] / 1000000.0,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[1, 0].plot(df_rt_02['time'],
                         df_rt_02['336: sig.model.sm_gemMeas.Pgen_W'] / 1000000.0,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[1, 0].plot(df_rt_03['time'],
                         df_rt_03['336: sig.model.sm_gemMeas.Pgen_W'] / 1000000.0,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[1, 1].plot(df_rt_03['time'],
                         (df_rt_03['305: sig.model.loads.L1_P_kW'] +
                          df_rt_03['309: sig.model.loads.L2_P_kW'] +
                          df_rt_03['313: sig.model.loads.L3_P_kW']) / 1000.0,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    axs_steps[1, 1].plot(df_rt_02['time'],
                         (df_rt_02['305: sig.model.loads.L1_P_kW'] +
                          df_rt_02['309: sig.model.loads.L2_P_kW'] +
                          df_rt_02['313: sig.model.loads.L3_P_kW']) / 1000.0,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[1, 1].plot(df_rt_01['time'],
                         (df_rt_01['305: sig.model.loads.L1_P_kW'] +
                          df_rt_01['309: sig.model.loads.L2_P_kW'] +
                          df_rt_01['313: sig.model.loads.L3_P_kW']) / 1000.0,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    ##########################################
    axs_steps[1, 2].plot(df_rt_01['time'],
                         df_rt_01['431: sig.model.flex_meas.Pavg_pu'] * FLEX_pow_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[1, 2].plot(df_rt_02['time'],
                         df_rt_02['431: sig.model.flex_meas.Pavg_pu'] * FLEX_pow_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[1, 2].plot(df_rt_03['time'],
                         df_rt_03['431: sig.model.flex_meas.Pavg_pu'] * FLEX_pow_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[2, 0].plot(df_rt_01['time'],
                         df_rt_01['459: sig.model.dcgrid_meas.FC_Pdc_pu'] * FCC_pow_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    # axs_steps[2, 0].plot(df_rt_01['time'],
    #                     (df_rt_01['456: sig.model.dcgrid_meas.FC_Idc_pu'] * df_rt_01['458: sig.model.dcgrid_meas.FCC_Vdc_pu']) * FCC_pow_pu_base,
    #                     color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
    #                     label=labeltext_rt[0])

    axs_steps[2, 0].plot(df_rt_02['time'],
                         df_rt_02['459: sig.model.dcgrid_meas.FC_Pdc_pu'] * FCC_pow_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[2, 0].plot(df_rt_03['time'],
                         df_rt_03['459: sig.model.dcgrid_meas.FC_Pdc_pu'] * FCC_pow_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[2, 1].plot(df_rt_01['time'],
                         df_rt_01['467: sig.model.dcgrid_meas.BT_Pdc_pu'] * BTC_pow_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[2, 1].plot(df_rt_02['time'],
                         df_rt_02['467: sig.model.dcgrid_meas.BT_Pdc_pu'] * BTC_pow_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[2, 1].plot(df_rt_03['time'],
                         df_rt_03['467: sig.model.dcgrid_meas.BT_Pdc_pu'] * BTC_pow_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ##########################################
    axs_steps[2, 2].plot(df_rt_01['time'],
                         df_rt_01['463: sig.model.dcgrid_meas.EL_Pdc_pu'] * ELC_pow_pu_base,
                         color=cor_rt[0], linewidth=linewidth_rt[0], linestyle=linstyle_rt[0],
                         label=labeltext_rt[0])

    axs_steps[2, 2].plot(df_rt_02['time'],
                         df_rt_02['463: sig.model.dcgrid_meas.EL_Pdc_pu'] * ELC_pow_pu_base,
                         color=cor_rt[1], linewidth=linewidth_rt[1], linestyle=linstyle_rt[1],
                         label=labeltext_rt[1])

    axs_steps[2, 2].plot(df_rt_03['time'],
                         df_rt_03['463: sig.model.dcgrid_meas.EL_Pdc_pu'] * ELC_pow_pu_base,
                         color=cor_rt[2], linewidth=linewidth_rt[2], linestyle=linstyle_rt[2],
                         label=labeltext_rt[2])

    ###############################################################
    # POWER FACTORY
    ###############################################################
    csvfolder = "../Powerfactory/simdata/"
    csvfolder = csvfolder + "20220824_3steps/"
    print('###########################')
    print('# POWERFACTORY')
    print("        csvfolder: ", csvfolder)

    for simcount in range(2, -1, -1):
        ##########################################################################
        # PLOT
        ##########################################################################

        df_PowFact = pd.read_csv(csvfolder + 'simulationdata_0' + str(simcount) + '.csv')
        print("                 ", 'simulationdata_0' + str(simcount) + '.csv')

        df_PowFact["time"] = df_PowFact["time"] + gambiarratempo

        axs_steps[0][0].plot(df_PowFact["time"], df_PowFact["vpcc"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[0][1].plot(df_PowFact["time"], df_PowFact["fmeas"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[0][2].plot(df_PowFact["time"], df_PowFact["pwf"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[1][0].plot(df_PowFact["time"], df_PowFact["pgts"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[1][1].plot(df_PowFact["time"], df_PowFact["pfixed"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[1][2].plot(df_PowFact["time"], df_PowFact["pflex"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[2][0].plot(df_PowFact["time"], df_PowFact["pfcc"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[2][1].plot(df_PowFact["time"], df_PowFact["pbtc"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])

        axs_steps[2][2].plot(df_PowFact["time"], df_PowFact["pelc"],
                             linestyle=linestyle_pf[simcount],
                             linewidth=linewidth_pf[simcount],
                             color=cor_pf[simcount],
                             label=labeltext_pf[simcount])


    ##########################################################################
    # axis limits
    ##########################################################################
    axs_steps[2][2].set_xticks(np.arange(-20, 180, 20))
    axs_steps[2][2].set_xlim([0, 120])

    axs_steps[0][0].set_yticks(np.arange(-10.900, 12.000, 0.025))
    axs_steps[0][0].set_ylim([10.950, 11.050])
    axs_steps[0][0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps[2][0].set_xlabel(r'Time (s)')
    axs_steps[2][1].set_xlabel(r'Time (s)')
    axs_steps[2][2].set_xlabel(r'Time (s)')

    axs_steps[0][0].set_ylabel(r'Busbar volt. (kV)')
    axs_steps[0][1].set_ylabel(r'Busbar freq. (Hz)')
    axs_steps[0][2].set_ylabel(r'WF power (MW)')

    axs_steps[1][0].set_ylabel(r'GTs elec. power (MW)')
    axs_steps[1][1].set_ylabel(r'Load power (MW)')
    axs_steps[1][2].set_ylabel(r'FLX power (MW)')

    axs_steps[2][0].set_ylabel(r'FCC power (MW)')
    axs_steps[2][1].set_ylabel(r'BTC power (MW)')
    axs_steps[2][2].set_ylabel(r'ELC power (MW)')

    ##########################################################################
    # axis limits
    ##########################################################################
    axs_steps[2][2].set_xticks(np.arange(-20, 180, 10))
    axs_steps[2][2].set_xlim([0, 100])

    axs_steps[0][0].set_yticks(np.arange(-10.900, 12.000, 0.02))
    axs_steps[0][0].set_ylim([10.92, 11.02])
    axs_steps[0][0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    axs_steps[0][1].set_yticks(np.arange(48.000, 51, 0.2))
    axs_steps[0][1].set_ylim([48.95, 50.05])
    axs_steps[0][1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[0][2].set_yticks(np.arange(11, 13, 0.1))
    axs_steps[0][2].set_ylim([11.6, 11.9])
    axs_steps[0][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[1][0].set_yticks(np.arange(29, 40, 1))
    axs_steps[1][0].set_ylim([31, 36])
    axs_steps[1][0].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    axs_steps[1][1].set_yticks(np.arange(35, 45, 1))
    axs_steps[1][1].set_ylim([36.8, 40.2])
    axs_steps[1][1].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    axs_steps[1][2].set_yticks(np.arange(3, 7, 0.5))
    axs_steps[1][2].set_ylim([4.3, 6.2])
    axs_steps[1][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][0].set_yticks(np.arange(0, 3, 0.5))
    axs_steps[2][0].set_ylim([-0.05, 2.5])
    axs_steps[2][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][1].set_yticks(np.arange(0, 3, 0.5))
    # axs_steps[2][1].set_ylim([-0.05, 2.5])
    axs_steps[2][1].set_ylim([-0.05, 1.55])
    axs_steps[2][1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    axs_steps[2][2].set_yticks(np.arange(-3, 1, 0.5))
    # axs_steps[2][2].set_ylim([-2.55, 0.0])
    axs_steps[2][2].set_ylim([-1.55, 0.05])
    axs_steps[2][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # https://matplotlib.org/stable/gallery/color/named_colors.html
    # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'

    axs_steps[0][0].annotate(r'a', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][1].annotate(r'b', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][2].annotate(r'c', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][0].annotate(r'd', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][1].annotate(r'e', xy=(0.15, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][2].annotate(r'f', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][0].annotate(r'g', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][1].annotate(r'h', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[2][2].annotate(r'i', xy=(0.9, 0.15), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axs_steps[1][1].legend(loc='best', frameon=False, prop={'size': 9})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig_steps.align_ylabels(axs_steps[:, :])
    fig_steps.tight_layout()
    fig_steps.show()
    # plt.savefig(figure_full_path, format='eps')
    plt.savefig(figure_full_path, format='pdf')

    plt.show()


def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_charts_from_csv_mat()

if __name__ == '__main__':
    main()
