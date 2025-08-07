# Makefile for LaTeX project with XeLaTeX
# Author: Generated for main.tex project
# Note: This project uses fontspec, requiring XeLaTeX or LuaLaTeX
#
# USAGE:
#   make         # Automatically installs dependencies and compiles
#   make clean   # Remove temporary files
#   make view    # Compile and view PDF
#   make help    # Show all commands

# Detect OS for package installation
UNAME := $(shell uname -s)
ifeq ($(UNAME),Linux)
    DISTRO := $(shell lsb_release -si 2>/dev/null || echo "Unknown")
endif

# Variables
MAIN = main
LATEX = xelatex
# Alternative: use lualatex if you have issues with xelatex
# LATEX = lualatex
BIBTEX = bibtex
MAKEGLOSSARIES = makeglossaries
VIEWER = xdg-open
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# ========================================
# PROJECT CONFIGURATION
# ========================================
# Configure your project Meta and Etapa here
# This will automatically use the correct official color
PROJECT_META = 2
PROJECT_ETAPA = 2

# Source files and dependencies
TEX_FILES = $(wildcard *.tex) \
            $(wildcard caps/*.tex) \
            $(wildcard settings/*.tex) \
            $(wildcard siglas/*.tex)

BIB_FILES = $(wildcard refs/*.bib)

IMG_FILES = $(wildcard images/*.png) \
            $(wildcard images/*.jpg) \
            $(wildcard images/*.pdf) \
            $(wildcard images/*.eps)

# Output files
PDF = $(MAIN).pdf
AUX = $(MAIN).aux
LOG = $(MAIN).log
BBL = $(MAIN).bbl
BLG = $(MAIN).blg
GLO = $(MAIN).glo
GLS = $(MAIN).gls
GLG = $(MAIN).glg
ACN = $(MAIN).acn
ACR = $(MAIN).acr
ALG = $(MAIN).alg
IST = $(MAIN).ist
TOC = $(MAIN).toc
LOF = $(MAIN).lof
LOT = $(MAIN).lot
OUT = $(MAIN).out

# Temporary files to clean
TEMP_FILES = $(AUX) $(LOG) $(BBL) $(BLG) $(GLO) $(GLS) $(GLG) \
             $(ACN) $(ACR) $(ALG) $(IST) $(TOC) $(LOF) $(LOT) $(OUT) \
             *.aux *.log *.bbl *.blg *.glo *.gls *.glg *.acn *.acr \
             *.alg *.ist *.toc *.lof *.lot *.out *.fls *.fdb_latexmk \
             *.synctex.gz *.nav *.snm *.vrb *.dvi *.ps *.pdf

# Default target - automatically installs dependencies if needed
.PHONY: all
all: auto-setup update-project-color $(PDF)

# Automatic setup - installs missing dependencies without asking
.PHONY: auto-setup
auto-setup:
	@if ! command -v $(LATEX) >/dev/null 2>&1 || ! command -v $(BIBTEX) >/dev/null 2>&1 || ! command -v $(MAKEGLOSSARIES) >/dev/null 2>&1; then \
		echo "=========================================" && \
		echo "📦 Setting up LaTeX environment..." && \
		echo "=========================================" && \
		$(MAKE) install-deps-auto; \
	fi

# Update project color based on Meta and Etapa
.PHONY: update-project-color
update-project-color:
	@echo "🎨 Setting project color for Meta $(PROJECT_META) Etapa $(PROJECT_ETAPA)"
	@mkdir -p scripts
	@bash scripts/update_project_color.sh "$(PROJECT_META)" "$(PROJECT_ETAPA)"

# Main compilation rule
$(PDF): $(TEX_FILES) $(IMG_FILES)
	@echo "========================================="
	@echo "Starting LaTeX compilation..."
	@echo "========================================="
	
	# First pass - generate aux files
	@echo "[1/5] First LaTeX pass..."
	@$(LATEX) $(LATEX_FLAGS) $(MAIN).tex || \
		(echo "" && \
		 echo "❌ Compilation failed! Check main.log for details" && \
		 echo "Common issues: missing .tex files, undefined commands, or package conflicts" && \
		 exit 1)
	
	# Generate glossaries if needed
	@if [ -f $(MAIN).glo ] || [ -f $(MAIN).acn ]; then \
		echo "[2/5] Processing glossaries..."; \
		$(MAKEGLOSSARIES) $(MAIN); \
	else \
		echo "[2/5] No glossaries to process."; \
	fi
	
	# Run BibTeX if aux file exists and contains citations
	@if grep -q "\\citation" $(AUX) 2>/dev/null; then \
		echo "[3/5] Processing bibliography..."; \
		$(BIBTEX) $(MAIN); \
	else \
		echo "[3/5] No citations found."; \
	fi
	
	# Second pass - incorporate bibliography and glossaries
	@echo "[4/5] Second LaTeX pass..."
	@$(LATEX) $(LATEX_FLAGS) $(MAIN).tex || \
		(echo "❌ Second pass failed! Check main.log" && exit 1)
	
	# Third pass - resolve cross-references
	@echo "[5/5] Final LaTeX pass..."
	@$(LATEX) $(LATEX_FLAGS) $(MAIN).tex || \
		(echo "❌ Final pass failed! Check main.log" && exit 1)
	
	@echo "========================================="
	@echo "✅ Compilation complete: $(PDF)"
	@echo "========================================="

# Quick compilation (single pass, no bibliography/glossary update)
.PHONY: quick
quick: auto-setup
	@echo "Quick compilation (single pass)..."
	@$(LATEX) $(LATEX_FLAGS) $(MAIN).tex || \
		(echo "❌ Quick compilation failed! Check main.log" && exit 1)
	@echo "✅ Quick compilation complete: $(PDF)"

# Force full recompilation
.PHONY: force
force: clean all

# View the PDF
.PHONY: view
view: auto-setup $(PDF)
	$(VIEWER) $(PDF) &

# Continuous compilation (watches for changes)
.PHONY: watch
watch:
	@echo "Watching for changes... (Press Ctrl+C to stop)"
	@while true; do \
		$(MAKE) -q all || $(MAKE) all; \
		sleep 2; \
	done

# Clean temporary files but keep PDF
.PHONY: clean
clean:
	@echo "Cleaning temporary files..."
	@rm -f $(TEMP_FILES)
	@find . -name "*.aux" -type f -delete
	@echo "Temporary files removed."

# Clean everything including PDF
.PHONY: distclean
distclean: clean
	@echo "Removing PDF output..."
	@rm -f $(PDF)
	@echo "All generated files removed."

# Check for required tools
.PHONY: check
check:
	@echo "Checking for required tools..."
	@which $(LATEX) > /dev/null || (echo "ERROR: $(LATEX) not found. Run 'make install-deps' to install." && exit 1)
	@which $(BIBTEX) > /dev/null || (echo "ERROR: $(BIBTEX) not found" && exit 1)
	@which $(MAKEGLOSSARIES) > /dev/null || (echo "ERROR: $(MAKEGLOSSARIES) not found" && exit 1)
	@echo "All required tools found."

# Help target
.PHONY: help
help:
	@echo "LaTeX Makefile - Available Commands:"
	@echo "========================================="
	@echo "COMPILATION:"
	@echo "  make         - Install deps (if needed) and compile"
	@echo "  make quick   - Quick compilation (single pass)"
	@echo "  make force   - Clean and full recompilation"
	@echo "  make view    - Compile and open PDF viewer"
	@echo "  make watch   - Continuous compilation on file changes"
	@echo ""
	@echo "PROJECT CONFIGURATION:"
	@echo "  Current: Meta $(PROJECT_META) Etapa $(PROJECT_ETAPA)"
	@echo "  To change: Edit PROJECT_META and PROJECT_ETAPA in Makefile"
	@echo "  Or run: make PROJECT_META=1 PROJECT_ETAPA=3"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "  make clean   - Remove temporary files"
	@echo "  make distclean - Remove all generated files"
	@echo "  make deps-check - Check which packages are installed"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "Just run 'make' and everything will be handled automatically!"

# Check for missing LaTeX packages and system dependencies
.PHONY: deps-check
deps-check:
	@echo "Checking for required LaTeX packages and tools..."
	@echo "========================================="
	
	# Check for XeLaTeX
	@if ! command -v xelatex >/dev/null 2>&1; then \
		echo "❌ XeLaTeX is NOT installed"; \
		echo "   Required for fontspec support"; \
	else \
		echo "✓ XeLaTeX is installed"; \
	fi
	
	# Check for BibTeX
	@if ! command -v bibtex >/dev/null 2>&1; then \
		echo "❌ BibTeX is NOT installed"; \
	else \
		echo "✓ BibTeX is installed"; \
	fi
	
	# Check for makeglossaries
	@if ! command -v makeglossaries >/dev/null 2>&1; then \
		echo "❌ makeglossaries is NOT installed"; \
		echo "   Required for glossary/acronym support"; \
	else \
		echo "✓ makeglossaries is installed"; \
	fi
	
	# Check for essential LaTeX packages using kpsewhich
	@echo ""
	@echo "Checking LaTeX packages:"
	@for pkg in fontspec xcolor glossaries hyperref graphicx babel abntex2; do \
		if kpsewhich $pkg.sty >/dev/null 2>&1; then \
			echo "✓ $pkg package found"; \
		else \
			echo "❌ $pkg package NOT found"; \
		fi \
	done
	
	@echo "========================================="
	@echo "Run 'make install-deps' to install missing packages"

# Automatic installation (no prompts)
.PHONY: install-deps-auto
install-deps-auto:
	@if [ "$(DISTRO)" = "Ubuntu" ] || [ "$(DISTRO)" = "Debian" ]; then \
		echo "📦 Installing LaTeX packages (this may take a few minutes)..."; \
		sudo apt-get update -qq && \
		sudo apt-get install -y -qq \
			texlive-xetex \
			texlive-latex-extra \
			texlive-fonts-recommended \
			texlive-fonts-extra \
			texlive-lang-portuguese \
			texlive-bibtex-extra \
			texlive-publishers \
			biber \
			latexmk >/dev/null 2>&1 || \
		(echo "⚠️  Installing minimal package set..." && \
		 sudo apt-get install -y -qq \
			texlive-xetex \
			texlive-latex-extra \
			texlive-fonts-recommended >/dev/null 2>&1); \
	elif [ "$(DISTRO)" = "Fedora" ] || [ "$(DISTRO)" = "RedHat" ]; then \
		echo "📦 Installing LaTeX packages for Fedora/RedHat..."; \
		sudo dnf install -y -q \
			texlive-xetex \
			texlive-collection-latexextra \
			texlive-collection-fontsrecommended \
			texlive-collection-langportuguese \
			texlive-glossaries \
			texlive-abntex2 >/dev/null 2>&1; \
	elif [ "$(DISTRO)" = "Arch" ] || [ "$(DISTRO)" = "Manjaro" ]; then \
		echo "📦 Installing LaTeX packages for Arch..."; \
		sudo pacman -S --needed --noconfirm -q \
			texlive-core \
			texlive-latexextra \
			texlive-fontsextra \
			texlive-langextra \
			texlive-bibtexextra \
			texlive-publishers \
			biber >/dev/null 2>&1; \
	elif command -v tlmgr >/dev/null 2>&1; then \
		echo "📦 Installing LaTeX packages via tlmgr..."; \
		tlmgr update --self >/dev/null 2>&1; \
		tlmgr install \
			xetex \
			fontspec \
			glossaries \
			glossaries-extra \
			hyperref \
			xcolor \
			babel \
			babel-portuges \
			abntex2 \
			biber \
			biblatex-abnt >/dev/null 2>&1; \
	else \
		echo "⚠️  Could not detect package manager. Please install TeX Live manually:"; \
		echo "  Ubuntu/Debian: sudo apt-get install texlive-full"; \
		echo "  Fedora: sudo dnf install texlive-scheme-full"; \
		echo "  Arch: sudo pacman -S texlive-most texlive-lang"; \
		echo "  macOS: brew install --cask mactex"; \
		exit 1; \
	fi
	@echo "✅ Dependencies ready!"

# Install missing dependencies (interactive version)
.PHONY: install-deps
install-deps:
	@echo "Installing missing dependencies..."
	@echo "========================================="
	
	# Detect package manager and install accordingly
	@if [ "$(DISTRO)" = "Ubuntu" ] || [ "$(DISTRO)" = "Debian" ]; then \
		echo "Detected Debian/Ubuntu system"; \
		echo "Installing TeX Live packages..."; \
		echo "This will require sudo privileges"; \
		echo "";
		sudo apt-get update && sudo apt-get install -y \
			texlive-xetex \
			texlive-latex-extra \
			texlive-fonts-recommended \
			texlive-fonts-extra \
			texlive-lang-portuguese \
			texlive-bibtex-extra \
			texlive-publishers \
			biber \
			latexmk; \
		echo ""; \
		echo "Installing abntex2..."; \
		if ! kpsewhich abntex2.cls >/dev/null 2>&1; then \
			sudo apt-get install -y texlive-publishers || \
			(echo "Trying to install abntex2 via tlmgr..." && \
			 tlmgr install abntex2 2>/dev/null || \
			 		echo "Could not install abntex2 automatically"); \
		fi; \
	elif [ "$(DISTRO)" = "Fedora" ] || [ "$(DISTRO)" = "RedHat" ]; then \
		echo "Detected Fedora/RedHat system"; \
		sudo dnf install -y \
			texlive-xetex \
			texlive-collection-latexextra \
			texlive-collection-fontsrecommended \
			texlive-collection-langportuguese \
			texlive-glossaries \
			texlive-abntex2; \
	elif [ "$(DISTRO)" = "Arch" ] || [ "$(DISTRO)" = "Manjaro" ]; then \
		echo "Detected Arch-based system"; \
		sudo pacman -S --needed --noconfirm \
			texlive-core \
			texlive-latexextra \
			texlive-fontsextra \
			texlive-langextra \
			texlive-bibtexextra \
			texlive-publishers \
			biber; \
	elif command -v tlmgr >/dev/null 2>&1; then \
		echo "Using tlmgr to install packages..."; \
		tlmgr update --self; \
		tlmgr install \
			xetex \
			fontspec \
			glossaries \
			glossaries-extra \
			hyperref \
			xcolor \
			babel \
			babel-portuges \
			abntex2 \
			biber \
			biblatex-abnt; \
	else \
		echo "Unable to detect package manager."; \
		echo "Please install TeX Live manually:"; \
		echo "  Ubuntu/Debian: sudo apt-get install texlive-full"; \
		echo "  Fedora: sudo dnf install texlive-scheme-full"; \
		echo "  Arch: sudo pacman -S texlive-most texlive-lang"; \
		echo "  macOS: brew install --cask mactex"; \
		echo "  Windows: Download MiKTeX or TeX Live from their websites"; \
		exit 1; \
	fi
	
	@echo "========================================="
	@echo "Installation complete!"
	@echo "Run 'make deps-check' to verify all packages are installed"

# Quick dependency installation (minimal set)
.PHONY: install-deps-minimal
install-deps-minimal:
	@echo "Installing minimal dependencies for compilation..."
	@if [ "$(DISTRO)" = "Ubuntu" ] || [ "$(DISTRO)" = "Debian" ]; then \
		sudo apt-get update && sudo apt-get install -y \
			texlive-xetex \
			texlive-latex-extra \
			texlive-fonts-recommended; \
	else \
		echo "Run 'make install-deps' for full installation"; \
	fi

# Statistics about the document
.PHONY: stats
stats: $(PDF)
	@echo "Document statistics:"
	@echo -n "  Pages: "
	@pdfinfo $(PDF) 2>/dev/null | grep Pages | awk '{print $$2}' || echo "N/A"
	@echo -n "  File size: "
	@du -h $(PDF) | cut -f1
	@echo -n "  Word count (approximate): "
	@ps2ascii $(PDF) 2>/dev/null | wc -w || echo "N/A"

# Debug information
.PHONY: debug
debug:
	@echo "Main file: $(MAIN).tex"
	@echo "TeX files found: $(words $(TEX_FILES))"
	@echo "BIB files found: $(words $(BIB_FILES))"
	@echo "Image files found: $(words $(IMG_FILES))"
	@ls -la $(MAIN).* 2>/dev/null || echo "No output files yet."

# Prevent deletion of intermediate files
.PRECIOUS: %.aux %.bbl %.gls %.acr

# Mark the default goal
.DEFAULT_GOAL := all
