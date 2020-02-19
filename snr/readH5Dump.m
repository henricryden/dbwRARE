function data = readH5Dump(file)
% Usage: data = readH5Dump(filename)
%
% read HDF5 files creted by KS::saveToHDF5
% output is complex either if the file contains a dataset 
% named complexdata or the first dimension is two.

info = h5info(file);
try
    if length(info.Datasets) == 1
        if (strcmp(info.Datasets.Name, 'complexdata'))
            raw = h5read(file, '/complexdata');

            sz = size(raw);
            raw = reshape(raw, prod(sz(1:end-1)), 2);
            data = complex(raw(:,1), raw(:,2));
            if length(sz(1:end-1)) == 1
                %resizeDims = [sz(1:end-1) 1];
                data = data(:);
            else
                resizeDims = sz(1:end-1);
                data = reshape(data, resizeDims);
            end
            
        else
            data = h5read(file, '/realdata');
            sz = size(data);
        end
    else if length(info.Datasets) == 2
        if strcmp(info.Datasets(1).Name, 'real') || strcmp(info.Datasets(1).Name, 'imag')
            data = h5read(file, '/real') + 1i*h5read(file, '/imag');
        end
    end
      %  if (sz(1) == 2)
      %      data = complex(data(1,:), data(2,:));
      %      data = reshape(data, sz(2:end));
      %  end
    end
catch
    raw = h5read(file, '/mrdata');
    %sz = size(raw.real);
    %raw = reshape(raw, prod(sz(1:end-1)), 2);
    data = complex(raw.real, raw.imag);
end
end