import warnings

import msmbuilder.featurizer
from msmbuilder.example_datasets import fetch_alanine_dipeptide
from msmbuilder.example_datasets import fetch_fs_peptide

warnings.filterwarnings('ignore', message='.*Unlikely unit cell vectors.*')


def test_alanine_dipeptide():
    # will produce 0 features because not enough peptides

    dataset = fetch_alanine_dipeptide()
    trajectories = dataset["trajectories"]
    featurizer = msmbuilder.featurizer.AlphaAngleFeaturizer()
    nothing = featurizer.transform(trajectories)

    assert (nothing[0].shape[1] == 0)


def test_fs_peptide():
    # will produce 36 features

    dataset = fetch_fs_peptide()
    trajectories = dataset["trajectories"]
    featurizer = msmbuilder.featurizer.AlphaAngleFeaturizer()
    alphas = featurizer.transform(trajectories)

    assert (alphas[0].shape[1] == 36)


def test_fs_peptide_nosincos():
    # will produce 18 features

    dataset = fetch_fs_peptide()
    trajectories = dataset["trajectories"]
    featurizer = msmbuilder.featurizer.AlphaAngleFeaturizer(sincos=False)
    alphas = featurizer.transform(trajectories)

    assert (alphas[0].shape[1] == 18)
