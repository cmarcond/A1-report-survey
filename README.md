# Parameterized SAC Report Template

A professional, fully-parameterized LaTeX report template for the ITA-SAC (Instituto Tecnológico de Aeronáutica) project, designed to produce Brazilian ABNT-compliant academic reports with dynamic institutional branding and automated asset generation.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd parameterized-sac-report

# Install dependencies and build
make              # Full build with all assets
make view         # Build and open PDF

# For continuous editing
make watch        # Auto-recompile on changes
```

## 📋 Prerequisites

### Required Software
- **TeX Distribution**: TeX Live or MiKTeX (with XeLaTeX)
- **Python 3**: For asset generation scripts
- **ImageMagick**: For PNG processing
- **Make**: Build automation

### Installation by OS

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y texlive-full python3 imagemagick make
```

#### macOS
```bash
brew install --cask mactex
brew install python3 imagemagick make
```

#### Fedora/RHEL
```bash
sudo dnf install texlive-scheme-full python3 ImageMagick make
```

## 🏗️ Project Architecture

### Dynamic Asset Generation System

The project features a sophisticated **hybrid Python/LaTeX architecture** that automatically generates branded assets based on configuration:

```
asset_config.json → Python Scripts → PNG Assets → LaTeX Compilation → PDF
```

### Directory Structure

```
parameterized-sac-report/
├── main.tex                  # Main LaTeX entry point
├── Makefile                  # Build automation
├── includes/
│   └── asset_config.json    # Central configuration file
├── scripts/                 # Python asset generators
│   ├── generate_cover.py
│   ├── generate_background.py
│   └── resolve_project_colors.py
├── capas/                    # Generated PNG assets (auto-created)
│   ├── cover.png
│   ├── background.png
│   └── background_pretex.png
├── caps/                     # Chapter content files
│   ├── cap00.tex            # Abstract
│   ├── cap01.tex            # Introduction
│   └── ...                  # Additional chapters
├── settings/                 # LaTeX configuration
│   ├── fonts.tex            # Font configuration
│   ├── setcolor.tex         # Color definitions
│   └── ...                  # Other settings
├── fonts/                    # Custom Cheltenham fonts
├── images/                   # Static images/logos
└── refs/                     # Bibliography
    └── referencias.bib
```

## ⚙️ Configuration

### Central Configuration File

All project parameters are centralized in `includes/asset_config.json`:

```json
{
  "project": {
    "title": "Your Report Title",
    "meta": 2,
    "etapa": 6,
    "meta_text": "Meta 2 | Etapa 6: Project Phase",
    "product_text": "Product Description",
    "month": "Agosto",
    "year": "2025"
  },
  "assets": {
    "images": {
      "institution_logo": "images/logoITA.png",
      "project_logo": "images/your_logo.png",
      "background_logo": "images/footer_logo.png"
    }
  },
  "theme": {
    "bg_color": "20,25,38",
    "footer_color": "58,118,173"
  }
}
```

### Color Themes

The system automatically selects colors based on meta/etapa values:
- **Meta 1**: Blue gradient palette (etapas 1-6)
- **Meta 2**: Teal gradient palette (etapas 1-10)
- **Custom**: Override with explicit color values

## 🛠️ Build Commands

### Primary Commands

| Command | Description |
|---------|-------------|
| `make` | Full compilation with asset generation |
| `make quick` | Single-pass compilation (faster) |
| `make view` | Compile and open PDF |
| `make watch` | Auto-recompile on file changes |
| `make clean` | Remove all generated files |

### Asset Management

| Command | Description |
|---------|-------------|
| `make generate-assets` | Generate all PNG assets |
| `make generate-cover` | Generate cover page only |
| `make generate-backgrounds` | Generate backgrounds only |
| `make clean-assets` | Remove generated PNGs |
| `make update-colors` | Update color configuration |

### Development Tools

| Command | Description |
|---------|-------------|
| `make install-deps` | Install TeX packages |
| `make test-colors` | Generate color palette preview |
| `make debug` | Verbose compilation output |

## 📝 Working with Content

### Adding a New Chapter

1. Create a new file in `caps/`:
```latex
% caps/cap12.tex
\chapter{Your Chapter Title}

Your content here...
```

2. Include it in `main.tex`:
```latex
\input{caps/cap12}
```

### Managing Citations

1. Add entries to `refs/referencias.bib`:
```bibtex
@article{author2024,
  author = {Author Name},
  title = {Article Title},
  journal = {Journal Name},
  year = {2024}
}
```

2. Cite in your text:
```latex
According to \citeonline{author2024}...
```

### Using Acronyms

1. Define in `siglas/cap_siglas.tex`:
```latex
\newacronym{AI}{AI}{Artificial Intelligence}
```

2. Use in text:
```latex
The \gls{AI} system...  % First use shows full form
```

## 🎨 Customization

### Quick Customization

Edit `includes/asset_config.json` to change:
- Report title and metadata
- Institution/project logos
- Color themes
- Date information

### Advanced Customization

#### Custom Color Palette
```json
"colors": {
  "project_main": "2f84c6",
  "coordination": "272a6a",
  "accent": "ff6b6b"
}
```

#### Font Configuration
Edit `settings/fonts.tex` to change typography:
```latex
\setmainfont{Your Font Name}
```

#### Page Layout
Modify `settings/setlayout.tex` for margins and spacing.

## 🐛 Troubleshooting

### Common Issues

#### "Runaway argument" Error
```bash
make clean && make  # Clean rebuild
```

#### Assets Not Generating
```bash
# Check Python and ImageMagick
python3 --version
convert --version

# Force regeneration
make clean-assets && make generate-assets
```

#### Font Loading Errors
```bash
# Use LuaLaTeX instead
make LATEX=lualatex
```

#### Bibliography Not Updating
```bash
make clean && make  # Full rebuild required
```

### Debug Mode
```bash
make debug  # Verbose output for troubleshooting
```

## 📚 Documentation

- **CLAUDE.md**: Detailed technical documentation for AI assistants
- **readme/**: Legacy documentation and font licensing
- **includes/README.md**: Configuration system documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make clean && make`
5. Submit a pull request

### Development Workflow

```bash
# Start development
git checkout -b feature/your-feature

# Make changes and test
make watch  # In terminal 1
# Edit files in terminal 2

# Validate before commit
make clean && make
git add .
git commit -m "feat: your feature description"
```

## 📄 License

This project uses:
- **LaTeX**: LaTeX Project Public License
- **Cheltenham Fonts**: Licensed for project use
- **ABNTeX2**: LaTeX Project Public License
- **Python Scripts**: MIT License

## 🏢 About

Developed for the ITA-SAC project "Estudos para Aviação de Hoje e do Amanhã" in collaboration with:
- Instituto Tecnológico de Aeronáutica (ITA)
- SAC - Secretaria de Aviação Civil

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review `CLAUDE.md` for technical details
3. Open an issue on GitHub

---

*Built with ❤️ for academic excellence and professional presentation*