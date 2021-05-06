# AMD-Instruction-Roofline-using-rocProf-Metrics
This repository contains example spreadsheets and scripts to construct instruction roofline models for AMD GPUs using metrics from [rocProf](https://github.com/ROCm-Developer-Tools/rocprofiler).

## Repository Overview

The Python files in this repository come from the [NERSC Roofline-on-NVIDIA-GPUs GitLab repo](https://gitlab.com/NERSC/roofline-on-nvidia-gpus). A few files were modified in order to be compatible with the metrics received from rocProf.

Directions on how to create a roofline model using the modified Python files are given as comments in the Python files. If there are any questions or clarifications needed, please feel free to create an issue.

## Creating an Instruction Roofline Model for AMD GPUs

### 1. Creating a metric query input file for rocProf
In order to profile metrics with rocProf, an input file (either .xml or .txt) needs to be created. An example of how to create that input file is found within the rocProf repo's documention (See Section 2.1 [here](https://github.com/ROCm-Developer-Tools/rocprofiler/blob/amd-master/doc/rocprof.md)). Alternatively, if following the methodology in this repository, an example input file is provided [here]().
