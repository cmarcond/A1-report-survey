#!/usr/bin/env python3
"""
generate_cover.py - Generate cover page PNG from parameters
"""

import os
import subprocess
import sys
import re
import json

def parse_meta_text(meta_text):
    """Parse meta text to extract Meta number, Etapa number and title"""
    # Example: "Meta 2 | Etapa 2: Sistema Distribuido"
    meta_match = re.search(r'Meta\s+(\d+)', meta_text)
    etapa_match = re.search(r'Etapa\s+(\d+):\s*(.+)', meta_text)
    
    meta_num = meta_match.group(1) if meta_match else "1"
    etapa_num = etapa_match.group(1) if etapa_match else "1"
    etapa_title = etapa_match.group(2).strip() if etapa_match else "Project"
    
    return meta_num, etapa_num, etapa_title

def parse_product_text(product_text):
    """Parse product text to extract product number"""
    # Example: "Produto 1" -> "I"
    match = re.search(r'Produto\s+(\d+)', product_text)
    if match:
        num = int(match.group(1))
        # Convert to Roman numerals for products 1-5
        roman = ["I", "II", "III", "IV", "V"]
        return roman[num-1] if num <= 5 else str(num)
    return "I"

def load_config():
    """Load configuration from JSON file"""
    # Get absolute path to project root (parent of scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    config_path = os.path.join(project_root, 'includes', 'asset_config.json')
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_theme_colors(etapa_num, config):
    """Get theme colors from config"""
    return config["theme"]

def create_latex_file(params, config):
    """Create the temporary LaTeX file for cover page"""
    # Parse parameters
    meta_num, etapa_num, etapa_title = parse_meta_text(params['meta_text'])
    product_num = parse_product_text(params['product_text'])
    colors = get_theme_colors(etapa_num, config)
    
    # Build the content line by line
    lines = [
        r'\documentclass[12pt]{report}',
        r'\usepackage{tikz}',
        r'\usepackage{fontspec}',
        r'\usepackage{graphicx}',
        r'\usepackage{xcolor}',
        r'\usetikzlibrary{calc}',
        r'',
        r'% Load semantic colors',
        r'\input{settings/setcolor_generated.tex}',
        r'',
        r'% Font setup',
        r'\newfontfamily\CheltenhamFont[',
        r'  Path=fonts/,',
        r'  Extension=.otf,',
        r'  Ligatures=TeX',
        r']{CheltenhamITCPro-Book}',
        r'',
        r'% Color definitions',
        rf'\definecolor{{coverBg}}{{RGB}}{{{colors["bg_color"]}}}',
        r'% Note: coverFooter now uses semantic projectMainColor from setcolor_generated.tex',
        r'',
        r'% Parameters',
        rf'\def\institutionName{{ITA}}',
        rf'\def\projectMeta{{{meta_num}}}',
        rf'\def\projectEtapa{{{etapa_num}}}',
        rf'\def\projectEtapaTitle{{{etapa_title}}}',
        rf'\def\projectTitle{{{params["title"]}}}',
        rf'\def\productNumber{{{product_num}}}',
        rf'\def\projectMonth{{{params["month"]}}}',
        rf'\def\projectYear{{{params["year"]}}}',
        rf'\def\institutionLogo{{{params["institution_logo"]}}}',
        rf'\def\projectLogo{{{params["project_logo"]}}}',
        r'',
        r'% Layout parameters',
        r'\def\institutionLogoWidth{7cm}',
        r'\def\projectLogoWidth{15cm}',
        r'\def\footerHeight{3.2cm}',
        r'\def\logoTopOffset{1.2cm}',
        r'\def\logoSideOffset{1.5cm}',
        r'\def\footerTextOffset{0.8cm}',
        r'\def\projectLogoYShift{-1cm}',
        r'\def\projectLogoXShift{-3cm}',
        r'\def\dateOffsetY{3.7cm}',
        r'',
        r'% Font sizes',
        r'\def\institutionFontSize{36}',
        r'\def\metaEtapaFontSize{24}',
        r'\def\titleFontSize{18}',
        r'\def\productFontSize{22}',
        r'\def\dateFontSize{20}',
        r'',
        r'\begin{document}',
        r'\thispagestyle{empty}',
        r'\begin{tikzpicture}[remember picture,overlay]',
        r'',
        r'  % Background color',
        r'  \fill[coverBg] (current page.south west) rectangle (current page.north east);',
        r'',
        r'  % Institution logo (top-left)',
        r'  \node[anchor=north west, xshift=\logoSideOffset, yshift=-\logoTopOffset]',
        r'       at (current page.north west)',
        r'       {\includegraphics[width=\institutionLogoWidth]{\institutionLogo}};',
        r'',
        r'  % Institution name + Meta/Etapa (top-right)',
        rf'  \node[anchor=north east, xshift=-\logoSideOffset, yshift=-\logoTopOffset,',
        rf'        align=right, text={colors["header_text"]}]',
        r'       at (current page.north east) {%',
        r'         {\CheltenhamFont\fontsize{\institutionFontSize}{0}\selectfont\bfseries \institutionName}\\[0.8em]',
        r'         {\CheltenhamFont\fontsize{\metaEtapaFontSize}{0}\selectfont Meta \projectMeta}\\[0.8em]',
        r'         {\CheltenhamFont\fontsize{\metaEtapaFontSize}{0}\selectfont Etapa \projectEtapa\ \projectEtapaTitle}',
        r'       };',
        r'',
        r'  % Project logo (center)',
        r'  \node[anchor=center, xshift=\projectLogoXShift, yshift=\projectLogoYShift]',
        r'       at (current page.center)',
        r'       {\includegraphics[width=\projectLogoWidth]{\projectLogo}};',
        r'',
        r'  % Date (bottom-right)',
        rf'  \node[anchor=south east, xshift=-\logoSideOffset, yshift=\dateOffsetY,',
        rf'        text={colors["header_text"]}]',
        r'       at (current page.south east)',
        r'       {{\CheltenhamFont\fontsize{\dateFontSize}{0}\selectfont \projectMonth\ \projectYear}};',
        r'',
        r'  % Footer bar',
    ]
    
    # Add footer using semantic project color (follows documentation: caps/cap08.tex)
    if 'footer_opacity' in colors:
        lines.append(rf'  \fill[projectMainColor, opacity={colors["footer_opacity"]}] (current page.south west) rectangle ++(\paperwidth, \footerHeight);')
    else:
        lines.append(r'  \fill[projectMainColor] (current page.south west) rectangle ++(\paperwidth, \footerHeight);')
    
    lines.extend([
        r'',
        r'  % Footer text',
        rf'  \node[anchor=south west, xshift=\logoSideOffset, yshift=\footerTextOffset,',
        rf'        align=left, text={colors["footer_text"]}]',
        r'       at (current page.south west) {%',
        r'         {\CheltenhamFont\fontsize{\productFontSize}{0}\selectfont\bfseries Produto \productNumber}\\[0.5em]',
        r'         {\CheltenhamFont\fontsize{\titleFontSize}{0}\selectfont \projectTitle}',
        r'       };',
        r'',
        r'\end{tikzpicture}',
        r'\end{document}',
    ])
    
    with open('build/cover_temp.tex', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

def compile_pdf():
    """Compile the LaTeX file to PDF"""
    cmd = ['xelatex', '-output-directory=build', '-interaction=nonstopmode', '-halt-on-error', 'build/cover_temp.tex']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def convert_to_png():
    """Convert PDF to PNG using ImageMagick"""
    if not os.path.exists('build/cover_temp.pdf'):
        print("❌ PDF file not found")
        return False
    
    # Check if convert command exists
    try:
        subprocess.run(['convert', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ImageMagick not found. PDF generated: build/cover_temp.pdf")
        print("   Install ImageMagick to convert to PNG: sudo apt-get install imagemagick")
        return False
    
    cmd = ['convert', '-density', '300', 'build/cover_temp.pdf', '-quality', '90', 'capas/cover.png']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("📄 Generating cover page PNG")
    
    # Load configuration
    config = load_config()
    
    # Get absolute path to project root for image paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Use JSON configuration with absolute paths
    project_logo_path = os.path.join(project_root, config["assets"]["images"]["project_logo"])
    institution_logo_path = os.path.join(project_root, config["assets"]["images"]["institution_logo"])
    
    # Verify required image files exist
    if not os.path.exists(project_logo_path):
        print(f"❌ Project logo not found: {project_logo_path}")
        sys.exit(1)
    if not os.path.exists(institution_logo_path):
        print(f"❌ Institution logo not found: {institution_logo_path}")
        sys.exit(1)
    
    params = {
        'project_logo': project_logo_path,
        'product_text': config["project"]["product_text"],
        'meta_text': config["project"]["meta_text"],
        'title': config["project"]["title"],
        'month': config["project"]["month"],
        'year': config["project"]["year"],
        'institution_logo': institution_logo_path
    }
    
    # Create directories
    os.makedirs('build', exist_ok=True)
    os.makedirs('capas', exist_ok=True)
    
    # Create LaTeX file
    create_latex_file(params, config)
    
    # Compile to PDF
    if compile_pdf():
        print("✅ LaTeX compilation successful")
        
        # Convert to PNG
        if convert_to_png():
            print("✅ Cover PNG generated: capas/cover.png")
        else:
            print("⚠️  PNG conversion failed, but PDF available: build/cover_temp.pdf")
    else:
        print("❌ LaTeX compilation failed! Check build/cover_temp.log for details")
        return 1
    
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
