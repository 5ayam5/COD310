---
geometry:
- top=25mm
- left=20mm
- right=20mm
- bottom=30mm
documentclass: extarticle
fontsize: 12pt
numbersections: true
title: COD310 Notes
--- 

# Stuff to Read
1. 3D memory systems - 3D DRAM
1. Memory leakage power
1. SPEC CPU2006 benchmarks
1. Hybrid Memory Cube (HMC), High Bandwidth Memory (HBM) and Wide IO (WIO)
1. CACTI-3DD

# Doubts
1. What mechanism controls the memory management in memory devices

# Leakage-Aware Dynamic Thermal Management of 3D Memories

## Overview (Abstract)
1. Controlling leakage by monitoring temperature
1. Turn off specific memory channels to control temperature (before turning off, migrate data to 2D memory) - **FastCool**
1. **Energy-Efficient FastCool (EEFC)** - decides which channels to be closed

## Introduction
1. 3D memory is stacked 2D DRAM, thus has higher power density
1. Power consumption involves dynamic (48%) and static/leakage power (52%)
1. Static power increases exponentially with temperature, thus a positive feedback between temperature and leakage

## Proposed DTM Strategies

### TAM (Thermal-Aware Migration) States
1. NORMAL
1. SWAP
1. E1 (thermal Emergency 1)
1. E2
1. E3
1. THROTTLE

![](TAM.png)

### Memory Delay Models
2D memory request time = Data Migration Delay (DMD) + Data Access Delay (DAD)

![](parameter_definitions.png)

#### DMD
$$DMD = (s_{3D} + s_{2D}) \times \max\left(\frac{1}{B_{3D}}, \frac{1}{B_{2D}}\right)$$
$$B_{3D} = b_{3D} \times n_{3D} \times (1 - \text{3D Memory Refresh Overhead})$$
$$B_{2D} = b_{2D} \times N_{2D} \times (1 - \text{2D Memory Refresh Overhead})$$
$$\text{Refresh Overhead} = \frac{\text{Time required to refresh a row}\times\text{Number of rows}}{\text{Refresh interval}}$$

#### DAD
$$DAD = DAD_B + DAD_L$$
$$A = A_{2D} + A_{3D}\text{, total 2D memory accesses}$$
$$DAD_B = \frac{A \times C}{B_{2D}}$$
$$DAD_L = QD + LD\text{, queuing delay + latency delay}$$

##### Latency Delay
$$LD = \frac{A \times L_{2D}}{BA_{2D} \times R_{2D} \times N_{2D}}$$

##### Queuing Delay
Uses Queuing Theory to model the waiting time. *M/M/1* model is used, having a single queue for each server, and arrival and service rates are Poisson and exponential respectively.
$$QD = \frac{A \times C}{T \times B_{2D}}\times\frac{N_{2D}}{B_{2D} - (A \times C / T)}$$
$$\left(\lambda = \frac{A \times C}{T \times N_{2D}}, \mu = \frac{B_{2D}}{N_{2D}}, \text{expected time} = \frac{\lambda}{\mu\times(\mu - \lambda)}\right)$$

### FastCool
1. Transition to E1 happens only if total access count of channels {5, 6, 9, 10} exceeds $A_{MIN}$ ($A_{MIN} = 160,000$)
$$A_{3D} > A_{MIN}$$
1. Queuing stability needs to be ensured before migrating ($\lambda < \mu$)
$$A < \frac{B_{2D} \times T}{C}$$
1. Ensure transfer to 2D memory happens only if 2D delay is below a certain threshold to prevent slow down of operations
$$Delay < D_{MAX} (= 8.415 ms)$$

### FC Policy Improvements
*later*

### EEFC
*later*

### Leakage Current Estimation
*later*

### DTM Policy Implementation
*later*


# PredictNcool: Leakage Aware Thermal Management for 3D Memories Using a Lightweight Temperature Predictor

## Overview
1. Instead of reacting to temperature changes, this model attempts to utilise predicted temperature changes to reduce application runtime and memory energy
1. Symmetries in floor-plan and other design insights are used to reduct the predictor model parameters


# CoreMemDTM: Integrated Processor Core and 3D Memory Dynamic Thermal Management for Improved Performance

## Overview
Independent thermal management of core and memory leads to inefficient management since both cores and memories slow down


