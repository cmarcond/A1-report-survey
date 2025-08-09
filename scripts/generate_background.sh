#!/bin/bash
# generate_background.sh - Generate background PNG from dynamic content

echo "📄 Generating background PNG from dynamic content page"

# Create build and capas directories
mkdir -p build capas

# Create temporary LaTeX file
cat > background_temp.tex << 'EOF'
\documentclass[12pt]{report}
\input{settings/usepackage.tex}
\input{settings/setcolor.tex}
\input{settings/dynamic_contentpage.tex}
\begin{document}
\pagestyle{empty}
\makeDynamicContentPage{airdata}
\end{document}
EOF

# Compile with XeLaTeX
xelatex -output-directory=build -interaction=nonstopmode -halt-on-error background_temp.tex

# Keep temporary file for debugging (comment out to clean up)
# rm -f background_temp.tex

# Convert PDF to PNG if ImageMagick is available
if command -v convert >/dev/null 2>&1; then
    convert -density 300 build/background_temp.pdf -quality 90 capas/background.png
    echo "✅ Background PNG generated: capas/background.png"
else
    echo "⚠️  ImageMagick not found. PDF generated: build/background_temp.pdf"
    echo "   Install ImageMagick to convert to PNG: sudo apt-get install imagemagick"
fi