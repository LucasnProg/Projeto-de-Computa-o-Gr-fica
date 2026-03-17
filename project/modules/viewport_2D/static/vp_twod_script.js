document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-2d');
    const canvasWorld = document.getElementById('canvas-mundo');
    const ctx = canvas.getContext('2d');
    const ctxWorld = canvasWorld.getContext('2d');

    const squareSizeInput = document.getElementById('square-size');
    const startXInput = document.getElementById('start-x');
    const startYInput = document.getElementById('start-y');
    const generateSquareBtn = document.getElementById('generate-square-btn');

    const transXInput = document.getElementById('trans-x');
    const transYInput = document.getElementById('trans-y');
    const addTransBtn = document.getElementById('add-translation-btn');

    const scaleXInput = document.getElementById('scale-x');
    const scaleYInput = document.getElementById('scale-y');
    const addScaleBtn = document.getElementById('add-scale-btn');

    const rotAngleInput = document.getElementById('rot-angle');
    const addRotBtn = document.getElementById('add-rotation-btn');

    const reflectXCheck = document.getElementById('reflect-x');
    const reflectYCheck = document.getElementById('reflect-y');
    const addReflectBtn = document.getElementById('add-reflection-btn');

    const shearXInput = document.getElementById('shear-x');
    const shearYInput = document.getElementById('shear-y');
    const addShearBtn = document.getElementById('add-shear-btn');

    const verticesInfo = document.getElementById('vertices-info');
    const queueLog = document.getElementById('queue-log');

    const applyQueueBtn = document.getElementById('apply-queue-btn');
    const clearQueueBtn = document.getElementById('clear-queue-btn');
    const clearBtn = document.getElementById('clear-btn');

    U_MAX = 150
    U_MIN = 30
    V_MAX = 200
    V_MIN = 20

    X_MAX = 300
    X_MIN = 0
    Y_MAX = 300
    Y_MIN = 0

    let originalObject = [];
    let currentObject = [];
    let transformQueue = [];

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#ccc';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.stroke();

        ctxWorld.clearRect(0, 0, width, height);
        ctxWorld.strokeStyle = '#ccc';
        ctxWorld.lineWidth = 1;
        ctxWorld.beginPath();
        ctxWorld.moveTo(width / 2, 0); ctxWorld.lineTo(width / 2, height);
        ctxWorld.moveTo(0, height / 2); ctxWorld.lineTo(width, height / 2);
        ctxWorld.stroke();
    };

    const drawPolygon = async (points) => {
        if (points.length < 2) return;

        const { width, height } = ctxWorld.canvas;
        const centerX = width / 2;
        const centerY = height / 2;

        ctxWorld.strokeStyle = 'black';
        ctxWorld.lineWidth = 1;
        ctxWorld.beginPath();

        ctxWorld.moveTo(centerX + points[0].x, centerY - points[0].y);
        for (let i = 1; i < points.length; i++) {
            ctxWorld.lineTo(centerX + points[i].x, centerY - points[i].y);
        }
        ctxWorld.closePath();
        ctxWorld.stroke();
        ctxWorld.setLineDash([]);

        try {
            const response = await fetch('/api/vp_twod/window_to_vp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ points: points })
            });

            if (!response.ok) throw new Error('Erro na conversão para Viewport');

            const data = await response.json();
            const unclippedPoints = data.unclipped;
            const clippedPoints = data.clipped;

            const { width, height } = ctx.canvas;
            const centerX = width / 2;
            const centerY = height / 2;

            ctx.strokeStyle = 'black';
            ctx.lineWidth = 1;
            ctx.beginPath();

            if (unclippedPoints && unclippedPoints.length >= 2) {
                ctx.strokeStyle = '#e4e4e4';
                ctx.lineWidth = 1;
                ctx.setLineDash([3, 3]);
                ctx.beginPath();
                ctx.moveTo(centerX + unclippedPoints[0].x, centerY - unclippedPoints[0].y);
                for (let i = 1; i < unclippedPoints.length; i++) {
                    ctx.lineTo(centerX + unclippedPoints[i].x, centerY - unclippedPoints[i].y);
                }
                ctx.closePath();
                ctx.stroke();
                ctx.setLineDash([]);

            }

            if (clippedPoints && clippedPoints.length >= 3) {
                ctx.fillStyle = '#f7f3f3b4';
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#000000';
                ctx.beginPath();
                ctx.moveTo(centerX + clippedPoints[0].x, centerY - clippedPoints[0].y);
                for (let i = 1; i < clippedPoints.length; i++) {
                    ctx.lineTo(centerX + clippedPoints[i].x, centerY - clippedPoints[i].y);
                }
                ctx.closePath();

                ctx.fill();
                ctx.stroke();
            }

        } catch (error) {
            console.error(error);
            alert("Erro de comunicação com a API ao desenhar a Viewport.");
        }
    };

    const redraw = async () => {
        drawAxes();
        drawWindow();
        drawVp()
        if (currentObject.length > 0) {
            drawPolygon(currentObject);
            updateInfoPanel();
        }
    };

    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
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

    const updateInfoPanel = () => {
        if (currentObject.length === 0) {
            verticesInfo.value = 'Nenhum objeto gerado.';
            return;
        }
        verticesInfo.value = currentObject.map((p, i) => `Vértice ${i + 1}: (${p.x.toFixed(2)}, ${p.y.toFixed(2)})`).join('\n');
    };

    const updateQueuePanel = () => {
        if (transformQueue.length === 0) {
            queueLog.value = 'Nenhuma transformação na fila.';
        } else {
            queueLog.value = transformQueue.map((item, index) => `${index + 1}. ${item.msg}`).join('\n');
        }
    };

    generateSquareBtn.addEventListener('click', async () => {
        const size = parseInt(squareSizeInput.value);
        const startX = parseInt(startXInput.value);
        const startY = parseInt(startYInput.value);

        originalObject = [
            { x: startX, y: startY },
            { x: startX + size, y: startY },
            { x: startX + size, y: startY + size },
            { x: startX, y: startY + size }
        ];
        currentObject = JSON.parse(JSON.stringify(originalObject));
        transformQueue = [];
        updateQueuePanel();
        drawWindow();
        drawVp();
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
        const tx = parseFloat(transXInput.value), ty = parseFloat(transYInput.value);
        addToQueue('translate', { tx, ty }, `Translação (${tx}, ${ty})`);
    });

    addScaleBtn.addEventListener('click', () => {
        const sx = parseFloat(scaleXInput.value), sy = parseFloat(scaleYInput.value);
        addToQueue('scale', { sx, sy }, `Escala (${sx}, ${sy})`);
    });

    addRotBtn.addEventListener('click', () => {
        const angle = parseFloat(rotAngleInput.value);
        addToQueue('rotate', { angle }, `Rotação (${angle}°)`);
    });

    addReflectBtn.addEventListener('click', () => {
        const reflect_x = reflectXCheck.checked;
        const reflect_y = reflectYCheck.checked;

        if (!reflect_x && !reflect_y) {
            alert("Selecione pelo menos um eixo para refletir!");
            return;
        }

        let msg = "Reflexão em ";
        if (reflect_x && reflect_y) msg += "X e Y";
        else if (reflect_x) msg += "X";
        else msg += "Y";

        addToQueue('reflection', { reflect_x, reflect_y }, msg);
    });

    addShearBtn.addEventListener('click', () => {
        const shx = parseFloat(shearXInput.value), shy = parseFloat(shearYInput.value);
        addToQueue('shear', { shx, shy }, `Cisalhamento (${shx}, ${shy})`);
    });



    applyQueueBtn.addEventListener('click', async () => {
        if (transformQueue.length === 0) {
            alert("A fila está vazia! Adicione transformações primeiro.");
            return;
        }

        applyQueueBtn.disabled = true;

        for (const action of transformQueue) {
            try {
                const response = await fetch('/api/vp_twod/transform', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: action.type, points: currentObject, params: action.params })
                });

                if (!response.ok) throw new Error('Erro na API');

                currentObject = await response.json();
                await redraw();

                await new Promise(r => setTimeout(r, 200));

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

    clearBtn.addEventListener('click', () => {
        originalObject = [];
        currentObject = [];
        transformQueue = [];
        updateQueuePanel();
        drawAxes();
        updateInfoPanel();
    });

    drawAxes();
    updateInfoPanel();
    updateQueuePanel();
    drawWindow();
    drawVp();
});