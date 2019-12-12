import argparse
import numpy as np
from supportFunctions import weightsFromFraction, getDephasingTimes, weightedCrbTwoEchoes
import bokeh
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import ColumnDataSource, CustomJS, Title, HoverTool, Span, NormalHead, Arrow, LinearColorMapper, ColorBar
from bokeh.palettes import viridis, plasma
from bokeh.layouts import column, row
from bokeh.models.widgets import Slider

def calcAndPlotWeighted(xres, yres, args):
    fs = np.linspace(0, 1, xres)
    ts = np.linspace(0, 2.3e-3, yres)
    
    NSA_weighted = np.zeros((yres, xres, 3), dtype=np.float32)
    
    for t1Idx, t1 in enumerate(ts):
        for fIdx, f in enumerate(fs):
            NSA_weighted[t1Idx, fIdx, :] = np.reciprocal(weightedCrbTwoEchoes(3, [0, t1], weightsFromFraction(f)))
    mapper1 = LinearColorMapper(palette='Spectral10', low=0, high=1)
    
    CDSimages = [ColumnDataSource({'imageData': [NSA_weighted[:,:,0]]}),
                 ColumnDataSource({'imageData': [NSA_weighted[:,:,1]]}),
                 ColumnDataSource({'imageData': [NSA_weighted[:,:,2]]})]
    
    p1 = figure(width=400, height=350, tools='hover',toolbar_location=None, title='NSA Water, 0% FF, weighted')
    p1.image(image='imageData', x=0, y=0, dw=xres, dh=yres, color_mapper=mapper1, source= CDSimages[2])
    colorBar = ColorBar(color_mapper=mapper1, location=(0,0))
    p1.add_layout(colorBar, 'right')
    p1.x_range.range_padding = p1.y_range.range_padding = 0
    if args.svg is True:
        from bokeh.io import export_svgs
        p1.output_backend = 'svg'
        export_svgs(p1, filename=args.filename + '.svg')
    else:
        show(p1)
    
def calcAndPlotUnweighted(xres, yres, args):
    ts = np.linspace(0, 2.3e-3, yres)
    
    NSA_equalWeights = np.zeros((yres, yres, 3), dtype=np.float32)
    
    for t1Idx, t1 in enumerate(ts):
        for t2Idx, t2 in enumerate(ts):
            NSA_equalWeights[t1Idx, t2Idx, :] = np.reciprocal(weightedCrbTwoEchoes(3, [t1, t2], weightsFromFraction(0.5)))
    mapper1 = LinearColorMapper(palette='Spectral10', low=0, high=1)
    
    CDSimages = [ColumnDataSource({'imageData': [NSA_equalWeights[:,:,0]]}),
                 ColumnDataSource({'imageData': [NSA_equalWeights[:,:,1]]}),
                 ColumnDataSource({'imageData': [NSA_equalWeights[:,:,2]]})]
    
    p1 = figure(width=400, height=350, tools='hover',toolbar_location=None, title='NSA Water, 0% FF, unweighted')
    p1.image(image='imageData', x=0, y=0, dw=xres, dh=yres, color_mapper=mapper1, source= CDSimages[2])
    colorBar = ColorBar(color_mapper=mapper1, location=(0,0))
    p1.add_layout(colorBar, 'right')
    p1.x_range.range_padding = p1.y_range.range_padding = 0
    if args.svg is True:
        from bokeh.io import export_svgs
        p1.output_backend = 'svg'
        export_svgs(p1, filename='unweighted.svg')
    else:
        show(p1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        type=str,
                        default='WeightedNSAfromCRB')
    parser.add_argument('-t', '--title',
                        help="Plot title",
                        default='Weighted Cramér Rao Bounds')
    parser.add_argument('-x', '--fres',
                        help="Plot resolution along f",
                        default=1024)
    parser.add_argument('--tmin',
                        help="Minimum t [ms]",
                        default=0)
    parser.add_argument('--tmax',
                        help="Maximum t [ms]",
                        default=2.3)
    parser.add_argument('-y', '--tres',
                        help='Resolution along t',
                        default=1024)
    parser.add_argument('--embed',
                        help='Output for embedding plot',
                        default=False)
    parser.add_argument('--svg',
                        help='SVG output',
                        default=True)
    args = parser.parse_args()
    #calcAndPlotWeighted(int(args.fres), int(args.tres), args)
    calcAndPlotUnweighted(int(args.fres), int(args.tres), args)