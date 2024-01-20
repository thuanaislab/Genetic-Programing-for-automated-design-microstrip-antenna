# [Genetic Programing for automated design microstrip antenna](https://ieeexplore.ieee.org/abstract/document/8879155)
Hybrid Genetic Programming with Accelerating Conjugate Direct Gradient Search for Automated Antenna Design. Any inquiries: thuan.aislab@gmail.com

<p align="center">
  <img src="https://github.com/thuanaislab/Genetic-Programing-for-automated-design-microstrip-antenna/blob/main/images/GP_lowlevel.png" width="430" title="hover text">
<p>

<p align="center">
  <img src="https://github.com/thuanaislab/Genetic-Programing-for-automated-design-microstrip-antenna/blob/main/images/smallsize_antenna.PNG" width="350" title="hover text">
<p>

## Genetic Programming Architecture

<p align="center">
  <img src="https://github.com/thuanaislab/Genetic-Programing-for-automated-design-microstrip-antenna/blob/main/images/gp1.png" width="550" title="hover text">
<p>

## Some Interesting Results Designed by Our Tool 

<p align="center">
  <img src="https://github.com/thuanaislab/Genetic-Programing-for-automated-design-microstrip-antenna/blob/main/images/result1.png" width="700" title="hover text">
<p>

<p align="center">
  <img src="https://github.com/thuanaislab/Genetic-Programing-for-automated-design-microstrip-antenna/blob/main/images/result2.png" width="700" title="hover text">
<p>

# Set up
- [anaconda](https://www.anaconda.com/products/individual) 
- geopandas==0.3.0
- [pstool](https://docs.microsoft.com/en-us/sysinternals/downloads/pstools)
- HFSS 14.0
- Create a folder HFSS_shared in C:/ and share it for everyone. The purpose is for parallelism computing
- I made a detail video guide for installation. You can find it in [here](https://youtu.be/mi2dpRd85NU)
# Running
```
python GP_main.py
```
## BibTex Citation 
If you find this project useful, please cite:
```
@inproceedings{bach2019evolved,
  title={Evolved design of microstrip patch antenna by genetic programming},
  author={Bach, Thuan Bui and Manh, Linh Ho and Khac, Kiem Nguyen and Beccaria, Michele and Massaccesi, Andrea and Zich, Riccardo},
  booktitle={2019 International Conference on Electromagnetics in Advanced Applications (ICEAA)},
  pages={1393--1397},
  year={2019},
  organization={IEEE}
}
```
