# Author: Robert McGibbon <rmcgibbo@gmail.com>
# Contributors: Matthew Harrigan <matthew.harrigan@outlook.com>
# Copyright (c) 2015, Stanford University
# All rights reserved.


from __future__ import absolute_import, print_function, division
import warnings

from sklearn import cluster, mixture

from ..base import BaseEstimator
from .base import MultiSequenceClusterMixin
from .kcenters import KCenters
from .ndgrid import NDGrid
from .agglomerative import LandmarkAgglomerative
from .regularspatial import RegularSpatial
from .kmedoids import KMedoids
from .minibatchkmedoids import MiniBatchKMedoids
from .apm import APM

# workaround for sklearn emitting too many warnings
warnings.filterwarnings("ignore", '', DeprecationWarning, r'^sklearn\.')

__all__ = ['KMeans', 'MiniBatchKMeans', 'AffinityPropagation', 'MeanShift',
           'GMM', 'SpectralClustering', 'Ward', 'KCenters', 'NDGrid',
           'LandmarkAgglomerative', 'RegularSpatial', 'KMedoids',
           'MiniBatchKMedoids', 'MultiSequenceClusterMixin', 'APM']


def _replace_labels(doc):
    """Really hacky find-and-replace method that modifies one of the sklearn
    docstrings to change the semantics of labels_ for the subclasses"""
    lines = doc.splitlines()
    labelstart, labelend = None, None
    foundattributes = False
    for i, line in enumerate(lines):
        if 'Attributes' in line:
            foundattributes = True
        if 'labels' in line and not labelstart and foundattributes:
            labelstart = len('\n'.join(lines[:i]))
        if labelstart and line.strip() == '' and not labelend:
            labelend = len('\n'.join(lines[:i + 1]))

    replace = '''\n    `labels_` : list of arrays, each of shape [sequence_length, ]
        The label of each point is an integer in [0, n_clusters).
    '''

    return doc[:labelstart] + replace + doc[labelend:]


class KMeans(MultiSequenceClusterMixin, cluster.KMeans, BaseEstimator):
    __doc__ = _replace_labels(cluster.KMeans.__doc__)


class MiniBatchKMeans(MultiSequenceClusterMixin, cluster.MiniBatchKMeans,
                      BaseEstimator):
    __doc__ = _replace_labels(cluster.MiniBatchKMeans.__doc__)


class AffinityPropagation(MultiSequenceClusterMixin,
                          cluster.AffinityPropagation, BaseEstimator):
    __doc__ = _replace_labels(cluster.AffinityPropagation.__doc__)


class MeanShift(MultiSequenceClusterMixin, cluster.MeanShift, BaseEstimator):
    __doc__ = _replace_labels(cluster.MeanShift.__doc__)


class SpectralClustering(MultiSequenceClusterMixin, cluster.SpectralClustering,
                         BaseEstimator):
    __doc__ = _replace_labels(cluster.SpectralClustering.__doc__)


class AgglomerativeClustering(MultiSequenceClusterMixin,
                              cluster.AgglomerativeClustering,
                              BaseEstimator):
    __doc__ = _replace_labels(cluster.AgglomerativeClustering.__doc__)

try:
    class Ward(MultiSequenceClusterMixin, cluster.Ward, BaseEstimator):
        __doc__ = _replace_labels(cluster.Ward.__doc__)
except AttributeError:
    class Ward(AgglomerativeClustering):
        __doc__ = AgglomerativeClustering.__doc__

        def __init__(self, *args, **kwargs):
            warnings.warn("sklearn.cluster.Ward was removed, "
                          "please use AgglomerativeClustering",
                          DeprecationWarning)
            super(Ward, self).__init__(*args, **kwargs)


class GMM(MultiSequenceClusterMixin, mixture.GMM, BaseEstimator):
    __doc__ = _replace_labels(mixture.GMM.__doc__)
