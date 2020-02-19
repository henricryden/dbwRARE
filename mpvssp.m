mp = permute(readH5Dump('/Data/20200217/20200217_k2d8smr008_Volunteer_e02224_s00008_ksfsehenricsagsnrdbwknee/multipeak/snr_pe_1/X.h5'), [3 2 4 1]);
sp = permute(readH5Dump('/Data/20200217/20200217_k2d8smr008_Volunteer_e02224_s00008_ksfsehenricsagsnrdbwknee/singlepeak/X.h5'), [3 2 4 1]);
%%


sl = 25;

uf = 1;
enh.fact = 3
enh.row = 140:190;
enh.col = 90:190;
mpenh = mp;
spenh = sp;

mpenh(enh.row,enh.col,sl,1) = mp(enh.row,enh.col,sl,1) * enh.fact;
spenh(enh.row,enh.col,sl,1) = sp(enh.row,enh.col,sl,1) * enh.fact;

h1 = figure('Name','mpW','units','normalized','Position',[0 0.5 .5 .5]);%subplot(1,4,1);
imagesc(abs(imresize(mpenh(:,:,sl,1),uf,'bicubic')),[0 3e5]); axis equal; colormap gray;
h2 = figure('Name','spW','units','normalized','Position',[0 0.5 .5 .5]);%subplot(1,4,2);
imagesc(abs(imresize(spenh(:,:,sl,1),uf,'bicubic')),[0 3e5]); axis equal; colormap gray;
h3 = figure('Name','mpF','units','normalized','Position',[0 0 .5 .5]);%subplot(1,4,3);
imagesc(abs(imresize(mp(:,:,sl,2),uf,'bicubic')),[0 4e5]); axis equal; colormap gray;
h4 = figure('Name','spF','units','normalized','Position',[0 0 .5 .5]);%subplot(1,4,4);
imagesc(abs(imresize(sp(:,:,sl,2),uf,'bicubic')),[0 4e5]); axis equal; colormap gray;
linkaxes;

saveas(h1,'mpW.svg');
saveas(h2,'spW.svg');
saveas(h3,'mpF.svg');
saveas(h4,'spF.svg');