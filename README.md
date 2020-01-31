# Overview
In this work we develop an approach to rapidly and cheaply generate large and diverse synthetic overhead imagery for training segmentation CNNs with CityEngine.  Using this approach, we generate and release a collection of synthetic overhead imagery, termed Synthinel-1, with full pixel-wise building labels.  We use several benchmark datasets to demonstrate that Synthinel-1 is consistently beneficial when used to augment real-world training imagery, especially when CNNs are tested on novel geographic locations or conditions.  <div align=center><img width="300" height="300" src="Externels/generate_img.png" alt="examples" align=center></div>
<p align=center>
    <em>Fig 1. (a) Illustration of a virtual city and two perspectives of a virtual camera, set by the designer.  The corresponding images for each camera are shown in panels (b) and (c).  The camera settings in (c) are used to generate the dataset in this work.  In (d) we show the corresponding ground truth labels extracted for the image in (c).   </em>
</p>

We summarized our work in paper "[The Synthinel-1 dataset: a collection of high resolution synthetic overhead imagery for building segmentation](https://arxiv.org/abs/2001.05130)" .


Synthinel-1 is now publicly released. Please download the dataset [here](https://drive.google.com/open?id=1T2fO-VLfyQoQdy5C4at_uHkP0KBRZkit).
<div align=center><img width="850" height="600" src="Externels/examples.gif" alt="examples" 
align=center></div>
<p align=center>
    <em>Fig 2. The automatic virtual city scene generation process.   </em>
</p>

### Examples
<div align=center><img width="900" height="270" src="Externels/examples2.png" alt="examples" 
align=center></div>
<p align=center>
    <em>Fig 3. Examples of caputured synthetic images in Synthinel.   </em>
</p>

### Our Experiments with Synthinel

In our experiments, we used two avaliable real-world dataset, Inria and DeepGlobe, to demonstrate the effectiveness of our synthetic dataset for pixel-wise building extraction task. We split Inria and DeepGlobe datasets into two disjoint subsets, one for training and one for testing, as illustrated in Fig 4. 
<div align=center><img width="450" height="300" src="Externels/dataset_split.png" alt="examples" 
align=center></div>
<p align=center>
    <em>Fig 4. Illustration of data handling for all experiments.    </em>
</p>

Then, we used two popular CNN models for image semantic segmentation, which are U-net and DeepLabV3. U-net is proposed in paper "U-Net: Convolutional Networks for Biomedical Image Segmentation" and DeepLabV3 is proposed in "Rethinking Atrous Convolution for Semantic Image Segmentation." For training, we have two schemes. For one scheme, we trained our networks only on real-world dataset. For the other, we trained the networks on real-world dataset jointly with synthetic dataset. Joinly training method is illustrated in our paper. For testing, we only tested our models on real-world datasets, Inria and DeepGlobe respectively. Specifically, we used the cross-domain testing to show the benefits of Synthinel. That is, for model trained on Inria, we tested it on DeepGlobe. For model trained on DeepGlobe, we tested it on Inria. The experiments decribed above is summarized in the following table,

<p align=center>
    <em>Table 1: Training and testing on different geographic locations. Results (intersection-over-union) of segmentation on popular building segmentation benchmark datasets.   </em>
</p>
<div align=center><img width="600" height="300" src="Externels/table.png" alt="examples" 
align=center></div>

### Dependencies

The dependencies to run the codes are 

* CityEngine 2019.0

### Third-Party Software
CityEngine used by Synthinel is a tool for rapidly generating large-scale virtual urban scenes. 

Research
---------

If you find our work is helpful for your research, we would very appreciate if you cite our paper.

    @inproceedings{synthinel2020,
        title={The Synthinel-1 dataset: a collection of high resolution synthetic overhead imagery for building segmentation},
        author={Fanjie Kong, Bohao Huang, Kyle Bradbury, Jordan Malof},
        booktitle={2020 Winter Conference on Applications of Computer Vision (WACV)},
        year={2020}
    }
    
    
   
### Research Logs

- Find some ground truths are not aligned with objects well. This is caused by the light variations in images for extracting ground truths. This can be fixed by changing the light angle to 90 degree and light intensity to 1 when shooting the images used for extracting ground truths.
