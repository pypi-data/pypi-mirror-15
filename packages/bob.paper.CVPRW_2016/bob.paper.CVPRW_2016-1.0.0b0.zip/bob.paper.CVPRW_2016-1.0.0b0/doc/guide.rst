.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Fri 29 Apr 2016 09:09:34 CEST 

==============
 User's Guide
==============


Reproduction of the Figure 1
----------------------------

The Figure 1 in the paper presents a plot explaining the intuition of the ISV.
To reproduce this plot run the following command::

  $ ./bin/ISV_intuition.py

An output file called **ISV_intuition.pdf** will be generated.



Reproduction of the Figures 3 and 4
----------------------------------

There are two ways to reproduce the Figures 3 and 4, either generate the plots directly from the pre-computed score files or execute every single experiment from scratch.

Generate the plots from the pre-computed scores
===============================================

This is the fastest way to do it and you can generate the plots via the 4 commands bellow::

  $ cd ./bob.paper.CVPRW_2016 #Moving to the package directory
  $ wget http://www.idiap.ch/resource/biometric/data/CVPRW_2016.tar.gz #Downloading the scores
  $ tar -xzvf CVPRW_2016.tar.gz  
  $ ./bin/generate_plot_results.py


Generate the plots from scratch
===============================

.. warning:: 

   This is the slowest way to do it and can take several days (specially for the CBSR NIR-VIS-2.0 database).
   This paper is a result of 175 experiments.

To run the experiments using the CUHK_CUFS, please, run variations following base command::

  $ ./bin/verify.py \
  --database "bob.bio.base.database.DatabaseBobZT(bob.db.cuhk_cufs.Database(original_directory = '[CUFS_DATABASE_DIR]',  arface_directory='[ARFACE_DATABASE_DIR]', xm2vts_directory='[XM2VTS_DATABASE_DIR]', original_extension = ['.jpg','.JPG','.ppm']), name='cuhk-cufs')" \
  --preprocessor face-crop-eyes \
  --extractor dct-blocks \
  --imports bob.db.cuhk_cufs bob.bio.base bob.bio.gmm \
  --temp-directory [INTERMEDIATE_FILE_DIRECTORY] \
  --result-directory [SCORES_DIRECTORY] \
  -vv \
  --groups dev \
  --protocol [DATABASE_PROTOCOL] \
  --algorithm "bob.bio.gmm.algorithm.ISV(subspace_dimension_of_u = [RANK_U], number_of_gaussians     = [GAUSSIAN_COMPONENTS], gmm_training_iterations = 10, update_weights   = False,update_variances = False)" \
  --sub-directory [DATABASE_PROTOCOL]/ISV_nofilter/g[GAUSSIAN_COMPONENTS]_u[RANK_U]
  
Where
 - [CUFS_DATABASE_DIR]: The directory of the CUHK-CUFS dataset
 - [ARFACE_DATABASE_DIR]: The directory of the ARFACE dataset (in order to get the ARFACE VIS images)
 - [XM2VTS_DATABASE_DIR]: The directory of the XM2VTS dataset (in order to get the XM2VTS VIS images)
 - [INTERMEDIATE_FILE_DIRECTORY]: The directory for the intermediate files (features, models, etc...)
 - [SCORES_DIRECTORY]: The directory for the scores
 - [DATABASE_PROTOCOL]: The database protocol [search_split1_p2s, search_split2_p2s, search_split3_p2s, search_split4_p2s, search_split5_p2s]
 - [RANK_U]: The rank of U. Specially for this paper was tested [200, 160, 100, 50, 10]
 - [GAUSSIAN_COMPONENTS]: Number of Gaussian components. Specially for this paper was tested [1024, 512, 256, 128, 64]
  


To run the experiments using the CBSR NIR-VIS-2.0, please, run variations following base command::

  $ ./bin/verify.py \
  --database "bob.bio.base.database.DatabaseBob(bob.db.cbsr_nir_vis_2.Database(original_directory = '[CBSR_DATABASE_DIR]', original_extension=['.bmp','.jpg'], annotation_directory='[ANNOTATIONS_DATABASE_DIR]'), name='cbsr_nir_vis_2')" \
  --preprocessor face-crop-eyes \
  --extractor dct-blocks \
  --imports bob.db.cuhk_cufs bob.bio.base bob.bio.gmm \
  --temp-directory [INTERMEDIATE_FILE_DIRECTORY] \
  --result-directory [SCORES_DIRECTORY] \
  -vv \
  --groups dev \
  --protocol [DATABASE_PROTOCOL] \
  --algorithm "bob.bio.gmm.algorithm.ISV(subspace_dimension_of_u = [RANK_U], number_of_gaussians     = [GAUSSIAN_COMPONENTS], gmm_training_iterations = 10, update_weights   = False,update_variances = False)" \
  --sub-directory [DATABASE_PROTOCOL]/ISV_nofilter/g[GAUSSIAN_COMPONENTS]_u[RANK_U]
  
Where
 - [CBSR_DATABASE_DIR]: The directory of the CBSR NIR-VIS-2.0 dataset
 - [ANNOTATIONS_DATABASE_DIR]: The directory of the annotations CBSR NIR-VIS-2.0 dataset
 - [INTERMEDIATE_FILE_DIRECTORY]: The directory for the intermediate files (features, models, etc...)
 - [SCORES_DIRECTORY]: The directory for the scores
 - [DATABASE_PROTOCOL]: The database protocol [search_split1_p2s, search_split2_p2s, search_split3_p2s, search_split4_p2s, search_split5_p2s]
 - [RANK_U]: The rank of U. Specially for this paper was tested [200, 160, 100, 50, 10]
 - [GAUSSIAN_COMPONENTS]: Number of Gaussian components. Specially for this paper was tested [1024, 512, 256, 128, 64]


Once you have all the scores generated from this sequence of experiments, you can ran the command bellow to generate the plots::

  $ ./bin/generate_plot_results.py
  
  
  


