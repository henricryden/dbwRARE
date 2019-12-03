import numpy as np
from supportFunctions import weightsFromFraction
from bokeh.plotting import figure, output_file, save

fs = np.linspace(0,1,100)
weights = np.zeros((100,2))
for fidx, f in enumerate(fs):
    weights[fidx,:] = np.array(weightsFromFraction(f))
print(weights)

p1 = figure(width=350, height=200, toolbar_location=None)
p1.line(fs, weights[:,0],line_color='navy')
p1.line(fs, weights[:,1],line_color='chocolate')
p1.xaxis.axis_label = 'f'
p1.yaxis.axis_label = 'weight'
output_file('weights.html')
save(p1, filename='weights.html', title='')