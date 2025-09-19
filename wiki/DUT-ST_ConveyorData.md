# ST_ConveyorData

*Last updated: 2025-09-19 08:05:58*

## Overview

- **Type**: STRUCT
- **File**: `PLC/DUTs/ST_ConveyorData.TcDUT`
- **Author**: Demo System
- **Version**: 1.0

## Members
| Name | Type | Default | Comment |
|------|------|---------|---------|
| `Author` | Demo System
	// Version | - | - |
| `bRunning` | BOOL | - | Conveyor is currently running |
| `bFault` | BOOL | - | Fault condition present |
| `bReady` | BOOL | - | Ready for operation |
| `nSpeed` | INT | - | Current speed percentage (0-100) |
| `nSpeedSetpoint` | INT | - | Desired speed percentage |
| `nStartCount` | UDINT | - | Number of times started |
| `tRunTime` | TIME | - | Total running time |
| `tLastStartTime` | TIME | - | Time of last start |
| `sConveyorName` | STRING(50) | - | Conveyor identification name |
| `nMaxSpeed` | INT | 100 | Maximum allowed speed |
| `nMinSpeed` | INT | 10 | Minimum running speed |
| `tMaintenanceDue` | TIME | - | Time until maintenance due |
| `nMaintenanceCycles` | UDINT | - | Cycles until maintenance |
| `sLastMaintenance` | STRING(20) | - | Last maintenance date |
| `rAvgCurrent` | REAL | - | Average motor current |
| `rMaxCurrent` | REAL | - | Peak motor current |
| `nFaultCount` | UDINT | - | Total fault occurrences |
| `sLastFault` | STRING(100) | - | Description of last fault |

## Comments

- Conveyor Data Structure
- Contains all relevant data for a conveyor system
- Author: Demo System
- Version: 1.0
- Status information
- Conveyor is currently running
- Fault condition present
- Ready for operation
- Speed and control
- Current speed percentage (0-100)
- Desired speed percentage
- Operational data
- Number of times started
- Total running time
- Time of last start
- Configuration
- Conveyor identification name
- Maximum allowed speed
- Minimum running speed
- Maintenance data
- Time until maintenance due
- Cycles until maintenance
- Last maintenance date
- Diagnostic information
- Average motor current
- Peak motor current
- Total fault occurrences
- Description of last fault

---
*[Back to Data Types Overview](Data-Types.md)*