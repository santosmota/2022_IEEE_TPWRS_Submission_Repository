%%%% SINTEF - BEGIN %%%%

% 20221216 - The cases are no longer used in this way since the first
% submission to IEEE TPWRS
%%% Cases
%caso = 1; %Case 1: FCRN provided by ESS, Flex
%caso = 2; %Case 2: FCRN provided by ESS + GT
caso = 3; %Case 3: FCR is provided by GT  

% 20221216 - FCRN DB
% attempt to improve the response when wind power oscillations are simulated
% First submission
    % FCRNDB = 0.0025;
    % SECDB is hardcoded in the block as +-btc.Pfdroop.DB*0.8
%
FCRNDB = 0.0002;
% FCRNDB = 0.0025;


OLDWAYS = 0; % For the comparison with the OLD ways different than ZERO  
             % Then I change the case 3 and FCRD

%% System
systemBase = {};

% System baseValues
%systemBase.Sn = 60e3; % VA
systemBase.Sn = 2*44e6; % VA
systemBase.cosphi = 0.8; % 
systemBase.Pn = systemBase.cosphi * systemBase.Sn; % 
%systemBase.Vn = 400;  % V rms phase to phase
systemBase.Vn = 11000;  % V rms phase to phase
systemBase.fn = 50; % Hz
%systemBase.fn = 60; % Hz

systemBase.Vn_phase = systemBase.Vn/sqrt(3); % V
systemBase.In   = systemBase.Sn/(systemBase.Vn*sqrt(3)) ; % A
systemBase.Zn   = systemBase.Vn*systemBase.Vn/systemBase.Sn ; % Ohm
systemBase.Rn   = systemBase.Zn; % Ohm
systemBase.Wn   = 2*pi()*systemBase.fn ; % rad/s
systemBase.Ln   = systemBase.Zn/systemBase.Wn ; % H
systemBase.Cn   = 1/(systemBase.Zn*systemBase.Wn) ; % F

%% Grid parameters
grid.rss = 0.02;    % Maximum steady-state frequency deviation [pu]
grid.rtr = 0.05;    % Maximum transient frequency deviation [pu]


%% SM

% Change to pu- input 
sm.fn=systemBase.fn; % [Hz] Rated electric frequency 
sm.Vn=systemBase.Vn; % [Vrms] Rated line voltage 
sm.Sn=systemBase.Sn; % [VA] Rated VA
sm.Vn_phase = sm.Vn/sqrt(3); % V
sm.In   = sm.Sn/(sm.Vn*sqrt(3)) ; % A
sm.Zn   = sm.Vn*sm.Vn/sm.Sn ; % Ohm
sm.Rn   = sm.Zn; % Ohm
sm.Wn   = 2*pi()*sm.fn ; % rad/s
sm.Ln   = sm.Zn/sm.Wn ; % H
sm.Cn   = 1/(sm.Zn*sm.Wn) ; % F

sm.r_pu=0.002; % [pu] SM stator resistance
sm.x_pu=0.362; %0.2; % [pu] SM stator reactance

sm.R=sm.r_pu*sm.Rn; % 5*0.0064; %Ohm
sm.L=sm.x_pu*sm.Ln; %3*2.0368E-4; %H

sm.phaseInitial=0; %[rad] Initial phase angle of phase 1 (electric)

sm.inertiaSeconds= 5.1;      % [s] Mechanical inertia (=wJ/T)
sm.mechanicalDamping=0.01; % [pu] Mechanical damping 
sm.initialSpeed=1 ;        % [pu] Initial turbine speed

sm.minSpeedForTorqueCalc=0.1; % [pu] Miniumum speed to use when calculating torque based on power and speed (prevent divison by zero)
sm.speedBlockingLimit=1.3 ; % [pu] Override limit on speed calculation. Speed will be forced below limit

%% Measurements
sm.V_measure_T=0.005; % [s] LP filter time constant for SM volatge measurement
sm.I_measure_T=0.005; % [s] LP filter time constant for SM current measurement
sm.P_measure=0.04; % LP filter time constant for SM power measurement
sm.Q_measure=0.04; % LP filter time constant for SM reactive power measurement

%% SM Governor
%governor.kP = 20;% [pu] Proportonal gain  u=(Kp+kI/s+ s kd)e
%governor.kI = governor.kP/10; % [pu] Integral gain  u=(Kp+kI/s + s kd)e
governor.kP = 12e6 / (0.8*sm.Sn) / grid.rss; % 1/0.047;% [pu] Proportonal gain  u=(Kp+kI/s+ s kd)e
governor.kI = 0; % [pu] Integral gain  u=(Kp+kI/s + s kd)e
governor.kd = 0 ;                   % [pu] Derivative gain
governor.derivativeLP = 0.001 ;     % [s] Low pass filter before derivative in PID
governor.LPfilterActuator.T1 = 0.4;  % [s] LP filter time constant to simulate governor actuator
governor.LPfilterActuator.T2 = 0.1;  % [s] LP filter time constant to simulate governor actuator
governor.LPfilterActuator.T = 0.5; % not used anymore
% 0.5 = T1 + T2
% Governor GAST
% R = 4.7%
% T1 = 0.4
% T2 = 0.1
% T3 = 3
% AT = 1
% Kt = 2
% Vmax = 1
% Vmin = 0

governor.speedErrMax=1 ; % [pu] Maximum speed error limit
governor.speedErrMin=-1 ; % [pu] Minimum speed error limit

governor.init = 0; %[pu] Initial output command at time zero
governor.saturationUpper=0.8; %[pu] Upper saturation limit for controller (anti-wind-up and output limit)
governor.saturationLower=0; %[pu] Lower saturation limit for controller (anti-wind-up and output limit)

governor.DB = 0.0225; %0.025;   % Droop deadband
governor.flp = 10;      % Droop low pass frequency [Hz]

governor.powerMeasSaturationUpper=1; %[pu] Upper saturation limit for for power measurement
governor.powerMeasSaturationLower=-1; %[pu] Lower saturation limit for power measurement
governor.LPfilterPowerMeasurementDroop.T=0.4; % [s] LP filter time constant for power measurement used for droop

governor.LPfilterFrequencyMeasurement.T=0.1; %0.002 % [s] LP filter time constant for frequency measurement

governor.powerDroop.K=0;%0.06; % [pu]
governor.droopOutputMax=0.2 ; % Maximum speed ref modification from droop
governor.droopOutputMin=-0.2 ;  % Minimum speed ref modification from droop

governor.powerControl.errMax=0.2; % [pu] Limiter on power error signal
governor.powerControl.errMin=-0.2; % [pu] Limiter on power error signal
governor.powerControl.kP=1/governor.kP;% 5; []  Proportional gain power controller
governor.powerControl.kI=governor.powerControl.kP/governor.LPfilterActuator.T; % 0.1; [] Integral gain power controller
governor.powerControl.saturationUpper=0.1 ; % [] Maximum speed ref modification from power controller
governor.powerControl.saturationLower=-0.1; % [] Minimum speed ref modification from power controller
governor.LPfilterPowerMeasurementPowerControl.T=0.01 ; % [s] LP filter time constant for power measurement used for power control


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FCR N and D
governor.FCR.Ts =  Ts_phy;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
governor.FCR.N.DB = FCRNDB; % 0.0025; 

governor.FCR.N.kp_case1 = 0 / (1 - governor.FCR.N.DB*systemBase.fn) * systemBase.fn / systemBase.Sn; %0MH/Hz    %governor.FCR.N.DB*systemBase.fn
governor.FCR.N.MaxDroopContrib_case1 = 0;
governor.FCR.N.MinDroopContrib_case1 = 0;

governor.FCR.N.kp_case2 = 1.5e6 / (1 - governor.FCR.N.DB*systemBase.fn) * systemBase.fn / systemBase.Sn; %1.5MW/Hz (compensated for deadband)
governor.FCR.N.MaxDroopContrib_case2 = 1.5 / 88;
governor.FCR.N.MinDroopContrib_case2 = -1.5 / 88;

if OLDWAYS == 0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    governor.FCR.N.kp_case3 = 3e6 / (1 - governor.FCR.N.DB*systemBase.fn) * systemBase.fn / systemBase.Sn; %3MW/Hz (compensated for deadband)
    governor.FCR.N.MaxDroopContrib_case3 = 3 / 88;
    governor.FCR.N.MinDroopContrib_case3 = -3 / 88;
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    governor.FCR.D.MaxOutput = 0.8 / 0.8; %divided by the minium compensation for speed
    governor.FCR.D.MinOutput = 0;
    governor.FCR.D.kp = 6e6 / 1 * systemBase.fn / systemBase.Sn; %6MH/Hz
    governor.FCR.D.DB = 0.02; 
    governor.FCR.D.MaxDroopContrib = 0.8;
    governor.FCR.D.MinDroopContrib = -0.8;

else 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % governor.FCR.N.kp_case3 = 1.333333e6 / (1 - governor.FCR.N.DB*systemBase.fn) * systemBase.fn / systemBase.Sn; %3MW/Hz (compensated for deadband)
    governor.FCR.N.kp_case3 = 1e6 / (1 - governor.FCR.N.DB*systemBase.fn) * systemBase.fn / systemBase.Sn; %3MW/Hz (compensated for deadband)
    governor.FCR.N.MaxDroopContrib_case3 = 6 / 88;
    governor.FCR.N.MinDroopContrib_case3 = -6 / 88;
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    governor.FCR.D.MaxOutput = 0.8 / 0.8; %divided by the minium compensation for speed
    governor.FCR.D.MinOutput = 0;   
    % governor.FCR.D.kp = 1.333333e6 / 1 * systemBase.fn / systemBase.Sn; %6MH/Hz
    governor.FCR.D.kp = 0e6 / 1 * systemBase.fn / systemBase.Sn; %6MH/Hz
    governor.FCR.D.DB = 0.02; 
    governor.FCR.D.MaxDroopContrib = 0.8;
    governor.FCR.D.MinDroopContrib = -0.8;
   
end

%% SM Automatic Voltage Regulator

% Add exciter time constant in the model 0.1 s
avr.fieldWinding.T1 = 0.25; %1; % [s] Time constant representing the field winding time constant
avr.fieldWinding.T2 = 1.5; %1; % [s] Time constant representing the field winding time constant

avr.LPfilterVoltageMeasurement.T= 0.05 ; % [s] Time constant for LP filter of voltage measurement

avr.ErrMax=0.5; % Maximum error to controller input
avr.ErrMin=-0.5; % Minimum error to controller input

% Check 
% Check PI tuning, probably have to increase Kp
avr.kP=2.5;  %5;     % [pu] Proportonal gain  u=(Kp+kI/s+ s kd)e
avr.kI=1;    %5;     % [pu] Integral gain  u=(Kp+kI/s + s kd)e
avr.kd= 0;    % [pu] Derivative gain
avr.derivativeLP=0.001;    % [s] Low pass filter before derivative in PID
avr.init=1 ; % [pu] Initial value for integrator 
avr.saturationUpper=0.5;     %[pu] Maximum controller output  (note: This is relative to reference since reference is feed-forwarded)
avr.saturationLower=-0.5;     %[pu] Minimum controller output  (note: This is relative to reference since reference is feed-forwarded)

avr.LPfilterPowerMeasurementDroop.T=0.02; % [s] LP filter time constant active power measurement 
avr.activePowerDroop.K=0;   % [pu/pu] Droop based on active power

avr.LPfilterReactivePowerMeasurementDroop.T=0.02;  % [s] LP filter time constant reactive power measurement
avr.reactivePowerDroop.K=0; % [pu/pu] Droop based on reactive power

avr.droopSaturationUpper=0.2; % [pu] Maximum contribution from droop
avr.droopSaturationLower=-0.2; % [pu] Minimum contribution from droop

%Reactive power consensus 
avr.Qctrl.Fs_control = 1/Ts_phy;                       % [Hz] Sampling frequency controller
avr.Qctrl.Ts_control = 1/avr.Qctrl.Fs_control;    % [s] Sampling time controller A/D converter
avr.Qctrl.Kg = 1;
avr.Qctrl.Kp = 0.05;
avr.Qctrl.Ti = 5;
avr.Qctrl.deltaUmaxPos = 0.02;
avr.Qctrl.deltaUmaxNeg = -0.02;
avr.Qctrl.Umax = 1.02;
avr.Qctrl.Umin = 0.98;




%% Load 1 (Series RL)
i=1;
load.P(i) = 37e6;
load.cosphi(i) = 0.95;
load.Rpu(i) = systemBase.Sn/load.P(i) ; % [pu] Resistance
load.Xpu(i) = systemBase.Sn/(load.P(i)*tan(acos(load.cosphi(i)))) ; % [pu] Reactance
load.R(i) = load.Rpu(i)* systemBase.Rn ; % [ohm]
load.L(i) = load.Xpu(i) * systemBase.Ln ; % [H]
load.ConstPratio(i)=0.7;

%% Load 2 (Series RL)
i=2;
load.P(i) = 6e6;
load.cosphi(i) = 0.95;
load.Rpu(i) = systemBase.Sn/load.P(i) ; % [pu] Resistance
load.Xpu(i) = systemBase.Sn/(load.P(i)*tan(acos(load.cosphi(i)))) ; % [pu] Reactance
load.R(i) = load.Rpu(i)* systemBase.Rn ; % [ohm]
load.L(i) = load.Xpu(i) * systemBase.Ln ; % [H]
load.ConstPratio(i)=0.7;

%% Load 3 (Series RL)
i=3;
load.P(i) = 3e6;
load.cosphi(i) = 0.95;
load.Rpu(i) = systemBase.Sn/load.P(i) ; % [pu] Resistance
load.Xpu(i) = systemBase.Sn/(load.P(i)*tan(acos(load.cosphi(i)))) ; % [pu] Reactance
load.R(i) = load.Rpu(i)* systemBase.Rn ; % [ohm]
load.L(i) = load.Xpu(i) * systemBase.Ln ; % [H]
load.ConstPratio(i)=0.7;

%% Interface to real HW lab

interface.Rs=0.001;%0.1; % [Ohm] Serial interface resistance (at output to lab)
%interface.Rp=100; % [Ohm] Paralell interface resistance (at  output to lab)
interface.Rp=100000; % [Ohm] Paralell interface resistance (at  output to lab)

%%%% SINTEF - END %%%%


%%%% NTNU - BEGIN %%%%

% %% SM
% sm = {};
% 
% % Rated values
% sm.fn=systemBase.fn;            % [Hz] electric frequency 
% sm.Vn=systemBase.Vn;            % [Vrms] Line voltage 
% sm.Sn=systemBase.Sn;            % [VA] Apparent power
% sm.Vn_phase = sm.Vn/sqrt(3);    % [Vrms] Phase voltage
% sm.In = sm.Sn/(sm.Vn*sqrt(3));  % [A] Line current
% sm.Zn = sm.Vn*sm.Vn/sm.Sn ;     % [Ohm] Base impedance
% sm.Rn = sm.Zn;                  % [Ohm] Base resistance
% sm.Wn = 2*pi()*sm.fn ;          % [rad/s] Base frequency
% sm.Ln = sm.Zn/sm.Wn ;           % [H] Base inductance
% sm.Cn = 1/(sm.Zn*sm.Wn) ;       % [F] Base capacitance
% sm.cosphi = 0.8;                % [-] Power factor
% sm.sat = [0.6404,0.7127,0.8441,0.9214,0.9956,1.082,1.19,1.316,1.457;0.7,0.7698,0.8872,0.9466,0.9969,1.046,1.1,1.151,1.201]; % No-load saturation curve
% 
% % Impedances and time constants
% sm.Xd = 2.12;               % d-axis steady-state impendance [pu]
% sm.Xdp = 0.299;             % d-axis transient impendance [pu]
% sm.Xdpp = 0.188;            % d-axis subtransient impendance [pu]
% sm.Xq = 0.982;              % q-axis steady-state impendance [pu]
% sm.Xqpp = 0.24;             % q-axis subtransient impendance [pu]
% sm.Xl = 0.131;              % Leakage impendance [pu]
% sm.TdpSC = 0.92;            % d-axis transient time - short-circuit [s]
% sm.TdppSC = 0.022;          % d-axis subtransient time - short-circuit [s]
% sm.TqppSC = 0.0334;         % q-axis subtransient time - short-circuit [s]
% sm.Rs = 0.0242;             % Stator (armature) resistance [pu]
% sm.M = 2.03;                % Inertia constant [s]
% sm.p = 2;                   % Pairs of poles
% 
% % Measurements
% sm.V_measure_T=0.005; % [s] LP filter time constant for SM volatge measurement
% sm.I_measure_T=0.005; % [s] LP filter time constant for SM current measurement
% sm.P_measure=0.04; % LP filter time constant for SM power measurement
% sm.Q_measure=0.04; % LP filter time constant for SM reactive power measurement
% 
% %% SM Exciter
% exc = {};
% exc.Tr = 1/(2*sm.fn);       % Input filter time constant [s]
% exc.Ka = 100;               % Proportional gain
% exc.VRmax = 5;              % Maximum output [pu]
% exc.VRmin = exc.VRmax*cos(deg2rad(150)); % Minimum output [pu]
% exc.Kf = 1e-5;              % Rate feedback (derivative) gain 
% exc.Tf = 0.01;              % Rate feedback (reset) time [s] 
% exc.Tb = 0.01;              % 1st lag time constant [s]
% exc.Tc = exc.Tb/10;     % 1st lead time constant [s]
% exc.Tb1 = 0;                % 2nd lag time constant [s]
% exc.Tc1 = 0;                % 2nd lead time constant [s]
% 
% %% Turbine
% turb = {};
% turb.T = 2.25;              % [s] Equivalent first-order delay
% 
% %% Turbine Governor
% gov = {};
% gov.Kp = 12e6/(sm.Sn*sm.cosphi*sys.rss); % [pu/pu] Permanent droop (proportional gain)
% gov.DB = 0.00025;           % [pu] Deadband
% gov.Kd = 0;                 % [pu/pu] Transient droop (derivative gain)
% gov.Tr = 0.1;               % [s] Reset time for transient droop [s]
% gov.flp = 3*2*pi();         % [rad/s] Low-pass frequency


%% Wind farm - Collector system
col = {};
col.Un = 33000;                     % [Vrms] Line voltage
col.Uanp = col.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage 
col.cosphi = 0.8;                   % [-] Power factor
col.Sn = 12e6/col.cosphi;           % [VA] Wind farm power: 13.33MVA for cosphi=0.9
col.Iap = col.Sn/col.Un*sqrt(2/3);  % [Vpeak] phase to ground voltage 
col.Trafo.xsc = 0.12;               % [pu] Transformer short circuit reactance 
col.Trafo.rsc = 0.005;              % [pu] Transformer short circuit resistance

%95 mm2
%17MVA at 33kV
% DIGISILENT POWER FACTORY - 30kV Paper	NEKBA 3x95rm 18/30kV
% VERY SIMILAR TO OTHER CABLES 20kV and 30kV cables
% but not the most capacitive of them
col.Cable.Rpos = 194.800E-3;        % [Ohm/km] Resistance positive sequence
col.Cable.Lpos = 379.998E-6;        % [H/km] Inductance positive sequence
col.Cable.Cpos = 250.000E-9;        % [F/km] Capacitance positive sequence
col.Cable.Rzero = 779.200E-3;       % [Ohm/km] Resistance zero sequence
col.Cable.Lzero = 1.520E-3;         % [H/km] Inductance zero sequence
col.Cable.Czero = 246.900E-9;       % [F/km] Capacitance positive sequence

col.Cable.Limport = 4;              % [km] Import lenght
col.Cable.LinterWT = 2;             % [km] Inter WT lenght

%% Wind farm - Specification
wf = {};

% Wind turbine parameters
wf.Tlp = 1.2;               % Inertia constant
wf.Rdiam = 126;             % Rotor diameter [m]
wf.Lmm = wf.Rdiam/5;        % Lenght scale [m]
wf.Turb = 3; % 2.5; % 6;                % Turbulence intensity [%]

% Power curve - Wind speed [m/s]
wf.pcurve.wind = [0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;25;26;50];
% Power curve - Power [pu]
wf.pcurve.power = [0;0;0;0;0.029;0.0725;0.1304;0.2101;0.3261;0.4638;0.6232;0.7754;0.8913;0.9565;0.9855;1;1;1;0;0];


%% Wind turbine 1 - Specification
wt1 = {};

% Sampling time, system frequency, switching frequency
wt1.Fn = systemBase.fn;
wt1.Fs_control = 1/Ts_phy;          % [Hz] Sampling frequency controller
wt1.Fsw = 5e3;                      % [Hz] Sampling frequency PWM
wt1.Ts_control = 1/wt1.Fs_control;  % [s] Sampling time controller A/D converter

% Grid-side converter
wt1.Pn = 4e6;                       % [W] Active power
wt1.cosphi = 0.8;                   % [-] Power factor
wt1.Sn = wt1.Pn/wt1.cosphi;         % [VA] Apparent power
wt1.Un = 690;                       % [Vrms] Line voltage (at LV side of trafo)
wt1.Uanp = wt1.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage (at LV side of trafo)
wt1.Uabp = wt1.Un*sqrt(2);          % [Vpeak] Line voltage (at LV side of trafo)
wt1.Iap = wt1.Sn/wt1.Un*sqrt(2/3);  % [Apeak] Line current (at LV side of trafo)
wt1.Udc = 1200;                     % [Vdc] Rated dc voltage
wt1.Idc = wt1.Sn/wt1.Udc;           % [Adc] Rated dc current
wt1.Cdc = wt1.Idc/(2*wt1.Fn*wt1.Udc); % [F] DC link capacitor
wt1.LCL.l2 = 0.08;                  % [pu] Short circuit reactance of trafo
wt1.LCL.r2 = 0.005;                 % [pu] Short circuit resistance of trafo
wt1.LCL.r1 = 0.01;                  % [pu] LCL main reactance resistance
wt1.dampDC = 0.8; %sqrt(2)/2;             % [-] damping Udc controller 

%% Wind turbine 1 - Grid-converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% WIND TURBINES');
[designOk, wt1.LCL] = GC_LCLdesign(wt1);
if designOk == 1 
    [wt1.CurrContSingle, wt1.DCVContSingle] = GC_PItuning(wt1,0);
    [wt1.CurrContDual, wt1.DCVContDual] = GC_PItuning(wt1,1);
end

%% Wind turbine 1 - Controllers
% Current 
wt1.CurrCont.PImax = 1.5;           % [pu] max value of PI output
wt1.CurrCont.PImin = -1.5;          % [pu] min value of PI output
wt1.CurrCont.x = wt1.LCL.l1;        % [pu] reactance for dq decoupling
wt1.CurrCont.f_LPF_noise = wt1.LCL.fres;    % [Hz] low pass cutout filter
wt1.CurrCont.zeta = sqrt(2)/2;      % [pu] damping coefficient for notch filters
wt1.filtertype = 1;                 % None = 0; Notch = 1; DSC = 2

%DC link voltage
wt1.DCVCont.PImax = 1.5;            % [pu] Max value of PI output
wt1.DCVCont.PImin = -1.5;           % [pu] Min value of PI output
wt1.DCVCont.Start = 0.2;

%AC voltage controller
wt1.ACVCont.PImax = 1.5;            % [pu] Max value of PI output
wt1.ACVCont.PImin = -1.5;           % [pu] Min value of PI output
wt1.ACVCont.kg = 1;                 % [pu/pu] Loop gain kg(kp + 1/sTi)
wt1.ACVCont.kp = 0.00;              % [pu/pu] Proportional gain kg(kp + 1/sTi)
wt1.ACVCont.Ti = 0.15;               % [s] Integral time
wt1.ACVCont.kiq_droop = 0.00;

%Q consensus controller
wt1.Qctrl.Umax = 1.05;
wt1.Qctrl.Umin = 0.95;
wt1.Qctrl.deltaUmaxPos = (wt1.Qctrl.Umax - wt1.Qctrl.Umin);
wt1.Qctrl.deltaUmaxNeg = -wt1.Qctrl.deltaUmaxPos; 
wt1.Qctrl.Ti = 5;
wt1.Qctrl.Kg = 1;
wt1.Qctrl.Kp = 0.05;



%% Wind turbine 2 - Specification
wt2 = wt1;
wt2.DCVCont.Start = 0.25;

%% Wind turbine 3 - Specification
wt3 = wt1;
wt3.DCVCont.Start = 0.3;


%% Wind turbine 1,2,3 - Kaimal Model - White Noise Seed

wt1.Kaimal.Seed = 0;
wt2.Kaimal.Seed = 111;
wt3.Kaimal.Seed = 256;


%% Flex load - Specification
flex = {};

% Sampling time, system frequency, switching frequency
flex.Fn = systemBase.fn;
flex.Fs_control = 1/Ts_phy;          % [Hz] Sampling frequency controller
flex.Fsw = 2.5e3;                      % [Hz] Sampling frequency PWM
flex.Ts_control = 1/flex.Fs_control;  % [s] Sampling time controller A/D converter

% Grid-side converter
flex.Pn = 7.6e6;                     % [W] Active power
flex.cosphi = 0.9;                   % [-] Power factor
flex.Sn = flex.Pn/flex.cosphi;       % [VA] Apparent power
flex.Un = 690;                       % [Vrms] Line voltage (at LV side of trafo)
flex.Uanp = flex.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage (at LV side of trafo)
flex.Uabp = flex.Un*sqrt(2);          % [Vpeak] Line voltage (at LV side of trafo)
flex.Iap = flex.Sn/flex.Un*sqrt(2/3);  % [Apeak] Line current (at LV side of trafo)
flex.Udc = 1200;                     % [Vdc] Rated dc voltage
flex.Idc = flex.Sn/flex.Udc;           % [Adc] Rated dc current
flex.Cdc = flex.Idc/(2*flex.Fn*flex.Udc); % [F] DC link capacitor
flex.LCL.l2 = 0.06;                  % [pu] Short circuit reactance of trafo
flex.LCL.r2 = 0.005;                 % [pu] Short circuit resistance of trafo
flex.LCL.r1 = 0.01;                  % [pu] LCL main reactance resistance
flex.dampDC = 0.8; %sqrt(2)/2;             % [-] damping Udc controller 

%% Flex load - Grid-converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% FLEX LOAD');
[designOk, flex.LCL] = GC_LCLdesign(flex);
if designOk == 1 
    [flex.CurrContDual, flex.DCVContDual] = GC_PItuning(flex,1);
    [flex.CurrContSingle, flex.DCVContSingle] = GC_PItuning(flex,0);
end

%% Flex load - Controllers
% Current 
flex.CurrCont.PImax = 1.5;           % [pu] max value of PI output
flex.CurrCont.PImin = -1.5;          % [pu] min value of PI output
flex.CurrCont.x = flex.LCL.l1;        % [pu] reactance for dq decoupling
flex.CurrCont.f_LPF_noise = flex.LCL.fres;    % [Hz] low pass cutout filter
flex.CurrCont.zeta = sqrt(2)/2;      % [pu] damping coefficient for notch filters
flex.filtertype = 0;                 % Notch = 0; DSC = 1

%DC link voltage
flex.DCVCont.PImax = 1.5;            % [pu] Max value of PI output
flex.DCVCont.PImin = -1.5;           % [pu] Min value of PI output
flex.DCVCont.Start = 0.15;

% Daniel used Ti = 10x the calculated value


%AC voltage controller
%flex.ACVCont.PImax = 1.5;            % [pu] Max value of PI output
%flex.ACVCont.PImin = -1.5;           % [pu] Min value of PI output
%flex.ACVCont.kg = 1;                 % [pu/pu] Loop gain kg(kp + 1/sTi)
%flex.ACVCont.kp = 0.00;              % [pu/pu] Proportional gain kg(kp + 1/sTi)
%flex.ACVCont.Ti = 0.15;               % [s] Integral time
%flex.ACVCont.kiq_droop = 0.00;

% Active power control
%flex.PCont.DB = grid.rss/10;        % Deadband
flex.PCont.DB = FCRNDB; % 0.0025;             % Deadband used in DigSilent Power Factory (0.125Hz)

%flex.PCont.Kp = 0.2/grid.rss;       % Permanent droop (proportional gain)
flex.PCont.Kp_case1 = 1.5e6/(1 - systemBase.fn*flex.PCont.DB)*systemBase.fn/flex.Sn; %11.27819549 this was considering Snflex=Pnflex;   % Permanent droop, 1.5MW/Hz compensated for deadband of 0.125Hz
flex.PCont.Kp_case2 = 0;

if OLDWAYS ==0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    flex.PCont.Kp_case3 = 0;
else
    % flex.PCont.Kp_case3 = 1.333333e6/(1 - systemBase.fn*flex.PCont.DB)*systemBase.fn/flex.Sn;
    flex.PCont.Kp_case3 = 1e6/(1 - systemBase.fn*flex.PCont.DB)*systemBase.fn/flex.Sn;
end

flex.Pcont.MaxDroopContrib = 1.5e6 / flex.Sn; %0.2;
flex.Pcont.MinDroopContrib = -1.5e6 / flex.Sn;    

flex.PCont.Kd = 0;                  % Transient droop (derivative gain)
flex.PCont.Tr = 0.1;                % Reset time for transient droop
flex.PCont.flp = 30;                % Low-pass frequency 



%% ESS - Grid converter specification
ess = {};

% Sampling time, system frequency, switching frequency
ess.Fn = systemBase.fn;
ess.Fs_control = 1/Ts_phy;          % [Hz] Sampling frequency controller
ess.Fsw = 5e3;                      % [Hz] Sampling frequency PWM
ess.Ts_control = 1/wt1.Fs_control;  % [s] Sampling time controller A/D converter

% Grid-side converter
ess.Pn = 8e6;                       % [W] Active power
ess.cosphi = 0.8;                   % [-] Power factor
ess.Sn = ess.Pn/ess.cosphi;         % [VA] Apparent power
ess.Un = 690;                       % [Vrms] Line voltage (at LV side of trafo)
ess.Uanp = ess.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage (at LV side of trafo)
ess.Uabp = ess.Un*sqrt(2);          % [Vpeak] Line voltage (at LV side of trafo)
ess.Iap = ess.Sn/ess.Un*sqrt(2/3);  % [Apeak] Line current (at LV side of trafo)
ess.Udc = 1200;                     % [Vdc] Rated dc voltage
ess.Idc = ess.Sn/ess.Udc;           % [Adc] Rated dc current
ess.Cdc = ess.Idc/(2*ess.Fn*ess.Udc); % [F] DC link capacitor
% Values for 150Vac and 95Iac
%ess.LCL.l2 = 0.108820196;           % [pu] Short circuit reactance of trafo
%ess.LCL.r2 = 0.05415936;            % [pu] Short circuit resistance of trafo
%ess.LCL.r1 = 0.02;                  % [pu] LCL main reactance resistance
% Values for 115Vac and 72Iac
ess.LCL.l2 = 0.107571055;           % [pu] Short circuit reactance of trafo
ess.LCL.r2 = 0.053537668;            % [pu] Short circuit resistance of trafo
ess.LCL.r1 = 0.02;                  % [pu] LCL main reactance resistance
ess.dampDC = 0.8; %sqrt(2)/2;       % [-] damping Udc controller 

%% ESS - Grid converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% ESS - Grid converter');
[designOk, ess.LCL] = GC_LCLdesign(ess);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Hardcoded Scaling of LCL and measurements for Lab purpose
% 150Vac 95Iac
%ess.LCL.L1 = 2.61135E-05;
%ess.LCL.l1 = 0.172312579;
%ess.LCL.fres = 1617.899265;
%ess.LCL.Cf = 957.357E-6;
%ess.LCL.cf = 0.014319309;
%ess.LCL.Rf = 0.034251012;
%ess.LCL.rf = 0.719407937;
%ess.HW.Udc = 260.86957;
%ess.HW.Uac = 150;
%ess.HW.Iac = 95;
%ess.HW.Idc = 94.6143316;
%ess.SIM.Iac = ess.Sn / systemBase.Vn * sqrt(1/3);
%%%%%%%%%%%%%%%%%%
%%%% 115Vac 72Aac
ess.LCL.L1 = 2.58138E-05;
ess.LCL.l1 = 0.170334897;
ess.LCL.fres = 1617.898743;
ess.LCL.Cf = 968.474E-6;
ess.LCL.cf = 0.014485588;
ess.LCL.Rf = 0.033857857;
ess.LCL.rf = 0.711150124;
ess.HW.Udc = 200;
ess.HW.Uac = 115;
ess.HW.Iac = 71.99808879;
ess.HW.Idc = 71.705;
ess.SIM.Iac = ess.Sn / systemBase.Vn * sqrt(1/3);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if designOk == 1 
    [ess.CurrContSingle, ess.DCVContSingle] = GC_PItuning(ess,0);
    [ess.CurrContDual, ess.DCVContDual] = GC_PItuning(ess,1);
end

% ESS - Grid converter controllers
ess.filtertype = 1;                 % None = 0; Notch = 1; DSC = 2

%Current 
ess.CurrCont.PImax = 1.5;           % [pu] max value of PI output
ess.CurrCont.PImin = -1.5;          % [pu] min value of PI output
ess.CurrCont.x = ess.LCL.l1;        % [pu] reactance for dq decoupling
ess.CurrCont.f_LPF_noise = ess.LCL.fres;    % [Hz] low pass cutout filter
ess.CurrCont.zeta = sqrt(2)/2;      % [pu] damping coefficient for notch filters

%DC link voltage
ess.DCVCont.PImax = 1.5;            % [pu] Max value of PI output
ess.DCVCont.PImin = -1.5;           % [pu] Min value of PI output
ess.DCVCont.Start = 0.1;

%AC voltage controller
ess.ACVCont.PImax = 1.5;            % [pu] Max value of PI output
ess.ACVCont.PImin = -1.5;           % [pu] Min value of PI output
ess.ACVCont.kg = 1;                 % [pu/pu] Loop gain kg(kp + 1/sTi)
ess.ACVCont.kp = 0.00;              % [pu/pu] Proportional gain kg(kp + 1/sTi)
ess.ACVCont.Ti = 0.15;               % [s] Integral time
ess.ACVCont.kiq_droop = 0.00;

%Q consensus controller
ess.Qctrl.Umax = 1.05;
ess.Qctrl.Umin = 0.95;
ess.Qctrl.deltaUmaxPos = (wt1.Qctrl.Umax - wt1.Qctrl.Umin);
ess.Qctrl.deltaUmaxNeg = -wt1.Qctrl.deltaUmaxPos; 
ess.Qctrl.Ti = 5;
ess.Qctrl.Kg = 1;
ess.Qctrl.Kp = 0.05;

% to be commented
ess.DCL.deltaTini = 0.1;

%% ESS - Fuel cell converter specification
fcc = {};
fcc.Pn = 4e6;                       % [W] rated power power
fcc.Udc = 600;                      % [Vdc] rated dc voltage (battery side, not DC link side)
fcc.Fsw = 5e3;                    % [Hz] converter switching frequency
fcc.eta = 0.98;                     % [pu] converter efficiency (for series R of inductor)
fcc.deltaimax = 0.05;               % [pu] maximum current ripple in pu of rated

%% ESS - Fuel cell converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% ESS - Fuel cell converter');
[fcc.filter] = BC_Ldesign(fcc);

%% ESS - Fuel cell converter controllers
% Current controller
fcc.Iref.rise = 0.02;                    % [pu/s] Iref rising slew rate 
fcc.Iref.fall = -1.0; %-0.1;            % [pu/s] Iref falling slew rate 
fcc.CurrCont.PImax = 0.9;               % [pu] max value of PI output
fcc.CurrCont.PImin = 0;                 % [pu] min value of PI output
fcc.CurrCont.Kg = 0.2; %0.5             % [-] loop gain of PI 
fcc.CurrCont.Kp = 1;                    % [-] proportional gain of PI 
fcc.CurrCont.Ti = fcc.filter.L / fcc.filter.R; % [s] integral time of PI

% Power controller
%fcc.PwrCont.Kg = 0.05;                 % [-] loop gain of PI 
%fcc.PwrCont.Kp = 1;                    % [-] proportional gain of PI 
%fcc.PwrCont.Ti = 10 * fcc.CurrCont.Ti; % [s] integral time of PI
fcc.Pfdroop.UdcComp.Fcutout = (1/1)/(2*pi); % filtering of Udc for compensation (power -> current)
fcc.Pfdroop.UdcComp.udcMax = 2.0;           % Max Udc meas for compensation
fcc.Pfdroop.UdcComp.udcMin = 0.5;           % Min Udc meas for compensation

% Fuel cell parameters
FC = {};
FC.Voltage = fcc.Udc/0.8; %divide by 0.8 to compensate for voltage drop
FC.Power = fcc.Pn;
%A_cell = 300;       % Area of cell [cm^2]
FC.A_cell = ceil(FC.Power/FC.Voltage/1.5);       % Area of cell [cm^2]
%N_cells = 455;      % Number of cells
FC.N_cells = ceil(FC.Voltage/0.8);      % Number of cells
FC.Alpha = 0.43;       % Transfer coefficient [-]
%io = 1e-5;          % Exchange current density [A/cm^2]         
FC.io = 1.6e-5;        % Exchange current density [A/cm^2]         
FC.il = 1.9;           % Limiting current density [A/cm^2]
FC.lm = 5e-3;          % Membrane thickness [cm]
FC.lambdam = 14;       % Membrane hydration parameter
FC.C = 6;              % Capacitance of charge double layer
FC.tau_e = 0.25;       % Time constant for gas flows [s]
FC.lambda_e = 0.16;    % Empirical constant dependent on mass flow delay



%% ESS - Electrolyzer converter specification
elc = {};
elc.Pn = 6e6;                       % [W] rated power power
elc.Udc = 600;                      % [Vdc] rated dc voltage (battery side, not DC link side)
elc.Fsw = 5e3;                      % [Hz] converter switching frequency
elc.eta = 0.98;                     % [pu] converter efficiency (for series R of inductor)
elc.deltaimax = 0.05;               % [pu] maximum current ripple in pu of rated

%% ESS - Electrolyzer converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% ESS - Electrolyzer converter');
[elc.filter] = BC_Ldesign(elc);

%% ESS - Electrolyzer converter controllers
% Current controller
elc.Iref.rise = 1.0; %0.1;            % [pu/s] Iref rising slew rate 
elc.Iref.fall = -0.02;                 % [pu/s] Iref falling slew rate 
elc.CurrCont.PImax = 0.9;             % [pu] max value of PI output
elc.CurrCont.PImin = 0;               % [pu] min value of PI output
elc.CurrCont.Kg = 0.2; %0.5;          % [-] loop gain of PI 
elc.CurrCont.Kp = 1;                  % [-] proportional gain of PI 
elc.CurrCont.Ti = elc.filter.L / elc.filter.R; %0.6*elc.filter.L / elc.filter.R;              % [s] integral time of PI

% Power controller
%elc.PwrCont.Kg = 0.05; %0.5;           % [-] loop gain of PI 
%elc.PwrCont.Kp = 1;                    % [-] proportional gain of PI 
%elc.PwrCont.Ti = 10 * elc.CurrCont.Ti; % [s] integral time of PI
elc.Pfdroop.UdcComp.Fcutout = (1/1)/(2*pi); % filtering of Udc for compensation (power -> current)
elc.Pfdroop.UdcComp.udcMax = 2.0;           % Max Udc meas for compensation
elc.Pfdroop.UdcComp.udcMin = 0.5;           % Min Udc meas for compensation

% Electrolizer parameters
ELY = {};
ELY.Voltage = elc.Udc;
ELY.Power = elc.Pn;
%A_cell = 680;          % Area of cell [cm^2]
ELY.A_cell = ceil(ELY.Power/ELY.Voltage/2);       % Area of cell [cm^2]
%N_cells = 100;         % Number of cells
ELY.N_cells = ceil(ELY.Voltage/1.6);      % Number of cells
ELY.Alpha = 0.43;       % Transfer coefficient [-]
%io = 1e-5;          % Exchange current density [A/cm^2]         
ELY.io = 1.6e-5;        % Exchange current density [A/cm^2]         
ELY.il = 2.5;           % Limiting current density [A/cm^2]
ELY.lm = 25e-3;          % Membrane thickness [cm]
ELY.lambdam = 14;       % Membrane hydration parameter
ELY.C = 6;              % Capacitance of charge double layer
ELY.tau_e = 0.25;       % Time constant for gas flows [s]
ELY.lambda_e = 0.16;    % Empirical constant dependent on mass flow delay



%% ESS - Battery converter specification
btc = {};
%btc.Pn = 4.2e6;                       % [W] rated power power
btc.Pn = 1.54e6;                       % [W] rated power power
btc.Udc = 600;                      % [Vdc] rated dc voltage (battery side, not DC link side)
btc.Fsw = 5e3;                    % [Hz] converter switching frequency
btc.eta = 0.98;                     % [pu] converter efficiency (for series R of inductor)
btc.deltaimax = 0.05;               % [pu] maximum current ripple in pu of rated

%% ESS - Battery converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% ESS - Fuel cell converter');
[btc.filter] = BC_Ldesign(btc);

%% ESS - Battery converter controllers
% Current controller
btc.Iref.rise = 5e3;                % [pu/s] Iref rising slew rate 
btc.Iref.fall = -5e3;               % [pu/s] Iref falling slew rate 
btc.CurrCont.PImax = 0.9;           % [pu] max value of PI output
btc.CurrCont.PImin = 0;             % [pu] min value of PI output
btc.CurrCont.Kg = 0.2;              % [-] loop gain of PI 
btc.CurrCont.Kp = 1;                % [-] proportional gain of PI 
btc.CurrCont.Ti = btc.filter.L / btc.filter.R; %0.4*btc.filter.L / btc.filter.R;              % [s] integral time of PI

% Power controller
%btc.PwrCont.Kg = 0.05;                 % [-] loop gain of PI 
%btc.PwrCont.Kp = 1;                    % [-] proportional gain of PI 
%btc.PwrCont.Ti = 10 * btc.CurrCont.Ti; % [s] integral time of PI

% P-f Droop controller
%btc.Pfdroop.Kp = 1/grid.rss;             % Permanent droop (proportional gain)
btc.Pfdroop.DB = FCRNDB; % 0.0025;                  % Deadband (0.125Hz)

btc.Pfdroop.Kp_case1 = 1.5e6 / (1 - btc.Pfdroop.DB*systemBase.fn) * systemBase.fn / btc.Pn; % 55.65862709;       % 1.5MW/(1Hz - 0.125Hz) * 50Hz / 1.54MW
btc.Pfdroop.Kp_case2 = 1.5e6 / (1 - btc.Pfdroop.DB*systemBase.fn) * systemBase.fn / btc.Pn; % 55.65862709;       % 1.5MW/(1Hz - 0.125Hz) * 50Hz / 1.54MW

if OLDWAYS == 0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    btc.Pfdroop.Kp_case3 = 0;                 % 0MW/(1Hz - 0.125Hz) * 50Hz / 1.54MW
else
    % btc.Pfdroop.Kp_case3 = 1.333333e6 / (1 - btc.Pfdroop.DB*systemBase.fn) * systemBase.fn / btc.Pn;
    btc.Pfdroop.Kp_case3 = 1e6 / (1 - btc.Pfdroop.DB*systemBase.fn) * systemBase.fn / btc.Pn;
end
    
btc.Pfdroop.Kd = 0;                       % Transient droop (derivative gain)
btc.Pfdroop.Tr = 0.1;                     % Reset time for transient droop
btc.Pfdroop.flp = 450; %10; %0.2 * ess.LCL.fres;     % Low-pass frequency 
btc.Pfdroop.UdcComp.Fcutout = (1/0.010)/(2*pi); % filtering of Udc for compensation (power -> current)
btc.Pfdroop.UdcComp.udcMax = 1.2;             % Max Udc meas for compensation
btc.Pfdroop.UdcComp.udcMin = 0.8;           % Min Udc meas for compensation

BT = {};
BT.Pn = btc.Pn;
BT.Udc = btc.Udc;
BT.In = BT.Pn / BT.Udc;
BT.eta = 0.98;
BT.R12 = (BT.Pn * (1-BT.eta))/(BT.In^2);
BT.R1 = 0.6 * BT.R12;
BT.R2 = 0.4 * BT.R12;
BT.C = 20;
BT.E_Wh = 60e3; 
BT.UdcSOCfallrate = 0.1/0.4;

%% Secondary frequency control
f2ctrl.Kp = 1; %0.05;
f2ctrl.Ki = 1/10;
f2ctrl.PImax = 0.6; %(fcc.Pn + sm.Sn*governor.saturationUpper)/systemBase.Sn;
f2ctrl.PImin = -0.6; %-elc.Pn/systemBase.Sn;
f2ctrl.ondelay = 20; %30;
f2ctrl.offdelay = 60;


% WF consensus Q measureme
Qconsensus = {};
Qconsensus.QavgvCalcCutOutFreq = 0.5; % [Hz]



%% Initial conditions
turb.P0 = 0.027;         % [pu] Turbine power output

sm.Vt0 = 1;             % [pu] SM stator voltage
sm.Efd0 = 1.00182;            % [pu] SM field voltage
sm.dw0 = 0;             % [%] SM dw 
sm.th0 = -0.1;          % [deg] SM theta
sm.phi0 = -0.1;         % [deg] SM phi

ess.Vac0 = sm.Vt0;      % [pu] ESS AC voltage
ess.P0 = 0;             % [pu] ESS active power

wt1.Vac0 = sm.Vt0;      % [pu] WT1 AC voltage
wt2.Vac0 = sm.Vt0;      % [pu] WT2 AC voltage
wt3.Vac0 = sm.Vt0;      % [pu] WT3 AC voltage

% Original initial conditions from SINTEF template
avr.init=sm.Vt0;

%%%% NTNU - END %%%%
