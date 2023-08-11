##############################################################################################
# Auxiliary functions to control PowerFactory via Python
#     	The  functions may be ``hardcoded'' to the specific project
#     	Some functions may be more generic
###############################################################################################
# By: Daniel dos Santos Mota, 2023-01-05
# 	This file has been copied from a private repository into this public one.
#       Some comments have been added only to the copied file.
#	It has not been tested after copying.
###############################################################################################

import numpy as np
import pandas as pd

# open_project_study_case(app, proj_name='202202_RMS_Tests', study_case='Study Case'):
# calc_ini_rms(app, dtgrd=0.001):
# run_rms(app, tstop=15.0):
# run_modal(app):
# save_snapshot(app, suppressUserMessage=1):
# load_snapshot(app, suppressUserMessage=1):
# set_switch_transient_param(app, trans_name='PCC11kV_Z2',...
# def set_load_param(app, load_name='Z2.ElmLod',
# get_res_time(app, elmres):
# get_res_element(app, elmres, n_row, element_name='PLATPmeas.ElmVsc', signal_name='s:pfixed'):
# get_eigen_real_imag_participation(app, part_threshold=0.5,...
# set_iactrefgen_droop(app, controller_name='*BCiactref.ElmDsl',
# set_govdb_N_droop(app, controller_name='*GT1govdb.ElmDsl',


###############################################################################################
# FUNCTION: Open Project and Study Case
###############################################################################################
def open_project_study_case(app, proj_name='202207_RMS_Tests', study_case='Study Case'):
    print('----------------')
    print('Function:', open_project_study_case.__name__)

    # activate project
    project = app.ActivateProject(proj_name)
    proj = app.GetActiveProject()
    print('    Active Project : ', proj_name)

    # get the study case folder and activate project
    oFolder_studycase = app.GetProjectFolder('study')
    oCase = oFolder_studycase.GetContents(study_case)[0]
    oCase.Activate()
    print('    Active Study Case: ', study_case)

    return project, proj

###############################################################################################
# FUNCTION: Calculate initial conditions for rms Simulation
###############################################################################################
def calc_ini_rms(app, dtgrd=0.001):
    print('----------------')
    print('Function: ', calc_ini_rms.__name__)

    # calculate initial conditions
    o_init = app.GetFromStudyCase('ComInc')  # get initial condition calculation object
    o_init.iopt_sim = 'rms'  # force rms simulation
    o_init.iopt_net = 'sym'  # force balanced
    o_init.dtgrd = dtgrd     # integration time
    o_init.Execute()
    print('    Power factory command: ComInc.Execute')
    print('        simulation option:', o_init.iopt_sim)
    print('        network option:', o_init.iopt_net, ';sym=balanced     rst:unbalanced')
    print('        integration step size:', o_init.dtgrd, 's')


###############################################################################################
# FUNCTION: Set initial conditions and run RMS simulation
###############################################################################################
def run_rms(app, tstop=15.0):
    print('----------------')
    print('Function: ', run_rms.__name__)
    print('    tstop = ', tstop, 's')

    # run RMS-simulation
    o_rms = app.GetFromStudyCase('ComSim')  # get RMS-simulation object
    o_rms.tstop = tstop
    o_rms.Execute()
    print('    Power factory command: ComSim.Execute')

###############################################################################################
# FUNCTION: run modal analysis
###############################################################################################
def run_modal(app):
    print('----------------')
    print('Function: ', run_modal.__name__)
    print('    iopt_met = 0; 0:QR/QZ-Method     1:Selective method (Arnoldi/Lanczos)')
    print('    iLeft = 1')
    print('    iRight = 1')
    print('    iPart = 1')

    o_mod = app.GetFromStudyCase('ComMod')  # get Modal analysis object
    o_mod.iopt_met = 0  # 0:QR/QZ-Method     1:Selective method (Arnoldi/Lanczos)
    o_mod.iLeft = 1
    o_mod.iRight = 1
    o_mod.iPart = 1
    o_mod.Execute()
    print('    Power factory command: ComMod.Execute')


###############################################################################################
# FUNCTION: Save Snapshot
###############################################################################################
def save_snapshot(app, suppressUserMessage=1):
    print('----------------')
    print('Function: ', save_snapshot.__name__)
    print('    snapshotFilePath = empty, save to non persistent memory')
    print('    suppressUserMessage = ', suppressUserMessage, ': 1=supress, 0=asks before file overwriting')

    # run RMS-simulation
    o_rms = app.GetFromStudyCase('ComSim')  # get RMS-simulation object
    o_rms.SaveSnapshot()
    print('    Power factory command: ComSim.SaveSnapshot')

###############################################################################################
# FUNCTION: Load Snapshot
###############################################################################################
def load_snapshot(app, suppressUserMessage=1):
    print('----------------')
    print('Function: ', load_snapshot.__name__)
    print('    snapshotFilePath = empty, load from non persistent memory')
    print('    suppressUserMessage = ', suppressUserMessage, ': 1=supress, 0=asks before data overwriting')

    # run RMS-simulation
    o_rms = app.GetFromStudyCase('ComSim')  # get RMS-simulation object
    o_rms.LoadSnapshot()
    print('    Power factory command: ComSim.LoadSnapshot')


###############################################################################################
# FUNCTION: Set transient data
###############################################################################################
def set_switch_transient_param(app, trans_name='PCC11kV_Z2',
                               outserv=0,      # 0: in service       1: out of service
                               time=10,        # time of the transient in seconds
                               i_switch=1,     # 0:open              1: close
                               i_allph=1,      # 0:not all phases    1: all phase
                               i_a=1,          # 0:not this phase    1: this phase
                               i_b=1,          # 0:not this phase    1: this phase
                               i_c=1):          # 0:not this phase    1: this phase
    print('----------------')
    print('Function: ', set_switch_transient_param.__name__)
    transient_folder = app.GetFromStudyCase("Simulation Events/Fault.IntEvt")
    transients = transient_folder.GetContents()

    if transients != []:
        aux = 0
        for tran in transients:
            print('    loc_name: ', tran.loc_name)
            if tran.loc_name == trans_name:
                aux = 1
                tran.outserv = outserv
                tran.mtime = 0              # hours hardcoded to zero
                tran.hrtime = 0             # minutes hardcoded to zero
                tran.time = time            # time in seconds, accepts more than 60s, i.e., 1min30 -> 90s
                tran.i_switch = i_switch
                print('        outserv: ', tran.outserv, '; 0: in service    1: out of service')
                print('        hrtime: zero')
                print('        mtime: zero')
                print('        time: ', tran.time, 's')
                print('        i_switch: ', tran.i_switch, '; 0:open     1: close')

                if i_allph == 1:
                    tran.i_allph = i_allph
                    print('        i_allph: ', tran.i_allph, '; 1: all phases at once')
                else:
                    tran.i_a = i_a
                    tran.i_b = i_b
                    tran.i_c = i_c
                    print('        i_a: ', tran.i_a, '; 1: switch this phase')
                    print('        i_b: ', tran.i_b, '; 1: switch this phase')
                    print('        i_c: ', tran.i_c, '; 1: switch this phase')
            #else:
                #print('        No changes to this transient')
        if aux == 0:
            print(trans_name, ': search string not found (do not use .Evt*, not wildcards like *')
    else:
        print('No transients found in Simulation Events/Fault.IntEvt')

###############################################################################################
# FUNCTION: Set load parameters
###############################################################################################
def set_load_param(app, load_name='Z2.ElmLod',
                   input_mode='PC',    # DEF: default, PC: P, cos(phi)
                   bal_unb=0,          # 0: Balanced     1:Unbalanced
                   plini=3,            # active power in MW
                   qlini=0.986,          # reactive power
                   coslini=0.95,       # cosinus phi
                   pf_recap=0,         # 0: ind          1: cap
                   u0=1.0):            # rated voltage in pu
    print('----------------')
    print('Function: ', set_load_param.__name__)

    loads = app.GetCalcRelevantObjects(load_name)

    if loads != []:
        for load in loads:
            if input_mode == 'PC':
                load.mode_inp = input_mode
                load.i_sym = bal_unb
                load.plini = plini
                load.coslini = coslini
                load.pf_recap = pf_recap
                load.u0 = u0
                print('    load name: ', load.loc_name)
                print('        mode_inp: ', load.mode_inp)
                print('        i_sym: ', load.i_sym)
                print('        plini: ', load.plini)
                print('        coslini: ', load.coslini)
                print('        pf_recap: ', load.pf_recap)
            elif input_mode == 'DEF':
                load.mode_inp = input_mode
                load.i_sym = bal_unb
                load.plini = plini
                load.qlini = qlini
                load.u0 = u0
                print('    load name: ', load.loc_name)
                print('        mode_inp: ', load.mode_inp)
                print('        i_sym: ', load.i_sym)
                print('        plini: ', load.plini)
                print('        qlini: ', load.coslini)
            else:
                print('Load input_mode should either be PC(MW, cos phi) or DEF(MW, MVar)')
    else:
        print(load_name, ': load name not found')



###############################################################################################
# FUNCTION: Get time of the simulation results
###############################################################################################
def get_res_time(app, elmres):
    print('----------------')
    print('Function: ', get_res_time.__name__)
    print('    returns: b:tnow')

    n_row = elmres.GetNumberOfRows()

    # Get index of variable of interest
    col_index_time = app.ResGetIndex(elmres, elmres, 'b:tnow')

    # pre-allocate result variables
    result_time = np.zeros(n_row)

    # get results for each time step
    for i in range(n_row):
        result_time[i] = app.ResGetData(elmres, i, col_index_time)[1]

    return result_time


###############################################################################################
# FUNCTION: Get Results from element's RMS simulation
###############################################################################################
def get_res_element(app, elmres, n_row, element_name='PLATPmeas.ElmVsc', signal_name='s:pfixed'):
    print('----------------')
    print('Function: ', get_res_element.__name__)
    print('    element name =', element_name)
    print('    signal name  =', signal_name)

    o_element = app.GetCalcRelevantObjects(element_name)[0]

    # Get index of variable of interest
    col_index_signal = app.ResGetIndex(elmres, o_element, signal_name)

    # pre-allocate result variables
    result_signal = np.zeros(n_row)

    # get results for each time step
    for i in range(n_row):
        result_signal[i] = app.ResGetData(elmres, i, col_index_signal)[1]

    return result_signal


###############################################################################################
# FUNCTION: Get eigen values real and imaginary parts  # in work for getting participation factors
###############################################################################################
def get_eigen_real_imag_participation(app, part_threshold=0.5,
                                      elim_repeated_names=True, print_names_hard_way=False,
                                      include_states_in_names=False,
                                      add_partfact_to_name=False,
                                      savetotaleigen=False,
                                      csveigentotname='teste.csv'
                                      ):
    print('----------------')
    print('Function: ', get_eigen_real_imag_participation.__name__)
    print("    Modal/Eigenvalue Analysis(1).ElmRes")

    mod_res = app.GetFromStudyCase('Modal/Eigenvalue Analysis(1).ElmRes')
    mod_res.Load()

    n_row = mod_res.GetNumberOfRows()
    n_col = mod_res.GetNumberOfColumns()

    # Find the names of the columns the hard way
    if print_names_hard_way == True:
        for i in range(0, n_col, 1):
            print('--------------------------------------')
            print('Column number:', i)
            obj = mod_res.GetObject(i)
            print('    Object.loc_name:', obj.loc_name)
            print('    Long description:', mod_res.GetDescription(i, 0))
            #print('    Short description:', mod_res.GetDescription(i, 1))
            print('    Variable name:', mod_res.GetVariable(i))
            print('    Value[0]:', mod_res.GetValue(0, i)[0])
            print('    Value[1]:', mod_res.GetValue(0, i)[1])

    if savetotaleigen:
        com_res = app.GetFromStudyCase('Result Export.ComRes')
        # com_res.pResult = 'Modal/Eigenvalue Analysis(1).ElmRes'
        com_res.f_name = csveigentotname
        com_res.Execute()
                
    col_index_real = mod_res.FindColumn('b:eigvalr')
    col_index_imag = mod_res.FindColumn('b:eigvali')

    eigen_real = np.zeros(n_row)
    eigen_imag = np.zeros(n_row)
    eigen_part_names = []

    for i in range(n_row):
        eigen_part_names.append('')
        # print(' b:eigvalr= ', ModalRes.GetValue(i, ColIndex_Real)[1],
        #      ' b:eigvali= ', ModalRes.GetValue(i, ColIndex_Imag)[1])
        eigen_real[i] = mod_res.GetValue(i, col_index_real)[1]
        eigen_imag[i] = mod_res.GetValue(i, col_index_imag)[1]
        for j in range(0, n_col, 1):
            var_name = mod_res.GetVariable(j)
            if var_name.endswith('c:p_mag'):
                part_mag = mod_res.GetValue(i, j)[1]
                if part_mag > part_threshold:
                    obj = mod_res.GetObject(j)
                    if not include_states_in_names:
                        #print('Eigenvalue: ', eigen_real[i], ',', eigen_imag[i], ':', obj.loc_name, var_name, '= ', part_mag)
                        if elim_repeated_names:
                            if not eigen_part_names[i].endswith(obj.loc_name + ','):
                                eigen_part_names[i] = eigen_part_names[i] + obj.loc_name + ','
                        else:
                            eigen_part_names[i] = eigen_part_names[i] + obj.loc_name + ','
                    else:
                        eigen_part_names[i] = eigen_part_names[i] + obj.loc_name + ':' + var_name
                        eigen_part_names[i] = eigen_part_names[i][:-8]
                        if add_partfact_to_name:
                            eigen_part_names[i] = eigen_part_names[i] + ':' + str(part_mag)
                        eigen_part_names[i] = eigen_part_names[i] + ','
        eigen_part_names[i] = eigen_part_names[i][:-1]
    mod_res.Release()

    #print(eigen_part_names)

    return eigen_real, eigen_imag, eigen_part_names

###############################################################################################
# FUNCTION: Set BC, FLEX Droop max and min contribution
###############################################################################################
def set_iactrefgen_droop(app, controller_name='*BCiactref.ElmDsl',
                      #Tf=0.02,
                      ferrdb=0.0025,
                      kg=1.0,
                      kp=57.14,
                      #EnableInt=0.0,
                      #Ti=1.0,
                      pdroopmax=1.0,
                      pdroopmin=-1.0 #,
                      #kd=0.0, Td=0.05
                      ):

    controllers = app.GetCalcRelevantObjects(controller_name)
    print('----------------')
    print('Function: ', set_iactrefgen_droop.__name__)

    if controllers != []:
        for controller in controllers:
            #controller.Tf = Tf
            controller.ferrdb = ferrdb
            controller.kg = kg
            controller.kp = kp
            #controller.EnableInt = EnableInt
            #controller.Ti = Ti
            controller.pdroopmax = pdroopmax
            controller.pdroopmin = pdroopmin
            #controller.kd = kd
            #controller.Td = Td
            print('        parameter kg: ', controller.kg)
            print('        parameter ferrdb: ', controller.ferrdb)
            print('        parameter kp: ', controller.kp)
            #print('        parameter Ti: ', controller.Ti)
            #print('        parameter EnableInt: ', controller.EnableInt)
            #print('        parameter Kd: ', controller.Kd)
            #print('        parameter Td: ', controller.Td)
            print('        parameter pdroopmax: ', controller.pdroopmax)
            print('        parameter pdroopmin: ', controller.pdroopmin)
    else:
        print(controller_name, ': search string not found')


###############################################################################################
# FUNCTION: Set gov db normal droop max and min
###############################################################################################
def set_govdb_N_droop(app, controller_name='*GT1govdb.ElmDsl',
                      db_normal = 0.0025,
                      kN=0.0, #k_powperfreq_normal
                      deltaP_normal_max=0.0,
                      deltaP_normal_min=-0.0
                      ):
    controllers = app.GetCalcRelevantObjects(controller_name)
    print('----------------')
    print('Function: ', set_govdb_N_droop.__name__)

    if controllers != []:
        for controller in controllers:
            controller.db_normal = db_normal
            controller.kN = kN
            controller.deltaP_normal_max = deltaP_normal_max
            controller.deltaP_normal_min = deltaP_normal_min
            print('        parameter db_normal: ', controller.db_normal)
            print('        parameter kN: ', controller.kN)
            print('        parameter deltaP_normal_max: ', controller.deltaP_normal_max)
            print('        parameter deltaP_normal_min: ', controller.deltaP_normal_min)
    else:
        print(controller_name, ': search string not found')

#def main():
#    print('Emtpy main function.py')

#if __name__ == '__main__':
#    main()