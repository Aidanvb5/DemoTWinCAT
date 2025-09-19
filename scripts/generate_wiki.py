#!/usr/bin/env python3
"""
Generate Wiki Documentation
============================

Main script to generate wiki documentation from TwinCAT project files.
Can be run manually or automatically via CI/CD pipeline.

Usage:
    python generate_wiki.py [--project-dir DIR] [--output-dir DIR] [--verbose]

Author: Demo System
Date: 2024
Version: 1.0
"""

import argparse
import sys
import logging
from pathlib import Path

# Add the wiki_generator module to the path
sys.path.insert(0, str(Path(__file__).parent / "wiki_generator"))

from wiki_generator import WikiGenerator


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    """Main entry point for wiki generation."""
    parser = argparse.ArgumentParser(
        description='Generate wiki documentation from TwinCAT project files'
    )
    
    parser.add_argument(
        '--project-dir',
        type=str,
        default='DemoTwinCAT',
        help='Path to TwinCAT project directory (default: DemoTwinCAT)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='wiki',
        help='Output directory for wiki files (default: wiki)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse project but do not generate files'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate project directory
    project_path = Path(args.project_dir)
    if not project_path.exists():
        logger.error(f"Project directory does not exist: {project_path}")
        return 1
    
    # Check for TwinCAT project files
    project_files = list(project_path.glob("*.tsproj"))
    if not project_files:
        logger.warning(f"No TwinCAT project files found in: {project_path}")
        logger.info("Continuing anyway - will search for individual component files")
    
    try:
        # Create wiki generator
        generator = WikiGenerator(str(project_path), args.output_dir)
        
        if args.dry_run:
            logger.info("Dry run mode - parsing project only")
            project_data = generator.parser.parse_project()
            
            logger.info("Project parsing results:")
            logger.info(f"  POUs found: {len(project_data['pous'])}")
            logger.info(f"  DUTs found: {len(project_data['duts'])}")
            logger.info(f"  GVLs found: {len(project_data['gvls'])}")
            
            for pou in project_data['pous']:
                logger.info(f"    POU: {pou.name} ({pou.type})")
            
            for dut in project_data['duts']:
                logger.info(f"    DUT: {dut.name} ({dut.type})")
            
            for gvl in project_data['gvls']:
                logger.info(f"    GVL: {gvl.name}")
                
        else:
            # Generate wiki
            logger.info(f"Generating wiki from {project_path} to {args.output_dir}")
            generator.generate_wiki()
            logger.info("Wiki generation completed successfully!")
            
            # Show generated files
            output_path = Path(args.output_dir)
            if output_path.exists():
                wiki_files = list(output_path.glob("*.md"))
                logger.info(f"Generated {len(wiki_files)} wiki files:")
                for wiki_file in sorted(wiki_files):
                    logger.info(f"  - {wiki_file.name}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during wiki generation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())