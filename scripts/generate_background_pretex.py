#!/usr/bin/env python3
"""
generate_background_pretex.py - Generate pretextual background PNG with large center ITA logo
"""

import os
import subprocess
import sys

def create_latex_file(footer_logo='images/drone_logo.png',
                      product_text='Produto 1',
                      meta_text='Meta 2 | Etapa 6: Tarifação'):
    """Create the temporary LaTeX file with embedded config for pretextual pages"""
    # Build the content line by line to avoid encoding issues
    lines = [
        r'\documentclass[12pt]{report}',
        r'\input{settings/usepackage.tex}',
        r'\input{settings/setcolor.tex}',
        r'',
        r'% Embedded config from content_config_pretex.tex',
        rf'\def\pageProductText{{{product_text}}}',
        rf'\def\pageMetaText{{{meta_text}}}',
        r'\def\headerFontFamily{lmr}',
        r'',
        r'\def\pageInstitutionLogo{images/ita_traco.png}',
        rf'\def\pageFooterLogo{{{footer_logo}}}',
        r'',
        r'\definecolor{tarifacaoHeaderBlue}{RGB}{47,132,198}',
        r'\definecolor{tarifacaoHeaderText}{gray}{0.3}',
        r'\def\productTextColor{tarifacaoHeaderText}',
        r'\def\metaTextColor{tarifacaoHeaderBlue}',
        r'\def\separatorLineColor{tarifacaoHeaderBlue}',
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
        r'% Center ITA logo settings',
        r'\def\centerItaLogoWidth{12cm}',
        r'\def\centerItaLogoOpacity{0.2}',
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
        r'  % --- Center: Large ITA logo ------------------------------',
        r'  \node[anchor=center, opacity=\centerItaLogoOpacity]',
        r'       at (current page.center)',
        r'       {\includegraphics[width=\centerItaLogoWidth]{\pageInstitutionLogo}};',
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
    
    with open('background_pretex_temp.tex', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

def compile_pdf():
    """Compile the LaTeX file to PDF"""
    cmd = ['xelatex', '-output-directory=build', '-interaction=nonstopmode', '-halt-on-error', 'background_pretex_temp.tex']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def convert_to_png():
    """Convert PDF to PNG using ImageMagick"""
    if not os.path.exists('build/background_pretex_temp.pdf'):
        print("❌ PDF file not found")
        return False
    
    # Check if convert command exists
    try:
        subprocess.run(['convert', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ImageMagick not found. PDF generated: build/background_pretex_temp.pdf")
        print("   Install ImageMagick to convert to PNG: sudo apt-get install imagemagick")
        return False
    
    cmd = ['convert', '-density', '300', 'build/background_pretex_temp.pdf', '-quality', '90', 'capas/background_pretex.png']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("📄 Generating pretextual background PNG with large center ITA logo")
    
    # Parse command line arguments
    footer_logo = sys.argv[1] if len(sys.argv) > 1 else 'images/drone_logo.png'
    product_text = sys.argv[2] if len(sys.argv) > 2 else 'Produto 1'
    meta_text = sys.argv[3] if len(sys.argv) > 3 else 'Meta 2 | Etapa 6: Tarifação'
    
    # Create directories
    os.makedirs('build', exist_ok=True)
    os.makedirs('capas', exist_ok=True)
    
    # Create LaTeX file
    create_latex_file(footer_logo, product_text, meta_text)
    
    # Compile to PDF
    if compile_pdf():
        print("✅ LaTeX compilation successful")
        
        # Convert to PNG
        if convert_to_png():
            print("✅ Pretextual background PNG generated: capas/background_pretex.png")
        else:
            print("⚠️  PNG conversion failed, but PDF available: build/background_pretex_temp.pdf")
    else:
        print("❌ LaTeX compilation failed! Check build/background_pretex_temp.log for details")
        return 1
    
    # Clean up
    if os.path.exists('background_pretex_temp.tex'):
        os.remove('background_pretex_temp.tex')
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
