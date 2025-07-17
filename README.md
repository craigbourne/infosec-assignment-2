# Attack Tree Visualiser

> Interactive risk assessment tool for business decision-making

The Attack Tree Visualiser is a Python application that transforms attack trees into quantified business risk assessments, enabling executives to visualise security threats through monetary impact. This was developed to address Pampered Pets' digitalisation concerns following the initial risk identification report submitted for Assignment 1.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Assignment Context](#assignment-context)
- [Technical Architecture](#technical-architecture)
- [External Libraries](#external-libraries-and-code-attribution)
- [Testing](#testing-and-validation)
- [File Structure](#file-structure)
- [Business Results](#business-applications-and-results)
- [Academic Integrity](#academic-integrity-and-original-work)
- [References](#references)

## Overview

The Attack Tree Visualiser serves as an "unconventional executive summary" for risk assessment, transforming attack scenarios into visual representations with monetary impacts. Following the initial Assignment 1 risk identification report, this tool addresses the request from Pampered Pets' shop manager for a more accessible way to understand the implications of Pampered Pets' digitalisation.

**The Problem**: Traditional risk assessments often fail to communicate business impact, relying on technical severity ratings that don't reflect real business risk exposure. As Spring et al. (2021) demonstrate, "CVSS is designed to identify the technical severity of a vulnerability" whilst "what people seem to want to know, instead, is the risk a vulnerability or flaw poses to them" Hubbard (2020) found that popular methods employ "high, medium, low evaluation of likelihood and impact" without proper quantitative foundation.

**The Solution**: This application converts the attack trees and risk scenarios from Assignment 1 into quantified business impact analyses, enabling data-driven digitalisation decisions through interactive visual risk comparison.

**Methodological Foundation**: Following the Threat Modelling Manifesto framework (Threat Modeling Manifesto Working Group, 2020) and implementing Tarandach & Coles' (2020) attack tree methodology, the application converts abstract security threats into quantified business risks.

## Features

- **Attack Tree Management**: Load JSON attack trees representing current and post-digitalisation business scenarios
- **Interactive Risk Assessment**: Input monetary values for individual attack methods
- **Transparent Risk Aggregation**: OR/AND gate logic providing business-focused risk calculations
- **Scenario Comparison**: Pre/post digitalisation analysis validating Assignment 1 recommendations
- **Executive Visualisation**: Colour-coded diagrams with risk values and business summaries

## Installation

**System Requirements**
- Python 3.9 or higher
- [pip](https://pypi.org/project/pip/) package management
- Modern web browser
- Minimum 4GB RAM for attack tree processing

**Dependencies and Requirements**
The application requires three core Python libraries as specified in requirements.txt:

```bash
networkx>=3.0 
matplotlib>=3.7.0
numpy>=1.24.0
```

NetworkX provides graph algorithms for attack tree representation (NetworkX Developers, 2024), Matplotlib generates static, animated and interactive diagrams (Matplotlib Development Team et al., 2024) and NumPy provides numerical operations for risk calculations (NumPy Developers, 2024).

**Installation Steps**
```bash
# Verify Python version
python --version

# Clone repository
git clone https://github.com/craigbourne/infosec-assignment-2.git
cd infosec-assignment-2

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# or on Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

**Launch Application**
```bash
python src/attack_tree.py
```

**Menu Options**

The application provides six analysis scenarios based on the original Assignment 1 risk assessment:

![Menu with six options](images/1-six-options.jpg)

1. **Payment System Risks (Current)** - Pre-digitalisation baseline outlined in Assignment 1
2. **Supply Chain Risks (Current)** - Current local supplier model with 10-minute proximity advantage
3. **Payment System Risks (Digitalised)** - Post-implementation risks following digitalisation recommendations
4. **Supply Chain Risks (Digitalised)** - Demonstrates why local suppliers were recommended over international 24% cost savings
5. **Payment Systems Comparison** - Pre/post-digitalisation supporting the 50% growth opportunity analysis
6. **Supply Chains Comparison** - Local vs international supplier analysis validating Assignment 1 recommendations

**Risk Input Process**
1. Select analysis scenario from the menu
2. Users are then guided through entering costs for each attack method:
   - Prompts appear for each leaf node in the attack tree
   - Current values displayed, can be skipped or updated
   - Input validation ensures positive numbers or zero
