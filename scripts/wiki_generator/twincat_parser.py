#!/usr/bin/env python3
"""
TwinCAT Project Parser
======================

This module parses TwinCAT3 project files and extracts documentation information
for automatic wiki generation.

Author: Demo System
Date: 2024
Version: 1.0
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class POUInfo:
    """Program Organization Unit (POU) information."""
    name: str
    type: str  # PROGRAM, FUNCTION_BLOCK, FUNCTION
    file_path: str
    description: str
    author: str
    version: str
    date: str
    variables: List[Dict]
    implementation: str
    comments: List[str]


@dataclass
class DUTInfo:
    """Data Unit Type (DUT) information."""
    name: str
    type: str  # STRUCT, ENUM, etc.
    file_path: str
    description: str
    author: str
    version: str
    members: List[Dict]
    comments: List[str]


@dataclass
class GVLInfo:
    """Global Variable List (GVL) information."""
    name: str
    file_path: str
    description: str
    variables: List[Dict]
    comments: List[str]


class TwinCATParser:
    """Parser for TwinCAT3 project files."""
    
    def __init__(self, project_root: str):
        """Initialize parser with project root directory."""
        self.project_root = Path(project_root)
        self.pous = []
        self.duts = []
        self.gvls = []
        self.included_files = self._get_project_included_files()
        
    def parse_project(self) -> Dict:
        """Parse entire TwinCAT project and extract information."""
        logger.info(f"Parsing TwinCAT project at: {self.project_root}")
        
        # Find and parse all POU files
        self._parse_pous()
        
        # Find and parse all DUT files
        self._parse_duts()
        
        # Find and parse all GVL files
        self._parse_gvls()
        
        return {
            'pous': self.pous,
            'duts': self.duts,
            'gvls': self.gvls,
            'project_info': self._get_project_info()
        }
    
    def _parse_pous(self):
        """Parse all POU (Program Organization Unit) files."""
        pou_pattern = "**/*.TcPOU"
        all_pou_files = list(self.project_root.glob(pou_pattern))
        if self.included_files:
            pou_files = [p for p in all_pou_files if str(p.relative_to(self.project_root)).replace('\\','/') in self.included_files]
        else:
            pou_files = all_pou_files
        
        logger.info(f"Found {len(pou_files)} POU files")
        
        for pou_file in pou_files:
            try:
                pou_info = self._parse_pou_file(pou_file)
                if pou_info:
                    self.pous.append(pou_info)
            except Exception as e:
                logger.error(f"Error parsing POU file {pou_file}: {e}")
    
    def _parse_duts(self):
        """Parse all DUT (Data Unit Type) files."""
        dut_pattern = "**/*.TcDUT"
        all_dut_files = list(self.project_root.glob(dut_pattern))
        if self.included_files:
            dut_files = [p for p in all_dut_files if str(p.relative_to(self.project_root)).replace('\\','/') in self.included_files]
        else:
            dut_files = all_dut_files
        
        logger.info(f"Found {len(dut_files)} DUT files")
        
        for dut_file in dut_files:
            try:
                dut_info = self._parse_dut_file(dut_file)
                if dut_info:
                    self.duts.append(dut_info)
            except Exception as e:
                logger.error(f"Error parsing DUT file {dut_file}: {e}")
    
    def _parse_gvls(self):
        """Parse all GVL (Global Variable List) files."""
        gvl_pattern = "**/*.TcGVL"
        all_gvl_files = list(self.project_root.glob(gvl_pattern))
        if self.included_files:
            gvl_files = [p for p in all_gvl_files if str(p.relative_to(self.project_root)).replace('\\','/') in self.included_files]
        else:
            gvl_files = all_gvl_files
        
        logger.info(f"Found {len(gvl_files)} GVL files")
        
        for gvl_file in gvl_files:
            try:
                gvl_info = self._parse_gvl_file(gvl_file)
                if gvl_info:
                    self.gvls.append(gvl_info)
            except Exception as e:
                logger.error(f"Error parsing GVL file {gvl_file}: {e}")
    
    def _parse_pou_file(self, file_path: Path) -> Optional[POUInfo]:
        """Parse a single POU file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract POU information from XML
            pou_element = root.find(".//POU")
            if pou_element is None:
                return None
            
            name = pou_element.get("Name", "Unknown")
            pou_type = pou_element.get("SpecialFunc", "PROGRAM")
            
            # Extract declaration
            declaration_element = root.find(".//Declaration")
            declaration_text = ""
            if declaration_element is not None and declaration_element.text:
                declaration_text = declaration_element.text.strip()
            
            # Extract implementation
            implementation_element = root.find(".//Implementation/ST")
            implementation_text = ""
            if implementation_element is not None and implementation_element.text:
                implementation_text = implementation_element.text.strip()
            
            # Parse comments and documentation from declaration
            doc_info = self._extract_documentation(declaration_text)
            variables = self._extract_variables(declaration_text)
            
            return POUInfo(
                name=name,
                type=pou_type,
                file_path=str(file_path.relative_to(self.project_root)),
                description=doc_info.get('description', ''),
                author=doc_info.get('author', ''),
                version=doc_info.get('version', ''),
                date=doc_info.get('date', ''),
                variables=variables,
                implementation=implementation_text,
                comments=doc_info.get('comments', [])
            )
            
        except ET.ParseError as e:
            logger.error(f"XML parse error in {file_path}: {e}")
            return None
    
    def _parse_dut_file(self, file_path: Path) -> Optional[DUTInfo]:
        """Parse a single DUT file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract DUT information
            dut_element = root.find(".//DUT")
            if dut_element is None:
                return None
            
            name = dut_element.get("Name", "Unknown")
            
            # Extract declaration
            declaration_element = root.find(".//Declaration")
            declaration_text = ""
            if declaration_element is not None and declaration_element.text:
                declaration_text = declaration_element.text.strip()
            
            # Parse documentation and members
            doc_info = self._extract_documentation(declaration_text)
            members = self._extract_struct_members(declaration_text)
            
            # Determine DUT type (STRUCT, ENUM, etc.)
            dut_type = "STRUCT"
            if "TYPE" in declaration_text and "ENUM" in declaration_text:
                dut_type = "ENUM"
            
            return DUTInfo(
                name=name,
                type=dut_type,
                file_path=str(file_path.relative_to(self.project_root)),
                description=doc_info.get('description', ''),
                author=doc_info.get('author', ''),
                version=doc_info.get('version', ''),
                members=members,
                comments=doc_info.get('comments', [])
            )
            
        except ET.ParseError as e:
            logger.error(f"XML parse error in {file_path}: {e}")
            return None
    
    def _parse_gvl_file(self, file_path: Path) -> Optional[GVLInfo]:
        """Parse a single GVL file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract GVL information
            gvl_element = root.find(".//GVL")
            if gvl_element is None:
                return None
            
            name = gvl_element.get("Name", "Unknown")
            
            # Extract declaration
            declaration_element = root.find(".//Declaration")
            declaration_text = ""
            if declaration_element is not None and declaration_element.text:
                declaration_text = declaration_element.text.strip()
            
            # Parse documentation and variables
            doc_info = self._extract_documentation(declaration_text)
            variables = self._extract_variables(declaration_text, is_global=True)
            
            return GVLInfo(
                name=name,
                file_path=str(file_path.relative_to(self.project_root)),
                description=doc_info.get('description', ''),
                variables=variables,
                comments=doc_info.get('comments', [])
            )
            
        except ET.ParseError as e:
            logger.error(f"XML parse error in {file_path}: {e}")
            return None
    
    def _extract_documentation(self, text: str) -> Dict:
        """Extract documentation information from comments."""
        doc_info = {
            'description': '',
            'author': '',
            'version': '',
            'date': '',
            'comments': []
        }
        
        # Extract single-line comments
        comment_lines = re.findall(r'//\s*(.*)', text)
        doc_info['comments'] = comment_lines
        
        # Look for specific documentation patterns
        for line in comment_lines:
            line_lower = line.lower().strip()
            if line_lower.startswith('purpose:') or line_lower.startswith('description:'):
                doc_info['description'] = line.split(':', 1)[1].strip()
            elif line_lower.startswith('author:'):
                doc_info['author'] = line.split(':', 1)[1].strip()
            elif line_lower.startswith('version:'):
                doc_info['version'] = line.split(':', 1)[1].strip()
            elif line_lower.startswith('date:'):
                doc_info['date'] = line.split(':', 1)[1].strip()
        
        # Extract multi-line comment blocks
        comment_blocks = re.findall(r'\(\*\s*(.*?)\s*\*\)', text, re.DOTALL)
        if comment_blocks:
            doc_info['description'] = comment_blocks[0].strip()
        
        return doc_info
    
    def _extract_variables(self, text: str, is_global: bool = False) -> List[Dict]:
        """Extract variable declarations from text."""
        variables = []
        
        # Pattern to match variable declarations
        var_pattern = r'(\w+)\s*:\s*([^;:=]+)(?:\s*:=\s*([^;]+))?\s*;?\s*(?://\s*(.*))?'
        
        # Find VAR blocks
        var_blocks = []
        if is_global:
            var_blocks = re.findall(r'VAR_GLOBAL(.*?)END_VAR', text, re.DOTALL | re.IGNORECASE)
        else:
            var_blocks.extend(re.findall(r'VAR_INPUT(.*?)END_VAR', text, re.DOTALL | re.IGNORECASE))
            var_blocks.extend(re.findall(r'VAR_OUTPUT(.*?)END_VAR', text, re.DOTALL | re.IGNORECASE))
            var_blocks.extend(re.findall(r'VAR(?:\s|$)(.*?)END_VAR', text, re.DOTALL | re.IGNORECASE))
        
        for block in var_blocks:
            matches = re.finditer(var_pattern, block, re.MULTILINE)
            for match in matches:
                name = match.group(1).strip()
                data_type = match.group(2).strip()
                default_value = match.group(3).strip() if match.group(3) else ''
                comment = match.group(4).strip() if match.group(4) else ''
                
                # Skip empty names or keywords
                if name and not name.upper() in ['VAR', 'END_VAR', 'VAR_INPUT', 'VAR_OUTPUT']:
                    variables.append({
                        'name': name,
                        'type': data_type,
                        'default': default_value,
                        'comment': comment
                    })
        
        return variables
    
    def _extract_struct_members(self, text: str) -> List[Dict]:
        """Extract structure members from DUT declaration."""
        members = []
        
        # Find STRUCT block
        struct_match = re.search(r'STRUCT\s*(.*?)END_STRUCT', text, re.DOTALL | re.IGNORECASE)
        if struct_match:
            struct_content = struct_match.group(1)
            
            # Pattern to match member declarations
            member_pattern = r'(\w+)\s*:\s*([^;:=]+)(?:\s*:=\s*([^;]+))?\s*;?\s*(?://\s*(.*))?'
            
            matches = re.finditer(member_pattern, struct_content, re.MULTILINE)
            for match in matches:
                name = match.group(1).strip()
                data_type = match.group(2).strip()
                default_value = match.group(3).strip() if match.group(3) else ''
                comment = match.group(4).strip() if match.group(4) else ''
                
                if name:
                    members.append({
                        'name': name,
                        'type': data_type,
                        'default': default_value,
                        'comment': comment
                    })
        
        return members
    
    def _get_project_info(self) -> Dict:
        """Extract general project information."""
        project_info = {
            'name': 'Demo TwinCAT Project',
            'description': 'GitHub integration demonstration with TwinCAT3',
            'version': '1.0.0',
            'author': 'Demo System',
            'pou_count': len(self.pous),
            'dut_count': len(self.duts),
            'gvl_count': len(self.gvls)
        }
        
        # Try to read project file for additional info
        project_files = list(self.project_root.glob("*.tsproj"))
        if project_files:
            try:
                tree = ET.parse(project_files[0])
                root = tree.getroot()
                
                name_element = root.find(".//Name")
                if name_element is not None and name_element.text:
                    project_info['name'] = name_element.text
                    
            except Exception as e:
                logger.warning(f"Could not parse project file: {e}")
        
        return project_info

    def _get_project_included_files(self) -> List[str]:
        """Read .tsproj files to determine which source files are included.
        Returns normalized relative paths (with forward slashes).
        If no project file is found or parsing fails, returns an empty list to allow glob fallback.
        """
        includes: List[str] = []
        project_files = list(self.project_root.glob("*.tsproj"))
        for proj in project_files:
            try:
                tree = ET.parse(proj)
                root = tree.getroot()
                for compile_item in root.findall(".//{http://schemas.microsoft.com/developer/msbuild/2003}Compile"):
                    inc = compile_item.get("Include")
                    if inc:
                        # Normalize separators
                        includes.append(inc.replace('\\','/'))
                # Also support cases without namespace
                for compile_item in root.findall(".//Compile"):
                    inc = compile_item.get("Include")
                    if inc:
                        includes.append(inc.replace('\\','/'))
            except Exception as e:
                logger.warning(f"Could not parse project file for includes ({proj}): {e}")
        # Deduplicate
        return sorted(set(includes))


if __name__ == "__main__":
    # Example usage
    parser = TwinCATParser("../../DemoTwinCAT")
    project_data = parser.parse_project()
    
    print(f"Project: {project_data['project_info']['name']}")
    print(f"POUs: {len(project_data['pous'])}")
    print(f"DUTs: {len(project_data['duts'])}")
    print(f"GVLs: {len(project_data['gvls'])}")