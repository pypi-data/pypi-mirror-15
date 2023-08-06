.. vim: set fileencoding=utf-8 :
.. Manuel Guenther <manuel.guenther@idiap.ch>
.. Tue 24 Mar 14:55:33 CET 2015

===========================================================================
 Gender Classification by LUT based boosting of Overlapping Block Patterns
===========================================================================

This package provides the source code to run the experiments published in the Paper_ `Gender Classification by LUT based boosting of Overlapping Block Patterns`.
The gender classification pipeline consists of two main steps:  feature extraction and classification.
OBP features are used in our method along with boosting of look-up tables as weak classifiers.
This package relies on Bob_ to execute both feature extraction and classification.


.. note::
   Currently, this package only works in Unix-like environments and under MacOS.
   Due to limitations of the Bob_ library, MS Windows operating systems are not supported.
   We are working on a port of Bob_ for MS Windows, but it might take a while.

.. warning::
   We have lately detected a small issue in the I/O of the LFW annotations that would rotate the aligned faces upside-down.
   We have fixed these issues in version 1.0.3.
   Due to the wrong alignment, the algorithms on the LFW database might now have slightly different results.
   However, since the algorithms are not sensitive to the rotation of the face -- as long as we have the same rotation in both the training and the test set -- the results should be very similar.


Installation:
=============
This package uses several Bob_ libraries, which will be automatically installed locally using the command lines as listed below.
However, in order for the Bob_ packages to compile, certain `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ need to be installed.

This package
------------
The installation of this package relies on the `BuildOut <http://www.buildout.org>`_ system.
By default, the command line sequence::

  $ python bootstrap-buildout.py
  $ ./bin/buildout

should download and install all required packages of Bob_ in the versions that we used to produce the results.
Other versions of the packages might generate sightly different results.

.. note::
   To use the latest versions of all Bob_ packages, please remove the strict version numbers that are given in the **buildout.cfg** file in the main directory of this package.

Databases
---------
Experiments are executed based on two publicly available image databases.
The evaluation protocols for both databases are included into this package:

- To get a copy of the `MOBIO database <http://www.idiap.ch/dataset/mobio>`_, please follow the `Download Instructions <https://www.idiap.ch/dataset/mobio/download-proc>`__, and download the ``IMAGES_PNG.tar.gz`` and the ``IMAGE_ANNOTATIONS.tar.gz``.

- The images of the `Labeled Faces in the Wild database <http://vis-www.cs.umass.edu/lfw/>`__ can be downloaded from the database URL.
  Our experiments rely on the `images aligned with funneling` (not the ones aligned with deep funneling), and `automatic annotations <http://lear.inrialpes.fr/people/guillaumin/data.php>`__.


The Experiments:
================

Protocol:
----------

The test are performed on two face data sets: MOBIO and Labeled Faces in Wild (LFW).

1) MOBIO: The evaluation protocol we use consists of training, development and test sets.
   The number of images in each set are: 9598 in Training set, 9586 in Development set and 9592 in Test set.

2) LFW: The data set consists of more than 13,000 images collected from web.
   The images are split into 5 non-overlapping partitions and on each test round four partition are used for training and the fifth one is used for testing.
   The accuracy is reported as the mean over the five sets.

Algorithms:
------------
The following algorithms are implemented:

* PCA + LDA: PCA is used with 98% variance and Linear Discriminant Analysis is used as the classifier.

* LBPHS + LDA: Uniform Local Binary Patterns (LBP) features are extracted from the images by dividing it into 6x6 cells.
  The LBP features from different cells are concatenated and the same PCA + LDA classifier is used.

* MB-LBP + LUT Boosting: Multi Block- LBP features of square shape are extracted from face images.
  The block size is varied from 1 to 7.
  The features are boosted with LUT as the weak classifier.

* OBP + LUT Boosting: OBP features of square shape are extracted from the images.
  The block size is varied from 1 to 7.
  The features are boosted with LUT as the weak classifier.

* LBP + LUT Boosting (not part of the paper): LPB features in a single scale are extracted from the images.
  The features are boosted with LUT as the weak classifier.


User Guide:
-----------
To reproduce the results from the paper use the following commands:

1) Image preprocessing::

   $ ./bin/preprocess.py -d mobio -i <MOBIO-IMAGE-DIRECTORY> -a <MOBIO-ANNOTATION-DIRECTORY> -vv
   $ ./bin/preprocess.py -d lfw -i <LFW-FUNNELED-IMAGE-DIRECTORY> -a <LFW-FUNNELED-ANNOTATION-DIRECTORY> -vv

2) PCA+LDA on raw pixel values::

   $ ./bin/pca_lda.py -d mobio lfw -vv

3) PCA+LDA on LBPHS features::

   $ ./bin/pca_lda.py -d mobio lfw -vv -l

4) Boosting with three types of features: MB-LBP, OBP, and LBP (just for comparison, not in the paper)::

   $ ./bin/lbp_boosting.py -d mobio lfw -vv
   $ ./bin/lbp_boosting.py -d mobio lfw -vv -o
   $ ./bin/lbp_boosting.py -d mobio lfw -vv -b 1

5) Evaluation::

   $ ./bin/evaluate.py -d mobio lfw -vv

The last command will print out the results as they are reported in Table 1 of the Paper_ and generate the ROC curves as shown in Figure 5 of the Paper_.

.. _bob: http://www.idiap.ch/software/bob
.. _virtualbox: http://www.virtualbox.org
.. _paper: http://publications.idiap.ch/index.php/publications/show/3112
