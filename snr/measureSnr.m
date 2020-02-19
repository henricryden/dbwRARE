clear;
load('masks.mat')
load('dephasingtimes.mat');
wang.X1 = permute(readH5Dump([pwd filesep 'wang_snr_pe_1' filesep 'X.h5']),[3 2 4 1]);
wang.X2 = permute(readH5Dump([pwd filesep 'wang_snr_pe_2' filesep 'X.h5']),[3 2 4 1]);
dBW.X1 = permute(readH5Dump([pwd filesep 'dbw_snr_pe_1' filesep 'X.h5']),[3 2 4 1]);
dBW.X2 = permute(readH5Dump([pwd filesep 'dbw_snr_pe_2' filesep 'X.h5']),[3 2 4 1]);
sl = 10;

wang.X1 = squeeze(abs(wang.X1(:,:,sl,:)));
wang.X2 = squeeze(abs(wang.X2(:,:,sl,:)));
dBW.X1 = squeeze(abs(dBW.X1(:,:,sl,:)));
dBW.X2 = squeeze(abs(dBW.X2(:,:,sl,:)));

wang.wdiff = ( (wang.X1(:,:,1) - wang.X2(:,:,1)) / sqrt(2) ).^2;
wang.fdiff = ( (wang.X1(:,:,2) - wang.X2(:,:,2)) / sqrt(2) ).^2;
dBW.wdiff = ( (dBW.X1(:,:,1) - dBW.X2(:,:,1)) / sqrt(2) ).^2;
dBW.fdiff = ( (dBW.X1(:,:,2) - dBW.X2(:,:,2)) / sqrt(2) ).^2;


h = fspecial('disk',8);
wang.smooothedWdiff = sqrt(imfilter(wang.wdiff,h));
wang.smooothedFdiff = sqrt(imfilter(wang.fdiff,h));
dBW.smooothedWdiff = sqrt(imfilter(dBW.wdiff,h)); 
dBW.smooothedFdiff = sqrt(imfilter(dBW.fdiff,h));

wang.snrmap.F = wang.X1(:,:,2) ./ wang.smooothedFdiff;
wang.snrmap.W = wang.X1(:,:,1) ./ wang.smooothedWdiff;
dBW.snrmap.F = dBW.X1(:,:,2) ./ dBW.smooothedFdiff;
dBW.snrmap.W = dBW.X1(:,:,1) ./ dBW.smooothedWdiff;

watmaskColor = cat(3, watmask, zeros(size(watmask)), zeros(size(watmask)));
fatmaskColor = cat(3, fatmask, zeros(size(fatmask)), zeros(size(fatmask)));

climSNR = [0 60];
h1 = subplot(4,4,1);
render(wang.X1(:,:,1))
title(['Wang - W1']);

h2 = subplot(4,4,2);
render(wang.X2(:,:,1))
title(['Wang - W2']);

h3 = subplot(4,4,3);
render(wang.smooothedWdiff,[])
title(['Wang - smooth(W1-W2)']);
hold(h3,'on');
hMask = imshow(watmaskColor);
set(hMask,'AlphaData',.5*watmask);

h4 = subplot(4,4,4);
render(wang.snrmap.W,climSNR)
title(['Wang - SNR (W)']);
hold(h4,'on');
hMask = imshow(watmaskColor);
set(hMask,'AlphaData',.5*watmask);

h5 = subplot(4,4,5);
render(wang.X1(:,:,2),[])
title(['Wang - F1']);

h6 = subplot(4,4,6);
render(wang.X1(:,:,2))
title(['Wang - F2']);

h7 = subplot(4,4,7);
render(wang.smooothedFdiff,[])
title(['Wang - smooth(F1 - F2)']);
set(h7,'CLim',get(h3,'CLim'));
hold(h7,'on');
hMask = imshow(fatmaskColor);
set(hMask,'AlphaData',.5*fatmask);

h8 = subplot(4,4,8);
render(wang.snrmap.F,climSNR);
hold(h8,'on');
hMask = imshow(fatmaskColor);
set(hMask,'AlphaData',.5*fatmask);

% dBW plot
title(['dBW - SNR (F)']);
h9 = subplot(4,4,9);
render(dBW.X1(:,:,1))
title(['dBW - W1']);

h10 = subplot(4,4,10);
render(dBW.X2(:,:,1))
title(['dBW - W2']);

h11 = subplot(4,4,11);
render(dBW.smooothedWdiff,[])
title(['dBW - smooth(W1-W2)']);
hold(h11,'on');
hMask = imshow(watmaskColor);
set(hMask,'AlphaData',.5*watmask);

h12 = subplot(4,4,12);
render(dBW.snrmap.W,climSNR)
title(['dBW - SNR (W)']);
hold(h12,'on');
hMask = imshow(watmaskColor);
set(hMask,'AlphaData',.5*watmask);

h13 = subplot(4,4,13);
render(dBW.X1(:,:,2),[])
title(['dBW - F1']);

h14 = subplot(4,4,14);
render(dBW.X1(:,:,2))
title(['dBW - F2']);

h15 = subplot(4,4,15);
render(dBW.smooothedFdiff,[])
title(['dBW - smooth(F1 - F2)']);
set(h15,'CLim',get(h3,'CLim'));
hold(h15,'on');
hMask = imshow(fatmaskColor);
set(hMask,'AlphaData',.5*fatmask);

h16 = subplot(4,4,16);
render(dBW.snrmap.F,climSNR);
hold(h16,'on');
hMask = imshow(fatmaskColor);
set(hMask,'AlphaData',.5*fatmask);
title(['dBW - SNR (F)']);

colorbar(h4)
colorbar(h8)
colorbar(h12)
colorbar(h16)
linkaxes;
xlim([150 260])
ylim([15 125])

wang.snr.w = wang.snrmap.W(watmask);
wang.snr.f = wang.snrmap.F(fatmask);
dBW.snr.w = dBW.snrmap.W(watmask);
dBW.snr.f = dBW.snrmap.F(fatmask);
%
disp(['Wang Water SNR = ' num2str(mean(wang.snr.w))])
disp(['Wang Fat SNR = ' num2str(mean(wang.snr.f))])
disp(['Wang Water SNR = ' num2str(mean(dBW.snr.w))])
disp(['Wang Fat SNR = ' num2str(mean(dBW.snr.f))])
disp(['dBW / Wang Water SNR = ' num2str(mean(dBW.snr.w)/mean(wang.snr.w))])
disp(['dBW / Wang Fat SNR = ' num2str(mean(dBW.snr.f)/mean(wang.snr.f))])


dbw.sampleduration = sum(abs(dephasingtimes.dbw(end,:) - dephasingtimes.dbw(1,:)));
wang.sampleduration = sum(abs(dephasingtimes.wang(end,:) - dephasingtimes.wang(1,:)));

disp(['SNR gain from increased sample duration is ' num2str(sqrt(dbw.sampleduration / wang.sampleduration))])

%%
figure;
hl=subplot(1,2,1);
plot(dephasingtimes.dbw,'linewidth',1.5,'color',[.3 .2 .6]);
hr=subplot(1,2,2);
plot(dephasingtimes.wang,'linewidth',1.5,'color',[.6 .3 .2]);
set(hr,'YLim',get(hl,'YLim'))
xlabel(hl,'Sample index')
xlabel(hr,'Sample index')
ylabel(hl,'Dephasing time [s]')
grid(hl,'on')
grid(hr,'on')
line(hl,[160 160], get(hl,'YLim'),'linestyle','--','color','k')
line(hr,[160 160], get(hl,'YLim'),'linestyle','--','color','k')
set([hl hr],'fontsize',14)
