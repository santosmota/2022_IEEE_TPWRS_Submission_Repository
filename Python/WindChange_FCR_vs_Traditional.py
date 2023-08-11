#################################################################
# Generates figure 10
# which contains steps of 6MW for comparing FCR with Traditional Droop
#################################################################

from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import scipy.io

import matplotlib.pyplot as plt

# plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'cmr10'
plt.rc('axes', unicode_minus=False)

#############
# solves a warning with a previous syntax for using the package
# https://stackoverflow.com/questions/65645194/warning-set-it-to-a-single-string-instead
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
from matplotlib.ticker import FormatStrFormatter


def plot_charts():
    print("#####################")
    print("Function name: ", plot_charts.__name__)

    ###############################################################
    # hardcoded choices
    ###############################################################
    transient_type = 'Wind'  # the 6MW one
    # transient_type = 'Load3'  # the 3MW one

    GT_w_pu_base = 50.0  # Hz
    GT_S_pu_base = 88.0

    Sys_P_pu_base = 88.0 * 0.8

    FLEX_pu_base = -7.6 / 0.9
    BTC_pu_base = 1.54

    FCC_pu_base = 4.0
    ELC_pu_base = 6.0

    COL_S_pu_base = 12.0 / 0.8

    gambiarra_time = 10.0

    #####################################
    # SIGNAL LIST
    #####################################
    # FOLDER LOCATION
    signal_list_folder = '../RTLab/simdata/20230106/'
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


    # TKINTER TO OPEN THE FILE
    # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # data_folder = '../../RTLab/simdata/20221219/'
    # data_full_path_01 = askopenfilename(initialdir=data_folder)  # show an "Open" dialog box and return the path to the selected file

    #################
    # FILE ONE
    if transient_type == 'Load3':
        data_full_path = '../RTLab/simdata/20221220/RT_Wind_3MW_FCR.mat'
    else:
        # data_full_path = '../RTLab/simdata/20221220/RT_Wind_6MW_FCR.mat'
        data_full_path = '../RTLab/simdata/20230106/PHIL_Wind_12_6m_s_FCR.mat'

    print('Chosen file ONE: ', data_full_path)
    mat = scipy.io.loadmat(data_full_path)
    for key in mat.keys():
        dados = np.transpose(np.array(mat[key]))

    df_01 = pd.DataFrame(dados, columns=signal_names)

    #################
    # FILE TWO
    if transient_type == 'Load3':
        data_full_path = '../RTLab/simdata/20221220/PHIL_Wind_3MW_Trad.mat'
    else:
        # data_full_path = '../RTLab/simdata/20221223/RT_Wind_6MW_Trad.mat'
        data_full_path = '../RTLab/simdata/20230106/PHIL_Wind_12_6m_s_Trad.mat'

    print('Chosen file TWO: ', data_full_path)
    mat = scipy.io.loadmat(data_full_path)
    for key in mat.keys():
        dados = np.transpose(np.array(mat[key]))

    df_02 = pd.DataFrame(dados, columns=signal_names)

    ###############################################################
    # CREATING THE NAME OF THE FIGURE, FROM THE NAME OF THE MAT FILE
    # index = data_full_path.rfind('/')  # index to last character '/'
    # figure_folder = data_full_path[0:index + 1]  # selects figure folder

    figure_full_path = '../RTLab/simdata/20230106/' + 'Wind_12_6_m_s.pdf'

    #####################################
    # TRANSIENT TYPE, TIME, AND OTHER CHOICES
    #####################################
    if transient_type == 'Load3':
        trig_01 = df_01['499: sig.model.gui_commands.load3_connect'].gt(0.5).idxmax()
        trig_02 = df_02['499: sig.model.gui_commands.load3_connect'].gt(0.5).idxmax()

    elif transient_type == 'Load2':
        trig_01 = df_01['498: sig.model.gui_commands.load2_connect'].gt(0.5).idxmax()
        trig_02 = df_02['498: sig.model.gui_commands.load2_connect'].gt(0.5).idxmax()

    else:
        trig_01 = df_01['359: sig.model.windfarm_meas.COL.Pavg_pu'].lt(0.8).idxmax()
        trig_02 = df_02['359: sig.model.windfarm_meas.COL.Pavg_pu'].lt(0.8).idxmax()

    print('Making array of time')
    df_01['time'] = df_01['1: Time'].values - df_01.at[trig_01, '1: Time'] + gambiarra_time
    df_02['time'] = df_02['1: Time'].values - df_02.at[trig_02, '1: Time'] + gambiarra_time

    ###############################################################
    # size of the figure (in inches)
    ###############################################################
    # figsizex = 4
    # figsizey = 6  # 3 on top of each other

    figsizex = 10  # same as in Fig.9 first submission
    figsizey = 3.3  # 5 was in the Fig.9 of first submission

    fig_steps, axs_steps = plt.subplots(2, 3, sharex=True,
                                        figsize=(figsizex, figsizey),
                                        num='FCRxTrad')

    cor = ['blue', 'red']
    lst = ['solid', 'solid', 'dashed']
    linw = [0.75, 0.75]  # if using dotted, better to use 1.0 linewidth
    lab = [r'FCR$_{\textrm{N}+\textrm{D}}$', 'Traditional']

    ##########################################################################
    # PLOT
    #########################################################################
    # selecting the figure
    # plt.figure('FCRD')  # select the figure

    ##########################################
    # Busbar frequency
    axs_steps[0][0].plot(df_01['time'],
                      df_01['340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_w_pu_base,
                      color=cor[0], linewidth=linw[0], linestyle=lst[0],
                      label=lab[0])

    axs_steps[0][0].plot(df_02['time'],
                      df_02['340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_w_pu_base,
                      color=cor[1], linewidth=linw[1], linestyle=lst[1],
                      label=lab[1])

    axs_steps[0][0].plot([5, 55],
                         [49, 49],
                         color='black', linewidth=linw[0], linestyle=lst[2],
                         label=r'FCR$_{\textrm{N},\textrm{D}}$ limit')

    ##########################################
    # Mechanical power - GTs
    axs_steps[1][0].plot(df_01['time'],
                      df_01['347: sig.model.turb_meas.driving_torque'] * df_01[
                          '340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_S_pu_base,
                      color=cor[0], linewidth=linw[0], linestyle=lst[0],
                      label=r'FCR$_{\textrm{D}}$+Secon.pow.')

    axs_steps[1][0].plot(df_01['time'],
                         df_01['518: sig.model.secCtrl_meas.Psec_gt'] * GT_S_pu_base + 0.38 * GT_S_pu_base,
                         color=cor[0], linewidth=linw[0], linestyle=lst[2],
                         label=lab[0])

    axs_steps[1][0].plot(df_02['time'],
                      df_02['347: sig.model.turb_meas.driving_torque'] * df_02[
                          '340: sig.model.sm_gemMeas.sm_freq [pu]'] * GT_S_pu_base,
                      color=cor[1], linewidth=linw[1], linestyle=lst[1],
                      label=r'Trad.droop+Secon.pow.')

    axs_steps[1][0].plot(df_02['time'],
                         df_02['518: sig.model.secCtrl_meas.Psec_gt'] * GT_S_pu_base + 0.38 * GT_S_pu_base,
                         color=cor[1], linewidth=linw[1], linestyle=lst[2],
                         label=lab[1])

    ##########################################
    # Battery
    axs_steps[0][1].plot(df_01['time'],
                      df_01['471: sig.model.dcgrid_meas.BT_Pdc_pu'] * BTC_pu_base,
                      color=cor[0], linewidth=linw[0], linestyle=lst[0],
                      label=lab[0])

    axs_steps[0][1].plot(df_02['time'],
                      df_02['471: sig.model.dcgrid_meas.BT_Pdc_pu'] * BTC_pu_base,
                      color=cor[1], linewidth=linw[1], linestyle=lst[1],
                      label=lab[1])

    ##########################################
    # Flex
    axs_steps[1][1].plot(df_01['time'],
                      df_01['435: sig.model.flex_meas.Pavg_pu'] * FLEX_pu_base,
                      color=cor[0], linewidth=linw[0], linestyle=lst[0],
                      label=lab[0])

    axs_steps[1][1].plot(df_02['time'],
                      df_02['435: sig.model.flex_meas.Pavg_pu'] * FLEX_pu_base,
                      color=cor[1], linewidth=linw[1], linestyle=lst[1],
                      label=lab[1])

    ##########################################
    # Load
    axs_steps[0][2].plot(df_01['time'],
                         df_01['305: sig.model.loads.L1_P_kW'] / 1000.0 +
                         df_01['309: sig.model.loads.L2_P_kW'] / 1000.0 +
                         df_01['313: sig.model.loads.L3_P_kW'] / 1000.0 -
                         df_01['359: sig.model.windfarm_meas.COL.Pavg_pu'] * COL_S_pu_base,
                         color=cor[0], linewidth=linw[0], linestyle=lst[0],
                         label=lab[0])

    axs_steps[0][2].plot(df_02['time'],
                         df_02['305: sig.model.loads.L1_P_kW'] / 1000.0 +
                         df_02['309: sig.model.loads.L2_P_kW'] / 1000.0 +
                         df_02['313: sig.model.loads.L3_P_kW'] / 1000.0 -
                         df_02['359: sig.model.windfarm_meas.COL.Pavg_pu'] * COL_S_pu_base,
                         color=cor[1], linewidth=linw[1], linestyle=lst[1],
                         label=lab[1])


    ##########################################
    # Secondary controller
    # ELC + FCC
    axs_steps[1][2].plot(df_01['time'],
                         df_01['463: sig.model.dcgrid_meas.FC_Pdc_pu'] * FCC_pu_base +
                         df_01['467: sig.model.dcgrid_meas.EL_Pdc_pu'] * ELC_pu_base,
                         color=cor[0], linewidth=linw[0], linestyle=lst[0],
                         label=r'ELC+FCC(FCR)')

    axs_steps[1][2].plot(df_02['time'],
                         df_02['463: sig.model.dcgrid_meas.FC_Pdc_pu'] * FCC_pu_base +
                         df_02['467: sig.model.dcgrid_meas.EL_Pdc_pu'] * ELC_pu_base,
                         color=cor[1], linewidth=linw[1], linestyle=lst[1],
                         label=r'ELC+FCC(Tradit.)')

    # Secondary controller
    axs_steps[1][2].plot(df_01['time'],
                         df_01['517: sig.model.secCtrl_meas.Psec_pusysb'] * Sys_P_pu_base,
                         color=cor[0], linewidth=linw[0], linestyle=lst[2],
                         label=r'Sec.ref.(FCR)')

    axs_steps[1][2].plot(df_02['time'],
                         df_02['517: sig.model.secCtrl_meas.Psec_pusysb'] * Sys_P_pu_base,
                         color=cor[1], linewidth=linw[1], linestyle=lst[2],
                         label=r'Sec.ref.(Tradit.)')

    ##########################################################################
    # axis names
    ##########################################################################
    axs_steps[1][0].set_xlabel(r'Time (s)')
    axs_steps[1][1].set_xlabel(r'Time (s)')
    axs_steps[1][2].set_xlabel(r'Time (s)')

    axs_steps[0][0].set_ylabel(r'Busbar freq.(Hz)')
    axs_steps[1][0].set_ylabel(r'GTs mech.power(MW)')
    axs_steps[0][1].set_ylabel(r'BTC power (MW)')
    axs_steps[1][1].set_ylabel(r'FLEX power (MW)')
    axs_steps[0][2].set_ylabel(r'Load minus WF(MW)')
    axs_steps[1][2].set_ylabel(r'Second.control.(MW)')

    ##########################################################################
    # axis limits
    ##########################################################################
    axs_steps[1][0].set_xticks(np.arange(-20, 180, 10))
    axs_steps[1][0].set_xlim([-0, 90])  # 120

    axs_steps[0][0].set_yticks(np.arange(40, 60, 1))
    axs_steps[0][0].set_ylim([47, 50.25])

    axs_steps[1][0].set_yticks(np.arange(30, 46, 2))
    axs_steps[1][0].set_ylim([32, 40])

    axs_steps[0][2].set_yticks(np.arange(10, 40, 2))
    axs_steps[0][2].set_ylim([24, 36])

    axs_steps[1][2].set_yticks(np.arange(-12, 20, 4))
    axs_steps[1][2].set_ylim([-13, 9])

    #axs_steps[1][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ## axs_steps[0][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ## axs_steps[1][2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    ##########################################################################
    # Arrows
    ##########################################################################
    # GT Power
    axs_steps[1][0].annotate(r'Tradit.droop+sec.power',
                             xy=(23, 39.5), xycoords='data',
                             fontsize=9,
                             xytext=(42, 39.0), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    axs_steps[1][0].annotate(r'FCR$_{\textrm{D}}$+sec.power',
                             fontsize=9,
                             xy=(12.0, 39), xycoords='data',
                             xytext=(35.0, 34.5), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    axs_steps[1][0].annotate(r'Secondary power references (dashed)',
                             fontsize=9,
                             xy=(12.0, 34.5), xycoords='data',
                             xytext=(16.0, 32.5), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    ##########################
    # BTC power
    axs_steps[0][1].annotate(r'FCR$_{\textrm{N}}$',
                             fontsize=9,
                             xy=(55.0, 1.22), xycoords='data',
                             xytext=(70.0, 1.35), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    axs_steps[0][1].annotate(r'Traditional droop',
                             fontsize=9,
                             xy=(45, 0.8), xycoords='data',
                             xytext=(20, 0.25), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    ##########################
    # FLEX power
    axs_steps[1][1].annotate(r'Traditional droop',
                             fontsize=9,
                             xy=(50, 5.3), xycoords='data',
                             xytext=(15, 5.8), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    axs_steps[1][1].annotate(r'FCR$_{\textrm{N}}$',
                             fontsize=9,
                             xy=(80, 5.45), xycoords='data',
                             xytext=(75, 4.75), textcoords='data',
                             ha='left',
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    ##########################################################################
    # chart identification - legend - abcdefghi
    ##########################################################################
    # # https://matplotlib.org/stable/gallery/color/named_colors.html
    # # colors lightgray gray aliceblue whitesmoke
    corlegenda = 'whitesmoke'

    axs_steps[0][0].annotate(r'a', xy=(0.05, 0.3), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][1].annotate(r'b', xy=(0.05, 0.3), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[0][2].annotate(r'c', xy=(0.05, 0.3), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][0].annotate(r'd', xy=(0.05, 0.3), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][1].annotate(r'e', xy=(0.05, 0.3), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    axs_steps[1][2].annotate(r'f', xy=(0.05, 0.2), xycoords='axes fraction',
                             bbox=dict(boxstyle='circle', fc=corlegenda))

    ##########################################################################
    # axis legends
    ##########################################################################
    axs_steps[0][0].legend(loc='best', frameon=False, prop={'size': 9})
    axs_steps[0][2].legend(loc='best', frameon=False, prop={'size': 9})
    axs_steps[1][2].legend(loc='best', frameon=False, prop={'size': 9})

    ##########################################################################
    # align, tighten, shown and save
    ##########################################################################
    fig_steps.align_ylabels(axs_steps[:])
    fig_steps.tight_layout()
    fig_steps.show()
    plt.savefig(figure_full_path, format='pdf')

    plt.show()


def main():
    print("#####################")
    print("Function name: ", main.__name__)

    plot_charts()


if __name__ == '__main__':
    main()

