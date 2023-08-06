#/*##########################################################################
#
# The fisx library for X-Ray Fluorescence
#
# Copyright (c) 2014-2016 European Synchrotron Radiation Facility
#
# This file is part of the fisx X-ray developed by V.A. Sole
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
#ifndef FISX_XRF_H
#define FISX_XRF_H
#include "fisx_xrfconfig.h"
#include "fisx_elements.h"
#include <iostream>

namespace fisx
{

class XRF
{

typedef std::map<std::string, std::map<int, std::map<std::string, std::map<std::string, double> > > > \
        expectedLayerEmissionType;
typedef std::map<std::string, std::map<int, std::map<std::string, std::map<std::string, double> > > >::const_iterator \
        iteratorExpectedLayerEmissionType;

public:
    /*!
    Default constructor
    */
    XRF();

    /*!
    Constructor with configuration file
    */
    XRF(const std::string & configurationFile);

    /*!
    Read the configuration from file
    */
    void readConfigurationFromFile(const std::string & fileName);

    /*!
    Set the excitation beam
    */
    void setBeam(const Beam & beam);

    /*!
    Easy to wrap funtion to set the excitation beam
    \param energies Set of double values corresponding to energies (in keV) describing
           the incoming beam
    \param weight Set of weights with the relative intensity of each energy
    \param characteristic Integer flag currently ignored by fisx library
    \param divergency Beam divergency in degrees (currently ignored by fisx library)
    */
    void setBeam(const std::vector<double> & energies, \
                 const std::vector<double> & weight, \
                 const std::vector<int> & characteristic = std::vector<int>(), \
                 const std::vector<double> & divergency = std::vector<double>());

    /*!
    Funtion to set a single energy excitation beam
    \param energy Energy of the incoming beam
    */
    void setBeam(const double & energy, const double & divergency = 0.0);


    /*!
    Set the beam filters to be applied
    */
    void setBeamFilters(const std::vector<Layer> & filters);

    /*!
    Set the sample description.
    It consists on a set of layers of different materials, densities and thicknesses.
    The top layer will be taken as reference layer. This can be changed calling setRefenceLayer
    */
    void setSample(const std::vector<Layer> & layers, const int & referenceLayer = 0);

    /*!
    Convenience method for single layer samples.
    */
    void setSample(const std::string & name, \
                   const double & density = 1.0, \
                   const double & thickness = 1.0);

    /*!
    Convenience method for single layer samples.
    */
    void setSample(const Layer & layer);

    /*!
    It consists on a set of layers of different materials, densities and thicknesses and
    "funny" factors.
    */
    void setAttenuators(const std::vector<Layer> & attenuators);

    /*!
    Set the detector. For the time being it is very simple.
    It has active area/diameter, material, density, thickness and distance.
    */
    void setDetector(const Detector & detector);


    /*!
    Set the excitation geometry.
    For the time being, just the incident, outgoing angles and scattering angle to detector
    center. A negative scattering angle of 90 degrees indicates the scattering angle is the
    sum of alphaIn and alphaOut.
    */
    void setGeometry(const double & alphaIn, const double & alphaOut,\
                      const double & scatteringAngle = -90.);

    /*!
    Set the reference layer. The detector distance is measured from the reference layer surface.
    If not specified, the lauer closest to the detector
    */
    void setReferenceLayer(const int & index);
    void setRefenceLayer(const std::string & name);

    /*!
    Set the elements library to be used.
    */
    //void setElementsReference(const Elements & elements);

    /*!
    Collimators are not implemented yet. The collimators are attenuators that take into account their distance to
    the sample, their diameter, thickness and density
    */
    void setCollimators();
    void addCollimator();

    /*!
    Get the current configuration
    */
    const XRFConfig & getConfiguration();

    /*!
    Set the configuration
    */
    void setConfiguration(const XRFConfig & configuration);

    /*!
    Get the expected fluorescence emission coming from primary excitation per unit photon.
    It needs to be multiplied by the mass fraction and the total number of photons to get
    the actual primary fluorescence.

    The output is a map:

    Element -> Family -> Line -> energy: double, ratio: double

    */
    std::map< std::string, std::map< std::string, std::map<std::string, std::map<std::string, double> > > >\
                getExpectedPrimaryEmission(const std::vector<std::string> & elementList,
                                           const Elements & elements);

    /*!
    Methods coordinating all the calculation
    void detectedEmission()
    void expectedEmission():
    void expectedFluorescence();
    void expectedScattering();
    void peakRatios();
    */
    double getGeometricEfficiency(const int & layerIndex = 0) const;

    std::map<std::string, std::map<std::string, double> > getFluorescence(const std::string & element, \
                const Elements & elementsLibrary, const int & sampleLayerIndex = 0, \
                const std::string & lineFamily = "", const int & secondary = 0, \
                const int & useGeometricEfficiency = 1);


    /*!
    Return a complete output of the form
    [Element Family][Layer][line]["energy"] - Energy in keV of the emission line
    [Element Family][Layer][line]["primary"] - Primary rate prior to correct for detection efficiency
    [Element Family][Layer][line]["secondary"] - Secondary rate prior to correct for detection efficiency
    [Element Family][Layer][line]["rate"] - Overall rate
    [Element Family][Layer][line]["efficiency"] - Detection efficiency
    [Element Family][Layer][line][element line layer] - Secondary rate (prior to correct for detection efficiency)
    due to the fluorescence from the given element, line and layer index composing the map key.
    */
    std::map<std::string, std::map<int, std::map<std::string, std::map<std::string, double> > > > \
                getMultilayerFluorescence(const std::string & element, \
                const Elements & elementsLibrary, const int & sampleLayerIndex = 0, \
                const std::string & lineFamily = "", const int & secondary = 0, \
                const int & useGeometricEfficiency = 1, const int & useMassFractions = 0, \
                const double & secondaryCalculationLimit = 0.0);
    /*!
    Basis method called by all the other convenience methods.
    \param elementFamilyLayer - Vector of strings. Each string represents the information we are interested on.\n
    "Cr"     - We want the information for Cr, for all line families and sample layers\n
    "Cr K"   - We want the information for Cr, for the family of K-shell emission lines, in all layers.\n
    "Cr K 0" - We want the information for Cr, for the family of K-shell emission lines, in layer 0.
    \param elementsLibrary - Instance of library to be used for all the Physical constants
    \param secondary - Flag to indicate different levels of secondary excitation to be considered.\n
                0 Means not considered\n
                1 Consider secondary excitation\n
                2 Consider tertiary excitation\n
    \param useGeometricEfficiency - Take into account solid angle or not. Default is 1 (yes)

    \param useMassFractions - If 0 (default) the output corresponds to the requested information if the mass
    fraction of the element would be one on each calculated sample layer. To get the actual signal, one
    has to multiply the rates by the actual mass fraction of the element on each sample layer.
                       If set to 1, the rate will be already corrected by the actual mass fraction.

    \return Return a complete output of the form:\n
    [Element Family][Layer][line]["energy"] - Energy in keV of the emission line\n
    [Element Family][Layer][line]["primary"] - Primary rate prior to correct for detection efficiency\n
    [Element Family][Layer][line]["secondary"] - Secondary rate prior to correct for detection efficiency\n
    [Element Family][Layer][line]["rate"] - Overall rate\n
    [Element Family][Layer][line]["efficiency"] - Detection efficiency\n
    [Element Family][Layer][line][element line layer] - Secondary rate (prior to correct for detection efficiency)
    due to the fluorescence from the given element, line and layer index composing the map key.\n
    [Element Family][Layer][line]["massFraction"] - Mass fraction of the element in the considered layer
    */
    std::map<std::string, std::map<int, std::map<std::string, std::map<std::string, double> > > > \
                getMultilayerFluorescence(const std::vector<std::string> & elementFamilyLayer, \
                const Elements & elementsLibrary, const int & secondary = 0, \
                const int & useGeometricEfficiency = 1, \
                const int & useMassFractions = 0, \
                const double & secondaryCalculationLimit = 0.0);

    std::map<std::string, std::map<int, std::map<std::string, std::map<std::string, double> > > > \
                getMultilayerFluorescence(const std::vector<std::string> & elementList,
                                          const Elements & elementsLibrary, \
                                          const std::vector<int> & layerList, \
                                          const std::vector<std::string> &  familyList, \
                                          const int & secondary = 0, \
                                          const int & useGeometricEfficiency = 1, \
                                          const int & useMassFractions = 0, \
                                          const double & secondaryCalculationLimit = 0.0);


    double getEnergyThreshold(const std::string & elementName, const std::string & family, \
                                const Elements & elementsLibrary) const;


    /*!
    Return the expected fluorescent spectrum per unit photon

    channel vector of channel values at which the spectrum is to be evaluated

    detectorParameters is <string, double> map that may contain the following keys:

    Zero : Energy calibration parameter. Energy at channel 0. Term A in Energy (keV) = A + B * channel.
    Gain : Term B in Energy (keV) = A + B * channel
    Noise : Electronic noise in keV
    Fano : Fano factor
    QuantumEnergy : Average energy (in keV) to create a "signal quantum" (an electron-hole pair in Si)
                    In scintillator detectors is ~100 eV and in gas detectors ~30 eV.

    If any of those keys is not present, the associated value will be taken from the configuration.

    shapeParameters is a map that may contain the following keys:

    ShortTailArea : Area in the short exponential tail respect to the main gaussian area
    ShortTailSlope : The slope of the short exponential tail in main gaussian sigma units
    LongTailArea : Area in the long exponential tail respect to the main gaussian area
    LongTailSlope : The slope of the long exponential tail in main gaussian sigma units
    StepHeight : Height of the step tail relative to the main gaussian height
    Eta : Pseudo-voigt function parameter. (1.0 - Eta) * GaussianTerm + Eta * LorentzianTerm

    If Eta is present, the other parameters are ignored. A value of Eta equal to 0.0 or an empty map
    will force a Gaussian response regardless of the remaining parameters.

    peakFamilyAreas is a map that contains the total area associated to a certain peak family.
    In order to foresee "per layer" calculations the keys have the from "Element Family number" where
    number is optional. For instance:

    Cr K : Total Chromium K-shell area
    Cr K 0 : Total Chromium K-shell area coming from layer 0.

    Obviously both types of keys should not be used for the same element and family.

    */
    std::map<std::string, std::vector<double> > getSpectrum(const std::vector<double> & channel, \
                const std::map<std::string, double> & detectorParameters = (std::map<std::string, double> ()), \
                const std::map<std::string, double> & shapeParameters = (std::map<std::string, double> ()), \
                const std::map<std::string, double> & peakFamilyArea = (std::map<std::string, double> ()), \
                const expectedLayerEmissionType & emissionRatios = (expectedLayerEmissionType())) const;

    /*!
    Alternative method in a more traditional way.
    */
    void getSpectrum(double * channel, double * energy, double *spectrum, int nChannels, \
                const std::map<std::string, double> & detectorParameters = (std::map<std::string, double> ()), \
                const std::map<std::string, double> & shapeParameters = (std::map<std::string, double> ()), \
                const std::map<std::string, double> & peakFamilyArea = (std::map<std::string, double> ()), \
                const expectedLayerEmissionType & emissionRatios = (expectedLayerEmissionType())) const;

private:
    /*!
    Reference to elements library to be used for calculations
    */
    /*!
    The internal configuration
    */
    XRFConfig configuration;

    /*!
    Some optimization flags
    */
    bool recentBeam;

    expectedLayerEmissionType lastMultilayerFluorescence;
};

} // namespace fisx

#endif // FISX_XRF_H
