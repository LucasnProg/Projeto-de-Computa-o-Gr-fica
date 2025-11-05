document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-3d');
    const ctx = canvas.getContext('2d');
    
    // --- Seletores dos Controles de Objeto ---
    const verticesInput = document.getElementById('object-vertices');
    const edgesInput = document.getElementById('object-edges');
    const generateObjBtn = document.getElementById('generate-object-btn');
    
    // --- Seletores dos Controles de Transformação ---
    const transXInput = document.getElementById('trans-x');
    const transYInput = document.getElementById('trans-y');
    const transZInput = document.getElementById('trans-z');
    const applyTransBtn = document.getElementById('apply-translation-btn');

    const scaleXInput = document.getElementById('scale-x');
    const scaleYInput = document.getElementById('scale-y');
    const scaleZInput = document.getElementById('scale-z');
    const applyScaleBtn = document.getElementById('apply-scale-btn');

    const rotAxisSelect = document.getElementById('rot-axis');
    const rotAngleInput = document.getElementById('rot-angle');
    const applyRotBtn = document.getElementById('apply-rotation-btn');

    // NOVOS Seletores
    const shearPlaneSelect = document.getElementById('shear-plane');
    const shearAInput = document.getElementById('shear-a');
    const shearBInput = document.getElementById('shear-b');
    const applyShearBtn = document.getElementById('apply-shear-btn');
    
    const reflectPlaneSelect = document.getElementById('reflect-plane');
    const applyReflectBtn = document.getElementById('apply-reflection-btn');

    // --- Seletores do Histórico ---
    const historyLog = document.getElementById('history-log');
    const clearTransformsBtn = document.getElementById('clear-transforms-btn');

    // --- Estado da Aplicação ---
    // Removemos os objetos fixos, eles agora vêm do usuário
    let currentVertices = [];
    let currentEdges = [];
    let transformHistory = [];
    const BASE_TRANSFORM = 'T(100,50,0)'; // Posição inicial

    // --- Funções de Desenho ---
    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#d3d0d0ff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2); // X
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height); // Y
        ctx.stroke();
    };

    // Modificado para aceitar arestas como argumento
    const drawEdges = (projectedPoints, edges) => {
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        
        edges.forEach(edge => {
            // Garante que os índices da aresta são válidos
            if (edge[0] >= projectedPoints.length || edge[1] >= projectedPoints.length) {
                console.warn("Índice de aresta fora dos limites:", edge);
                return;
            }
            const p1 = projectedPoints[edge[0]];
            const p2 = projectedPoints[edge[1]];
            
            const p1_canvas = worldToCanvas(p1.x, p1.y);
            const p2_canvas = worldToCanvas(p2.x, p2.y);
            
            ctx.beginPath();
            ctx.moveTo(p1_canvas.x, p1_canvas.y);
            ctx.lineTo(p2_canvas.x, p2_canvas.y);
            ctx.stroke();
        });
    };

    const updateHistoryLog = () => {
        historyLog.innerHTML = '<ul>' + transformHistory.map(item => `<li>${item}</li>`).join('') + '</ul>';
    };

    // --- Função Principal de Renderização ---
    const render = async () => {
        if (currentVertices.length === 0) {
            drawAxes();
            return; // Não renderiza se não houver objeto
        }
        
        drawAxes();
        
        const payload = {
            vertices: currentVertices,     // Usa os vértices definidos pelo usuário
            transforms: transformHistory
        };

        try {
            const response = await fetch('/api/3d/render', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            
            drawEdges(data.projected_points, currentEdges); // Usa as arestas do usuário
            updateHistoryLog();

        } catch (err) {
            console.error(err);
        }
    };
    
    // --- Lógica da UI (Event Listeners) ---

    // NOVO: Gerador de Objeto
    generateObjBtn.addEventListener('click', () => {
        // 1. Parse Vértices
        try {
            currentVertices = verticesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                if (parts.length !== 3 || parts.some(isNaN)) {
                    throw new Error(`Linha de vértice inválida: "${line}"`);
                }
                return { x: parts[0], y: parts[1], z: parts[2] };
            });
        } catch (e) {
            alert(`Erro ao processar vértices: ${e.message}`);
            return;
        }

        // 2. Parse Arestas (Base 0)
        try {
            currentEdges = edgesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                if (parts.length !== 2 || parts.some(isNaN)) {
                    throw new Error(`Linha de aresta inválida: "${line}"`);
                }
                // Converte de índice 1 (humano) para 0 (array), se preferir.
                // Mas o exemplo é base 0, então mantemos.
                return [parts[0], parts[1]];
            });
        } catch (e) {
            alert(`Erro ao processar arestas: ${e.message}`);
            return;
        }

        // 3. Reseta transformações e renderiza
        clearTransformsBtn.click();
    });

    clearTransformsBtn.addEventListener('click', () => {
        transformHistory = [BASE_TRANSFORM];
        render();
    });
    
    // --- Botões "Aplicar" ---

    applyTransBtn.addEventListener('click', () => {
        const tx = parseFloat(transXInput.value);
        const ty = parseFloat(transYInput.value);
        const tz = parseFloat(transZInput.value);
        transformHistory.push(`T(${tx},${ty},${tz})`);
        render();
    });

    applyScaleBtn.addEventListener('click', () => {
        const sx = parseFloat(scaleXInput.value);
        const sy = parseFloat(scaleYInput.value);
        const sz = parseFloat(scaleZInput.value);
        transformHistory.push(`S(${sx},${sy},${sz})`);
        render();
    });

    applyRotBtn.addEventListener('click', () => {
        const axis = rotAxisSelect.value; // Rx, Ry, ou Rz
        const angle = parseFloat(rotAngleInput.value);
        transformHistory.push(`${axis}(${angle})`);
        render();
    });
    
    // NOVO: Listeners para Cisalhamento e Reflexão
    
    applyShearBtn.addEventListener('click', () => {
        const plane = shearPlaneSelect.value; // Sh_xy, Sh_xz, Sh_yz
        const a = parseFloat(shearAInput.value);
        const b = parseFloat(shearBInput.value);
        transformHistory.push(`${plane}(${a},${b})`);
        render();
    });

    applyReflectBtn.addEventListener('click', () => {
        const plane = reflectPlaneSelect.value; // Rf_xy, Rf_xz, Rf_yz
        transformHistory.push(`${plane}()`);
        render();
    });

    // Renderização inicial
    // Simula um clique no botão para carregar o objeto padrão (cubo)
    generateObjBtn.click();
});