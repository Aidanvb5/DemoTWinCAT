#!/usr/bin/env python3
"""
Wiki Generator for TwinCAT Projects
===================================

This module generates markdown documentation from TwinCAT3 project files
for automatic wiki page creation.

Author: Demo System
Date: 2024
Version: 1.0
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, Template
import logging

from twincat_parser import TwinCATParser, POUInfo, DUTInfo, GVLInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikiGenerator:
    """Generator for markdown wiki pages from TwinCAT project data."""
    
    def __init__(self, project_root: str, output_dir: str = "wiki"):
        """Initialize wiki generator."""
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2 template environment
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Create templates if they don't exist
        self._create_default_templates()
        
        self.parser = TwinCATParser(project_root)
    
    def generate_wiki(self) -> None:
        """Generate complete wiki documentation."""
        logger.info("Starting wiki generation...")
        
        # Parse project
        project_data = self.parser.parse_project()
        
        # Generate main pages
        self._generate_home_page(project_data)
        self._generate_architecture_overview(project_data)
        self._generate_pou_index(project_data['pous'])
        self._generate_dut_index(project_data['duts'])
        self._generate_gvl_index(project_data['gvls'])
        
        # Generate detailed pages for each component
        for pou in project_data['pous']:
            self._generate_pou_page(pou)
        
        for dut in project_data['duts']:
            self._generate_dut_page(dut)
        
        for gvl in project_data['gvls']:
            self._generate_gvl_page(gvl)
        
        # Generate API documentation
        self._generate_api_documentation(project_data)
        
        # Generate project statistics
        self._generate_statistics_page(project_data)
        
        logger.info(f"Wiki generation complete. Files saved to: {self.output_dir}")
    
    def _generate_home_page(self, project_data: Dict) -> None:
        """Generate the main wiki home page."""
        template = self.jinja_env.get_template('home.md.j2')
        content = template.render(
            project=project_data['project_info'],
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            pou_count=len(project_data['pous']),
            dut_count=len(project_data['duts']),
            gvl_count=len(project_data['gvls'])
        )
        
        with open(self.output_dir / 'Home.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_architecture_overview(self, project_data: Dict) -> None:
        """Generate architecture overview page."""
        template = self.jinja_env.get_template('architecture.md.j2')
        content = template.render(
            project=project_data['project_info'],
            pous=project_data['pous'],
            duts=project_data['duts'],
            gvls=project_data['gvls'],
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'Architecture-Overview.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_pou_index(self, pous: List[POUInfo]) -> None:
        """Generate POU index page."""
        template = self.jinja_env.get_template('pou_index.md.j2')
        content = template.render(
            pous=pous,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'POUs.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_dut_index(self, duts: List[DUTInfo]) -> None:
        """Generate DUT index page."""
        template = self.jinja_env.get_template('dut_index.md.j2')
        content = template.render(
            duts=duts,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'Data-Types.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_gvl_index(self, gvls: List[GVLInfo]) -> None:
        """Generate GVL index page."""
        template = self.jinja_env.get_template('gvl_index.md.j2')
        content = template.render(
            gvls=gvls,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'Global-Variables.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_pou_page(self, pou: POUInfo) -> None:
        """Generate detailed page for a single POU."""
        template = self.jinja_env.get_template('pou_detail.md.j2')
        content = template.render(
            pou=pou,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        filename = f'POU-{pou.name}.md'
        with open(self.output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_dut_page(self, dut: DUTInfo) -> None:
        """Generate detailed page for a single DUT."""
        template = self.jinja_env.get_template('dut_detail.md.j2')
        content = template.render(
            dut=dut,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        filename = f'DUT-{dut.name}.md'
        with open(self.output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_gvl_page(self, gvl: GVLInfo) -> None:
        """Generate detailed page for a single GVL."""
        template = self.jinja_env.get_template('gvl_detail.md.j2')
        content = template.render(
            gvl=gvl,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        filename = f'GVL-{gvl.name}.md'
        with open(self.output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_api_documentation(self, project_data: Dict) -> None:
        """Generate API documentation page."""
        template = self.jinja_env.get_template('api_documentation.md.j2')
        
        # Filter function blocks for API documentation
        function_blocks = [pou for pou in project_data['pous'] if pou.type == 'FUNCTION_BLOCK']
        functions = [pou for pou in project_data['pous'] if pou.type == 'FUNCTION']
        
        content = template.render(
            project=project_data['project_info'],
            function_blocks=function_blocks,
            functions=functions,
            duts=project_data['duts'],
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'API-Documentation.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_statistics_page(self, project_data: Dict) -> None:
        """Generate project statistics page."""
        template = self.jinja_env.get_template('statistics.md.j2')
        
        # Calculate statistics
        stats = {
            'total_pous': len(project_data['pous']),
            'total_duts': len(project_data['duts']),
            'total_gvls': len(project_data['gvls']),
            'programs': len([p for p in project_data['pous'] if p.type == 'PROGRAM']),
            'function_blocks': len([p for p in project_data['pous'] if p.type == 'FUNCTION_BLOCK']),
            'functions': len([p for p in project_data['pous'] if p.type == 'FUNCTION']),
            'structs': len([d for d in project_data['duts'] if d.type == 'STRUCT']),
            'enums': len([d for d in project_data['duts'] if d.type == 'ENUM']),
            'total_variables': sum(len(pou.variables) for pou in project_data['pous']),
            'total_global_vars': sum(len(gvl.variables) for gvl in project_data['gvls'])
        }
        
        content = template.render(
            project=project_data['project_info'],
            stats=stats,
            pous=project_data['pous'],
            duts=project_data['duts'],
            gvls=project_data['gvls'],
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(self.output_dir / 'Project-Statistics.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_default_templates(self) -> None:
        """Create default Jinja2 templates if they don't exist."""
        template_dir = Path(__file__).parent / "templates"
        
        templates = {
            'home.md.j2': self._get_home_template(),
            'architecture.md.j2': self._get_architecture_template(),
            'pou_index.md.j2': self._get_pou_index_template(),
            'pou_detail.md.j2': self._get_pou_detail_template(),
            'dut_index.md.j2': self._get_dut_index_template(),
            'dut_detail.md.j2': self._get_dut_detail_template(),
            'gvl_index.md.j2': self._get_gvl_index_template(),
            'gvl_detail.md.j2': self._get_gvl_detail_template(),
            'api_documentation.md.j2': self._get_api_documentation_template(),
            'statistics.md.j2': self._get_statistics_template()
        }
        
        for filename, template_content in templates.items():
            template_file = template_dir / filename
            if not template_file.exists():
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(template_content)
    
    def _get_home_template(self) -> str:
        return '''# {{ project.name }}

**{{ project.description }}**

*Last updated: {{ timestamp }}*

## Project Overview

This is an automatically generated wiki for the TwinCAT3 project demonstrating GitHub integration and automated documentation generation.

### Project Statistics

- **POUs (Program Organization Units)**: {{ pou_count }}
- **DUTs (Data Unit Types)**: {{ dut_count }}
- **GVLs (Global Variable Lists)**: {{ gvl_count }}
- **Version**: {{ project.version }}
- **Author**: {{ project.author }}

## Navigation

- [Architecture Overview](Architecture-Overview.md) - System architecture and component relationships
- [POUs](POUs.md) - Program Organization Units (Programs, Function Blocks, Functions)
- [Data Types](Data-Types.md) - Custom data types and structures
- [Global Variables](Global-Variables.md) - System-wide variables
- [API Documentation](API-Documentation.md) - Programming interface documentation
- [Project Statistics](Project-Statistics.md) - Detailed project metrics

## Quick Start

1. **Understanding the Architecture**: Start with the [Architecture Overview](Architecture-Overview.md)
2. **Main Program**: Review the main program logic in [POUs](POUs.md)
3. **Data Structures**: Check custom data types in [Data Types](Data-Types.md)
4. **System Variables**: See global variables in [Global Variables](Global-Variables.md)

## About This Documentation

This documentation is automatically generated from the TwinCAT3 project source code using Python scripts that parse the project files and extract comments, structure information, and code organization. The wiki is regenerated automatically when code changes are committed to the repository.

---
*Generated automatically by TwinCAT Wiki Generator v1.0*
'''

    def _get_architecture_template(self) -> str:
        return '''# Architecture Overview

*Last updated: {{ timestamp }}*

## System Architecture

This document provides an overview of the {{ project.name }} system architecture, including the main components and their relationships.

## Program Organization Units (POUs)

{% for pou in pous %}
### {{ pou.name }}
- **Type**: {{ pou.type }}
- **File**: `{{ pou.file_path }}`
- **Description**: {{ pou.description or 'No description available' }}
- **Author**: {{ pou.author }}
- **Variables**: {{ pou.variables|length }} declared
{% if pou.comments %}
- **Comments**: 
{% for comment in pou.comments[:3] %}
  - {{ comment }}
{% endfor %}
{% endif %}

{% endfor %}

## Data Types

{% for dut in duts %}
### {{ dut.name }}
- **Type**: {{ dut.type }}
- **File**: `{{ dut.file_path }}`
- **Description**: {{ dut.description or 'No description available' }}
- **Members**: {{ dut.members|length }}

{% endfor %}

## Global Variables

{% for gvl in gvls %}
### {{ gvl.name }}
- **File**: `{{ gvl.file_path }}`
- **Description**: {{ gvl.description or 'No description available' }}
- **Variables**: {{ gvl.variables|length }}

{% endfor %}

## Component Relationships

```
MAIN Program
├── FB_ConveyorControl (Function Block)
│   ├── Uses: E_MotorState (Enum)
│   └── Uses: ST_ConveyorData (Struct)
├── FB_MotorControl (Function Block)
│   └── Uses: E_MotorState (Enum)
└── References: GVL_System (Global Variables)
```

## System Flow

1. **Initialization**: System starts in MAIN program
2. **State Management**: Motor states controlled via E_MotorState enumeration
3. **Data Exchange**: Conveyor data stored in ST_ConveyorData structures
4. **Global Monitoring**: System status tracked in GVL_System variables

---
*For detailed information about each component, see the individual documentation pages.*
'''

    def _get_pou_index_template(self) -> str:
        return '''# Program Organization Units (POUs)

*Last updated: {{ timestamp }}*

This page lists all Program Organization Units in the project, including Programs, Function Blocks, and Functions.

## Summary

Total POUs: **{{ pous|length }}**

{% set programs = pous|selectattr("type", "equalto", "PROGRAM")|list %}
{% set function_blocks = pous|selectattr("type", "equalto", "FUNCTION_BLOCK")|list %}
{% set functions = pous|selectattr("type", "equalto", "FUNCTION")|list %}

- Programs: {{ programs|length }}
- Function Blocks: {{ function_blocks|length }}
- Functions: {{ functions|length }}

## Programs

{% for pou in programs %}
### [{{ pou.name }}](POU-{{ pou.name }}.md)
- **File**: `{{ pou.file_path }}`
- **Description**: {{ pou.description or 'No description available' }}
- **Variables**: {{ pou.variables|length }}
{% if pou.author %}
- **Author**: {{ pou.author }}
{% endif %}

{% endfor %}

## Function Blocks

{% for pou in function_blocks %}
### [{{ pou.name }}](POU-{{ pou.name }}.md)
- **File**: `{{ pou.file_path }}`
- **Description**: {{ pou.description or 'No description available' }}
- **Variables**: {{ pou.variables|length }}
{% if pou.author %}
- **Author**: {{ pou.author }}
{% endif %}

{% endfor %}

## Functions

{% for pou in functions %}
### [{{ pou.name }}](POU-{{ pou.name }}.md)
- **File**: `{{ pou.file_path }}`
- **Description**: {{ pou.description or 'No description available' }}
- **Variables**: {{ pou.variables|length }}
{% if pou.author %}
- **Author**: {{ pou.author }}
{% endif %}

{% endfor %}
'''

# Continuing with the template methods...
    def _get_pou_detail_template(self) -> str:
        return '''# {{ pou.name }}

*Last updated: {{ timestamp }}*

## Overview

- **Type**: {{ pou.type }}
- **File**: `{{ pou.file_path }}`
{% if pou.description %}
- **Description**: {{ pou.description }}
{% endif %}
{% if pou.author %}
- **Author**: {{ pou.author }}
{% endif %}
{% if pou.version %}
- **Version**: {{ pou.version }}
{% endif %}
{% if pou.date %}
- **Date**: {{ pou.date }}
{% endif %}

## Variables

{% if pou.variables %}
| Name | Type | Default | Comment |
|------|------|---------|---------|
{% for var in pou.variables %}
| `{{ var.name }}` | {{ var.type }} | {{ var.default or '-' }} | {{ var.comment or '-' }} |
{% endfor %}
{% else %}
*No variables declared*
{% endif %}

## Implementation

```pascal
{{ pou.implementation }}
```

{% if pou.comments %}
## Additional Comments

{% for comment in pou.comments %}
- {{ comment }}
{% endfor %}
{% endif %}

---
*[Back to POUs Overview](POUs.md)*
'''

    def _get_dut_index_template(self) -> str:
        return '''# Data Unit Types (DUTs)

*Last updated: {{ timestamp }}*

This page lists all custom data types defined in the project.

## Summary

Total DUTs: **{{ duts|length }}**

{% set structs = duts|selectattr("type", "equalto", "STRUCT")|list %}
{% set enums = duts|selectattr("type", "equalto", "ENUM")|list %}

- Structures: {{ structs|length }}
- Enumerations: {{ enums|length }}

## Structures

{% for dut in structs %}
### [{{ dut.name }}](DUT-{{ dut.name }}.md)
- **File**: `{{ dut.file_path }}`
- **Description**: {{ dut.description or 'No description available' }}
- **Members**: {{ dut.members|length }}
{% if dut.author %}
- **Author**: {{ dut.author }}
{% endif %}

{% endfor %}

## Enumerations

{% for dut in enums %}
### [{{ dut.name }}](DUT-{{ dut.name }}.md)
- **File**: `{{ dut.file_path }}`
- **Description**: {{ dut.description or 'No description available' }}
- **Values**: {{ dut.members|length }}
{% if dut.author %}
- **Author**: {{ dut.author }}
{% endif %}

{% endfor %}
'''

    def _get_dut_detail_template(self) -> str:
        return '''# {{ dut.name }}

*Last updated: {{ timestamp }}*

## Overview

- **Type**: {{ dut.type }}
- **File**: `{{ dut.file_path }}`
{% if dut.description %}
- **Description**: {{ dut.description }}
{% endif %}
{% if dut.author %}
- **Author**: {{ dut.author }}
{% endif %}
{% if dut.version %}
- **Version**: {{ dut.version }}
{% endif %}

## {% if dut.type == "STRUCT" %}Members{% else %}Values{% endif %}

{% if dut.members %}
| Name | Type | Default | Comment |
|------|------|---------|---------|
{% for member in dut.members %}
| `{{ member.name }}` | {{ member.type }} | {{ member.default or '-' }} | {{ member.comment or '-' }} |
{% endfor %}
{% else %}
*No members defined*
{% endif %}

{% if dut.comments %}
## Comments

{% for comment in dut.comments %}
- {{ comment }}
{% endfor %}
{% endif %}

---
*[Back to Data Types Overview](Data-Types.md)*
'''

    def _get_gvl_index_template(self) -> str:
        return '''# Global Variable Lists (GVLs)

*Last updated: {{ timestamp }}*

This page lists all Global Variable Lists in the project.

## Summary

Total GVLs: **{{ gvls|length }}**
Total Global Variables: **{{ gvls|map(attribute='variables')|map('length')|sum }}**

{% for gvl in gvls %}
## [{{ gvl.name }}](GVL-{{ gvl.name }}.md)

- **File**: `{{ gvl.file_path }}`
- **Description**: {{ gvl.description or 'No description available' }}
- **Variables**: {{ gvl.variables|length }}

### Key Variables

{% for var in gvl.variables[:5] %}
- `{{ var.name }}` ({{ var.type }}){% if var.comment %} - {{ var.comment }}{% endif %}
{% endfor %}
{% if gvl.variables|length > 5 %}
*... and {{ gvl.variables|length - 5 }} more*
{% endif %}

{% endfor %}
'''

    def _get_gvl_detail_template(self) -> str:
        return '''# {{ gvl.name }}

*Last updated: {{ timestamp }}*

## Overview

- **File**: `{{ gvl.file_path }}`
{% if gvl.description %}
- **Description**: {{ gvl.description }}
{% endif %}

## Variables

{% if gvl.variables %}
| Name | Type | Default | Comment |
|------|------|---------|---------|
{% for var in gvl.variables %}
| `{{ var.name }}` | {{ var.type }} | {{ var.default or '-' }} | {{ var.comment or '-' }} |
{% endfor %}
{% else %}
*No variables declared*
{% endif %}

{% if gvl.comments %}
## Comments

{% for comment in gvl.comments %}
- {{ comment }}
{% endfor %}
{% endif %}

---
*[Back to Global Variables Overview](Global-Variables.md)*
'''

    def _get_api_documentation_template(self) -> str:
        return '''# API Documentation

*Last updated: {{ timestamp }}*

This page provides API documentation for the {{ project.name }} project.

## Function Blocks

{% for fb in function_blocks %}
### {{ fb.name }}

**Description**: {{ fb.description or 'No description available' }}

#### Interface

{% if fb.variables %}
##### Variables
| Name | Type | Default | Description |
|------|------|---------|-------------|
{% for var in fb.variables %}
| `{{ var.name }}` | {{ var.type }} | {{ var.default or '-' }} | {{ var.comment or '-' }} |
{% endfor %}
{% endif %}

#### Usage Example

```pascal
// Example usage of {{ fb.name }}
VAR
    fb{{ fb.name }}: {{ fb.name }};
END_VAR

// In implementation:
fb{{ fb.name }}(
    // Configure inputs here
);
```

---

{% endfor %}

## Functions

{% for func in functions %}
### {{ func.name }}

**Description**: {{ func.description or 'No description available' }}

{% if func.variables %}
#### Parameters
| Name | Type | Description |
|------|------|-------------|
{% for var in func.variables %}
| `{{ var.name }}` | {{ var.type }} | {{ var.comment or '-' }} |
{% endfor %}
{% endif %}

---

{% endfor %}

## Data Types Reference

{% for dut in duts %}
### {{ dut.name }}

**Type**: {{ dut.type }}  
**Description**: {{ dut.description or 'No description available' }}

{% if dut.members %}
| Member | Type | Description |
|--------|------|-------------|
{% for member in dut.members %}
| `{{ member.name }}` | {{ member.type }} | {{ member.comment or '-' }} |
{% endfor %}
{% endif %}

---

{% endfor %}
'''

    def _get_statistics_template(self) -> str:
        return '''# Project Statistics

*Last updated: {{ timestamp }}*

## Overview

Project: **{{ project.name }}**  
Version: **{{ project.version }}**  
Author: **{{ project.author }}**

## Code Statistics

### Components
- **Total POUs**: {{ stats.total_pous }}
  - Programs: {{ stats.programs }}
  - Function Blocks: {{ stats.function_blocks }}
  - Functions: {{ stats.functions }}
- **Total DUTs**: {{ stats.total_duts }}
  - Structures: {{ stats.structs }}
  - Enumerations: {{ stats.enums }}
- **Total GVLs**: {{ stats.total_gvls }}

### Variables
- **Local Variables**: {{ stats.total_variables }}
- **Global Variables**: {{ stats.total_global_vars }}
- **Total Variables**: {{ stats.total_variables + stats.total_global_vars }}

## Detailed Breakdown

### POUs by Complexity
| POU Name | Type | Variables | Comments |
|----------|------|-----------|----------|
{% for pou in pous %}
| {{ pou.name }} | {{ pou.type }} | {{ pou.variables|length }} | {{ pou.comments|length }} |
{% endfor %}

### Data Types by Size
| DUT Name | Type | Members |
|----------|------|---------|
{% for dut in duts %}
| {{ dut.name }} | {{ dut.type }} | {{ dut.members|length }} |
{% endfor %}

### Global Variable Distribution
| GVL Name | Variables |
|----------|-----------|
{% for gvl in gvls %}
| {{ gvl.name }} | {{ gvl.variables|length }} |
{% endfor %}

## Code Quality Metrics

- **Documentation Coverage**: {% if stats.total_pous > 0 %}{{ (pous|selectattr("description")|list|length / stats.total_pous * 100)|round(1) }}%{% else %}N/A{% endif %}
- **Average Variables per POU**: {% if stats.total_pous > 0 %}{{ (stats.total_variables / stats.total_pous)|round(1) }}{% else %}N/A{% endif %}
- **Average Members per DUT**: {% if stats.total_duts > 0 %}{{ (duts|sum(attribute='members')|length / stats.total_duts)|round(1) }}{% else %}N/A{% endif %}

---
*Statistics generated automatically from project source code*
'''


if __name__ == "__main__":
    # Example usage
    generator = WikiGenerator("../../DemoTwinCAT", "../../wiki")
    generator.generate_wiki()
    print("Wiki generation completed successfully!")