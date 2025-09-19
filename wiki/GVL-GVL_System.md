# GVL_System

*Last updated: 2025-09-19 07:11:12*

## Overview

- **File**: `PLC/GVLs/GVL_System.TcGVL`
- **Description**: System-wide variables for demo application

## Variables

| Name | Type | Default | Comment |
|------|------|---------|---------|
| `Purpose` | System-wide variables for demo application
	// Author | - | - |
| `Date` | 2024
	// | - | - |
| `bSystemRunning` | BOOL | FALSE | Overall system running status |
| `bSystemInitialized` | BOOL | FALSE | System initialization complete |
| `bEmergencyActive` | BOOL | FALSE | Emergency stop active |
| `sSystemStatus` | STRING(255) | - | System status message |
| `nCycleCount` | UDINT | 0 | PLC cycle counter |
| `nErrorCount` | UDINT | 0 | Total error count |
| `nWarningCount` | UDINT | 0 | Total warning count |
| `tSystemUptime` | TIME | - | System uptime |
| `tLastCycleTime` | TIME | - | Last cycle execution time |
| `tMaxCycleTime` | TIME | - | Maximum cycle time recorded |
| `sApplicationName` | STRING(50) | 'Demo TwinCAT GitHub Integration' | - |
| `sVersion` | STRING(20) | '1.0.0' | - |
| `sAuthor` | STRING(50) | 'Demo System' | - |
| `sBuildDate` | STRING(20) | '2024-01-01' | HMI Interface Variables |
| `bHMI_AutoMode` | BOOL | TRUE | HMI Auto mode selection |
| `bHMI_ManualMode` | BOOL | FALSE | HMI Manual mode selection |
| `bHMI_StartSystem` | BOOL | FALSE | HMI Start system command |
| `bHMI_StopSystem` | BOOL | FALSE | HMI Stop system command |
| `bHMI_ResetAlarms` | BOOL | FALSE | HMI Reset alarms command |
| `stSystemDiag` | ST_SystemDiagnostics | - | System diagnostics structure |
| `arAlarmHistory` | ARRAY[1..10] OF STRING(100) | - | Alarm history buffer |
| `nAlarmHistoryIndex` | INT | 1 | Current alarm history index |
| `bHMI_Connected` | BOOL | FALSE | HMI connection status |
| `bSCADA_Connected` | BOOL | FALSE | SCADA connection status |
| `nCommErrors` | UDINT | 0 | Communication error count |
| `ST_SystemDiagnostics` | STRUCT
		// CPU Usage and Performance
		rCPU_Usage | - | - |
| `rMemory_Usage` | REAL | - | Memory usage percentage |
| `nTask_Overruns` | UDINT | - | Task overrun count |
| `rCPU_Temperature` | REAL | - | CPU temperature (°C) |
| `rSystem_Temperature` | REAL | - | System temperature (°C) |
| `bTemperature_Warning` | BOOL | - | Temperature warning flag |
| `nNetworkRx_Packets` | UDINT | - | Received network packets |
| `nNetworkTx_Packets` | UDINT | - | Transmitted network packets |
| `nNetwork_Errors` | UDINT | - | Network error count |
| `bIO_Status_OK` | BOOL | TRUE | I/O system status |
| `nIO_Modules_Active` | INT | - | Number of active I/O modules |
| `nIO_Modules_Fault` | INT | - | Number of faulty I/O modules |

## Comments

- =====================================================
- Global Variable List - System Variables
- Purpose: System-wide variables for demo application
- Author: Demo System
- Date: 2024
- =====================================================
- System Status
- Overall system running status
- System initialization complete
- Emergency stop active
- System status message
- System Counters
- PLC cycle counter
- Total error count
- Total warning count
- System Timing
- System uptime
- Last cycle execution time
- Maximum cycle time recorded
- Version Information
- HMI Interface Variables
- HMI Auto mode selection
- HMI Manual mode selection
- HMI Start system command
- HMI Stop system command
- HMI Reset alarms command
- Diagnostic Variables
- System diagnostics structure
- Alarm history buffer
- Current alarm history index
- Communication Status
- HMI connection status
- SCADA connection status
- Communication error count
- Additional diagnostic structure
- CPU Usage and Performance
- CPU usage percentage
- Memory usage percentage
- Task overrun count
- Temperature Monitoring
- CPU temperature (°C)
- System temperature (°C)
- Temperature warning flag
- Network Statistics
- Received network packets
- Transmitted network packets
- Network error count
- I/O Status
- I/O system status
- Number of active I/O modules
- Number of faulty I/O modules

---
*[Back to Global Variables Overview](Global-Variables.md)*