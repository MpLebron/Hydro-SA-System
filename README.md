# Hydro-SA-System: Sensitivity Analysis for Hydrological Models

This repository hosts the **Hydro-SA-System**, a prototype system for facilitating sensitivity analysis (SA) of hydrological models (HMs), as described in the paper *"Facilitating Sensitivity Analysis of Hydrological Models Through Knowledge-Driven Configuration and Distributed Online Model Services"* . The system integrates **knowledge-driven configuration** with **distributed online model services** to streamline SA processes, enhance computational efficiency, and promote knowledge sharing among researchers.

## System Overview

### Purpose
The Hydro-SA-System simplifies the complex and computationally intensive process of sensitivity analysis for hydrological models. It enables researchers to identify influential parameters, optimize model calibration, and gain deeper insights into hydrological dynamics.

### Core Innovations
- **Knowledge-Driven Configuration**:
  - **Rule-Based Knowledge Repository**: Provides standardized guidance for SA configuration across stages like Design of Experiment (DoE), method selection, and result evaluation.
  - **Case-Based Knowledge Repository**: Recommends similar SA cases to leverage prior experience.
  - **Multiple SA Methods**: Supports Morris, eFAST, PAWN, and more.
- **Distributed Online Model Services**:
  - Encapsulates HMs as web services for seamless integration and reuse.
  - Utilizes distributed computing to handle large-scale SA tasks efficiently.
  - Employs Model Description Language (MDL) to standardize model descriptions.

### Main Features
- Guided SA configuration with rule-based and case-based support
- Reuse of prior SA cases to reduce redundant efforts
- Distributed computing for scalable, high-performance simulations
- Modular SA pipeline including parameter sampling, simulation, sensitivity computation, and visualization

## Technical Architecture

### Frontend (SA-front-project)
- Built with Vue.js 2 + ElementUI
- Key components:
  - Knowledge Library (libraryPage)
  - Project Management (managePage)
  - Model Management (modelList)
  - SA Process Components (dataState, paramState, processStep, etc.)
  - Result Visualization (scoreSA, simResult)

### Backend (SA-back-project)
- Built with Spring Boot
- Core modules:
  - Model Service Management (ComputableModelController)
  - Knowledge Library Management (ExperienceLibraryController)
  - Project Management (ProjectController)
  - Simulation Service (SimulationController)
  - Distributed Task Management (TaskDao)

### Distributed Computing
- Task Management Layer: Task parsing and distribution
- Data Exchange Layer: Unified data I/O interface
- Model Execution Layer: Model service containers

## Usage Guide

1. **Create an SA Project**
   - Access the web interface.
   - Initialize a new SA_Project with study area and model details

2. **Configure Parameters and Model**
   - Define parameters (SA_Param) with ranges and distributions
   - Upload input datasets and configure simulation settings (SimSetting)
   - Optionally refer to recommended cases from ExperienceLibrary

3. **Select SA Method**
   - Choose from supported methods based on research objectives
   - Specify Quantity of Interest (QoI) and sample size

4. **Execute Analysis**
   - Run the SA pipeline through SimulationService
   - Monitor progress via web interface

5. **View Results**
   - Review sensitivity indices and convergence metrics
   - Compare results with observed data and visualize outputs

## Installation

### Prerequisites
- Java 8+
- Node.js 12+
- MongoDB 4.0+
- 4GB+ RAM
- 20GB+ Storage