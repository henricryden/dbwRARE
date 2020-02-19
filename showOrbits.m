dBW.X1 = permute(readH5Dump('/Data/20191108_k2d8smr010_Volunteer_e02281_s00002_ksfsedixondbwfse/X.h5'),[3 2 4 1]);
dBW.pocs = dft(permute(readH5Dump(['/Data/20191108_k2d8smr010_Volunteer_e02281_s00002_ksfsedixondbwfse/pocs.h5']),[3 2 4 1]),-1,1);


sl = 3;

rows = 30:300;
cols = 45:270;
dBW.X1 = squeeze(abs(dBW.X1(rows,cols,sl,:)));
dBW.pocs = squeeze(abs(dBW.pocs(rows,cols,sl,:)));

ipscale = [0 4e5];
wscale = [0 2e5];

close all;
uf = 2;
f1 = figure('name','W','units','normalized','position',[0.3 0 .3 .5]);
ha1=axes;
imagesc(ha1,abs(imresize(dBW.X1(:,:,1),uf,'bicubic')),'parent',ha1);
axis equal;
colormap gray;

f2 = figure('name','F','units','normalized','position',[0.0 0.0 .3 .5]);
ha2=axes;
imagesc(f2,abs(imresize(dBW.X1(:,:,2),uf,'bicubic')),'parent',ha2);
axis equal;
colormap gray;

f3 = figure('name','POCS1','units','normalized','position',[0.3 0.5 .3 .5]);
ha3=axes;
imagesc(abs(imresize(dBW.pocs(:,:,1),uf,'bicubic')),'parent',ha3);
axis equal;
colormap gray;

f4 = figure('name','POCS2','units','normalized','position',[0.0 0.5 .3 .5]);
ha4=axes;
imagesc(abs(imresize(dBW.pocs(:,:,2),uf,'bicubic')),'parent',ha4);
axis equal;
colormap gray;

f5 = figure('name','genIP','units','normalized','position',[0.0 0.5 .3 .5]);
ha5=axes;
imagesc(abs(imresize(dBW.X1(:,:,2) + dBW.X1(:,:,1),uf,'bicubic')),'parent',ha5);
axis equal;
colormap gray;

%%
set([ha2 ha4],'clim',ipscale)
set([ha1 ha3],'clim',wscale)

saveas(f1,[get(f1,'name') '.svg']);
saveas(f2,[get(f2,'name') '.svg']);
saveas(f3,[get(f3,'name') '.svg']);
saveas(f4,[get(f4,'name') '.svg']);

close all;

function A = amplifyimage(A, r, c, amp)
    A(r,c,:) = A(r,c,:) * amp;
end


