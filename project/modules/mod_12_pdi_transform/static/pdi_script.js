document.addEventListener('DOMContentLoaded', () => {
    // Seletores dos Canvas
    const canvasOrig = document.getElementById('canvas-original');
    const ctxOrig = canvasOrig.getContext('2d');
    const canvasTrans = document.getElementById('canvas-transform');
    const ctxTrans = canvasTrans.getContext('2d');

    // Seletor do Input de Imagem
    const imageUpload = document.getElementById('image-upload');

    // Seletores dos Controles de Transformação
    const transXInput = document.getElementById('trans-x');
    const transYInput = document.getElementById('trans-y');
    const scaleXInput = document.getElementById('scale-x');
    const scaleYInput = document.getElementById('scale-y');
    const rotAngleInput = document.getElementById('rot-angle');
    const shearXInput = document.getElementById('shear-x');
    const shearYInput = document.getElementById('shear-y');
    const reflectXCheck = document.getElementById('reflect-x');
    const reflectYCheck = document.getElementById('reflect-y');

    const applyBtn = document.getElementById('apply-transform-btn');
    const clearBtn = document.getElementById('clear-btn');

    // Armazena a imagem carregada pelo usuário
    let loadedImage = null;

    // --- Funções de Desenho ---

    function drawAxes(ctx) {
        ctx.strokeStyle = '#d3d0d0ff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, ctx.canvas.height / 2); ctx.lineTo(ctx.canvas.width, ctx.canvas.height / 2); // Eixo X
        ctx.moveTo(ctx.canvas.width / 2, 0); ctx.lineTo(ctx.canvas.width / 2, ctx.canvas.height); // Eixo Y
        ctx.stroke();
    }

    function resetCanvas(ctx) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        drawAxes(ctx);
    }

    // Carrega a imagem do input e a desenha no canvas "Original"
    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                loadedImage = img; // Salva a imagem
                resetCanvas(ctxOrig);
                // Desenha a imagem original centrada
                const x = (ctxOrig.canvas.width - img.width) / 2;
                const y = (ctxOrig.canvas.height - img.height) / 2;
                ctxOrig.drawImage(img, x, y);
                // Aplica a transformação inicial
                applyTransformations();
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });

    /**
     * Aplica as transformações espaciais na imagem.
     * Esta é a implementação PDI (baseada no Ogê Marques) usando a API do Canvas.
     */
    function applyTransformations() {
        if (!loadedImage) return;

        resetCanvas(ctxTrans);

        // Pega os valores
        const tx = parseFloat(transXInput.value);
        const ty = parseFloat(transYInput.value);
        const sx = parseFloat(scaleXInput.value);
        const sy = parseFloat(scaleYInput.value);
        const angle = parseFloat(rotAngleInput.value) * (Math.PI / 180); // para radianos
        const shx = parseFloat(shearXInput.value);
        const shy = parseFloat(shearYInput.value);
        const rfx = reflectXCheck.checked;
        const rfy = reflectYCheck.checked;

        // --- Lógica de Transformação Espacial (PDI) ---
        //
        // (1).pdf"]

        // 1. Salva o estado do canvas
        ctxTrans.save();

        // 2. Define o centro do canvas (0,0) para o meio da tela
        //    Isso torna as transformações (especialmente rotação) mais intuitivas
        ctxTrans.translate(ctxTrans.canvas.width / 2, ctxTrans.canvas.height / 2);

        // 3. Aplica as transformações em ordem
        //    (Translação, Rotação, Escala, Cisalhamento, Reflexão)
        //    Note que as transformações do canvas são aplicadas na ordem inversa (LIFO).

        // --- Matriz de Transformação Afim ---
        // O canvas nos permite aplicar a matriz de transformação 2D diretamente
        // M = T * R * Rf * S * Sh

        // Translação
        ctxTrans.translate(tx, -ty); // Y do canvas é invertido

        // Rotação (em torno do (0,0) do canvas, que agora é o centro)
        ctxTrans.rotate(-angle); // Ângulo negativo para rotação "horária" padrão

        // Reflexão (é apenas uma escala negativa)
        // (1).pdf"]
        ctxTrans.scale(rfy ? -1 : 1, rfx ? -1 : 1);

        // Escala
        ctxTrans.scale(sx, sy);

        // Cisalhamento
        // A função ctx.transform() multiplica a matriz atual
        // Matriz de Cisalhamento:
        // | 1   shx |
        // | shy 1   |
        ctxTrans.transform(1, shy, shx, 1, 0, 0);

        // 4. Desenha a imagem
        // Desenha a imagem centrada na origem (0,0) do canvas transformado
        const x = -loadedImage.width / 2;
        const y = -loadedImage.height / 2;
        ctxTrans.drawImage(loadedImage, x, y);

        // 5. Restaura o estado do canvas
        // Isso remove todas as transformações para a próxima renderização
        ctxTrans.restore();
    }

    // --- Event Listeners ---
    applyBtn.addEventListener('click', applyTransformations);

    clearBtn.addEventListener('click', () => {
        // Reseta os valores dos inputs
        transXInput.value = 0;
        transYInput.value = 0;
        scaleXInput.value = 1.0;
        scaleYInput.value = 1.0;
        rotAngleInput.value = 0;
        shearXInput.value = 0;
        shearYInput.value = 0;
        reflectXCheck.checked = false;
        reflectYCheck.checked = false;

        // Redesenha
        if (loadedImage) {
            resetCanvas(ctxOrig);
            const x = (ctxOrig.canvas.width - loadedImage.width) / 2;
            const y = (ctxOrig.canvas.height - loadedImage.height) / 2;
            ctxOrig.drawImage(loadedImage, x, y);
        } else {
            resetCanvas(ctxOrig);
        }
        applyTransformations();
    });

    // Inicializa os canvas
    resetCanvas(ctxOrig);
    resetCanvas(ctxTrans);
});