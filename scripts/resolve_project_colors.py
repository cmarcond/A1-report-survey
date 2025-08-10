#!/usr/bin/env python3
"""
resolve_project_colors.py - Resolve project colors based on meta/etapa configuration
"""

import os
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

def resolve_color(color_spec, meta, etapa, palette):
    """Resolve a color specification (auto or explicit hex)"""
    if color_spec == "auto":
        # Look up the specific meta/etapa color
        meta_key = f"meta{meta}"
        etapa_key = f"etapa{etapa}"
        
        if meta_key in palette and etapa_key in palette[meta_key]:
            return palette[meta_key][etapa_key]
        else:
            # Fallback to coordination color if specific etapa not found
            if meta_key in palette and "coordination" in palette[meta_key]:
                return palette[meta_key]["coordination"]
            else:
                print(f"⚠️  Warning: No color found for {meta_key} {etapa_key}, using fallback")
                return "2f84c6"  # Fallback to airdata blue
    else:
        # Use explicit hex color
        return color_spec

def resolve_all_colors(config):
    """Resolve all color specifications in the config"""
    project = config["project"]
    colors = config["colors"]
    palette = colors["palette"]
    
    meta = project["meta"]
    etapa = project["etapa"]
    
    resolved = {}
    
    # Resolve main color specs
    resolved["project_main"] = resolve_color(colors["project_main"], meta, etapa, palette)
    resolved["coordination"] = resolve_color(colors["coordination"], meta, etapa, palette)
    resolved["institution"] = colors["institution"]
    resolved["accent"] = resolve_color(colors["accent"], meta, etapa, palette)
    
    # For coordination, use the coordination color of the current meta
    meta_key = f"meta{meta}"
    if meta_key in palette and "coordination" in palette[meta_key]:
        resolved["coordination"] = palette[meta_key]["coordination"]
    
    # For accent, use the coordination color as well
    resolved["accent"] = resolved["coordination"]
    
    return resolved, meta, etapa, palette

def generate_latex_colors(resolved_colors, meta, etapa, palette):
    """Generate LaTeX color definitions"""
    lines = []
    lines.append("% settings/setcolor_generated.tex")
    lines.append("% --- AUTO-GENERATED color definitions from asset_config.json ---")
    lines.append("% DO NOT EDIT MANUALLY - This file is regenerated during build")
    lines.append("")
    lines.append("% Importante: não utilize o comando \\usepackage{xcolor} aqui.")
    lines.append("% Esse pacote já está carregado no arquivo settings/usepackage.tex.")
    lines.append("")
    
    # Main project colors (resolved)
    lines.append("% ========================================")
    lines.append("% RESOLVED PROJECT COLORS")
    lines.append("% ========================================")
    lines.append("")
    lines.append(f"% Current project: Meta {meta} Etapa {etapa}")
    lines.append(f"\\definecolor{{projectMainColor}}{{HTML}}{{{resolved_colors['project_main']}}}")
    lines.append(f"\\definecolor{{projectCoordColor}}{{HTML}}{{{resolved_colors['coordination']}}}")
# Note: airdataBlue removed - use semantic projectMainColor instead
    lines.append(f"\\definecolor{{projectAccentColor}}{{HTML}}{{{resolved_colors['accent']}}}")
    lines.append("")
    
    # Full palette (for palette generator and reference)
    lines.append("% ========================================")
    lines.append("% FULL COLOR PALETTE - METAS E ETAPAS")
    lines.append("% ========================================")
    lines.append("")
    
    # Generate all coordination colors
    lines.append("% Cores de Coordenação")
    for meta_key, meta_colors in palette.items():
        if "coordination" in meta_colors:
            coord_name = f"coord{meta_key.capitalize()}"
            lines.append(f"\\definecolor{{{coord_name}}}{{HTML}}{{{meta_colors['coordination']}}}")
    lines.append("")
    
    # Generate all meta/etapa colors
    for meta_key, meta_colors in palette.items():
        lines.append(f"% --- {meta_key.upper()} ---")
        for etapa_key, color_hex in meta_colors.items():
            if etapa_key != "coordination":  # Skip coordination, already handled above
                color_name = f"{meta_key}{etapa_key}"
                lines.append(f"\\definecolor{{{color_name}}}{{HTML}}{{{color_hex}}}")
        lines.append("")
    
    # Special colors
    lines.append("% ========================================")
    lines.append("% CORES ESPECIAIS")
    lines.append("% ========================================")
    lines.append("")
    lines.append("% Cor creme para fundo de capa")
    lines.append("\\definecolor{creamBg}{RGB}{250,245,225}")
    lines.append("")
    
    return lines

def write_latex_file(lines, output_path):
    """Write LaTeX color definitions to file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines))
        return True
    except Exception as e:
        print(f"❌ Failed to write LaTeX file: {e}")
        return False

def main():
    print("🎨 Resolving project colors from configuration...")
    
    # Load configuration
    config = load_config()
    
    # Resolve colors
    resolved_colors, meta, etapa, palette = resolve_all_colors(config)
    
    print(f"📋 Project: Meta {meta} Etapa {etapa}")
    print(f"🎯 Main Color: #{resolved_colors['project_main']}")
    print(f"🏛️  Coordination: #{resolved_colors['coordination']}")
    print(f"✨ Accent: #{resolved_colors['accent']}")
    
    # Generate LaTeX
    latex_lines = generate_latex_colors(resolved_colors, meta, etapa, palette)
    
    # Write to settings directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, 'settings', 'setcolor_generated.tex')
    
    if write_latex_file(latex_lines, output_path):
        print(f"✅ Generated color definitions: {output_path}")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())