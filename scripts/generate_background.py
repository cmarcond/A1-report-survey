#!/usr/bin/env python3
"""
generate_background.py - Generate background PNG from dynamic content page
"""

import os
import subprocess
import sys
import json

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

def create_latex_file(footer_logo='images/airdata_logo.png', 
                      product_text='Produto 1',
                      meta_text='Meta 1 | Etapa 6: Airdata',
                      institution_logo='images/ita_traco.png'):
    """Create the temporary LaTeX file with embedded config"""
    # Build the content line by line to avoid encoding issues
    lines = [
        r'\documentclass[12pt]{report}',
        r'\input{settings/usepackage.tex}',
        r'\input{settings/setcolor_generated.tex}',
        r'',
        r'% Embedded config from content_config_airdata.tex',
        rf'\def\pageProductText{{{product_text}}}',
        rf'\def\pageMetaText{{{meta_text}}}',
        r'\def\headerFontFamily{lmr}',
        r'',
        rf'\def\pageInstitutionLogo{{{institution_logo}}}',
        rf'\def\pageFooterLogo{{{footer_logo}}}',
        r'',
        r'% Use generated project colors',
        r'\definecolor{airdataHeaderText}{gray}{0.3}',
        r'\def\productTextColor{airdataHeaderText}',
        r'\def\metaTextColor{projectMainColor}',
        r'\def\separatorLineColor{projectMainColor}',
        r'',
        r'\def\headerTopOffset{1.10cm}',
        r'\def\headerSideMargin{0.6cm}',
        r'\def\productFontSizePt{11.5}',
        r'\def\metaFontSizePt{11.5}',
        r'\def\separatorSpacing{0.55cm}',
        r'\def\separatorHeight{1.1cm}',
        r'\def\separatorLineWidth{0.4pt}',
        r'',
        r'\def\logoTopOffset{0.30cm}',
        r'\def\logoRightMargin{0.25cm}',
        r'\def\institutionLogoWidth{2.90cm}',
        r'\def\logoOpacity{1.0}',
        r'',
        r'\def\footerBottomOffset{0.50cm}',
        r'\def\footerSideMargin{0.45cm}',
        r'\def\footerLogoHeight{1.40cm}',
        r'',
        r'% Embedded dynamic content page (without titlepage wrapper for background)',
        r'\makeatletter',
        r'\@ifpackageloaded{tikz}{}{\RequirePackage{tikz}}',
        r'\@ifpackageloaded{fontspec}{}{\RequirePackage{fontspec}}',
        r'\makeatother',
        r'\usetikzlibrary{calc}',
        r'',
        r'\newfontfamily\HeaderFont[',
        r'  Path=fonts/,',
        r'  Extension=.otf,',
        r'  Ligatures=TeX,',
        r'  LetterSpace=1.3',
        r']{CheltenhamITCPro-Light}',
        r'\newcommand{\HeaderTextStyle}{\HeaderFont}',
        r'',
        r'\begin{document}',
        r'\thispagestyle{empty}',
        r'\begin{tikzpicture}[remember picture,overlay]',
        r'',
        r'  % White background for PNG generation',
        r'  \fill[white] (current page.south west) rectangle (current page.north east);',
        r'',
        r'  % --- Header: product/meta on the left --------------------',
        r'  \node (prod) [anchor=base west,',
        r'                xshift=\headerSideMargin, yshift=-\headerTopOffset]',
        r'        at (current page.north west)',
        r'        {{\HeaderTextStyle',
        r'          \textcolor{\productTextColor}{\fontsize{\productFontSizePt pt}{0}\selectfont \pageProductText}}};',
        r'',
        r'  % vertical separator aligned to prod baseline, centered by height',
        r'  \path let \p1=(prod.base east) in',
        r'       coordinate (sepA) at ($(prod.base east)+(\separatorSpacing,-.5*\separatorHeight)$);',
        r'  \draw[\separatorLineColor, line width=\separatorLineWidth]',
        r'       (sepA) -- ++(0,\separatorHeight);',
        r'',
        r'  % meta text to the right of the separator',
        r'  \node (meta) [anchor=base west]',
        r'        at ($(prod.base east)+(2*\separatorSpacing,0)$)',
        r'        {{\HeaderTextStyle',
        r'          \textcolor{\metaTextColor}{\fontsize{\metaFontSizePt pt}{0}\selectfont \pageMetaText}}};',
        r'',
        r'  % --- Header: logo on the right ---------------------------',
        r'  \node[anchor=north east,',
        r'        xshift=-\logoRightMargin, yshift=-\logoTopOffset,',
        r'        opacity=\logoOpacity]',
        r'       at (current page.north east)',
        r'       {\includegraphics[width=\institutionLogoWidth]{\pageInstitutionLogo}};',
        r'',
        r'  % --- Footer: logo bottom-left -----------------------------',
        r'  \node[anchor=south west,',
        r'        xshift=\footerSideMargin, yshift=\footerBottomOffset]',
        r'       at (current page.south west)',
        r'       {\includegraphics[height=\footerLogoHeight]{\pageFooterLogo}};',
        r'',
        r'\end{tikzpicture}',
        r'\end{document}',
    ]
    
    with open('build/background_temp.tex', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

def compile_pdf():
    """Compile the LaTeX file to PDF"""
    cmd = ['xelatex', '-output-directory=build', '-interaction=nonstopmode', '-halt-on-error', 'build/background_temp.tex']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def convert_to_png():
    """Convert PDF to PNG using ImageMagick"""
    if not os.path.exists('build/background_temp.pdf'):
        print("❌ PDF file not found")
        return False
    
    # Check if convert command exists
    try:
        subprocess.run(['convert', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ImageMagick not found. PDF generated: build/background_temp.pdf")
        print("   Install ImageMagick to convert to PNG: sudo apt-get install imagemagick")
        return False
    
    cmd = ['convert', '-density', '300', 'build/background_temp.pdf', '-quality', '90', 'capas/background.png']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("📄 Generating background PNG from dynamic content page")
    
    # Load configuration
    config = load_config()
    
    # Get absolute path to project root for image paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Use JSON configuration with absolute paths
    footer_logo = os.path.join(project_root, config["assets"]["images"]["background_logo"])
    institution_logo = os.path.join(project_root, config["assets"]["images"]["ita_traco_logo"])
    
    # Verify required image files exist
    if not os.path.exists(footer_logo):
        print(f"❌ Footer logo not found: {footer_logo}")
        sys.exit(1)
    if not os.path.exists(institution_logo):
        print(f"❌ Institution logo not found: {institution_logo}")
        sys.exit(1)
    
    product_text = config["project"]["product_text"]
    meta_text = config["project"]["meta_text"]
    
    # Create directories
    os.makedirs('build', exist_ok=True)
    os.makedirs('capas', exist_ok=True)
    
    # Create LaTeX file
    create_latex_file(footer_logo, product_text, meta_text, institution_logo)
    
    # Compile to PDF
    if compile_pdf():
        print("✅ LaTeX compilation successful")
        
        # Convert to PNG
        if convert_to_png():
            print("✅ Background PNG generated: capas/background.png")
        else:
            print("⚠️  PNG conversion failed, but PDF available: build/background_temp.pdf")
    else:
        print("❌ LaTeX compilation failed! Check build/background_temp.log for details")
        return 1
    
    
    return 0

if __name__ == '__main__':
    sys.exit(main())