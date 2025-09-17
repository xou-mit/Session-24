import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patheffects

def our_imshow ( im, ax=None, q=0.025, origin='lower', center=False, cval=0., qlow=None, qhigh=None, cmap='Greys', **kwargs ):
    if ax is None:
        ax = plt.subplot(111)   
    if hasattr(im, 'unit'):
        im = im.value
        
    
    if qlow is None:
        qlow = q
    else:
        print('Ignoring q, using qlow')
    if qhigh is None:
        qhigh = 1. - q    
    else:
        print('Ignoring q, using qhigh')
                     
    vmin,vmax = np.nanquantile(im, [qlow,qhigh])
    if center:
        vextremum = np.max(np.abs([cval-vmin,vmax-cval]))
        vmin = cval - vextremum
        vmax = cval + vextremum

    imshow_out = ax.imshow ( im, vmin=vmin, vmax=vmax, origin=origin,cmap=cmap, **kwargs )
    
    
    return imshow_out, ax

def our_contour ( im, ax=None, **kwargs ):
    if ax is None:
        ax = plt.subplot(111)
    X,Y = np.mgrid[:im.shape[0],:im.shape[1]]
    out = ax.contour ( Y, X, im, **kwargs)
    return out, ax


def our_text (
        rx, 
        ry, 
        text, 
        ax=None, 
        ha=None, 
        va=None, 
        bordercolor=None, 
        borderwidth=1., 
        coord_type='relative', 
        **kwargs 
    ):
    if ax is None:
        ax = plt.subplot(111)
    
    if ha is None:
        ha = 'right' if rx > 0.5 else 'left'
    if va is None:
        va = 'top' if ry > .5 else 'bottom'
    
    if isinstance(coord_type, tuple) or isinstance(coord_type,list):
        if coord_type[0] == 'relative':
            if ax.get_xscale() == 'log':
                rx = 10.**(-1.*np.subtract(*np.log10(ax.get_xlim()))*rx + np.log10(ax.get_xlim()[0]))
            else:
                rx = -1.*np.subtract(*ax.get_xlim())*rx + ax.get_xlim()[0]
        if coord_type[1] == 'relative':
            if ax.get_yscale() == 'log':
                ry = 10.**(-1.*np.subtract(*np.log10(ax.get_ylim()))*ry + np.log10(ax.get_ylim()[0]))
            else:
                ry = -1.*np.subtract(*ax.get_ylim())*ry + ax.get_ylim()[0] 

   
        txt = ax.text ( rx, ry, text, ha=ha, va=va, **kwargs ) 
    elif coord_type == 'relative':
        txt = ax.text ( rx, ry, text, transform=ax.transAxes, ha=ha, va=va, **kwargs )
    elif coord_type == 'absolute':
        txt = ax.text ( rx, ry, text, ha=ha, va=va, **kwargs )
        
    if bordercolor is not None:
        txt.set_path_effects ( [patheffects.withStroke(linewidth=borderwidth, foreground=bordercolor)])
    return ax