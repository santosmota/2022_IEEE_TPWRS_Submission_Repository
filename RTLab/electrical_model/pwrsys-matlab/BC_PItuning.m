%% PItuning.m
% Autors: Daniel dos Santos Mota, Erick Fernando Alves
% Date: 2021-11-11
%
% This function tunes the PI regulators of the battery side DC current
% of the energy storage devices
%
% Naming convention:
%   BC_    : battery converter, i.e., the converter connected to energy storage device
%   PI     : proportional and integral
%   tuning : self explanatory


%%
function [Icont] = BC_PItuning(param)
%% Interface
% Input Struct
% param
%   .Fsw        : [Hz] PWM switching frequency
%   .Ts_control : [s] sampling time of control loop
%   .L          : [H] converter main reactor
%   .R          : [Ohm] parasitic resistance of the main reactor
%   .ffilt      : [Hz] signal conditioning low-pass filter cutout frequency
%   .damping    : [] damping of the regulator (suggested 1 or higher)

%% Output Struct
% Icont         : kp (1 + 1/sTi)
%   .Ti         : [s] Integrator time
%   .kp         : [pu/pu] proportional gain
%
Icont = {};

disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% BATTERY CONVERTER - PI tuning');
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');


%% Fröhr and Orttenburger 1982 ISBN 0 85501 90 0 (Heyden & Son)
% 6.6 Modulus Hugging
% 6.6.2 System with large and small first order constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sum of small time constants
Tsum = 1 / (2*pi*param.ffilt) + 1 / param.Fsw + param.Ts_control;

% Equation (6.52) - Ti equal to main time constant
Icont.Ti = param.L / param.R;

% Equation (6.55) - but damping is choosen as 1, not as 0.707
% 2 * damping * sqrt(Kp / (Ti * Tsum)) = 1 / Tsum
% Kp = Ti / ( 4 * damping^2 * Tsum )
Icont.kp = Icont.Ti / (4 * param.damping^2 * Tsum);

disp('Current controller PI transfer function = kp (1 + 1/(sTi))');
disp(['    Sum of small time constants Tsum = ',num2str(Tsum),' s']);
disp(['    Damping chosen = ',num2str(param.damping)]);
disp(['    Ti = ',num2str(Icont.Ti),' s']);
disp(['    kp = ',num2str(Icont.kp),' pu/pu']);

