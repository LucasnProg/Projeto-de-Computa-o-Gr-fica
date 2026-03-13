# 💻 Projeto de Computação Gráfica (2025)

Uma aplicação web modular desenvolvida para demonstrar a implementação prática de algoritmos clássicos de Computação Gráfica. O projeto utiliza **Python (Flask)** no backend para o processamento matemático rigoroso e **JavaScript/HTML5 Canvas** no frontend para renderização e interação.

A arquitetura segue o padrão **MVC (Model-View-Controller)** adaptado com **Flask Blueprints**, separando a lógica matemática (`graphics_logic`) das rotas de aplicação.

---

### ✨ Módulos e Algoritmos Implementados

O projeto está dividido em módulos funcionais acessíveis via menu lateral:

#### 🟢 Primitivas Gráficas e Rasterização
- **3. Retas:**
  - Algoritmo **DDA** (Digital Differential Analyzer).
  - Algoritmo de **Bresenham** (Ponto Médio) clássico.
- **4. Circunferências:**
  - Algoritmo do **Ponto Médio** (Bresenham para Círculos) com simetria de 8 oitantes.
  - Métodos Explícito e Paramétrico (para comparação).
- **6. Elipses:**
  - Algoritmo do **Ponto Médio** para Elipses (divisão em Região 1 e Região 2 baseada no gradiente).
- **13. Curvas:**
  - **Curvas de Bézier Cúbicas**: Interpolação suave baseada em 4 pontos de controle.

#### 🔵 Transformações Geométricas
- **2. Sistemas de Coordenadas:**
  - Mapeamento entre Coordenadas de Mundo (WC), Normalizadas (NDC) e de Dispositivo (DC).
- **5. Transformações 2D:**
  - Translação, Escala, Rotação (com suporte a **Pivô Arbitrário**), Reflexão e Cisalhamento.
  - Uso de matrizes de transformação homogêneas 3x3.
- **10. Visualização 3D:**
  - Manipulação de objetos 3D (Vértices e Arestas).
  - Transformações 3D (Translação, Escala, Rotação em eixos X/Y/Z, Cisalhamento, Reflexão) usando **Matrizes 4x4**.
  - Projeção **Perspectiva** e Paralela.

#### 🔴 Recorte (Clipping)
- **7. Recorte de Linhas:**
  - Algoritmo de **Cohen-Sutherland** (Códigos de Região Binários).
- **8. Recorte de Polígonos (Convexos):**
  - Algoritmo de **Sutherland-Hodgman**.
- **9. Recorte de Polígonos (Gerais):**
  - Implementação baseada em **Weiler-Atherton** para recorte de polígonos sujeitos contra janelas de recorte.
- **11. Pipeline 2D Completo:**
  - Integração de Recorte (Mundo) -> Mapeamento Window-to-Viewport -> Renderização.

#### 🖼️ Processamento de Imagens
- **12. PDI:** Aplicação de filtros e transformações básicas em imagens raster.

---

### 🛠️ Arquitetura do Projeto

O código foi refatorado para garantir alta coesão e baixo acoplamento.

```text
project/
├── graphics_logic/          # PACOTE DE LÓGICA MATEMÁTICA (Core)
│   ├── __init__.py          # Exporta funções para os módulos
│   ├── lines.py             # DDA, Bresenham
│   ├── circles.py           # Ponto Médio
│   ├── ellipses.py          # Elipse Ponto Médio
│   ├── transformations.py   # Matrizes 2D (3x3)
│   ├── projection.py        # Matrizes 3D (4x4) e Projeção
│   ├── clipping.py          # Cohen-Sutherland, Sutherland-Hodgman, Weiler-Atherton
│   ├── bezier.py            # Polinômios de Bernstein
│   └── coordinates.py       # Conversão WC <-> DC
│
├── modules/                 # FLASK BLUEPRINTS (Rotas e Views)
│   ├── mod_1_main/          # Tela inicial
│   ├── mod_3_retas/         # Interface para Retas
│   ├── mod_5_twod/          # Interface para Transformações 2D
│   ├── mod_10_3d_viewing/   # Interface para 3D
│   └── ... (outros módulos)
│
├── static/                  # CSS e JS Globais
├── templates/               # Layout Base (Jinja2)
└── __init__.py              # Fábrica do App Flask
```

-----

### 🚀 Como Executar

**Pré-requisitos:** Python 3.10+ instalado.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/LucasnProg/Projeto-de-Computa-o-Gr-fica.git
    cd Computacao-grafica
    ```

2.  **Crie e ative o ambiente virtual:**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\Activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**

    ```bash
    python run.py
    ```

5.  **Acesse no navegador:**
    Abra [http://127.0.0.1:5001](http://127.0.0.1:5001)

-----

### 📚 Referências Bibliográficas

As implementações matemáticas seguem estritamente as definições acadêmicas encontradas em:

1.  **Hearn, D., & Baker, M. P.** *Computer Graphics with OpenGL*. 4th Edition. Pearson.
2.  **Foley, J. D., et al.** *Computer Graphics: Principles and Practice*. Addison-Wesley.
3.  **Anton, H., & Rorres, C.** *Álgebra Linear com Aplicações*. (Para operações matriciais).

-----
