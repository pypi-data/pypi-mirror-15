"""RingCube class definition"""
import os

import matplotlib.pyplot as plt
import numpy as np
from pysis import CubeFile

from .io import PathManager
from .meta import all_resonances as resonances
from .meta import meta_df
from .opusapi import MetaData

try:
    # prettier plots with seaborn
    import seaborn as sns
    _SEABORN_INSTALLED = True
except ImportError:
    _SEABORN_INSTALLED = False


class RingCube(CubeFile):

    def __init__(self, fname, **kwargs):
        fname = str(fname)
        super().__init__(fname, **kwargs)
        self.pm = PathManager(fname)
        try:
            self.meta = meta_df.loc[self.pm.img_id]
        except KeyError:
            self.meta = None

    def get_opus_meta_data(self):
        print("Getting metadata from the online OPUS database.")
        self.opusmeta = MetaData(self.pm._id)
        print("Done.")
        return self.opusmeta

    @property
    def meta_pixres(self):
        if self.meta is not None:
            return int(self.meta.pixres*1000)
        else:
            return np.nan

    @property
    def meta_litstatus(self):
        if self.meta is not None:
            return self.meta.lit_status.upper()
        else:
            return np.nan

    @property
    def mapping_label(self):
        return self.label['IsisCube']['Mapping']

    @property
    def minrad(self):
        return self.mapping_label['MinimumRingRadius']/1e6

    @property
    def maxrad(self):
        return self.mapping_label['MaximumRingRadius']/1e6

    @property
    def minlon(self):
        return self.mapping_label['MinimumRingLongitude']

    @property
    def maxlon(self):
        return self.mapping_label['MaximumRingLongitude']

    @property
    def img(self):
        "apply_numpy_special is inherited from CubeFile."
        return self.apply_numpy_specials()[0]

    @property
    def extent(self):
        return [self.minlon, self.maxlon, self.minrad, self.maxrad]

    @property
    def resolution_val(self):
        return self.mapping_label['PixelResolution'].value

    @property
    def resolution_unit(self):
        return self.mapping_label['PixelResolution'].units

    @property
    def plottitle(self):
        return os.path.basename(self.filename).split('.')[0]

    @property
    def plotfname(self):
        return self.filename.split('.')[0] + '.png'

    def imshow(self, data=None, plow=1, phigh=99, save=False, ax=None,
               interpolation='sinc', extra_title=None,
               set_extent=True, **kwargs):
        if data is None:
            data = self.img
        extent_val = self.extent if set_extent else None
        min_, max_ = np.percentile(data[~np.isnan(data)], (plow, phigh))
        if ax is None:
            if not _SEABORN_INSTALLED:
                fig, ax = plt.subplots(figsize=calc_4_3(9))
            else:
                sns.set_context('talk')
                fig, ax = plt.subplots()
        ax.imshow(data, extent=extent_val, cmap='gray', vmin=min_, vmax=max_,
                  interpolation=interpolation, origin='lower',
                  aspect='auto', **kwargs)
        ax.set_xlabel('Longitude [deg]')
        ax.set_ylabel('Radius [Mm]')
        ax.ticklabel_format(useOffset=False)
        # ax.grid('on')
        title = "{}, Label_Res: {} m/pix, Metadata_Res: {} m/pix, {}".format(
                        self.plottitle,
                        int(self.resolution_val),
                        self.meta_pixres,
                        self.meta_litstatus)
        if extra_title:
            title += ', ' + extra_title
        ax.set_title(title, fontsize=14)
        self.set_resonance_axis(ax)
        fig.tight_layout()
        if save:
            savename = self.plotfname
            if extra_title:
                savename = savename[:-4] + '_' + extra_title + '.png'
            fig.savefig(savename, dpi=150)

    def set_resonance_axis(self, ax):
        filter1 = (resonances['radius'] > (self.minrad*1000))
        filter2 = (resonances['radius'] < (self.maxrad*1000))
        newticks = resonances[filter1 & filter2]
        ax2 = ax.twinx()
        ax2.set_ybound(self.minrad, self.maxrad)
        ax2.ticklabel_format(useOffset=False)
        ax2.set_yticks(newticks.radius/1000)
        ax2.set_yticklabels(newticks.name)
        return ax2

    @property
    def mean_profile(self):
        return np.nanmean(self.img, axis=1)

    @property
    def density_wave_subtracted(self):
        subtracted = self.img - self.mean_profile[:, np.newaxis]
        return subtracted

    def imshow_subtracted(self, **kwargs):
        self.imshow(data=self.density_wave_subtracted, **kwargs)

    @property
    def imgmin(self):
        return np.nanmin(self.img)

    @property
    def imgmax(self):
        return np.nanmax(self.img)

    @property
    def imgminmax(self):
        return self.imgmin, self.imgmax

    @property
    def inner_zoom(self, data=None):
        if data is None:
            data = self.img
        shape = self.img.shape
        x1 = shape[0]//4
        x2 = 3*shape[0]//4
        y1 = shape[1]//4
        y2 = 3*shape[1]//4
        return data[x1:x2, y1:y2]

    @property
    def imagetime(self):
        return self.label['IsisCube']['Instrument']['ImageTime']
