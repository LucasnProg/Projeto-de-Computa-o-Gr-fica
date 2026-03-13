document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-clipping');
    const ctx = canvas.getContext('2d');
    
    // --- Seletores do DOM ---
    // Inputs da Janela
    const clipXminInput = document.getElementById('clip-xmin');
    const clipYminInput = document.getElementById('clip-ymin');
    const clipXmaxInput = document.getElementById('clip-xmax');
    const clipYmaxInput = document.getElementById('clip-ymax');
    // Inputs da Reta Estática
    const lineX1Input = document.getElementById('line-x1');
    const lineY1Input = document.getElementById('line-y1');
    const lineX2Input = document.getElementById('line-x2');
    const lineY2Input = document.getElementById('line-y2');
    // Botões e Info
    const clipLineBtn = document.getElementById('clip-line-btn');
    const clipInfo = document.getElementById('clip-info');
    const clearBtn = document.getElementById('clear-btn');
    
    // --- NOVO: Seletores de Animação ---
    const toggleAnimationBtn = document.getElementById('toggle-animation-btn');
    let animationId = null; // Guarda o ID do requestAnimationFrame
    let currentAngle = 0;   // Ângulo de rotação atual

    
    // ==========================================================
    // LÓGICA DE RECORTE (CLIENT-SIDE PARA ANIMAÇÃO)
    // Tradução do algoritmo de Cohen-Sutherland [cite: 256]
    // ==========================================================
    
    // [cite: 258-277]
    const INSIDE = 0; // 0b0000
    const LEFT = 1;   // 0b0001
    const RIGHT = 2;  // 0b0010
    const BOTTOM = 4; // 0b0100
    const TOP = 8;    // 0b1000

    /**
     * Calcula o auto-código (outcode) de 4 bits para um ponto (x,y). [cite: 258-277]
     */
    function computeOutcode(x, y, xmin, ymin, xmax, ymax) {
        let code = INSIDE;
        if (x < xmin) code |= LEFT;
        else if (x > xmax) code |= RIGHT;
        if (y < ymin) code |= BOTTOM;
        else if (y > ymax) code |= TOP;
        return code;
    }

    /**
     * Recorta uma linha contra a janela (Versão JS). [cite: 280-290]
     */
    function cohenSutherlandClip_JS(x1, y1, x2, y2, xmin, ymin, xmax, ymax) {
        let code1 = computeOutcode(x1, y1, xmin, ymin, xmax, ymax);
        let code2 = computeOutcode(x2, y2, xmin, ymin, xmax, ymax);
        let accepted = false;

        while (true) {
            // Teste de Aceitação Trivial [cite: 282]
            if ((code1 | code2) === 0) {
                accepted = true;
                break;
            } 
            // Teste de Rejeição Trivial [cite: 284-285]
            else if ((code1 & code2) !== 0) {
                break;
            } 
            // Subdivisão [cite: 286]
            else {
                let codeOut = code1 !== 0 ? code1 : code2;
                let x = 0, y = 0;

                // Encontra a interseção [cite: 288, 303, 304]
                if (codeOut & TOP) {
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1);
                    y = ymax;
                } else if (codeOut & BOTTOM) {
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1);
                    y = ymin;
                } else if (codeOut & RIGHT) {
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1);
                    x = xmax;
                } else if (codeOut & LEFT) {
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1);
                    x = xmin;
                }

                // Atualiza o ponto que estava fora [cite: 289]
                if (codeOut === code1) {
                    x1 = x; y1 = y;
                    code1 = computeOutcode(x1, y1, xmin, ymin, xmax, ymax);
                } else {
                    x2 = x; y2 = y;
                    code2 = computeOutcode(x2, y2, xmin, ymin, xmax, ymax);
                }
            }
        }

        if (accepted) {
            return { accepted: true, x1: x1, y1: y1, x2: x2, y2: y2 };
        } else {
            return { accepted: false };
        }
    }

    // ==========================================================
    // FUNÇÕES DE DESENHO E LÓGICA DA PÁGINA
    // ==========================================================

    // Converte coordenadas do mundo (centro 0,0) para coordenadas do canvas (topo 0,0)
    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
    };

    // Desenha uma linha de (x1,y1) a (x2,y2) em coordenadas do MUNDO
    const drawLine = (x1, y1, x2, y2, color = 'black', lineWidth = 1) => {
        const p1 = worldToCanvas(x1, y1);
        const p2 = worldToCanvas(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#d3d0d0ff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2); // Eixo X
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height); // Eixo Y
        ctx.stroke();
    };

    // Desenha a janela de recorte na tela
    const drawClippingWindow = (xmin, ymin, xmax, ymax) => {
        const p1 = worldToCanvas(xmin, ymax); // Canto superior esquerdo
        const p2 = worldToCanvas(xmax, ymin); // Canto inferior direito
        
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]); // Linha tracejada
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
        ctx.setLineDash([]); // Reseta o tracejado
    };

    const clearAll = () => {
        stopAnimation(); // Para a animação se estiver rodando
        drawAxes();
        // Redesenha a janela de recorte ao limpar
        drawClippingWindow(
            parseFloat(clipXminInput.value), parseFloat(clipYminInput.value),
            parseFloat(clipXmaxInput.value), parseFloat(clipYmaxInput.value)
        );
        clipInfo.value = 'Pronto para recortar.';
    };

    // --- Lógica de Animação (NOVA) ---

    function animationLoop() {
        // 1. Limpa o canvas e desenha os eixos/janela
        drawAxes();
        const xmin = parseFloat(clipXminInput.value);
        const ymin = parseFloat(clipYminInput.value);
        const xmax = parseFloat(clipXmaxInput.value);
        const ymax = parseFloat(clipYmaxInput.value);
        drawClippingWindow(xmin, ymin, xmax, ymax);

        // 2. Calcula os novos pontos da linha
        // Comprimento maior que a diagonal (diagonal de 600x600 é ~849)
        const L = 500; // Metade do comprimento da linha (total 1000)

        // Rotaciona no sentido horário (diminui o ângulo)
        currentAngle -= 0.01; // Pequeno ângulo
        
        const rad = currentAngle;
        const cosA = Math.cos(rad);
        const sinA = Math.sin(rad);

        // Pontos da linha com centro em (0,0)
        const x1_orig = -L * cosA;
        const y1_orig = -L * sinA;
        const x2_orig = L * cosA;
        const y2_orig = L * sinA;
        
        // 3. Desenha a linha original (em cinza)
        drawLine(x1_orig, y1_orig, x2_orig, y2_orig, '#cccccc', 2);

        // 4. Aplica o recorte (usando a versão JS)
        const clipped = cohenSutherlandClip_JS(x1_orig, y1_orig, x2_orig, y2_orig, xmin, ymin, xmax, ymax);
        
        // 5. Desenha o resultado do recorte
        if (clipped.accepted) {
            drawLine(clipped.x1, clipped.y1, clipped.x2, clipped.y2, 'black', 2);
            clipInfo.value = `RECORTANDO...\nÂngulo: ${(currentAngle * 180 / Math.PI).toFixed(0)}°\n` +
                 `P1': (${clipped.x1.toFixed(1)}, ${clipped.y1.toFixed(1)})\n` +
                 `P2': (${clipped.x2.toFixed(1)}, ${clipped.y2.toFixed(1)})`;
        } else {
            clipInfo.value = `REJEITADA\nÂngulo: ${(currentAngle * 180 / Math.PI).toFixed(0)}°`;
        }
        
        // 6. Continua o loop
        animationId = requestAnimationFrame(animationLoop);
    }

    function toggleAnimation() {
        if (animationId) {
            stopAnimation();
        } else {
            // Inicia a animação
            currentAngle = 0; // Reseta o ângulo
            toggleAnimationBtn.textContent = "Parar Animação";
            clipLineBtn.disabled = true; // Desabilita o outro botão
            animationLoop();
        }
    }

    function stopAnimation() {
        if (animationId) {
            cancelAnimationFrame(animationId);
            animationId = null;
        }
        toggleAnimationBtn.textContent = "Aplicar Item 2";
        clipLineBtn.disabled = false; // Reabilita o outro botão
    }

    // --- Event Listeners ---

    // Botão Original (Estático, via API Python)
    clipLineBtn.addEventListener('click', async () => {
        clearAll(); // Limpa e para qualquer animação

        const line = {
            x1: parseFloat(lineX1Input.value), y1: parseFloat(lineY1Input.value),
            x2: parseFloat(lineX2Input.value), y2: parseFloat(lineY2Input.value)
        };
        const window = {
            xmin: parseFloat(clipXminInput.value), ymin: parseFloat(clipYminInput.value),
            xmax: parseFloat(clipXmaxInput.value), ymax: parseFloat(clipYmaxInput.value)
        };

        // 1. Desenha a linha original (em cinza claro)
        drawLine(line.x1, line.y1, line.x2, line.y2, '#cccccc', 2);

        // 2. Envia para a API Python para recortar
        const payload = { ...line, ...window };
        const response = await fetch('/api/clipping/clip_line', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        // 3. Processa o resultado da API
        if (data.accepted) {
            const [x1, y1, x2, y2] = data.coords;
            // 4. Desenha a linha recortada (em preto)
            drawLine(x1, y1, x2, y2, 'black', 2);
            clipInfo.value = `LINHA ACEITA :\nNovos pontos:\n(${x1}, ${y1}) para (${x2}, ${y2})`;
        } else {
            clipInfo.value = 'LINHA REJEITADA :\nCompletamente fora da janela.';
        }
    });

    // Novo Botão (Animação, via JS)
    toggleAnimationBtn.addEventListener('click', toggleAnimation);
    
    // Botão de Limpar
    clearBtn.addEventListener('click', clearAll);

    // Inicializa a tela
    clearAll();
});