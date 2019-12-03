import numpy as np
from supportFunctions import fwModelMatrix, weightsFromFraction
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import ColumnDataSource, LinearColorMapper, CustomJS
from bokeh.models.widgets import Slider
# n - Number of samples
# t - Dephasing times [2,1]
# X - [Water, Fat]
# w - Weights [2,1]
# B0 - Field Strength [T]
def fwNoiseSim(n, t, X, w, B0):
    # Setup fat fraction et cetera
    noiseLevel = .01
    phideg = 10
    offr = 40 # Hz
    dTE = np.diff(t)[0]
   # t = [0, dTE]
    B = np.matrix(np.diag([1, np.exp(2j*np.pi*offr*dTE)]), copy=False)
    
    # Rearrange some input
    X = np.matrix(X).transpose()
    
    phi = np.exp(1j*phideg*np.pi/180.)
    # Fat dephasing and sampling operator
    A = np.diag(w) * fwModelMatrix(t,B0)
    try:
        np.linalg.inv(A)
    except:
        return [0, 0]
    forward = B*A*X*phi
    data = forward.repeat(n, axis=1) + np.random.normal(0,noiseLevel,size=(2, n)) + 1j*np.random.normal(0,noiseLevel,size=(2, n))
    
    # B0 estimation
    searchWidth = 20 # Hz
    nB0 = searchWidth*2+1
    bcand = np.linspace(offr - searchWidth, offr + searchWidth,nB0)
    Bcands = np.exp(2j*np.pi*bcand*dTE)
    allRes = np.zeros((nB0,n), dtype=np.float32)
    data_demod = np.zeros_like(data)
    phiEst = np.zeros((nB0, n), dtype=np.complex64)
    try:
        InvReAhA = np.linalg.inv(np.real( A.getH() * A ))
    except:
        return [0,0]
    for bIdx, b in enumerate(bcand):
        curModel = np.diag([1, Bcands[bIdx]]) * A
        D = np.conj(curModel) * InvReAhA * curModel.getH()
        curPhi = np.exp( -1j * .5 * np.angle(np.sum( np.multiply(data, D*data), axis=0))) # Note conjugate
        phiEst[bIdx,:] = curPhi
        curPhiM = np.repeat(curPhi, 2, axis=0)
        allRes[bIdx, :] = np.linalg.norm(
                np.multiply(data, curPhiM) - 
                curModel * np.real(np.linalg.inv(curModel) * np.multiply(data, curPhiM)), axis=0
             )
    
    bestBidx = np.argmin(allRes, axis=0)
    for sIdx, s in enumerate(data.T):
        data_demod[:, sIdx] = np.conj(np.diag([1, Bcands[bestBidx[sIdx]]])) * s.T * phiEst[bestBidx[sIdx],sIdx]
    realInverseModel = np.concatenate((A, np.conj(A)))
    estimates = np.real( np.linalg.pinv(realInverseModel) * np.concatenate((data_demod, np.conj(data_demod))) ) # realData
    estVar = np.var(estimates, axis=1, dtype=np.float64)
    return [noiseLevel**2 / estVar[0],
            noiseLevel**2 / estVar[1]]
    
nt = 192
nFrac = 192
nSamples = 1000
B0 = 3
FFs = np.linspace(start=0,stop=1, num=6, endpoint=True)

NSA_equalWeights = np.zeros((nt, nt, len(FFs), 2), dtype=np.float32)
NSA_weighted = np.zeros((nt, nFrac, len(FFs), 2), dtype=np.float32)
W = 1
F = 0


for FFidx, fatFraction in enumerate(FFs):
    for tIdx, t1 in enumerate(np.linspace(0, 2.3e-3, nt)):
        for t2Idx, t2 in enumerate(np.linspace(0, 2.3e-3, nt)):
            NSA_equalWeights[tIdx, t2Idx, FFidx, :] = fwNoiseSim(nSamples, [t1, t2], [1-fatFraction, fatFraction], weightsFromFraction(.5), B0)
        for fIdx, f in enumerate(np.linspace(0, 1, nFrac)):
            NSA_weighted[tIdx, fIdx, FFidx, :] = fwNoiseSim(nSamples, [0., t1], [1-fatFraction, fatFraction], weightsFromFraction(f), B0)
        print(tIdx)
    print(FFidx)
CDSimages = {'weighted': [ColumnDataSource({'imageData': [NSA_weighted[:,:,0,0]]}),
                          ColumnDataSource({'imageData': [NSA_weighted[:,:,0,1]]})],
             'unweighted': [ColumnDataSource({'imageData': [NSA_equalWeights[:,:,0,0]]}),
                            ColumnDataSource({'imageData': [NSA_equalWeights[:,:,0,1]]})]}
sliderCallbackW = CustomJS(
        args={
            'CDS': CDSimages['weighted'],
            'NSA': NSA_weighted},
        code="""
        FFidx = Math.round((cb_obj.value - cb_obj.start ) / cb_obj.step)
        CDS[0].data.imageData = [NSA.map(PF => PF.map(f => f[FFidx][0])).flat()]
        CDS[1].data.imageData = [NSA.map(PF => PF.map(f => f[FFidx][1])).flat()]
        CDS[0].change.emit();
        CDS[1].change.emit();
        """
        )
sliderW = Slider(start=0, end=1, value=0, step=.2, title="Fat fraction")
sliderW.js_on_change('value', sliderCallbackW)

sliderCallbackUW = CustomJS(
        args={
            'CDS': CDSimages['unweighted'],
            'NSA': NSA_equalWeights},
        code="""
        FFidx = Math.round((cb_obj.value - cb_obj.start ) / cb_obj.step)
        CDS[0].data.imageData = [NSA.map(PF => PF.map(f => f[FFidx][0])).flat()]
        CDS[1].data.imageData = [NSA.map(PF => PF.map(f => f[FFidx][1])).flat()]
        CDS[0].change.emit();
        CDS[1].change.emit();
        """
        )
sliderUW = Slider(start=0, end=1, value=0, step=.2, title="Fat fraction")
sliderUW.js_on_change('value', sliderCallbackUW)

mapper1 = LinearColorMapper(palette='Spectral10', low=0, high=1)
mapper2 = LinearColorMapper(palette='Spectral10', low=0, high=1)
p1 = figure(width=350, height=350, tools='hover',toolbar_location=None, title='NSA Water, unweighted')
p1.image(image='imageData', x=0, y=0, dw=nt, dh=nt, color_mapper=mapper1, source= CDSimages['unweighted'][0])
p2 = figure(width=350, height=350, tools='hover',toolbar_location=None, title='NSA Fat, unweighted')
p2.image(image='imageData', x=0, y=0, dw=nt, dh=nt, color_mapper=mapper1, source= CDSimages['unweighted'][1])
p3 = figure(width=350, height=350, tools='hover',toolbar_location=None, title='NSA Water, unweighted')
p3.image(image='imageData', x=0, y=0, dw=nFrac, dh=nt, color_mapper=mapper2, source= CDSimages['weighted'][0])
p4 = figure(width=350, height=350, tools='hover',toolbar_location=None, title='NSA Fat, weighted')
p4.image(image='imageData', x=0, y=0, dw=nFrac, dh=nt, color_mapper=mapper2, source= CDSimages['weighted'][1])

for p in [p1, p2, p3, p4]:
    p.x_range.range_padding = p.y_range.range_padding = 0
for p in [p3, p4]:
    p.xaxis.ticker = [0, (nFrac-1)/4, (nFrac-1)/2, 3*(nFrac-1)/4, nFrac-1]
    p.xaxis.major_label_overrides = {0:'0',
                                    (nFrac-1)/4: '.25',
                                    (nFrac-1)/2: '.5',
                                    3*(nFrac-1)/4: '.75',
                                    nFrac-1: '1'}
    p.yaxis.ticker = [0, (nt-1)/2, nt-1]
    p.yaxis.major_label_overrides = {0:'0',
                                    (nt-1)/2: 'pi',
                                    nt-1: '2pi'}

p1.yaxis.ticker = p2.yaxis.ticker = [0, (nt-1)/2, nt-1]
p1.yaxis.major_label_overrides = p2.yaxis.major_label_overrides = {0:'0', (nt-1)/2: 'pi', nt-1: '2pi'}
p1.xaxis.ticker = p2.xaxis.ticker = [0, (nt-1)/2, nt-1]
p1.xaxis.major_label_overrides = p2.xaxis.major_label_overrides = {0:'0', (nt-1)/2: 'pi', nt-1: '2pi'}
p3.xaxis.axis_label = p4.xaxis.axis_label = 'f'
p3.yaxis.axis_label = p4.yaxis.axis_label = 't2'
unw = column(row(p1, p2), sliderUW)
save(unw, filename='unweighted.html', title='')
output_file('unweighted.html')
weighted = column(row(p3, p4), sliderW)
output_file('weighted.html')
save(weighted, filename='weighted.html', title='')
