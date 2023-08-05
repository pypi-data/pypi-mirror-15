pyFDA
*****

Python Filter Design Analysis Tool
==================================

pyFDA is a GUI based tool in Python / Qt for analysing and designing discrete time filters. The capability for generating Verilog and VHDL code for the designed and quantized filters will be added in the next release.

Prerequisites
-------------

Besides standard python libraries, the project builds on the following libraries:

* numpy
* scipy
* matplotlib
* docutils
* pyQt4
* Optional: xlwt and / or XlsxWriter for exporting filter coefficients as \*.xls(x) files

Installing and starting pyFDA
-----------------------------

Download the zip file and extract it to a directory of your choice. Install it either to your ``<python>/Lib/site-packages`` subdirectory using

    ``>> python setup.py install``

or run it where you have installed the python source files using (for testing / development)

    ``>> python setup.py develop``

In both cases, start scripts ``pyfdax*`` are created in ``<python>/Scripts``.

For development, you can also run pyFDA using::

    In [1]: %run -m pyfda.pyfdax # IPython or
    >> python -m pyfda.pyfdax    # plain python interpreter

    
or files from pyFDA using e.g.::

    In [2]: %run -m pyfda.input_widgets.input_pz  # IPython or
    >> python -m pyfda.input_widgets.input_pz     # plain python interpreter
   
Customization
-------------

The layout and some default paths can be customized using the file ``pyfda/pyfda_rc.py``.

Features
--------

* **Filter design**
    * **Design methods** from scipy.signal: Equiripple, Firwin, Butterworth, Elliptic, Chebychev 1 and Chebychev 2 
    * **Remember all specifications** when changing filter design methods
    * **Fine-tune** manually the filter order and corner frequencies calculated by minimum order algorithms
    * **Compare filter designs** for a given set of specifications and different design methods
    * **Filter coefficients and poles / zeroes** can be displayed, edited and quantized

* **Clearly structured GUI**
    * only widgets needed for the currently selected design method are visible
    * enhanced matplotlib NavigationToolbar (nicer icons, additional functions)

* **Common interface for all filter design methods:**
    * specify frequencies as absolute values or normalized to sampling or Nyquist frequency
    * specify ripple and attenuations in dB, as voltage or as power ratios
    * enter expressions like exp(-pi/4 * 1j) with the help of the library ``simpleeval`` (https://pypi.python.org/pypi/simpleeval) (included in source files)

* **Graphical Analyses**
    * Magnitude response (lin / power / log) with optional display of specification bands, phase and an inset plot
    * Phase response (wrapped / unwrapped)
    * Group delay
    * Pole / Zero plot
    * Impulse response and step response (lin / log)
    * 3D-Plots (\|H(f)\|, mesh, surface, contour) with optional pole / zero display

* **Modular architecture**, facilitating the implementation of new filter design and analysis methods
    * Filter design files not only contain the actual algorithm but also dictionaries specifying which parameters and standard widgets have to be displayed in the GUI. 
    * Special widgets needed by design methods (e.g. for choosing the window type in Firwin) are included in the filter design file, not in the main program
    * Filter design files can be added and edited *without* changing or even restarting the program

* **Saving and loading**
    * Save and load filter designs in pickled and in numpy's NPZ-format
    * Export coefficients and poles/zeros as comma-separated values (CSV), in numpy's NPZ-format, in Excel (R) or in Matlab (R) workspace format

* **Display help files** (own / Python docstrings) as rich text
* **Runs under Python 2.7 and Python 3.3 ... 3.5**

Why yet another filter design tool?
+++++++++++++++++++++++++++++++++++
* **Education:** There is a very limited choice of user-friendly, license-free tools available to teach the influence of different filter design methods and specifications on time and frequency behaviour. It should be possible to run the tool without severe limitations also with the limited resolution of a beamer.
* **Show-off:** Demonstrate that Python is a potent tool for digital signal processing applications as well. The interfaces for textual filter design routines are a nightmare: linear vs. logarithmic specs, frequencies normalized w.r.t. to sampling or Nyquist frequency, -3 dB vs. -6 dB vs. band-edge frequencies ... (This is due to the different backgrounds and the history of filter design algorithms and not Python-specific.)
* **Fixpoint filter design for uCs:** Recursive filters have become a niche for experts. Convenient design and simulation support (round-off noise, stability under different quantization options and topologies) could attract more designers to these filters that are easier on hardware resources and much more suitable e.g. for uCs.
* **Fixpoint filter design for FPGAs**: Especially on low-budget FPGAs, multipliers are expensive. However, there are no good tools for designing and analyzing filters requiring a limited number of multipliers (or none at all) like CIC-, LDI- or Sigma-Delta based designs.
* **HDL filter implementation:** Implementing a fixpoint filter in VHDL / Verilog without errors requires some experience, verifying the correct performance in a digital design environment with very limited frequency domain simulation options is even harder. The Python module *myHDL* (http://myhdl.org) can automate both design and verification.


