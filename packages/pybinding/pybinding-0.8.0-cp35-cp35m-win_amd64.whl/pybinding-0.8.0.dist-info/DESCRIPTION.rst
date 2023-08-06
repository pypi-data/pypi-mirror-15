Documentation: http://pybinding.site/

v0.8.0 | 2016-07-01

##### New features

* Added support for scattering models. Semi-infinite leads can be attached to a finite-sized
  scattering region. Take a look at the documentation, specifically section 10 of the "Basic
  Tutorial", for details on how to construct such models.

* Added compatibility with [Kwant](http://kwant-project.org/) for transport calculations. A model
  can be constructed in Pybinding and then exported using the `Model.tokwant()` method. This makes
  it possible to use Kwant's excellent solver for transport problems. While Kwant does have its
  own model builder, Pybinding is much faster in this regard: by two orders of magnitude, see the
  "Benchmarks" page in the documentation for a performance comparison.

* *Experimental:* Initial CUDA implementation of KPM Green's function (only for diagonal elements
  for now). See the "Experimental Features" section of the documentation.

##### Improvements

* The performance of the KPM Green's function implementation has been improved significantly:
  by a factor of 2.5x. The speedup was achieved with CPU code using portable SIMD intrinsics
  thanks to [libsimdpp](https://github.com/p12tic/libsimdpp).

* The Green's function can now be computed for multiple indices simultaneously.

* The spatial origin of a lattice can be adjusted using the `Lattice.offset` attribute. See the
  "Advanced Topics" section.

##### Breaking changes

* The interface for structure plotting (as used in `System.plot()` and `StructureMap`) has been
  greatly improved. Some of the changes are not backwards compatible and may require some minor
  code changes after upgrading. See the "Plotting Guide" section of the documentation for details.

* The interfaces for the `Bands` and `StructureMap` result objects have been revised. Specifically,
  structure maps are now more consistent with ndarrays, so the old `smap.filter(smap.x > 0)` is
  replaced by `smap2 = smap[smap.x > 0]`. The "Plotting Guide" has a few examples and there is a
  full method listing in the "API Reference" section.

##### Documentation

* The API reference has been completely revised and now includes a summary on the main page.

* A few advanced topics are now covered, including some aspects of plotting. A few more random
  examples have also been added.

* Experimental features are now documented.

##### Bug fixes

* Fixed translational symmetry skipping directions for some 2D systems.
* Fixed computation of off-diagonal Green's function elements with `opt_level > 0`
* Fixed some issues with shapes which were not centered at `(x, y) = (0, 0)`.



