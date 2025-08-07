# Template LaTeX - Relatório TED ITA-SAC

Template profissional para relatórios do projeto TED ITA-SAC "Estudos para Aviação de Hoje e do Amanhã", com formatação ABNT e identidade visual Airdata.

## 🚀 Início Rápido

```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd A1-report-survey

# Configure sua Meta e Etapa no Makefile (linhas 32-33)
# PROJECT_META = 2
# PROJECT_ETAPA = 2

# Compile o documento
make
```

O comando `make` automaticamente:
- Instala dependências LaTeX necessárias
- Carrega as fontes Cheltenham ITC Pro do projeto
- Configura as cores oficiais da sua Meta/Etapa
- Compila o documento completo com bibliografia e siglas

## 📋 Pré-requisitos

- **Linux/macOS**: Sistema de pacotes (apt, dnf, brew, etc.)
- **Windows**: MiKTeX ou TeX Live
- **Espaço em disco**: ~2GB para instalação completa do TeX

## 🎯 Configuração do Projeto

### Definir sua Meta e Etapa

Edite o arquivo `Makefile` (linhas 32-33):

```makefile
PROJECT_META = 2    # Sua meta (1 ou 2)
PROJECT_ETAPA = 2   # Sua etapa (1-6 para Meta 1, 1-10 para Meta 2)
```

Ou compile com parâmetros:

```bash
make PROJECT_META=1 PROJECT_ETAPA=3
```

A cor oficial correspondente será aplicada automaticamente em:
- Capa do documento
- Cabeçalhos e destaques
- Elementos visuais

## 📝 Estrutura do Template

```
A1-report-survey/
├── main.tex              # Arquivo principal
├── Makefile              # Sistema de compilação
├── caps/                 # Capítulos do relatório
│   ├── cap00.tex         # Introdução
│   ├── cap01.tex         # Capítulo 1
│   └── ...
├── settings/             # Configurações do template
│   ├── setcolor.tex      # Cores oficiais do projeto
│   ├── coverpage.tex     # Design da capa
│   └── ...
├── refs/                 # Bibliografia
│   └── referencias.bib   # Arquivo BibTeX
├── siglas/               # Definições de siglas
│   └── cap_siglas.tex    # Lista de acrônimos
└── images/               # Imagens e logos

```

## 🔧 Comandos Principais

### Compilação

```bash
make              # Compilação completa (3 passos + bibliografia)
make quick        # Compilação rápida (1 passo)
make view         # Compila e abre o PDF
make watch        # Recompila automaticamente ao salvar arquivos
make force        # Limpa tudo e recompila do zero
```

### Manutenção

```bash
make clean        # Remove arquivos temporários
make distclean    # Remove TODOS os arquivos gerados
make deps-check   # Verifica dependências instaladas
make help         # Mostra todos os comandos disponíveis
```

## ✏️ Como Usar o Template

### 1. Adicionar Conteúdo

- **Capítulos**: Edite os arquivos em `caps/cap*.tex`
- **Novo capítulo**: Crie `caps/capXX.tex` e inclua em `main.tex`

### 2. Gerenciar Bibliografia

```latex
% Em refs/referencias.bib, adicione:
@article{silva2024,
  author = {Silva, João},
  title = {Título do Artigo},
  journal = {Nome da Revista},
  year = {2024}
}

% No texto, cite com:
\cite{silva2024}
```

### 3. Adicionar Siglas

```latex
% Em siglas/cap_siglas.tex, defina:
\newacronym{ANAC}{ANAC}{Agência Nacional de Aviação Civil}

% No texto, use:
\gls{ANAC}  % Primeira vez: Agência Nacional de Aviação Civil (ANAC)
\gls{ANAC}  % Próximas vezes: ANAC
```

### 4. Incluir Imagens

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{images/sua_imagem.png}
  \caption{Legenda da figura}
  \label{fig:label}
\end{figure}
```

## 🎨 Paleta de Cores Oficiais

Cada Meta/Etapa possui uma cor oficial que é aplicada automaticamente:

### Meta 1
- Coordenação: #272a6a
- Etapa 1: #283880
- Etapa 2: #204196
- Etapa 3: #2451a4
- Etapa 4: #2b61ae
- Etapa 5: #2d72ba
- Etapa 6: #2f84c6

### Meta 2
- Etapa 1: #388fcd
- Etapa 2: #6597ca
- Etapa 3: #6392bd
- Etapa 4: #618eb1
- Etapa 5: #5e89a7
- Etapa 6: #5c859c
- Etapa 7: #4d7d94
- Etapa 8: #3f738b
- Etapa 9: #306983
- Etapa 10: #215f7b

## 🐛 Resolução de Problemas

### Erro de compilação com fontes

```bash
# O template usa Cheltenham ITC Pro (incluída automaticamente em fonts/)
# As fontes são carregadas diretamente do projeto - não precisa instalar no sistema
# Certifique-se de usar XeLaTeX ou LuaLaTeX:
make LATEX=xelatex   # padrão
make LATEX=lualatex  # alternativa
```

### Bibliografia não atualiza

```bash
make clean && make   # Força recompilação completa
```

### Instalação de dependências falha

```bash
# Instalação manual no Ubuntu/Debian:
sudo apt-get install texlive-full

# Fedora:
sudo dnf install texlive-scheme-full

# macOS:
brew install --cask mactex
```

## 📦 Dependências do Template

O template requer os seguintes pacotes LaTeX (instalados automaticamente):

- **Motor**: XeLaTeX ou LuaLaTeX (para fontes customizadas)
- **ABNT**: abntex2cite (normas brasileiras)
- **Fontes**: fontspec, Cheltenham ITC Pro (incluída no projeto)
- **Cores**: xcolor com cores institucionais
- **Bibliografia**: BibTeX com estilo ABNT
- **Siglas**: glossaries-extra

## 🤝 Compartilhamento entre Equipes

Para compartilhar com colegas de outras Metas/Etapas:

1. **Faça um fork ou clone** este repositório
2. **Configure sua Meta/Etapa** no Makefile
3. **Substitua o conteúdo** dos capítulos em `caps/`
4. **Atualize a bibliografia** em `refs/referencias.bib`
5. **Compile** com `make`

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs: `main.log`
2. Execute: `make deps-check`
3. Tente: `make force` para recompilação limpa
4. Consulte a documentação ABNT em caso de dúvidas de formatação

---

**Projeto TED ITA-SAC** - Instituto Tecnológico de Aeronáutica / Secretaria de Aviação Civil