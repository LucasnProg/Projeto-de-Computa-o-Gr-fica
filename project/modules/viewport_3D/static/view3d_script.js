document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-3d');
    const ctx = canvas.getContext('2d');

    const verticesInput = document.getElementById('object-vertices');
    const edgesInput = document.getElementById('object-edges');
    const generateObjBtn = document.getElementById('generate-object-btn');

    const transXInput = document.getElementById('trans-x');
    const transYInput = document.getElementById('trans-y');
    const transZInput = document.getElementById('trans-z');
    const addTransBtn = document.getElementById('add-translation-btn');

    const scaleXInput = document.getElementById('scale-x');
    const scaleYInput = document.getElementById('scale-y');
    const scaleZInput = document.getElementById('scale-z');
    const addScaleBtn = document.getElementById('add-scale-btn');

    const rotAxisSelect = document.getElementById('rot-axis');
    const rotAngleInput = document.getElementById('rot-angle');
    const addRotBtn = document.getElementById('add-rotation-btn');

    const reflectPlaneSelect = document.getElementById('reflect-plane');
    const addReflectBtn = document.getElementById('add-reflection-btn');

    const shearAxisSelect = document.getElementById('shear-axis');
    const shearAInput = document.getElementById('shear-a');
    const shearBInput = document.getElementById('shear-b');
    const addShearBtn = document.getElementById('add-shear-btn');

    const queueLog = document.getElementById('queue-log');
    const applyQueueBtn = document.getElementById('apply-queue-btn');
    const clearQueueBtn = document.getElementById('clear-queue-btn');
    const clearBtn = document.getElementById('clear-transforms-btn');
    const openGlBtn = document.getElementById('open-opengl-btn');

    const U_MAX = 150, U_MIN = 30;
    const V_MAX = 200, V_MIN = 20;
    const X_MAX = 300, X_MIN = 0;
    const Y_MAX = 300, Y_MIN = 0;

    let currentObject = [];
    let currentEdges = [];
    let transformQueue = [];

    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#ccc';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.stroke();
    };

    const drawWindow = () => {
        const p1 = worldToCanvas(X_MIN, Y_MAX);
        const p2 = worldToCanvas(X_MAX, Y_MIN);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 1;
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
        ctx.setLineDash([]);
    };

    const drawVp = () => {
        const p1 = worldToCanvas(U_MIN, V_MAX);
        const p2 = worldToCanvas(U_MAX, V_MIN);
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 1;
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
        ctx.setLineDash([]);
    };

    const drawObject = async (points) => {
        if (points.length < 2) return;
        try {
            const response = await fetch('/api/vp_threed/window_to_vp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ points: points, edges: currentEdges })
            });

            if (!response.ok) throw new Error('Erro na conversão para Viewport');

            const data = await response.json();
            const unclippedPoints = data.unclipped;
            const clippedEdges = data.clipped_edges;

            if (unclippedPoints && unclippedPoints.length > 0) {
                ctx.strokeStyle = '#aaaaaa';
                ctx.lineWidth = 1;
                ctx.setLineDash([3, 3]);

                currentEdges.forEach(edge => {
                    if (edge[0] >= unclippedPoints.length || edge[1] >= unclippedPoints.length) return;
                    const p1 = worldToCanvas(unclippedPoints[edge[0]].x, unclippedPoints[edge[0]].y);
                    const p2 = worldToCanvas(unclippedPoints[edge[1]].x, unclippedPoints[edge[1]].y);

                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                });
                ctx.setLineDash([]);
            }

            if (clippedEdges && clippedEdges.length > 0) {
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 1;
                ctx.setLineDash([]);

                ctx.beginPath();
                clippedEdges.forEach(edge => {
                    const p1 = worldToCanvas(edge.x1, edge.y1);
                    const p2 = worldToCanvas(edge.x2, edge.y2);

                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                });
                ctx.stroke();
            }

        } catch (error) {
            console.error(error);
            alert("Erro de comunicação com a API ao desenhar a Viewport 3D.");
        }
    };

    const redraw = async () => {
        drawAxes();
        drawWindow();
        drawVp();
        if (currentObject.length > 0) {
            await drawObject(currentObject);
        }
    };

    const updateQueuePanel = () => {
        if (transformQueue.length === 0) {
            queueLog.value = 'Nenhuma transformação na fila.';
        } else {
            queueLog.value = transformQueue.map((item, index) => `${index + 1}. ${item.msg}`).join('\n');
        }
    };


    const loadObject = () => {
        try {
            currentObject = verticesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                return { x: parts[0], y: parts[1], z: parts[2] };
            });
            currentEdges = edgesInput.value.trim().split('\n').map(line => {
                const parts = line.split(',').map(Number);
                return [parts[0], parts[1]];
            });
        } catch (e) {
            console.error("Erro ao ler os vértices/arestas");
        }
    };

    generateObjBtn.addEventListener('click', async () => {
        loadObject();
        transformQueue = [];
        updateQueuePanel();
        await redraw();
    });

    const addToQueue = (type, params, msg) => {
        if (currentObject.length === 0) {
            alert("Gere um objeto primeiro!");
            return;
        }
        transformQueue.push({ type, params, msg });
        updateQueuePanel();
    };

    addTransBtn.addEventListener('click', () => {
        const tx = parseFloat(transXInput.value), ty = parseFloat(transYInput.value), tz = parseFloat(transZInput.value);
        addToQueue('translate', { tx, ty, tz }, `Translação (${tx}, ${ty}, ${tz})`);
    });

    addScaleBtn.addEventListener('click', () => {
        const sx = parseFloat(scaleXInput.value), sy = parseFloat(scaleYInput.value), sz = parseFloat(scaleZInput.value);
        addToQueue('scale', { sx, sy, sz }, `Escala (${sx}, ${sy}, ${sz})`);
    });

    addRotBtn.addEventListener('click', () => {
        const axis = rotAxisSelect.value;
        const angle = parseFloat(rotAngleInput.value);
        addToQueue('rotate', { axis, angle }, `Rotação em ${axis.toUpperCase()} (${angle}°)`);
    });

    addReflectBtn.addEventListener('click', () => {
        const axis = reflectPlaneSelect.value;
        addToQueue('reflection', { axis }, `Reflexão no Plano ${axis.toUpperCase()}`);
    });

    addShearBtn.addEventListener('click', () => {
        const axis = shearAxisSelect.value;
        const sh1 = parseFloat(shearAInput.value), sh2 = parseFloat(shearBInput.value);
        addToQueue('shear', { axis, sh1, sh2 }, `Cisalhamento no Eixo ${axis.toUpperCase()} (${sh1}, ${sh2})`);
    });

    applyQueueBtn.addEventListener('click', async () => {
        if (transformQueue.length === 0) {
            alert("A fila está vazia! Adicione transformações primeiro.");
            return;
        }

        applyQueueBtn.disabled = true;

        for (const action of transformQueue) {
            try {
                const response = await fetch('/api/vp_threed/transform', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: action.type, points: currentObject, params: action.params })
                });

                if (!response.ok) throw new Error('Erro na API');

                currentObject = await response.json();
                await redraw();

                await new Promise(r => setTimeout(r, 400));
            } catch (error) {
                console.error(error);
                alert(`Erro ao aplicar a transformação: ${action.msg}`);
                break;
            }
        }

        transformQueue = [];
        updateQueuePanel();
        applyQueueBtn.disabled = false;
    });

    clearQueueBtn.addEventListener('click', () => {
        transformQueue = [];
        updateQueuePanel();
    });

    clearBtn.addEventListener('click', async () => {
        loadObject();
        transformQueue = [];
        updateQueuePanel();
        await redraw();
    });

    openGlBtn.addEventListener('click', async () => {
        if (currentObject.length === 0) {
            alert("Gere o objeto primeiro.");
            return;
        }

        const sanitizedEdges = currentEdges.map(edge => [
            parseInt(edge[0]),
            parseInt(edge[1])
        ]);

        const payload = {
            points: currentObject,
            edges: sanitizedEdges
        };

        try {
            const response = await fetch('/api/vp_threed/opengl_view', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) alert("Erro ao abrir visualização 3D");
        } catch (error) {
            console.error("Erro:", error);
        }
    });

    loadObject();
    redraw();
    updateQueuePanel();
});