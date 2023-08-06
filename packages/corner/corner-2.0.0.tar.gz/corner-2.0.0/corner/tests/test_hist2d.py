# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.testing.decorators import image_comparison

import corner


def _run_hist2d(nm, N=50000, seed=1234, **kwargs):
    # Generate some fake data.
    np.random.seed(seed)
    x = np.random.randn(N)
    y = np.random.randn(N)

    fig, ax = pl.subplots(1, 1, figsize=(8, 8))
    corner.hist2d(x, y, ax=ax, **kwargs)


@image_comparison(baseline_images=["cutoff"], extensions=["png"])
def test_cutoff():
    _run_hist2d("cutoff", range=[(0, 4), (0, 2.5)])

@image_comparison(baseline_images=["cutoff2"], extensions=["png"])
def test_cutoff2():
    _run_hist2d("cutoff2", range=[(-4, 4), (-0.1, 0.1)], N=100000,
                fill_contours=True, smooth=1)

@image_comparison(baseline_images=["basic"], extensions=["png"])
def test_basic():
    _run_hist2d("basic")

@image_comparison(baseline_images=["color"], extensions=["png"])
def test_color():
    _run_hist2d("color", color="g")

@image_comparison(baseline_images=["levels1"], extensions=["png"])
def test_levels1():
    _run_hist2d("levels1", levels=[0.68, 0.95])

@image_comparison(baseline_images=["levels2"], extensions=["png"])
def test_levels2():
    _run_hist2d("levels2", levels=[0.5, 0.75])

@image_comparison(baseline_images=["filled"], extensions=["png"])
def test_filled():
    _run_hist2d("filled", fill_contours=True)

@image_comparison(baseline_images=["smooth1"], extensions=["png"])
def test_smooth1():
    _run_hist2d("smooth1", bins=50)

@image_comparison(baseline_images=["smooth2"], extensions=["png"])
def test_smooth2():
    _run_hist2d("smooth2", bins=50, smooth=(1.0, 1.5))

@image_comparison(baseline_images=["philsplot"], extensions=["png"])
def test_philsplot():
    _run_hist2d("philsplot", plot_datapoints=False, fill_contours=True,
                levels=[0.68, 0.95], color="g", bins=50, smooth=1.)

@image_comparison(baseline_images=["lowN"], extensions=["png"])
def test_lowN():
    _run_hist2d("lowN", N=20)

@image_comparison(baseline_images=["lowNfilled"], extensions=["png"])
def test_lowNfilled():
    _run_hist2d("lowNfilled", N=20, fill_contours=True)

@image_comparison(baseline_images=["lowNnofill"], extensions=["png"])
def test_lowNnofill():
    _run_hist2d("lowNnofill", N=20, no_fill_contours=True)
