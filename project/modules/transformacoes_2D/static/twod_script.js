document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-2d');
    const ctx = canvas.getContext('2d');

    const squareSizeInput = document.getElementById('square-size');
    const startXInput = document.getElementById('start-x');
    const startYInput = document.getElementById('start-y');
    const generateSquareBtn = document.getElementById('generate-square-btn');

    const transXInput = document.getElementById('trans-x');
    const transYInput = document.getElementById('trans-y');
    const applyTransBtn = document.getElementById('apply-translation-btn');

    const scaleXInput = document.getElementById('scale-x');
    const scaleYInput = document.getElementById('scale-y');
    const applyScaleBtn = document.getElementById('apply-scale-btn');

    const rotAngleInput = document.getElementById('rot-angle');
    const applyRotBtn = document.getElementById('apply-rotation-btn');

    const reflectXCheck = document.getElementById('reflect-x');
    const reflectYCheck = document.getElementById('reflect-y');
    const applyReflectBtn = document.getElementById('apply-reflection-btn');

    const shearXInput = document.getElementById('shear-x');
    const shearYInput = document.getElementById('shear-y');
    const applyShearBtn = document.getElementById('apply-shear-btn');

    const verticesInfo = document.getElementById('vertices-info');
    const clearBtn = document.getElementById('clear-btn');
    const historyLog = document.getElementById('history-log');

    let originalObject = [], currentObject = [], transformHistory = [];


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

    const drawPolygon = (points) => {
        if (points.length < 2) return;
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;

        ctx.strokeStyle = 'black';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(centerX + points[0].x, centerY - points[0].y);
        for (let i = 1; i < points.length; i++) {
            ctx.lineTo(centerX + points[i].x, centerY - points[i].y);
        }
        ctx.closePath();
        ctx.stroke();
    };

    const redraw = () => {
        drawAxes();
        if (currentObject.length > 0) {
            drawPolygon(currentObject);
            updateInfoPanel();
        }
    };


    const updateInfoPanel = () => {
        if (currentObject.length === 0) {
            verticesInfo.value = 'Nenhum objeto gerado.';
            historyLog.value = 'Nenhuma transformação aplicada.';
            return;
        }

        verticesInfo.value = currentObject.map((p, i) => `Vértice ${i + 1}: (${p.x.toFixed(2)}, ${p.y.toFixed(2)})`).join('\n');

        if (transformHistory.length === 0) {
            historyLog.value = 'Nenhuma transformação aplicada.';
        } else {
            historyLog.value = transformHistory.map((item, index) => `${index + 1}. ${item}`).join('\n');
        }
    };


    generateSquareBtn.addEventListener('click', () => {
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
        transformHistory = [];
        redraw();
    });

    const applyTransformation = async (type, params, historyMsg) => {
        if (currentObject.length === 0) {
            alert("Gere um objeto primeiro!");
            return;
        }
        try {
            const response = await fetch('/api/twod/transform', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: type, points: currentObject, params: params })
            });

            if (!response.ok) throw new Error('Erro na API');

            currentObject = await response.json();
            transformHistory.push(historyMsg);
            redraw();
        } catch (error) {
            console.error(error);
            alert("Erro ao aplicar transformação.");
        }
    };

    applyTransBtn.addEventListener('click', () => {
        const tx = parseFloat(transXInput.value), ty = parseFloat(transYInput.value);
        applyTransformation('translate', { tx, ty }, `Translação(${tx}, ${ty})`);
    });

    applyScaleBtn.addEventListener('click', () => {
        const sx = parseFloat(scaleXInput.value), sy = parseFloat(scaleYInput.value);
        applyTransformation('scale', { sx, sy }, `Escala(${sx}, ${sy})`);
    });

    applyRotBtn.addEventListener('click', () => {
        const angle = parseFloat(rotAngleInput.value);
        applyTransformation('rotate', { angle }, `Rotação(${angle}°)`);
    });

    applyReflectBtn.addEventListener('click', () => {
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

        applyTransformation('reflection', { reflect_x, reflect_y }, msg);
    });

    applyShearBtn.addEventListener('click', () => {
        const shx = parseFloat(shearXInput.value), shy = parseFloat(shearYInput.value);
        applyTransformation('shear', { shx, shy }, `Cisalhamento(${shx}, ${shy})`);
    });

    clearBtn.addEventListener('click', () => {
        originalObject = [];
        currentObject = [];
        transformHistory = [];
        drawAxes();
        updateInfoPanel();
    });

    drawAxes();
    updateInfoPanel();
});