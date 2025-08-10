# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a professional LaTeX report template for the ITA-SAC (Instituto Tecnológico de Aeronáutica) project "Estudos para Aviação de Hoje e do Amanhã". It produces Brazilian ABNT-compliant academic reports with custom institutional branding.

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
```

### Development Workflow
```bash
# For content changes in caps/*.tex files:
make quick        # Usually sufficient

# For bibliography/citation changes:
make              # Full compilation needed

# For continuous editing:
make watch        # In separate terminal
```

### Dependency Management
```bash
make install-deps # Auto-installs TeX packages based on OS
# Also requires: python3, imagemagick
```

## Architecture and Structure

### Core Architecture
The project follows a **hybrid Python/LaTeX architecture** with dynamic asset generation:

1. **`scripts/`** - Python scripts for dynamic PNG generation
2. **`main.tex`** - Entry point that orchestrates all LaTeX components
3. **`settings/`** - LaTeX formatting, styling, and configuration
4. **`caps/`** - Chapter content files (cap00.tex through cap11.tex)
5. **`capas/`** - Generated PNG assets (cover, backgrounds)
6. **Build Flow**: Python scripts → PNG assets → LaTeX compilation → PDF

### Key Technical Decisions

#### Asset Generation System
- **Python 3 + ImageMagick** required for PNG generation
- **LaTeX → PDF → PNG pipeline** for high-quality assets
- **Dynamic configuration** via Makefile variables
- **Automatic dependency tracking** - assets regenerate when config changes

#### Compilation Engine
- **Must use XeLaTeX or LuaLaTeX** (not pdfLaTeX) due to custom fonts
- XeLaTeX is preferred for fontspec compatibility
- The Makefile automatically handles the correct compilation sequence

#### Font System
- Uses custom **Cheltenham ITC Pro** fonts from `./fonts/` directory
- Loaded via `fontspec` package in `settings/fonts.tex`
- Falls back to system fonts if custom fonts unavailable

#### Brazilian Standards (ABNT)
- Implements ABNT NBR 14724:2011 via `abntex2cite` package
- Citations use `abntex2-alf` style (alphabetical)
- Formatting rules in `settings/setabnt.tex`

### File Organization Pattern

When adding new features or content:

1. **Content goes in `caps/`** - Create new .tex files for chapters
2. **Configuration goes in `settings/`** - Isolate formatting/styling changes
3. **References go in `refs/referencias.bib`** - All bibliography entries
4. **Acronyms go in `siglas/cap_siglas.tex`** - Define with `\newacronym`

### Build Process Internals

The Makefile implements a sophisticated hybrid compilation:

#### Asset Generation Phase
```
1. generate_cover.py → capas/cover.png
2. generate_background.py → capas/background.png  
3. generate_background_pretex.py → capas/background_pretex.png
```

#### LaTeX Compilation Phase
```
1. XeLaTeX (1st pass) → Generate .aux files
2. BibTeX → Process bibliography
3. makeglossaries → Process acronyms/glossary
4. XeLaTeX (2nd pass) → Resolve citations
5. XeLaTeX (3rd pass) → Finalize references/TOC
```

#### Key Dependencies
- PNG assets must exist before LaTeX compilation
- Asset regeneration triggered by Makefile variable changes
- Full pipeline runs on both `make` and `make quick`

## Working with Content

### Adding a New Chapter
1. Create `caps/capXX.tex` with your content
2. Add `\input{caps/capXX}` in `main.tex` at the appropriate position
3. Chapter title: `\chapter{Your Title}`

### Adding Citations
1. Add entry to `refs/referencias.bib`
2. Cite with `\cite{key}` or `\citeonline{key}`
3. Run `make` (full compilation) to update bibliography

### Adding Acronyms
1. Define in `siglas/cap_siglas.tex`: `\newacronym{ITA}{ITA}{Instituto Tecnológico de Aeronáutica}`
2. Use in text: `\gls{ITA}` (first use shows full form)
3. Run `make` to update acronym list

### Customizing Appearance

#### Makefile Configuration Variables
```makefile
# Background generation configuration
FOOTER_LOGO = images/logoAirdata.png
PRODUCT_TEXT = Produto 1
META_TEXT = Meta 2 | Etapa 2: Sistemas Distribuidos

# Cover page configuration  
COVER_TITLE = Relatório de Análise e Mapeamento das Bases de Dados
COVER_MONTH = Agosto
COVER_YEAR = 2025
COVER_INSTITUTION_LOGO = images/logoITA.png
COVER_PROJECT_LOGO = images/airdata_logo.png
```

#### LaTeX Styling
- **Colors**: Edit `settings/setcolor.tex` (institutional blue: #2f84c6)
- **Layout**: Modify `settings/setlayout.tex` for margins/spacing  
- **Titles**: Adjust `settings/settitles.tex` for heading styles
- **PNG Display**: `settings/coverpage_png.tex` handles full-page PNG rendering

## Common Issues and Solutions

### Asset Generation Issues
- **Missing Python 3**: Install `python3` package
- **Missing ImageMagick**: Install `imagemagick` package  
- **PNG not generated**: Check `scripts/` permissions and paths
- **Force regeneration**: `make clean-assets && make generate-assets`

### "Runaway argument" Error
- **Cause**: Corrupted auxiliary files from interrupted compilation
- **Fix**: `make clean && make` to regenerate clean auxiliaries

### Bibliography Not Updating
- Use `make clean && make` for full rebuild
- Ensure BibTeX entries have all required fields for ABNT

### Font Loading Errors
- Verify fonts exist in `./fonts/` directory
- Switch to LuaLaTeX if XeLaTeX has issues: `make LATEX=lualatex`

### Acronym List Empty
- Ensure acronyms are defined before use
- Run full compilation: `make` (not `make quick`)

### PDF Viewer Issues
- The Makefile auto-detects PDF viewers (evince, okular, xdg-open)
- Override with: `make view PDFVIEWER=your_viewer`

## Testing Changes

### Quick Iteration
```bash
# Terminal 1: Auto-compile
make watch

# Terminal 2: Edit files
# PDF updates automatically
```

### Validation Checklist
- [ ] Document compiles without errors
- [ ] TOC/LOF/LOT generate correctly
- [ ] Citations appear in bibliography
- [ ] Acronyms expand on first use
- [ ] Page numbers are sequential
- [ ] ABNT formatting maintained

## Project-Specific Context

### Institutional Requirements
- Must maintain Airdata branding (logo, colors, fonts)
- Follow ABNT standards for Brazilian academic submissions
- Support Portuguese language with proper hyphenation

### File Patterns to Preserve
- **Content separation**: Keep chapters in `caps/`, configuration in `settings/`
- **Asset generation**: Don't manually edit files in `capas/` (auto-generated)
- **Python scripts**: Modify generation logic in `scripts/` directory
- **Configuration**: Use Makefile variables, not hardcoded values

### Version Control Considerations
- **Generated files**: `*.aux`, `*.log`, `capas/*.png` are git-ignored
- **Source control**: Commit `.tex` files, Python scripts, and configuration
- **Asset tracking**: PNG assets regenerate automatically, don't commit
- **Build artifacts**: Use `make clean` before committing

## Current System Status

### Asset Generation System
- **Status**: Fully implemented and functional
- **Cover Generation**: `scripts/generate_cover.py` with theme auto-selection
- **Background Generation**: `scripts/generate_background.py` and `scripts/generate_background_pretex.py`
- **Integration**: Fully integrated into `make` pipeline
- **Dependencies**: Python 3 + ImageMagick required

### Recent Improvements
- Moved from LaTeX-based to Python-based asset generation
- Eliminated encoding issues with embedded configuration
- Added automatic dependency tracking in Makefile
- Implemented multi-commit Git workflow
- Cleaned up obsolete configuration files