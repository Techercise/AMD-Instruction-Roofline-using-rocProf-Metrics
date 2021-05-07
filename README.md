# AMD-Instruction-Roofline-using-rocProf-Metrics
This repository contains example spreadsheets and scripts to construct instruction roofline models for AMD GPUs using metrics from [rocProf](https://github.com/ROCm-Developer-Tools/rocprofiler).

## Repository Overview

The Python files in this repository come from the [NERSC Roofline-on-NVIDIA-GPUs GitLab repo](https://gitlab.com/NERSC/roofline-on-nvidia-gpus). A few files were modified in order to be compatible with the metrics received from rocProf.

Directions on how to create a roofline model using the modified Python files are given as comments in the Python files. If there are any questions or clarifications needed, please feel free to create an issue.

## Creating an Instruction Roofline Model for AMD GPUs

### 1. Creating a metric query input file for rocProf
In order to profile metrics with rocProf, an input file (either .xml or .txt) needs to be created. An example of how to create that input file is found within the rocProf repo's documention (See Section 2.1 [here](https://github.com/ROCm-Developer-Tools/rocprofiler/blob/amd-master/doc/rocprof.md)). Alternatively, if following the methodology in this repository, an example input file is provided [here](https://github.com/Techercise/AMD-Instruction-Roofline-using-rocProf-Metrics/blob/main/rocprof_input_file.txt).

### 2. Running or Submitting a Job
When running a job (or submitting a job to run), the binary file needs to be preceded by `rocProf -i` following the name of the rocProf input file. We give an example command using [PIConGPU](https://github.com/ComputationalRadiationPhysics/picongpu), a plasma-physics application:
```rocprof -i rocprof_input_file.txt --timestamp on ./bin/picongpu -d 1 1 1 -g  128 128 128 -s 10 --periodic 1 1 1```

After the job finishes running, the results will be stored in a csv file with the same name as the input file (ex: rocprof_input_file.csv).

### 3. After rocProf Metrics are Gathered
After you get a csv file with the metric data from rocProf, if there are multiple kernel streams, average out or find the max of the metric values (see the corresponding sample xlsx file [here](https://github.com/Techercise/AMD-Instruction-Roofline-using-rocProf-Metrics/blob/main/TWEAC_MI100_Instruction_Roofline_Metrics.xlsx)) and put the averages into a new csv file like [this one](https://github.com/Techercise/AMD-Instruction-Roofline-using-rocProf-Metrics/blob/main/LWFA_simulations/mi100_lw_cc_inst_output.csv).
**NOTE:** The only important parts of the sample csv file are the metric names, units, and values. The columns to the left of those three columns were put in place to make the csv look more like the csv files from Nsight Compute.

### 4. Run the Python code
The Python files `amd_postprocess_instruction.py` and `amd_plot_roofline_hierarchical.py` are virtually ready to run. Simply edit `amd_post_process_instruction.py` with the name of and path to your average values csv file (see Step 3). Then, if needed, edit `amd_plot_roofline_hierarchical.py` to update the memory bandwidth and theoretical peak GIPS values.
__If you need roofline data for more than one device, follow steps 1 - 3 again while running on the new device and then follow the comments in_ `amd_plot_roofline_hierarchical.py`.
