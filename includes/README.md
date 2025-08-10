# Document Metadata Include Files

This directory contains parameterized LaTeX include files for the document's pretextual pages. Edit these files to customize the document metadata without modifying the main LaTeX structure.

## Files

### `version_history.tex`
Document version history table. Update this file to add new versions:
- Version number
- Date (DD/MM/YYYY format)
- Responsible person
- Description of changes

### `coordination_team.tex`
General coordination and stage management information:
- **Coordenação Geral**: General project coordinator
- **Gerente da Etapa**: Stage manager

### `ita_team.tex`
ITA team members list. For each team member, provide:
- Name
- Role in the stage (Função na Etapa)

Note: The file currently has placeholders for 3 team members. Add or remove entries as needed.

### `product_description.tex`
Product information displayed on the title page:
- Product number (Produto 1, 2, etc.)
- Meta and Stage information (Meta X | Etapa Y: Description)
- Product name

## Usage

These files are automatically included in `caps/cap_pretexto.tex`. Simply edit the content in these files and recompile the document:

```bash
make quick  # For quick compilation
make        # For full compilation with bibliography
```

## Example Edits

### Adding a new version
Edit `version_history.tex` and add a new row before the empty rows:
```latex
\textcolor{gray}{1.1} & \textcolor{gray}{15/01/2025} & \textcolor{gray}{João Silva} & \textcolor{gray}{Adição do capítulo de resultados} \\
\hline
```

### Updating team members
Edit `ita_team.tex` and replace the placeholder text:
```latex
João Silva\\
Pesquisador\\
\vspace*{1cm}

Maria Santos\\
Analista de Dados\\
\vspace*{1cm}
```

### Changing product information
Edit `product_description.tex`:
```latex
\textcolor{airdataBlue}{\textbf{\LARGE Produto 2}}\\
\textcolor{airdataBlue}{Meta 1 \textbar{} Etapa 3: Análise de Dados}\\
\vspace*{5cm}	
Sistema de Monitoramento Aeroportuário
```