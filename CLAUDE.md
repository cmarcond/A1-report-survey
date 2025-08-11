# CLAUDE.md

This file provides comprehensive technical guidance to Claude Code (claude.ai/code) and other AI assistants when working with this LaTeX report template repository.

## Repository Overview

This is a professional, fully-parameterized LaTeX report template for the ITA-SAC (Instituto Tecnológico de Aeronáutica) project "Estudos para Aviação de Hoje e do Amanhã". It produces Brazilian ABNT-compliant academic reports with dynamic institutional branding through an innovative Python/LaTeX hybrid architecture.

## Key Features

- **Fully Parameterized**: All content configurable via `includes/asset_config.json`
- **Dynamic Asset Generation**: Python scripts automatically generate branded PNGs
- **ABNT Compliance**: Follows Brazilian academic standards (NBR 14724:2011)
- **Smart Color Theming**: Automatic palette selection based on project phase
- **Professional Typography**: Custom Cheltenham ITC Pro fonts
- **Build Automation**: Sophisticated Makefile with dependency tracking

## Essential Commands

### Building the Document
```bash
make              # Full compilation with asset generation and LaTeX compilation
make quick        # Asset generation + single-pass LaTeX (faster, for small changes)
make view         # Compile and open PDF
make watch        # Auto-recompile on file changes
make clean        # Remove all generated files
```

### Dynamic Asset Generation
```bash
make generate-assets      # Generate all assets (cover + backgrounds)
make generate-cover       # Generate cover PNG only
make generate-backgrounds # Generate background PNGs only
make clean-assets         # Remove generated PNG assets
make update-colors        # Update color configuration from JSON
```

### Development Workflow
```bash
# For content changes in caps/*.tex files:
make quick        # Usually sufficient

# For bibliography/citation changes:
make              # Full compilation needed

# For continuous editing:
make watch        # In separate terminal

# For debugging issues:
make debug        # Verbose output
```

### Dependency Management
```bash
make install-deps # Auto-installs TeX packages based on OS
# Also requires: python3, imagemagick
```

## Architecture and Structure

### Core Architecture
The project follows a **hybrid Python/LaTeX architecture** with dynamic asset generation:

1. **Configuration Phase**: `includes/asset_config.json` defines all parameters
2. **Generation Phase**: Python scripts create branded PNG assets
3. **Compilation Phase**: XeLaTeX processes the document with generated assets
4. **Output Phase**: Professional PDF with full ABNT compliance

### Build Pipeline Flow
```
asset_config.json
    ↓
Python Scripts (generate_*.py)
    ↓
PNG Assets (capas/*.png)
    ↓
XeLaTeX Compilation
    ↓
Final PDF
```

### Directory Structure
```
parameterized-sac-report/
├── includes/asset_config.json  # Central configuration
├── scripts/                    # Python generators
├── capas/                      # Generated assets
├── caps/                       # Chapter content
├── settings/                   # LaTeX configuration
├── fonts/                      # Custom fonts
└── main.tex                    # Entry point
```

### Key Technical Decisions

#### Asset Generation System
- **Technology**: Python 3 + ImageMagick for high-quality PNG generation
- **Configuration**: Single JSON file controls all parameters
- **Regeneration**: Automatic when configuration changes
- **Caching**: Assets only regenerate when needed

#### Compilation Engine
- **Engine**: XeLaTeX or LuaLaTeX (required for fontspec)
- **Sequence**: 3-pass compilation for references + BibTeX + glossaries
- **Optimization**: Quick mode for rapid iteration

#### Font System
- **Primary**: Cheltenham ITC Pro family (16 variants)
- **Loading**: Via fontspec package
- **Fallback**: System fonts if custom unavailable

#### Brazilian Standards (ABNT)
- **Package**: abntex2cite for citations
- **Style**: abntex2-alf (alphabetical)
- **Configuration**: settings/setabnt.tex

#### Color Management
- **Automatic**: Theme selection based on meta/etapa
- **Palettes**: Pre-defined gradients for each project phase
- **Override**: Custom colors via configuration

## Configuration System

### Central Configuration (`includes/asset_config.json`)

```json
{
  "project": {
    "title": "Report Title",
    "meta": 2,              // Project meta phase
    "etapa": 6,             // Project stage
    "meta_text": "Meta 2 | Etapa 6: Description",
    "product_text": "Product/Activity",
    "month": "Agosto",
    "year": "2025"
  },
  "assets": {
    "images": {
      "institution_logo": "images/logoITA.png",
      "project_logo": "images/project_logo.png",
      "background_logo": "images/footer_logo.png"
    }
  },
  "theme": {
    "bg_color": "20,25,38",      // RGB values
    "footer_color": "58,118,173"
  },
  "colors": {
    "project_main": "auto",       // Or hex color
    "palette": {
      // Predefined color palettes by meta/etapa
    }
  }
}
```

### Color Theme System

The system automatically selects colors based on:
1. **Meta value** (1 or 2)
2. **Etapa value** (1-10)
3. **Manual override** if specified

Example palette resolution:
- Meta 1, Etapa 3 → Blue shade #2451a4
- Meta 2, Etapa 6 → Teal shade #5c859c

## Working with Content

### File Organization Pattern

```
caps/                 # Chapter content
├── cap00.tex        # Abstract
├── cap01.tex        # Introduction
├── cap02.tex        # Chapter 2
└── ...

settings/            # Configuration
├── fonts.tex        # Typography
├── setcolor.tex     # Colors
├── setlayout.tex    # Page layout
└── ...

refs/                # Bibliography
└── referencias.bib  # BibTeX entries

siglas/              # Acronyms
└── cap_siglas.tex   # Glossary definitions
```

### Adding New Content

#### New Chapter
```latex
% caps/cap12.tex
\chapter{Chapter Title}
\section{Section Title}
Content here...
```

Then in `main.tex`:
```latex
\input{caps/cap12}
```

#### Citations
```latex
% In text
According to \citeonline{author2024}...
See \cite{author2024} for details.

% In referencias.bib
@article{author2024,
  author = {Name, Author},
  title = {Title},
  journal = {Journal},
  year = {2024}
}
```

#### Acronyms
```latex
% Define in siglas/cap_siglas.tex
\newacronym{ITA}{ITA}{Instituto Tecnológico de Aeronáutica}

% Use in text
The \gls{ITA} system...  % First: full form
The \gls{ITA} team...    % Later: acronym only
```

## Build Process Internals

### Asset Generation Phase
1. Python reads `asset_config.json`
2. Resolves colors based on meta/etapa
3. Generates LaTeX templates
4. Compiles templates to PDF
5. Converts PDF to PNG

### LaTeX Compilation Phase
1. **Pass 1**: XeLaTeX generates .aux files
2. **BibTeX**: Processes bibliography
3. **makeglossaries**: Processes acronyms
4. **Pass 2**: XeLaTeX resolves citations
5. **Pass 3**: XeLaTeX finalizes TOC/references

### Dependency Tracking
- Makefile monitors configuration changes
- Assets regenerate only when needed
- LaTeX recompiles on content changes

## Common Issues and Solutions

### Asset Generation Issues
```bash
# Missing Python 3
sudo apt-get install python3

# Missing ImageMagick
sudo apt-get install imagemagick

# Force regeneration
make clean-assets && make generate-assets
```

### Compilation Errors

#### "Runaway argument"
```bash
# Corrupted auxiliary files
make clean && make
```

#### Font Loading Errors
```bash
# Try LuaLaTeX instead
make LATEX=lualatex
```

#### Bibliography Not Updating
```bash
# Full rebuild required
make clean && make
```

### Performance Optimization

#### For Quick Iterations
```bash
make quick  # Single LaTeX pass
```

#### For Auto-Compilation
```bash
make watch  # Monitors file changes
```

## Testing and Validation

### Validation Checklist
- [ ] Document compiles without errors
- [ ] Cover page displays correctly
- [ ] TOC/LOF/LOT generate properly
- [ ] Citations appear in bibliography
- [ ] Acronyms expand on first use
- [ ] Page numbers sequential
- [ ] ABNT formatting maintained
- [ ] Colors match configuration

### Test Commands
```bash
# Full validation
make clean && make

# Test colors
make test-colors

# Debug mode
make debug
```

## Project Patterns and Best Practices

### File Organization
- **Content**: Always in `caps/` directory
- **Configuration**: Always in `settings/` directory
- **Assets**: Auto-generated in `capas/` (don't edit manually)
- **Static Images**: Place in `images/` directory

### Configuration Management
- **Single Source**: All parameters in `asset_config.json`
- **No Hardcoding**: Use configuration variables
- **Version Control**: Don't commit generated PNGs

### Development Workflow
1. Edit configuration in `asset_config.json`
2. Run `make` to generate assets and compile
3. Edit content in `caps/*.tex`
4. Use `make quick` for rapid iteration
5. Run `make clean && make` before commits

### Git Best Practices
```bash
# Before committing
make clean  # Remove generated files

# Files to ignore (already in .gitignore)
*.aux *.log *.out
capas/*.png
build/
```

## Advanced Customization

### Custom Color Palette
```json
"colors": {
  "project_main": "3498db",
  "coordination": "2c3e50",
  "institution": "e74c3c",
  "palette": {
    "custom": {
      "primary": "3498db",
      "secondary": "2ecc71"
    }
  }
}
```

### Custom Fonts
```latex
% In settings/fonts.tex
\setmainfont{Your Font}
\setsansfont{Sans Font}
\setmonofont{Mono Font}
```

### Page Layout
```latex
% In settings/setlayout.tex
\geometry{
  left=3cm,
  right=2cm,
  top=3cm,
  bottom=2cm
}
```

## Important Notes

### System Requirements
- **TeX Engine**: Must use XeLaTeX or LuaLaTeX (not pdfLaTeX)
- **Python**: Version 3.6+ required
- **ImageMagick**: For PNG conversion
- **Fonts**: Cheltenham ITC Pro family included

### Performance Tips
- Use `make quick` for content edits
- Use `make watch` for continuous editing
- Only use full `make` when changing bibliography or structure

### Troubleshooting Priority
1. Check `asset_config.json` syntax
2. Verify Python/ImageMagick installed
3. Run `make clean` for fresh start
4. Check font availability
5. Review compilation logs

## Project Context

This template was developed for professional academic reports requiring:
- Brazilian ABNT compliance
- Institutional branding
- Dynamic content generation
- Professional typography
- Automated workflows

The hybrid Python/LaTeX architecture enables both flexibility and automation, making it ideal for recurring reports with varying content but consistent branding.