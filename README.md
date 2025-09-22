# DemoTWinCAT

**Demo TwinCAT3 Project showcasing GitHub Integration and Automated Documentation (minimal example)**

This project demonstrates how to integrate TwinCAT3 industrial automation code with GitHub's collaboration features and automated documentation generation.

![TwinCAT3](https://img.shields.io/badge/TwinCAT3-v3.5.13-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Documentation](https://img.shields.io/badge/Documentation-Auto%20Generated-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Goals

- **Demonstrate GitHub Integration**: Manage a TwinCAT3 project with GitHub and CI
- **Automated Documentation**: Generate wiki documentation from the TwinCAT project
- **Minimal PLC Example**: Keep the PLC code simple and focused for clarity
- **Collaboration**: Enable team workflows for PLC projects with Git


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

You can also view the published wiki in the GitHub Wiki for this repository.

### Advanced Usage
```bash
# Generate with verbose output
python scripts/generate_wiki.py --verbose

# Specify custom directories
python scripts/generate_wiki.py --project-dir MyProject --output-dir docs

# Dry run to test parsing
python scripts/generate_wiki.py --dry-run
```

## PLC Example (Minimal)

The PLC code is intentionally minimal to focus on the tooling:

- Single program `MAIN` (`DemoTwinCAT/PLC/POUs/MAIN.TcPOU`)
- Inputs: `bSwitch1`, `bSwitch2`, `bEmergencyStop`
- Output: `bLamp`
- Logic: `bLamp` turns on when `bSwitch1` or `bSwitch2` is on, unless `bEmergencyStop` is active

No Function Blocks, DUTs, or GVLs are included in this demo to keep it lean.

## Automation Features

### GitHub Actions Workflows
The project includes automated workflows that trigger on:
- **Code Changes**: Auto-generate documentation when TwinCAT files change
- **Pull Requests**: Validate documentation generation on PRs
- **Manual Triggers**: Force documentation updates when needed
- **Releases**: Package documentation with release artifacts
- **Version Bumping**: Automatically bump semantic version on merges to main/development branches

### Automated Semantic Versioning
- **Version Format**: MAJOR.MINOR.PATCH.BUILD (e.g., 1.0.0.0)
- **Branch-based Bumping**: Different version components bumped based on target branch
  - `main` branch: Minor bumps for features, Patch bumps for fixes, Major bumps for breaking changes
  - `development` branch: Build bumps for development features
  - `hotfix/*` branches: Patch bumps for critical fixes
- **Fork Protection**: Version bumps are skipped for pull requests from forks
- **Git Tagging**: Automatic tag creation for main branch releases (e.g., v1.1.0.0)

### Documentation Updates
- **Regeneration on changes**: Documentation is generated during CI runs
- **Smart Commits**: Commits only when there are changes; messages include basic stats
- **Artifact Storage**: Documentation stored as workflow artifacts
- **Pages Deployment**: Optional deployment to GitHub Pages

## 📝 Documentation Philosophy

This project demonstrates automated documentation generation with these principles:

- **Code as Documentation**: Comments and structure become formal documentation
- **Always Up-to-Date**: Documentation regenerates automatically with code changes
- **Comprehensive Coverage**: Every component, variable, and interface documented
- **Developer Friendly**: Easy to read and navigate structure
- **Version Controlled**: Documentation history tracked alongside code

## 🔧 Technical Details

### Project Structure
- `DemoTwinCAT/` – TwinCAT project
   - `PLC/POUs/MAIN.TcPOU` – Main program (only source in this demo)
- `scripts/` – Wiki generator tooling
   - `generate_wiki.py` – Entry point to generate the wiki
   - `wiki_generator/` – Parser and Jinja2 templates
- `wiki/` – Generated markdown files

### Parser Notes
- The parser reads the `.tsproj` to know which files are part of the project
- In this demo, only `MAIN.TcPOU` is included; the generator adapts to the available sources
- The generator cleans the output directory before writing new files to avoid stale pages

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
