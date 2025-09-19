# Architecture Overview

*Last updated: 2025-09-19 07:11:12*

## System Architecture

This document provides an overview of the Demo TwinCAT Project system architecture, including the main components and their relationships.

## Program Organization Units (POUs)

### FB_MotorControl
- **Type**: None
- **File**: `PLC/POUs/FB_MotorControl.TcPOU`
- **Description**: No description available
- **Author**: 
- **Variables**: 32 declared
- **Comments**: 
  - Basic motor control inputs
  - Enable motor operation
  - Start motor command

### FB_ConveyorControl
- **Type**: None
- **File**: `PLC/POUs/FB_ConveyorControl.TcPOU`
- **Description**: No description available
- **Author**: 
- **Variables**: 21 declared
- **Comments**: 
  - Control inputs
  - Start conveyor command
  - Reset faults and errors

### MAIN
- **Type**: None
- **File**: `PLC/POUs/MAIN.TcPOU`
- **Description**: No description available
- **Author**: Demo System
- **Variables**: 10 declared
- **Comments**: 
  - Demo Application Main Program
  - This program demonstrates a simple conveyor control system
  - Author: Demo System


## Data Types

### ST_ConveyorData
- **Type**: STRUCT
- **File**: `PLC/DUTs/ST_ConveyorData.TcDUT`
- **Description**: No description available
- **Members**: 19

### E_MotorState
- **Type**: STRUCT
- **File**: `PLC/DUTs/E_MotorState.TcDUT`
- **Description**: No description available
- **Members**: 0


## Global Variables

### GVL_System
- **File**: `PLC/GVLs/GVL_System.TcGVL`
- **Description**: System-wide variables for demo application
- **Variables**: 39


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