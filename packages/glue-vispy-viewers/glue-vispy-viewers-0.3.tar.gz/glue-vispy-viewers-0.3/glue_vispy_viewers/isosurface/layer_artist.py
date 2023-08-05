from __future__ import absolute_import, division, print_function

import numpy as np

from vispy import scene
from vispy.color import Color

from glue.external.echo import CallbackProperty, add_callback
from glue.core.data import Subset
from glue.core.layer_artist import LayerArtistBase
from glue.utils import nonpartial
from glue.core.exceptions import IncompatibleAttribute

from .isosurface_visual import Isosurface

class IsosurfaceLayerArtist(LayerArtistBase):
    """
    A layer artist to render isosurfaces.
    """

    attribute = CallbackProperty()
    level = CallbackProperty()
    color = CallbackProperty()
    alpha = CallbackProperty()

    def __init__(self, layer, vispy_viewer):

        super(IsosurfaceLayerArtist, self).__init__(layer)

        self.layer = layer
        self.vispy_viewer = vispy_viewer

        self._iso_visual = Isosurface(np.ones((3, 3, 3)), level=0.5, shading='smooth')
        self.vispy_viewer.add_data_visual(self._iso_visual)

        # Set up connections so that when any of the properties are
        # modified, we update the appropriate part of the visualization
        add_callback(self, 'attribute', nonpartial(self._update_data))
        add_callback(self, 'level', nonpartial(self._update_level))
        add_callback(self, 'color', nonpartial(self._update_color))
        add_callback(self, 'alpha', nonpartial(self._update_color))

    @property
    def bbox(self):
        return (-0.5, self.layer.shape[2] - 0.5,
                -0.5, self.layer.shape[1] - 0.5,
                -0.5, self.layer.shape[0] - 0.5)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self._update_visibility()

    def redraw(self):
        """
        Redraw the Vispy canvas
        """
        self.vispy_viewer.canvas.update()

    def clear(self):
        """
        Remove the layer artist from the visualization
        """
        self._iso_visual.parent = None

    def update(self):
        """
        Update the visualization to reflect the underlying data
        """
        self.redraw()
        self._changed = False

    def _update_level(self):
        self._iso_visual.level = self.level
        self.redraw()

    def _update_color(self):
        self._update_vispy_color()
        self._iso_visual.color = self._vispy_color
        self.redraw()

    def _update_vispy_color(self):
        self._vispy_color = Color(self.color)
        self._vispy_color.alpha = self.alpha

    def _update_data(self):
        if isinstance(self.layer, Subset):
            try:
                mask = self.layer.to_mask()
            except IncompatibleAttribute:
                mask = np.zeros(self.layer.data.shape, dtype=bool)
            data = mask.astype(float)
        else:
            data = self.layer[self.attribute]
        self._iso_visual.set_data(np.nan_to_num(data).transpose())
        self.redraw()

    def _update_visibility(self):
        # if self.visible:
        #     self._iso_visual.parent =
        # else:
        #     self._multivol.disable(self.id)
        self.redraw()
