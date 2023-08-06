.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Thu 23 Jun 13:43:22 2016

===============================================
Reproducing paper published in Interspeech 2016
===============================================

This package is part of the Bob_ toolkit, which allows to reproduce the results experiments published in the following paper::

    @inproceedings{KorshunovInterspeech2016,
        author = {P. Korshunov AND S. Marcel},
        title = {Cross-database evaluation of audio-based spoofing detection systems},
        year = {2016},
        month = sep,
        booktitle = {Interspeech},
        address = {San Francisco, CA, USA},
    }


This package contains basic scripts to run Presentation Attack Detection (PAD) speech experiments presented in the paper.
It utilizes a more generic ``./bin/spoof.py`` script from Bob's package ``bob.pad.base`` that takes several parameters, including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A PAD algorithm

All these steps of the PAD system are given as configuration files.

To run all the experiments, two databases need to be downloaded: AVspoof_ and ASVspoof_. The paths to folders with the corresponding data need to be updated in the following files inside the ``src/bob.pad.speech/bob/pad/speech/config/database`` directory:

* asvspoof.py
* asvspoof_verify.py
* avspoof.py
* avspoof_verify.py

Once the databases are dowloaded, the corresponding Bob's interfaces need to be updated too. Please run the following commands::

    For AVspoof database: $ ./bin/bob_dbmanage.py avspoof download 
    For ASVspoof database: $ ./bin/bob_dbmanage.py asvspoof download

Now everything is ready to run the experiments. Here is a generic command for training GMM-based PAD system::

    $ ./bin/train_gmm.py -d DB_NAME -p Preprocessor -e Feature_Extractor -a gmm-toni -s Folder_Name -groups world --skip-enroller-training -vv

Here is the generic command to tune the system on developing set and evaluate on the test set::

    $ ./bin/spoof.py -d DB_NAME -p Preprocessor -e Feature_Extractor -a gmm --projector-file Projector_spoof.hdf5 -s Folder_Name -groups dev eval --skip-projector-training -vv

For example, to train and evaluate a GMM-based PAD system using MFCC-based features for Licit protocol of the ASVspoof database, the following commands need to be run::

    $ ./bin/train_gmm.py -d asvspoof-licit -p mod-4hz -e mfcc20 -a gmm-toni -s temp -groups world --skip-enroller-training -vv
    $ ./bin/train_gmm.py -d asvspoof-spoof -p mod-4hz -e mfcc20 -a gmm-toni -s temp -groups world --skip-enroller-training -vv
    $ ./bin/spoof.py -d asvspoof -p mod-4hz -e mfcc20 -a gmm --projector-file Projector_spoof.hdf5 -s temp -groups dev eval --skip-projector-training -vv
    
Then, using the obtained scores, error rates can be computed and DET curves plotted using the following script::

    $ ./bin/plot_pad_results.py -t scores_path/dev-attack -d scores_path/dev-real -f scores_path/eval-attack -e scores_path/eval-real -o plots"

Also, it is possible to reproduce the experiments presented in the paper using the following bash scripts that run for all PAD systems used::

    $ ./train_gmms.sh avspoof 20  # train for AVspoof database
    $ ./train_gmms.sh asvspoof 20  # train for ASVspoof database
    $ ./project_on_gmms.sh avspoof 20  # evaluate for AVspoof database
    $ ./project_on_gmms.sh asvspoof 20  # evaluate for ASVspoof database


Generate results from pre-computed scores
-----------------------------------------

If you want to avoid training all PAD systems and computing scores, we are providing the score files obtained for all the PAD systems presented in the paper. Hence, the error rates can be computed, as per Tables 1, 2, and 3 of the paper, and additional DET curves can be plotted by simply performing the following::

    $ #You should be inside the package directory bob.paper.interspeech_2016
    $ wget http://www.idiap.ch/resource/biometric/data/interspeech_2016.tar.gz #Download the scores
    $ tar -xzvf interspeech_2016.tar.gz  
    $ ./evaluate_scores.sh # compute error rates and plot the DET curves for each PAD system

The script will create folders for each different PAD system (it contains computed error rates and DET curves) and one ``stats.txt`` file with error rates from all systems in one LaTeX table.

To plot combined DET curves for different systems as per Figure 2 of the paper, the following script can be run::

    $ ./plot_pad_diff_methods.sh  # plot DET curves for selected PAD systems as in Figure 2

This script will plot several DET curves in a single PDF file inside the folder ``plots_compare_pads``.

Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. ASVspoof_: http://datashare.is.ed.ac.uk/handle/10283/853

