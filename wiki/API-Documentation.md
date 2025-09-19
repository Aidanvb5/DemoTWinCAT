# API Documentation

*Last updated: 2025-09-19 07:11:12*

This page provides API documentation for the Demo TwinCAT Project project.

## Function Blocks


## Functions


## Data Types Reference

### ST_ConveyorData

**Type**: STRUCT  
**Description**: No description available

| Member | Type | Description |
|--------|------|-------------|
| `Author` | Demo System
	// Version | - |
| `bRunning` | BOOL | Conveyor is currently running |
| `bFault` | BOOL | Fault condition present |
| `bReady` | BOOL | Ready for operation |
| `nSpeed` | INT | Current speed percentage (0-100) |
| `nSpeedSetpoint` | INT | Desired speed percentage |
| `nStartCount` | UDINT | Number of times started |
| `tRunTime` | TIME | Total running time |
| `tLastStartTime` | TIME | Time of last start |
| `sConveyorName` | STRING(50) | Conveyor identification name |
| `nMaxSpeed` | INT | Maximum allowed speed |
| `nMinSpeed` | INT | Minimum running speed |
| `tMaintenanceDue` | TIME | Time until maintenance due |
| `nMaintenanceCycles` | UDINT | Cycles until maintenance |
| `sLastMaintenance` | STRING(20) | Last maintenance date |
| `rAvgCurrent` | REAL | Average motor current |
| `rMaxCurrent` | REAL | Peak motor current |
| `nFaultCount` | UDINT | Total fault occurrences |
| `sLastFault` | STRING(100) | Description of last fault |

---

### E_MotorState

**Type**: STRUCT  
**Description**: No description available


---

