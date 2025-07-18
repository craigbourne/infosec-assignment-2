# Attack Tree Visualiser

> Visual risk assessment tool for business decision-making

The Attack Tree Visualiser is a Python application that transforms attack trees into quantified business risk assessments, allowing business stakeholders to visualise security threats through monetary impact. This was developed to address Pampered Pets' digitalisation concerns following an initial risk identification report submitted for Assignment 1.

## Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Assignment 1 Validation and Business Impact](#assignment-1-validation-and-business-impact)
- [Testing and Validation](#testing-and-validation)
- [References](#references)

## Overview
The Attack Tree Visualiser serves as an "unconventional executive summary" for risk assessment, transforming attack scenarios into visual representations with monetary impacts. Following the initial Assignment 1 risk identification report, this application addresses the request from Pampered Pets' shop manager for a more accessible way to understand the implications of Pampered Pets' digitalisation.

**The Problem**: Traditional risk assessments can fail to communicate business impact, relying on technical severity ratings that do not reflect real business risk exposure. As Spring et al. (2021) demonstrate, "CVSS is designed to identify the technical severity of a vulnerability" whilst "what people seem to want to know, instead, is the risk a vulnerability or flaw poses to them" Hubbard (2020) found that popular methods employ "high, medium, low evaluation of likelihood and impact" without proper quantitative foundation.

**The Solution**: The application converts the attack trees and risk scenarios from Assignment 1 into quantified business impacts, enabling data-driven digitalisation decisions through visual analysis.

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

[NetworkX](https://networkx.org/) provides graph algorithms for attack tree representation (NetworkX Developers, 2024), [Matplotlib](https://matplotlib.org/) generates static, animated and interactive diagrams (Matplotlib Development Team et al., 2024) and [NumPy](https://numpy.org/) provides numerical operations for risk calculations (NumPy Developers, 2024).

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

![Terminal prompts](images/2-terminal-prompts.jpg)

3. **Risk breakdown analysis**: System provides detailed breakdown showing:
   - Individual attack costs
   - Sum of all individual attacks
   - Calculated overall risk using OR/AND gate logic
   - Explanation of logic differences

4. **Visual representation**: Attack tree diagram displays with:
   - Colour-coded nodes (red for attacks, blue for logic gates)
   - Monetary values prominently shown on nodes
   - Total risk exposure in summary box
   - Clear hierarchical structure

![Attack tree example](images/3-attacktree-diagram.jpg)

5. **Business recommendations**: Analysis provides contextual guidance based on risk differentials and Assignment 1 findings

**Example: Payment System Analysis**
When selecting option 1 (Payment System Current), the application guides users through risk value input for threats including:
- Malware installation on POS systems
- Physical access to payment terminals
- WiFi interception of transaction data
- Credential theft from unsecured systems

![Menu choice 1](images/4-choice-1.jpg)

**Attack Tree Logic Implementation**
The application implements attack tree logic following Tarandach & Coles (2020):
- **OR gates represent alternative attack paths**: Attackers will choose the most feasible route, so the system takes the maximum risk value from child nodes
- **AND gates represent required attack sequences**: All steps must succeed for the attack to work, so risks are cumulative (summed)
- **Leaf nodes**: Individual attack methods with business impact values input by the user
- **Overall risk calculation**: Reflects realistic business exposure rather than theoretical maximum, using transparent logical aggregation

This methodology addresses the "Risk = Threat Capability × Vulnerability × Impact" framework established in FAIR model literature, focusing on impact assessment with transparent logical aggregation.

## File Structure
![File Structure](images/file-structure.jpg)
