document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-3d');
    const ctx = canvas.getContext('2d');

    const verticesInput = document.getElementById('object-vertices');
    const edgesInput = document.getElementById('object-edges');
    const generateObjBtn = document.getElementById('generate-object-btn');

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

    const shearPlaneSelect = document.getElementById('shear-plane');
    const shearAInput = document.getElementById('shear-a');
    const shearBInput = document.getElementById('shear-b');
    const shearAxisSelect = document.getElementById('shear-axis');
    const applyShearBtn = document.getElementById('apply-shear-btn');

    const reflectPlaneSelect = document.getElementById('reflect-plane');
    const applyReflectBtn = document.getElementById('apply-reflection-btn');

    const historyLog = document.getElementById('history-log');
    const clearTransformsBtn = document.getElementById('clear-transforms-btn');

    const openGlBtn = document.getElementById("OpenGLBtn");

    let originalVertices = []; 
    let currentVertices = [];
    let currentEdges = [];
    let transformHistory = [];
    const BASE_TRANSFORM = { type: 'translate', tx: 0, ty: 0, tz: 0 };

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
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.stroke();
    };

    const drawEdges = (projectedPoints, edges) => {
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 1;

        edges.forEach(edge => {
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
        const formatItem = (item) => {
            switch (item.type) {
                case 'translate': return `Translação: T(${item.tx}, ${item.ty}, ${item.tz})`;
                case 'scale': return `Escala: S(${item.sx}, ${item.sy}, ${item.sz})`;
                case 'rotate': return `Rotação: R_${item.axis.toUpperCase()}(${item.angle}°)`;
                case 'shear': return `Cisalhamento: Eixo ${item.axis.toUpperCase()} (${item.sh1}, ${item.sh2})`;
                case 'reflect': return `Reflexão: Plano ${item.axis.toUpperCase()}`;
                default: return 'Transformação';
            }
        };
        historyLog.innerHTML = transformHistory.map(item => `${formatItem(item)}`).join('');
    };

    const render = async () => {
        if (originalVertices.length === 0) {
            drawAxes();
            return;
        }

        drawAxes();

        const payload = {
            vertices: originalVertices,
            transforms: transformHistory
        };

        try {
            const response = await fetch('/api/3d/render', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            currentVertices = data.new_object;
            updateHistoryLog();

            const projection = await fetch('/api/3d/project_object', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    vertices: currentVertices,
                    edges: currentEdges
                })
            });

            const projecao = await projection.json();

            drawEdges(projecao.projected_points, currentEdges);


        } catch (err) {
            console.error(err);
        }
    };


    openGlBtn.addEventListener('click', async () => {
        const payload = {
            vertices: currentVertices,
            edges: currentEdges,
        };

        try {
            const response = await fetch('/api/3d/opengl_view', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) alert("Erro ao abrir visualização 3D");
        } catch (error) {
            console.error("Erro:", error);
        }
    });

    generateObjBtn.addEventListener('click', () => {
        try {
            originalVertices = verticesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                if (parts.length !== 3 || parts.some(isNaN)) {
                    throw new Error(`Linha de vértice inválida: "${line}"`);
                }
                return { x: parts[0], y: parts[1], z: parts[2] };
            });

            currentVertices = JSON.parse(JSON.stringify(originalVertices));
        } catch (e) {
            alert(`Erro ao processar vértices: ${e.message}`);
            return;
        }

        try {
            currentEdges = edgesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                if (parts.length !== 2 || parts.some(isNaN)) {
                    throw new Error(`Linha de aresta inválida: "${line}"`);
                }
                return [parts[0], parts[1]];
            });
        } catch (e) {
            alert(`Erro ao processar arestas: ${e.message}`);
            return;
        }

        clearTransformsBtn.click();
    });

    clearTransformsBtn.addEventListener('click', () => {
        transformHistory = [BASE_TRANSFORM];
        render();
    });


    applyTransBtn.addEventListener('click', () => {
        transformHistory.push({
            type: 'translate',
            tx: parseFloat(transXInput.value),
            ty: parseFloat(transYInput.value),
            tz: parseFloat(transZInput.value)
        });
        render();
    });

    applyScaleBtn.addEventListener('click', () => {
        transformHistory.push({
            type: 'scale',
            sx: parseFloat(scaleXInput.value),
            sy: parseFloat(scaleYInput.value),
            sz: parseFloat(scaleZInput.value)
        });
        render();
    });

    applyRotBtn.addEventListener('click', () => {
        const axisRaw = rotAxisSelect.value;
        const axis = axisRaw.replace('R', '').toLowerCase();

        transformHistory.push({
            type: 'rotate',
            axis: axis,
            angle: parseFloat(rotAngleInput.value)
        });
        render();
    });


    applyShearBtn.addEventListener('click', () => {
        transformHistory.push({
            type: 'shear',
            axis: shearAxisSelect.value,
            sh1: parseFloat(shearAInput.value),
            sh2: parseFloat(shearBInput.value)
        });
        render();
    });

    applyReflectBtn.addEventListener('click', () => {
        transformHistory.push({
            type: 'reflect',
            axis: reflectPlaneSelect.value
        });
        render();
    });

    generateObjBtn.click();
});