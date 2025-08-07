#!/bin/bash
# update_project_color.sh - Update the project color based on Meta and Etapa

PROJECT_META="${1:-2}"
PROJECT_ETAPA="${2:-2}"

# Define the official color codes
declare -A COLORS

# Meta 1 colors
COLORS["1,coord"]="272a6a"
COLORS["1,1"]="283880"
COLORS["1,2"]="204196"
COLORS["1,3"]="2451a4"
COLORS["1,4"]="2b61ae"
COLORS["1,5"]="2d72ba"
COLORS["1,6"]="2f84c6"

# Meta 2 colors
COLORS["2,coord"]="388fcd"
COLORS["2,1"]="388fcd"
COLORS["2,2"]="6597ca"
COLORS["2,3"]="6392bd"
COLORS["2,4"]="618eb1"
COLORS["2,5"]="5e89a7"
COLORS["2,6"]="5c859c"
COLORS["2,7"]="4d7d94"
COLORS["2,8"]="3f738b"
COLORS["2,9"]="306983"
COLORS["2,10"]="215f7b"

# Get the color for the specified Meta and Etapa
COLOR_KEY="${PROJECT_META},${PROJECT_ETAPA}"
PROJECT_COLOR="${COLORS[$COLOR_KEY]}"

if [ -z "$PROJECT_COLOR" ]; then
    echo "Error: Invalid Meta ($PROJECT_META) or Etapa ($PROJECT_ETAPA)"
    exit 1
fi

# Update the projectMainColor in setcolor.tex
SETCOLOR_FILE="settings/setcolor.tex"

# Create backup
cp "$SETCOLOR_FILE" "${SETCOLOR_FILE}.bak" 2>/dev/null

# Update the color definition to reference the actual meta/etapa color
sed -i "s/\\\\definecolor{projectMainColor}{HTML}{[a-fA-F0-9]\{6\}}/\\\\definecolor{projectMainColor}{named}{meta${PROJECT_META}etapa${PROJECT_ETAPA}}/" "$SETCOLOR_FILE"

echo "✅ Project color updated to Meta ${PROJECT_META} Etapa ${PROJECT_ETAPA} (#${PROJECT_COLOR})"
echo "   Run 'make' to compile with the new color"