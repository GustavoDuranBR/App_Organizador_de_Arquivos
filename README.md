## Organizador de Arquivos

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Descrição do projeto 

O Organizador de Arquivos é uma aplicação para organizar arquivos em pastas de acordo com diferentes critérios, como tipo de arquivo ou parte do nome.

### Funcionalidades

- **Seleção de Arquivos:** Escolha entre diferentes critérios de seleção, como Extensão, Parte do Nome ou Ambos, para organizar seus arquivos de maneira eficiente.
  **Exemplo:**
  - Selecione "Extensão" para organizar arquivos com base em sua extensão.
  - Selecione "Parte do Nome" para agrupar arquivos contendo uma determinada parte do nome.
  - Selecione "Ambos" para combinar ambas as opções e refinar ainda mais a organização.

- **Ação:** Escolha entre "Copy" (Copiar) ou "Move" (Mover) para especificar como deseja organizar os arquivos selecionados.
  **Exemplo:**
  - Selecione "Copy" para copiar os arquivos selecionados para a pasta de destino.
  - Selecione "Move" para mover os arquivos selecionados para a pasta de destino.

- **Tipo de Arquivo:** Selecione o tipo de arquivo que deseja organizar, como .txt, .jpg, .pdf, etc.
  **Exemplo:**
  - Selecione ".txt" para organizar apenas arquivos de texto.
  - Selecione ".jpg" para organizar apenas imagens JPEG.

- **Parte do Nome:** Digite uma parte do nome para agrupar arquivos que contenham essa parte específica no nome.
  **Exemplo:**
  - Digite "relatório" para agrupar arquivos que tenham "relatório" em seu nome.

### Demonstração
  <img src="https://github.com/GustavoDuranBR/App_Organizador_de_Arquivos/assets/81047389/23284e39-eb5d-4468-bfdb-26fd583c152b" width="350" alt="Demonstração do Organizador de Arquivos">

### 🛠️ Instalação 🛠️ 

#### Requisitos

- ``Python 3.x:``
- Dependências adicionais (listadas no arquivo `requirements.txt`)

```bash
pip install -r requirements.txt
```
---

### ✔️ Tecnologias Utilizadas

- ``Python 3.x:`` Linguagem de programação utilizada para desenvolver o aplicativo.
- ``Tkinter:`` Biblioteca gráfica padrão do Python para criar interfaces gráficas de usuário (GUI).
- ``Pillow:`` Biblioteca de processamento de imagens utilizada para redimensionar e exibir imagens na interface.
- ``Shutil:`` Módulo Python para operações de alto nível em arquivos e diretórios, utilizado para mover e copiar arquivos.
- ``Datetime:`` Módulo Python para trabalhar com datas e horários, utilizado para registrar o timestamp das ações de organização.
- ``os:`` Módulo Python que fornece uma interface para interagir com o sistema operacional, utilizado para manipular caminhos de arquivos e pastas.
- ``ttkthemes:`` Biblioteca que fornece temas adicionais para widgets Tkinter.
- ``PIL:`` Abreviação de Python Imaging Library, agora renomeada como Pillow, é uma biblioteca de processamento de imagens em Python.
  
Essas tecnologias foram fundamentais para o desenvolvimento do File Organizer App, oferecendo funcionalidades essenciais para a criação da interface gráfica, manipulação de arquivos e organização dos mesmos de acordo com as preferências do usuário.

--- 

### Uso

Execute o seguinte comando no terminal para iniciar a aplicação:

```bash
python file_organizer_app.py
```

### Contribuição

Sinta-se à vontade para contribuir! Consulte nosso [guia de contribuição](CONTRIBUTING.md) para obter mais informações.

### Problemas e Melhorias

Encontrou um bug ou gostaria de sugerir uma melhoria? Por favor, [abra uma issue](https://github.com/GustavoDuranBR/App_Organizador_de_Arquivos/issues).
