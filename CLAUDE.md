# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a professional LaTeX report template for the ITA-SAC (Instituto Tecnológico de Aeronáutica) project "Estudos para Aviação de Hoje e do Amanhã". It produces Brazilian ABNT-compliant academic reports with custom institutional branding.

## Essential Commands

### Building the Document
```bash
make              # Full compilation with dependency installation
make quick        # Single-pass compilation (faster, for small changes)
make view         # Compile and open PDF
make watch        # Auto-recompile on file changes
make clean        # Remove all generated files
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
```

## Architecture and Structure

### Core Architecture
The project follows a **modular LaTeX architecture** with centralized configuration:

1. **`main.tex`** - Entry point that orchestrates all components
2. **`settings/`** - All formatting, styling, and configuration isolated here
3. **`caps/`** - Chapter content files (cap00.tex through cap11.tex)
4. **Content Flow**: main.tex → settings → caps → compiled PDF

### Key Technical Decisions

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

The Makefile implements a sophisticated multi-pass compilation:

```
1. XeLaTeX (1st pass) → Generate .aux files
2. BibTeX → Process bibliography
3. makeglossaries → Process acronyms/glossary
4. XeLaTeX (2nd pass) → Resolve citations
5. XeLaTeX (3rd pass) → Finalize references/TOC
```

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
- **Colors**: Edit `settings/setcolor.tex` (institutional blue: #2f84c6)
- **Layout**: Modify `settings/setlayout.tex` for margins/spacing
- **Titles**: Adjust `settings/settitles.tex` for heading styles
- **Cover**: Edit `settings/coverpage.tex` for cover page design

## Common Issues and Solutions

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
- Don't modify `settings/*.tex` unless changing global formatting
- Keep chapter files focused on content only
- Maintain modular structure for reusability

### Version Control Considerations
- Generated files (*.aux, *.log, etc.) are git-ignored
- Only commit source .tex files and assets
- The main.pdf is currently tracked (consider if this should continue)