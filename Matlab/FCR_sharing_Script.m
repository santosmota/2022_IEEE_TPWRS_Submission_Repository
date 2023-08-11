clearvars;
close all;

Sn = 88;            % MW
Tgov1 = 0.1;        % s
Tgov2 = 0.4;
Tess = 0.05;        % s
H = 2.5;            % s
Fn = 50;            % Hz

Kgt = [12 10  8  6  4  2 0];    % MW/Hz
Kess = [0  2  4  6  8 10 12];   % MW/Hz

KGT =  Kgt(1);
KESS = Kess(1);
open_system('FCR_sharing');

for i = 1:length(Kgt)
    KGT =  Kgt(i);
    KESS = Kess(i);
    
    io(1) = linio('FCR_sharing/StepLoad',1,'input');
    io(2) = linio('FCR_sharing/Integrator',1,'output');
    
    linsys = linearize('FCR_sharing',io);
    figure(1)
    hold on
    step(linsys)
    
    figure(2)
    hold on
    e = eig(linsys.A);
    ereal = real(e);
    eimag = imag(e);
    plot(ereal,eimag,'x')

    filename = strcat('mateigen_run_',int2str(i),'.csv');
    eexp = [ereal, eimag];
    csvwrite(filename, eexp)
    
end


figure(1)
hold off

figure(2)
hold off




