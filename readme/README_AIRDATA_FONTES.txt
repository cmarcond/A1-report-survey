Template AIRDATA - Relatórios Técnicos
======================================

Este projeto contém um template LaTeX padronizado para os relatórios técnicos do projeto AIRDATA, utilizando a fonte  Cheltenham ITC Pro.

Estrutura de Pastas
-----------------------------------------------------------------------
.
├── main.tex                # Documento principal
├── settings/fonts.tex      # Configurações de fonte e estilo
├── fonts/                  # Arquivos .otf da fonte Cheltenham
│   ├── CheltenhamITCPro-Book.otf
│   ├── CheltenhamITCPro-BookItalic.otf
│   ├── CheltenhamITCPro-Bold.otf
│   ├── CheltenhamITCPro-BoldItalic.otf
│   ├── CheltenhamITCPro-Light.otf
│   ├── CheltenhamITCPro-LightItalic.otf
│   ├── CheltenhamITCPro-Ultra.otf
│   └── CheltenhamITCPro-UltraItalic.otf

Requisitos
-----------------------------------------------------------------------
- Compilador: XeLaTeX (ou LuaLaTeX)
- Distribuição LaTeX recomendada: TinyTeX ou TeX Live 2023+

Uso da Fonte Cheltenham ITC Pro
-----------------------------------------------------------------------
A fonte é definida no arquivo defs_settings.tex via o pacote fontspec:

Exemplos de uso
-----------------------------------------------------------------------

Texto normal (Book)

{\useFontLight Texto em estilo Light}

{\useFontUltra Texto em estilo Ultra}


Compilação
-----------------------------------------------------------------------
No terminal, use:

    xelatex main.tex

Observações
-----------------------------------------------------------------------
- Os arquivos .otf não estão registrados no sistema e são carregados diretamente da pasta ./fonts/

- O uso da fonte requer XeLaTeX. Não funcionará com pdflatex.


