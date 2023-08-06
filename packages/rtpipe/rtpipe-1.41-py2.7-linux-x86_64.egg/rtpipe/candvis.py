from scipy.special import erfinv
import numpy as n
import logging, pickle, os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from bokeh.plotting import ColumnDataSource, figure, save, output_file, vplot, hplot
from bokeh.models import HoverTool, TapTool, OpenURL
from collections import OrderedDict 
from rtpipe.parsecands import read_noise, read_candidates


def plot_interactive(mergepkl, noisepkl=None, thresh=6.0, thresh_link=7.0, ignoret=None, savehtml=True, urlbase='http://www.aoc.nrao.edu/~claw/realfast/plots'):
    """ Backwards compatible function for making interactive candidate summary plot """

    data = calcdata(mergepkl)
    circleinds = calcinds(data, thresh, ignoret)
    crossinds = calcinds(data, -1*thresh, ignoret)
    edgeinds = calcinds(data, thresh_link, ignoret)

    ontime = calcontime(data)
    logger.info('Total on target time: {} s'.format(ontime))

    if noisepkl:
        noiseplot = plotnoise(noisepkl)
    else:
        noiseplot = None

    combined = plotall(data, circleinds=circleinds, crossinds=crossinds, edgeinds=edgeinds, htmlname=None, noiseplot=noiseplot)

    if savehtml:
        output_file(mergepkl.rstrip('.pkl') + '.html')
        save(combined)
    else:
        return combined


def calcdata(mergepkl, sizerange=(2,70)):
    """ Converts candidate data from merged pkl file to dictionary for bokeh """

    # get cands from pkl
    with open(mergepkl,'r') as pkl:
        d = pickle.load(pkl)
        cands = pickle.load(pkl)

    # define columns to extract
    if 'snr2' in d['features']:
        snrcol = d['features'].index('snr2')
    elif 'snr1' in d['features']:
        snrcol = d['features'].index('snr1')
    l1col = d['features'].index('l1')
    m1col = d['features'].index('m1')
    specstdcol = d['features'].index('specstd')
    imkurcol = d['features'].index('imkurtosis')
    dtindcol = d['featureind'].index('dtind')
    dmindcol = d['featureind'].index('dmind')
    intcol = d['featureind'].index('int')
    segmentcol = d['featureind'].index('segment')
    scancol = d['featureind'].index('scan')

    # define data to plot
    snr = [cands[k][snrcol] for k in cands.iterkeys()]
    abssnr = [abs(cands[k][snrcol]) for k in cands.iterkeys()]
    dm = [d['dmarr'][k[dmindcol]] for k in cands.iterkeys()]
    l1 = [cands[k][l1col] for k in cands.iterkeys()]
    m1 = [cands[k][m1col] for k in cands.iterkeys()]
    time = [24*3600*d['segmenttimesdict'][k[scancol]][k[segmentcol],0] + d['inttime']*k[intcol] for k in cands.iterkeys()]
    time = time - min(time)
    specstd = [cands[k][specstdcol] for k in cands.iterkeys()]
    imkur = [cands[k][imkurcol] for k in cands.iterkeys()]
    key = [k for k in cands.iterkeys()]
    scan, seg, candint, dmind, dtind, beamnum = zip(*key)
    zs = normprob(d, snr)
    sizes = calcsize(snr)
    colors = colorsat(l1, m1)

    data = dict(snr=snr, dm=dm, l1=l1, m1=m1, time=time, specstd=specstd,
                imkur=imkur, scan=scan, seg=seg, candint=candint, dmind=dmind,
                dtind=dtind, sizes=sizes, colors=colors, key=key, zs=zs, abssnr=abssnr)
    return data


def calcignoret(data, ignoret=None, threshold=20):
    """ Find bad time ranges from distribution of candidates.

    ignoret is list of tuples [(t0, t1), (t2, t3)] defining ranges to ignore.
    threshold is made above std of candidate distribution in time.
    """

    time = data['time']
    time.sort()

    ww = n.ones(len(time), dtype=bool)  # initialize pass filter
    if ignoret:
        for (t0, t1) in ignoret:
            ww = ww & n.where( (time < t0) | (time > t1), True, False )

    bins = n.round(time[ww]).astype('int')
    counts = n.bincount(bins)
    high = n.where(counts > n.median(counts) + threshold*counts.std())[0]

    for hh in high:
        logger.info('High times:')
        logger.info('Bin (sec); Count (per sec)')
        logger.info('{}\t{}'.format(high, counts[high]))
    return ignoret   # convenience


def calcinds(data, threshold, ignoret=None):
    """ Find indexes for data above (or below) given threshold. """

    # select by time, too

    inds = []
    for i in range(len(data['time'])):
        snr = data['snr'][i]
        time = data['time'][i]
        if (threshold >= 0 and snr > threshold) or (threshold < 0 and snr < threshold):
            if ignoret:
                incl = [t0 for (t0, t1) in ignoret if n.round(time).astype(int) in range(t0,t1)]
                logger.debug('{} {} {} {}'.format(n.round(time).astype(int), t0, t1, incl))
                if not incl:
                    inds.append(i)
            else:
                inds.append(i)

    return inds


def calcontime(data):
    """ Given indices of good times, calculate total on time in data. """

    time = data['time']
    time_min = min(time)
    time_max = max(time)

    # extend this to use ignoret or circleinds

    return time_max - time_min


def plotall(data, circleinds=None, crossinds=None, edgeinds=None, htmlname=None, noiseplot=None, urlbase='http://www.aoc.nrao.edu/~claw/realfast/plots'):
    """ Create interactive plot from data dictionary

    data has keys of snr, time, dm, sizes, key and more.
    Optional index arguments are used to filter full data set.
    This can be used to remove bad segments or apply different symbols to subsets.
    """

    # set up data dictionary
    if not circleinds: circleinds = range(len(data))
    source = ColumnDataSource(data = dict({(key, tuple([value[i] for i in circleinds])) 
                                           for (key, value) in data.iteritems()}))

    # set ranges
    dm = data['dm']
    dm_min = min(min(dm), max(dm)/1.2)
    dm_max = max(max(dm), min(dm)*1.2)
    time = data['time']
    time_min = min(time)
    time_max = max(time)
    specstd = data['specstd']
    specstd_min = min(specstd)
    specstd_max = max(specstd)
    imkur = data['imkur']
    imkur_min = min(imkur)
    imkur_max = max(imkur)
    l1 = data['l1']
    l1_min = min(l1)
    l1_max = max(l1)
    m1 = data['m1']
    m1_min = min(m1)
    m1_max = max(m1)

    TOOLS = "hover,tap,pan,box_select,wheel_zoom,reset"

    # DM-time plot
    dmt = figure(plot_width=1000, plot_height=500, toolbar_location="left", x_axis_label='Time (s; relative)',
                 y_axis_label='DM (pc/cm3)', x_range=(time_min, time_max), y_range=(dm_min, dm_max), 
                 webgl=True, tools=TOOLS)
    dmt.circle('time', 'dm', size='sizes', source=source, line_color=None, fill_color='colors', 
               fill_alpha=0.2)

    # image location plot
    loc = figure(plot_width=475, plot_height=425, toolbar_location="left", x_axis_label='l1 (rad)', y_axis_label='m1 (rad)',
                 x_range=(l1_min, l1_max), y_range=(m1_min,m1_max), tools=TOOLS, webgl=True)
    loc.circle('l1', 'm1', size='sizes', source=source, line_color=None, fill_color='colors',
               fill_alpha=0.2)

    # cand spectrum/image statistics plot
    stat = figure(plot_width=475, plot_height=425, toolbar_location="left", x_axis_label='Spectral std',
                  y_axis_label='Image kurtosis', x_range=(specstd_min, specstd_max), 
                  y_range=(imkur_min, imkur_max), tools=TOOLS, webgl=True)
    stat.circle('specstd', 'imkur', size='sizes', source=source, line_color=None, fill_color='colors',
                fill_alpha=0.2)

    # norm prob plot
    norm = figure(plot_width=475, plot_height=425, toolbar_location="left", x_axis_label='SNR observed',
                  y_axis_label='SNR expected', tools=TOOLS, webgl=True)
    norm.circle('snr', 'zs', size='sizes', source=source, line_color=None, fill_color='colors', fill_alpha=0.2)

    # set up negative symbols, if indexes in place
    if crossinds:
        sourceneg = ColumnDataSource(data = dict({(key, tuple([value[i] for i in crossinds]))
                                                  for (key, value) in data.iteritems()}))
        dmt.cross('time', 'dm', size='sizes', source=sourceneg, line_color='colors', line_alpha=0.2)
        loc.cross('l1', 'm1', size='sizes', source=sourceneg, line_color='colors', line_alpha=0.2)
        stat.cross('specstd', 'imkur', size='sizes', source=sourceneg, line_color='colors', line_alpha=0.2)
        norm.cross('abssnr', 'zs', size='sizes', source=sourceneg, line_color='colors', line_alpha=0.2)

    if edgeinds:
        sourceedge = ColumnDataSource(data = dict({(key, tuple([value[i] for i in edgeinds]))
                                                   for (key, value) in data.iteritems()}))
        dmt.circle('time', 'dm', size='sizes', source=sourceedge, line_color='colors', fill_color=None, line_alpha=0.5)
        loc.circle('l1', 'm1', size='sizes', source=sourceedge, line_color='colors', fill_color=None, line_alpha=0.5)
        stat.circle('specstd', 'imkur', size='sizes', source=sourceedge, line_color='colors', fill_color=None, line_alpha=0.5)
        norm.circle('snr', 'zs', size='sizes', source=sourceedge, line_color='colors', fill_color=None, line_alpha=0.5)

    # define hover and url behavior
    hover = dmt.select(dict(type=HoverTool)); hover.tooltips = OrderedDict([('SNR', '@snr'), ('time', '@time'), ('key', '@key')])
    hover = loc.select(dict(type=HoverTool)); hover.tooltips = OrderedDict([('SNR', '@snr'), ('time', '@time'), ('key', '@key')])
    hover = stat.select(dict(type=HoverTool));  hover.tooltips = OrderedDict([('SNR', '@snr'), ('time', '@time'), ('key', '@key')])
    hover = norm.select(dict(type=HoverTool));  hover.tooltips = OrderedDict([('SNR', '@snr'), ('time', '@time'), ('key', '@key')])
    if htmlname:
        url = '%s/%s_sc@scan-seg@seg-i@candint-dm@dmind-dt@dtind.png' % (urlbase, os.path.basename(htmlname.rstrip('.html')) )
        taptool = dmt.select(type=TapTool);  taptool.callback = OpenURL(url=url)
        taptool = loc.select(type=TapTool);  taptool.callback = OpenURL(url=url)    
        taptool = stat.select(type=TapTool);  taptool.callback = OpenURL(url=url)    
        taptool = norm.select(type=TapTool);  taptool.callback = OpenURL(url=url)

    # arrange plots
    top = hplot(vplot(dmt), width=1000)
    middle = hplot(vplot(loc), vplot(stat), width=1000)
    if noiseplot:
        bottom = hplot(vplot(norm), vplot(noiseplot), width=1000)
    else:
        bottom = hplot(vplot(norm), width=1000)
    combined = vplot(top, middle, bottom, width=1000)

    if htmlname:
        output_file(htmlname)
        save(combined)
    else:
        return combined


def plotnoise(noisepkl):
    """ Merged noise pkl converted to interactive cumulative histogram """

    # noise histogram
    noises = read_noise(noisepkl)
    imnoise = n.sort(noises[4])
    frac = [float(count)/len(imnoise) for count in reversed(range(1, len(imnoise)+1))]
    noiseplot = figure(plot_width=475, plot_height=425, toolbar_location="left", x_axis_label='Noise image std',
                       y_axis_label='Cumulative fraction', tools='pan, wheel_zoom, reset')
    noiseplot.line(imnoise, frac)

    return noiseplot


def normprob(d, snrs):
    """ Function takes state dict and snr list 
    Returns list of expected snr given each input value's frequency of occurrence via the normal probability assumption
    input should be all of one sign (all pos or neg)
    """

#    signs = [n.sign(snr) for snr in snrs]
#    assert all(signs) or not all(signs), 'Signs of all snr values should be the same'

    # define norm quantile functions
    Z = lambda quan: n.sqrt(2)*erfinv( 2*quan - 1) 
    quan = lambda ntrials, i: (ntrials + 1/2. - i)/ntrials

    # calc number of trials
    npix = d['npixx']*d['npixy']
    if d.has_key('goodintcount'):
        nints = d['goodintcount']
    else:
        nints = d['nints']
    ndms = len(d['dmarr'])
    dtfactor = n.sum([1./i for i in d['dtarr']])    # assumes dedisperse-all algorithm
    ntrials = npix*nints*ndms*dtfactor
    logger.info('Calculating normal probability distribution for npix*nints*ndms*dtfactor = %d' % (ntrials))

    # calc normal quantile
#    try:
#        if n.sign(snrs[0]) > 0:
    snrsortpos = sorted([s for s in snrs if s > 0], reverse=True)
    snrsortneg = sorted([abs(s) for s in snrs if s < 0], reverse=True)
    zval = []
    for snr in snrs:
        if snr >= 0:
            zval.append(Z(quan(ntrials, snrsortpos.index(snr)+1)))
        else:
            zval.append(Z(quan(ntrials, snrsortneg.index(abs(snr))+1)))

    return zval

def candfilter(d, cands, thresh=0):
    """ filters candidate data. if thresh is negative, returns values less than thresh.
    default thresh=0 returns all
    """

    if thresh > 0:
        snr = [cands[k][0] for k in cands.iterkeys() if cands[k][0] > thresh]
        dm = [d['dmarr'][k[3]] for k in cands.iterkeys() if cands[k][0] > thresh]
        l1 = [cands[k][2] for k in cands.iterkeys() if cands[k][0] > thresh]
        m1 = [cands[k][3] for k in cands.iterkeys() if cands[k][0] > thresh]
        time = [d['segmenttimesdict'][k[0]][k[1],0] + (d['inttime']/(24*3600.))*k[2] for k in cands.iterkeys() if cands[k][0] > thresh]
        specstd = [cands[k][4] for k in cands.iterkeys() if cands[k][0] > thresh]
        imkur = [cands[k][8] for k in cands.iterkeys() if cands[k][0] > thresh]
        key = [k for k in cands.iterkeys() if cands[k][0] > thresh]
        zs = normprob(d, snr)
    elif thresh < 0:
        snr = [cands[k][0] for k in cands.iterkeys() if cands[k][0] < thresh]
        dm = [d['dmarr'][k[3]] for k in cands.iterkeys() if cands[k][0] < thresh]
        l1 = [cands[k][2] for k in cands.iterkeys() if cands[k][0] < thresh]
        m1 = [cands[k][3] for k in cands.iterkeys() if cands[k][0] < thresh]
        time = [d['segmenttimesdict'][k[0]][k[1],0] + (d['inttime']/(24*3600.))*k[2] for k in cands.iterkeys() if cands[k][0] < thresh]
        specstd = [cands[k][4] for k in cands.iterkeys() if cands[k][0] < thresh]
        imkur = [cands[k][8] for k in cands.iterkeys() if cands[k][0] < thresh]
        key = [k for k in cands.iterkeys() if cands[k][0] < thresh]
        zs = normprob(d, snr)
    else:
        snr = [cands[k][0] for k in cands.iterkeys()]
        dm = [d['dmarr'][k[3]] for k in cands.iterkeys()]
        l1 = [cands[k][2] for k in cands.iterkeys()]
        m1 = [cands[k][3] for k in cands.iterkeys()]
        time = [d['segmenttimesdict'][k[0]][k[1],0] + (d['inttime']/(24*3600.))*k[2] for k in cands.iterkeys()]
        specstd = [cands[k][4] for k in cands.iterkeys()]
        imkur = [cands[k][8] for k in cands.iterkeys()]
        key = [k for k in cands.iterkeys()]
        zs = []

    sizes = calcsize(snr)
    colors = colorsat(l1, m1)
    return snr, dm, l1, m1, time, specstd, imkur, key, sizes, colors, zs

def calcsize(snr, sizerange=(3,60)):
    """ Takes snr list and returns value to scale symbol size.
    """

    if snr:
        smax = max([abs(s) for s in snr])
        smin = min([abs(s) for s in snr])
        return [sizerange[0] + sizerange[1] * ((abs(s) - smin)/(smax - smin))**3 for s in snr]
    else:
        return []
    
def colorsat(l,m):
    """ Returns color for given l,m
    Designed to look like a color wheel that is more saturated in middle.
    """

    if l:
        lm = n.zeros(len(l), dtype='complex')
        lm.real = l; lm.imag = m
        red = 0.5*(1+n.cos(n.angle(lm)))
        green = 0.5*(1+n.cos(n.angle(lm) + 2*3.14/3))
        blue = 0.5*(1+n.cos(n.angle(lm) - 2*3.14/3))
        amp = 256*n.abs(lm)/n.abs(lm).max()
        return ["#%02x%02x%02x" % (n.floor(amp[i]*red[i]), n.floor(amp[i]*green[i]), n.floor(amp[i]*blue[i])) for i in range(len(l))]
    else:
        return []
