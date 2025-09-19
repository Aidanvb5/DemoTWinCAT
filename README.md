# DemoTWinCAT

**Demo TwinCAT3 Project showcasing GitHub Integration and Automated Documentation**

This project demonstrates how to integrate TwinCAT3 industrial automation code with GitHub's collaboration features and automated documentation generation.

![TwinCAT3](https://img.shields.io/badge/TwinCAT3-v3.5.13-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Documentation](https://img.shields.io/badge/Documentation-Auto%20Generated-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Goals

- **Demonstrate GitHub Integration**: Show how TwinCAT3 projects can be effectively managed in GitHub
- **Automated Documentation**: Generate comprehensive wiki documentation from code comments and structure
- **Best Practices**: Illustrate modern DevOps practices for industrial automation projects
- **Collaboration**: Enable team collaboration on PLC/automation projects using Git workflows

## 🏗️ Project Structure

```
DemoTWinCAT/
├── DemoTwinCAT/              # Main TwinCAT3 project
│   ├── PLC/                  # PLC project components
│   │   ├── POUs/            # Program Organization Units
│   │   │   ├── MAIN.TcPOU           # Main program
│   │   │   ├── FB_ConveyorControl.TcPOU  # Conveyor control function block
│   │   │   └── FB_MotorControl.TcPOU     # Motor control function block
│   │   ├── DUTs/            # Data Unit Types
│   │   │   ├── E_MotorState.TcDUT       # Motor state enumeration
│   │   │   └── ST_ConveyorData.TcDUT    # Conveyor data structure
│   │   ├── GVLs/            # Global Variable Lists
│   │   │   └── GVL_System.TcGVL         # System global variables
│   │   └── VISUs/           # Visualizations
│   ├── System/              # System configuration
│   └── DemoTwinCAT.tsproj   # TwinCAT project file
├── scripts/                 # Python automation scripts
│   ├── wiki_generator/      # Wiki generation modules
│   │   ├── twincat_parser.py    # TwinCAT project parser
│   │   ├── wiki_generator.py    # Wiki content generator
│   │   └── templates/           # Jinja2 templates for documentation
│   └── generate_wiki.py     # Main wiki generation script
├── wiki/                    # Generated documentation (auto-updated)
├── .github/                 # GitHub workflows and templates
│   └── workflows/
│       └── generate-wiki.yml    # Auto-documentation workflow
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Features

### TwinCAT3 Demo Application
- **Conveyor Control System**: Realistic industrial automation example
- **State Machine Logic**: Proper state management for motor control
- **Function Blocks**: Reusable, parameterizable control logic
- **Data Structures**: Well-defined data types for system communication
- **Global Variables**: System-wide monitoring and control variables
- **Comprehensive Comments**: Detailed documentation in code

### Automated Documentation
- **Python-based Parser**: Extracts information from TwinCAT XML files
- **Markdown Generation**: Creates structured wiki pages automatically  
- **Component Documentation**: Detailed pages for each POU, DUT, and GVL
- **API Documentation**: Function interface documentation
- **Architecture Overview**: System structure and relationships
- **Project Statistics**: Code metrics and quality indicators

### GitHub Integration
- **Automated Workflows**: Generate documentation on code changes
- **Release Management**: Create releases with documentation packages
- **Issue Templates**: Structured templates for bug reports and features
- **Branch Protection**: Enforce code review and testing workflows
- **Pages Deployment**: Host documentation on GitHub Pages

## 📖 Generated Documentation

The project automatically generates comprehensive documentation available in the [Wiki](wiki/) folder:

- **[Home](wiki/Home.md)** - Project overview and navigation
- **[Architecture Overview](wiki/Architecture-Overview.md)** - System architecture
- **[POUs](wiki/POUs.md)** - Program Organization Units index
- **[Data Types](wiki/Data-Types.md)** - Custom data types and structures
- **[Global Variables](wiki/Global-Variables.md)** - System-wide variables
- **[API Documentation](wiki/API-Documentation.md)** - Programming interfaces
- **[Project Statistics](wiki/Project-Statistics.md)** - Code metrics

### Component Documentation
Each major component has detailed documentation:
- **[MAIN Program](wiki/POU-MAIN.md)** - Main application logic
- **[FB_ConveyorControl](wiki/POU-FB_ConveyorControl.md)** - Conveyor control function block
- **[FB_MotorControl](wiki/POU-FB_MotorControl.md)** - Advanced motor control
- **[E_MotorState](wiki/DUT-E_MotorState.md)** - Motor state enumeration
- **[ST_ConveyorData](wiki/DUT-ST_ConveyorData.md)** - Conveyor data structure
- **[GVL_System](wiki/GVL-GVL_System.md)** - System global variables

## 🛠️ Getting Started

### Prerequisites
- **TwinCAT3** (v3.5.13 or later) for opening and editing the project
- **Python 3.11+** for running documentation scripts
- **Git** for version control

### Opening the TwinCAT Project
1. Clone this repository:
   ```bash
   git clone https://github.com/Aidanvb5/DemoTWinCAT.git
   cd DemoTWinCAT
   ```

2. Open `DemoTwinCAT.sln` in TwinCAT3 XAE (eXtended Automation Engineering)

3. Build and download the project to your target system

### Generating Documentation Locally
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate wiki documentation:
   ```bash
   python scripts/generate_wiki.py
   ```

3. Documentation will be generated in the `wiki/` folder

### Advanced Usage
```bash
# Generate with verbose output
python scripts/generate_wiki.py --verbose

# Specify custom directories
python scripts/generate_wiki.py --project-dir MyProject --output-dir docs

# Dry run to test parsing
python scripts/generate_wiki.py --dry-run
```

## 🤖 Automation Features

### GitHub Actions Workflows
The project includes automated workflows that trigger on:
- **Code Changes**: Auto-generate documentation when TwinCAT files change
- **Pull Requests**: Validate documentation generation on PRs
- **Manual Triggers**: Force documentation updates when needed
- **Releases**: Package documentation with release artifacts

### Documentation Updates
- **Automatic Detection**: Only regenerates when source files change
- **Smart Commits**: Descriptive commit messages with project statistics
- **Artifact Storage**: Documentation stored as workflow artifacts
- **Pages Deployment**: Optional deployment to GitHub Pages

## 📊 Project Statistics

The current project contains:
- **3 POUs** (1 Program, 2 Function Blocks)
- **2 DUTs** (1 Structure, 1 Enumeration)  
- **1 GVL** with comprehensive system variables
- **50+ documented variables** across all components
- **Comprehensive commenting** throughout the codebase

## 🤝 Contributing

We welcome contributions to improve this demonstration project:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines
- Follow TwinCAT naming conventions (PascalCase for POUs, snake_case for variables)
- Add comprehensive comments to new code
- Update documentation when adding new components
- Test wiki generation before submitting PRs

## 📝 Documentation Philosophy

This project demonstrates automated documentation generation with these principles:

- **Code as Documentation**: Comments and structure become formal documentation
- **Always Up-to-Date**: Documentation regenerates automatically with code changes
- **Comprehensive Coverage**: Every component, variable, and interface documented
- **Developer Friendly**: Easy to read and navigate structure
- **Version Controlled**: Documentation history tracked alongside code

## 🔧 Technical Details

### Parser Capabilities
The Python parser can extract:
- POU information (Programs, Function Blocks, Functions)
- Variable declarations with types and comments
- Data type definitions (Structs, Enums)
- Global variable lists
- Implementation code and documentation comments
- Project structure and relationships

### Supported TwinCAT Elements
- ✅ Programs, Function Blocks, Functions
- ✅ Structured Text (ST) implementation
- ✅ Variable declarations (VAR, VAR_INPUT, VAR_OUTPUT, VAR_GLOBAL)
- ✅ Data Unit Types (DUTs) - Structs and Enums
- ✅ Global Variable Lists (GVLs)
- ✅ XML project files (.tsproj, .TcPOU, .TcDUT, .TcGVL)
- ⚠️ Visualizations (basic support)
- ❌ Ladder Logic (LD), Function Block Diagram (FBD)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Beckhoff Automation** for TwinCAT3 platform
- **GitHub** for excellent collaboration tools
- **Python Community** for XML parsing and template libraries
- **Open Source Community** for inspiration and best practices

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and community interaction
- **Wiki**: Check the auto-generated wiki for detailed component documentation

---

**🎉 This project demonstrates the power of combining industrial automation with modern software development practices!**
