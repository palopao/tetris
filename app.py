import streamlit as st
import json

st.set_page_config(
    page_title="Tetris - Streamlit",
    layout="centered",
    initial_sidebar_state="collapsed"
)

INITIAL_SCORES = [
    {"nome": "José Torres", "pontos": 149083},
]

initial_scores_json = json.dumps(INITIAL_SCORES)

html_game_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
    html, body {{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
        background-color: transparent;
        color: white;
        font-family: system-ui, -apple-system, sans-serif;
        user-select: none;
        -webkit-user-select: none;
    }}
    #game-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        padding: 5px 10px;
    }}
    #header-container {{
        text-align: center;
        width: 100%;
        margin-bottom: 8px;
    }}
    .ascii-title {{
        font-family: monospace;
        font-weight: bold;
        font-size: 10px;
        line-height: 1.1;
        margin: 0 auto;
        white-space: pre;
        display: inline-block;
        text-align: left;
    }}
    .c-red {{ color: #ff4d4d; }}
    .c-orange {{ color: #ff8800; }}
    .c-yellow {{ color: #ffcc00; }}
    .c-green {{ color: #4dff4d; }}
    .c-cyan {{ color: #00ccff; }}
    .c-purple {{ color: #b366ff; }}
    .c-gray {{ color: #888888; }}

    /* HUD Centrado e Espaçado Uniformemente */
    #hud {{
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        max-width: 530px;
        font-weight: bold;
        font-size: 13px;
        color: #ddd;
        background: #1e1e24;
        padding: 10px 0;
        border-radius: 6px;
        box-sizing: border-box;
        margin-bottom: 10px;
    }}
    #hud > div {{
        flex: 1;
        text-align: center;
    }}

    #main-layout {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: flex-start;
        justify-content: center;
        width: 100%;
        max-width: 530px;
    }}
    #sidebar-left {{
        width: 110px;
        background: #18181c;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    #sidebar-left h4 {{
        margin: 0 0 8px 0;
        font-size: 12px;
        text-align: center;
        border-bottom: 1px solid #444;
        padding-bottom: 4px;
        color: #ffbd45;
        width: 100%;
    }}
    #nextCanvas {{
        background-color: #111;
        border: 1px solid #333;
        border-radius: 4px;
        display: block;
    }}
    #canvas-holder {{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        touch-action: none;
    }}
    #gameCanvas {{
        background-color: #111;
        border: 2px solid #333;
        border-radius: 4px;
        display: block;
        touch-action: none;
    }}
    #sidebar-scores {{
        width: 130px;
        background: #18181c;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px;
        box-sizing: border-box;
        max-height: 504px;
        overflow-y: auto;
    }}
    #sidebar-scores h4 {{
        margin: 0 0 8px 0;
        font-size: 12px;
        text-align: center;
        border-bottom: 1px solid #444;
        padding-bottom: 4px;
        color: #ffbd45;
    }}

    /* Nome em cima e Pontuação em baixo */
    .score-item {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        font-size: 11px;
        margin-bottom: 6px;
        padding-bottom: 4px;
        border-bottom: 1px solid #26262e;
    }}
    .score-item b {{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 100%;
        color: #ffffff;
    }}
    .score-item span {{
        color: #aaa;
        font-size: 10px;
        margin-top: 2px;
    }}

    .controls {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        width: 100%;
        max-width: 530px;
        margin-top: 10px;
    }}
    button {{
        background-color: #262730;
        color: white;
        border: 1px solid #464b5d;
        padding: 12px 6px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
        cursor: pointer;
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
    }}
    button:active {{
        background-color: #3f4252;
    }}
    #overlay {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.92);
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        width: 200px;
        border: 1px solid #555;
        z-index: 10;
    }}
    input[type="text"] {{
        width: 90%;
        padding: 8px;
        margin: 10px 0;
        border-radius: 4px;
        border: 1px solid #666;
        background-color: #222;
        color: white;
        box-sizing: border-box;
    }}
    .keyboard-hint {{
        font-size: 11px;
        color: #aaa;
        text-align: center;
        margin: 6px 0 0 0;
    }}

    /* Ajustes para Ecrãs Pequenos / Telemóveis */
    @media (max-width: 540px) {{
        .ascii-title {{
            font-size: 7px;
        }}
        #hud {{
            font-size: 11px;
            padding: 8px 0;
        }}
        #main-layout {{
            justify-content: center;
            gap: 8px;
        }}
        #sidebar-left {{
            width: 80px;
            padding: 4px;
        }}
        #nextCanvas {{
            width: 60px;
            height: 60px;
        }}
        #gameCanvas {{
            width: 200px;
            height: 400px;
        }}
        #sidebar-scores {{
            width: 100%;
            max-width: 290px;
            max-height: 180px;
            margin-top: 4px;
        }}
    }}
</style>
</head>
<body>

<div id="game-container">
    <div id="header-container">
        <pre class="ascii-title">
<span class="c-red">   ______</span><span class="c-orange"> ______</span><span class="c-yellow"> ______</span><span class="c-green"> ____</span><span class="c-cyan">   ____</span><span class="c-purple"> _____</span>
<span class="c-red">  /_  __/</span><span class="c-orange">/ ____/</span><span class="c-yellow">/_  __/</span><span class="c-green">/ __ \\</span><span class="c-cyan"> /  _/</span><span class="c-purple">/ ___/</span>
<span class="c-red">   / /</span><span class="c-orange">  / __/</span><span class="c-yellow">    / /</span><span class="c-green">  / /_/ /</span><span class="c-cyan"> / /</span><span class="c-purple">  \\__ \\</span>
<span class="c-red">  / /</span><span class="c-orange">  / /___</span><span class="c-yellow">   / /</span><span class="c-green">  / _, _/</span><span class="c-cyan">_/ /</span><span class="c-purple">  ___/ /</span>
<span class="c-red"> /_/</span><span class="c-orange">  /_____/</span><span class="c-yellow">  /_/</span><span class="c-green">  /_/ |_/</span><span class="c-cyan">/___/</span><span class="c-purple"> /____/</span>
          <span class="c-gray">(por José Torres)</span>
        </pre>
    </div>

    <div id="hud">
        <div>Pontos: <span id="scoreVal">0</span></div>
        <div>Nível: <span id="levelVal">1</span></div>
        <div>Linhas: <span id="linesVal">0</span></div>
    </div>

    <div id="main-layout">
        <div id="sidebar-left">
            <h4>Próxima</h4>
            <canvas id="nextCanvas" width="80" height="80"></canvas>
        </div>

        <div id="canvas-holder">
            <canvas id="gameCanvas"></canvas>
            <div id="overlay">
                <h3 id="overlayTitle" style="margin-top:0;">Tetris</h3>
                <p id="overlayMsg" style="font-size:13px; color:#ccc;">Clique para começar</p>
                <button id="startBtn" onclick="startGame()" style="width:100%; padding:10px;">Iniciar Jogo</button>
                <div id="scoreForm" style="display:none;">
                    <input type="text" id="playerName" placeholder="O seu nome" maxlength="12" />
                    <br/>
                    <button id="saveBtn" onclick="submitScore()" style="width:100%; padding:10px; background-color:#2e7d32;">Guardar Pontuação</button>
                    <button id="cancelBtn" onclick="cancelScore()" style="width:100%; padding:6px; margin-top:8px; background-color:transparent; border:1px solid #666; color:#bbb; border-radius:4px; font-weight:bold; cursor:pointer;">✕</button>
                </div>
            </div>
        </div>

        <div id="sidebar-scores">
            <h4>Classificação</h4>
            <div id="scoresList"></div>
        </div>
    </div>

    <div class="controls">
        <button id="btnRotate">Rodar</button>
        <button id="btnLeft">Esquerda</button>
        <button id="btnRight">Direita</button>
        <button id="btnDown">Baixar</button>
        <button id="btnDrop">Queda</button>
        <button id="btnPause">Pausar</button>
    </div>

    <div class="keyboard-hint">
        <p><strong>Computador:<br></strong> Setas / A/D (mover) • Seta Cima / W (rodar) • P (pausar)</p>
        <p><strong>Telemóvel:<br></strong> Deslizar no jogo (mover) • Toque (rodar)</p>
    </div>
</div>

<script>
const INITIAL_SCORES = {initial_scores_json};
const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 25;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = COLS * BLOCK_SIZE;
canvas.height = ROWS * BLOCK_SIZE;

const nextCanvas = document.getElementById('nextCanvas');
const nextCtx = nextCanvas.getContext('2d');

const COLORS = [
    "#00F0F0", "#0000F0", "#F0A000", "#F0F000", "#00F000", "#A000F0", "#F00000"
];

const SHAPES = [
    // 0: I
    [
        [[0, 0], [1, 0], [2, 0], [3, 0]],
        [[2, -1], [2, 0], [2, 1], [2, 2]],
        [[0, 1], [1, 1], [2, 1], [3, 1]],
        [[1, -1], [1, 0], [1, 1], [1, 2]]
    ],
    // 1: J
    [
        [[0, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [2, 0], [1, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [2, 2]],
        [[1, 0], [1, 1], [1, 2], [0, 2]]
    ],
    // 2: L
    [
        [[0, 1], [1, 1], [2, 1], [2, 0]],
        [[1, 0], [1, 1], [1, 2], [2, 2]],
        [[0, 1], [1, 1], [2, 1], [0, 2]],
        [[0, 0], [1, 0], [1, 1], [1, 2]]
    ],
    // 3: O
    [
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 0], [1, 0], [0, 1], [1, 1]]
    ],
    // 4: S
    [
        [[1, 0], [2, 0], [0, 1], [1, 1]],
        [[1, 0], [1, 1], [2, 1], [2, 2]],
        [[1, 1], [2, 1], [0, 2], [1, 2]],
        [[0, 0], [0, 1], [1, 1], [1, 2]]
    ],
    // 5: T
    [
        [[1, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [1, 1], [2, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [1, 2]],
        [[1, 0], [0, 1], [1, 1], [1, 2]]
    ],
    // 6: Z
    [
        [[0, 0], [1, 0], [1, 1], [2, 1]],
        [[2, 0], [1, 1], [2, 1], [1, 2]],
        [[0, 1], [1, 1], [1, 2], [2, 2]],
        [[1, 0], [0, 1], [1, 1], [0, 2]]
    ]
];

let board = [];
let currentPiece = null;
let nextPiece = null;
let score = 0;
let level = 1;
let linesCleared = 0;
let isStarted = false;
let isPaused = false;
let isGameOver = false;
let lastDropTime = 0;

function getScores() {{
    const saved = localStorage.getItem('tetris_highscores');
    if (saved) {{
        try {{ return JSON.parse(saved); }} catch(e) {{}}
    }}
    return INITIAL_SCORES;
}}

function renderScores() {{
    const list = getScores();
    const container = document.getElementById('scoresList');
    if (!list || list.length === 0) {{
        container.innerHTML = '<div style="font-size:11px; color:#888;">Sem registos</div>';
        return;
    }}
    let html = '';
    list.slice(0, 10).forEach((item, idx) => {{
        html += `<div class="score-item"><b>${{idx + 1}}. ${{item.nome}}</b><span>${{item.pontos.toLocaleString()}} pts</span></div>`;
    }});
    container.innerHTML = html;
}}

function initBoard() {{
    board = [];
    for (let r = 0; r < ROWS; r++) {{
        board[r] = [];
        for (let c = 0; c < COLS; c++) {{
            board[r][c] = null;
        }}
    }}
}}

function spawnPiece() {{
    if (!nextPiece) {{
        nextPiece = {{ type: Math.floor(Math.random() * 7) }};
    }}
    currentPiece = {{
        type: nextPiece.type,
        rot: 0,
        x: 3,
        y: 0
    }};
    nextPiece = {{ type: Math.floor(Math.random() * 7) }};
    
    if (!validMove(currentPiece.type, currentPiece.rot, currentPiece.x, currentPiece.y)) {{
        isGameOver = true;
        showGameOver();
    }}
}}

function validMove(p, r, x, y) {{
    const shape = SHAPES[p][r];
    for (let i = 0; i < shape.length; i++) {{
        const nx = x + shape[i][0];
        const ny = y + shape[i][1];
        if (nx < 0 || nx >= COLS || ny >= ROWS) return false;
        if (ny >= 0 && board[ny][nx] !== null) return false;
    }}
    return true;
}}

function lockPiece() {{
    const shape = SHAPES[currentPiece.type][currentPiece.rot];
    for (let i = 0; i < shape.length; i++) {{
        const nx = currentPiece.x + shape[i][0];
        const ny = currentPiece.y + shape[i][1];
        if (ny >= 0 && ny < ROWS && nx >= 0 && nx < COLS) {{
            board[ny][nx] = COLORS[currentPiece.type];
        }}
    }}
    clearLines();
    spawnPiece();
}}

function clearLines() {{
    let lines = 0;
    for (let r = ROWS - 1; r >= 0; r--) {{
        if (board[r].every(cell => cell !== null)) {{
            board.splice(r, 1);
            board.unshift(new Array(COLS).fill(null));
            lines++;
            r++;
        }}
    }}
    if (lines > 0) {{
        score += lines * 100 * level;
        linesCleared += lines;
        level = 1 + Math.floor(linesCleared / 10);
        updateHUD();
    }}
}}

function moveLeft() {{
    if (isStarted && !isPaused && !isGameOver && validMove(currentPiece.type, currentPiece.rot, currentPiece.x - 1, currentPiece.y)) {{
        currentPiece.x--;
    }}
}}

function moveRight() {{
    if (isStarted && !isPaused && !isGameOver && validMove(currentPiece.type, currentPiece.rot, currentPiece.x + 1, currentPiece.y)) {{
        currentPiece.x++;
    }}
}}

function rotatePiece() {{
    if (!isStarted || isPaused || isGameOver) return;
    const nextRot = (currentPiece.rot + 1) % 4;
    if (validMove(currentPiece.type, nextRot, currentPiece.x, currentPiece.y)) {{
        currentPiece.rot = nextRot;
    }}
}}

function moveDown() {{
    if (!isStarted || isPaused || isGameOver) return;
    if (validMove(currentPiece.type, currentPiece.rot, currentPiece.x, currentPiece.y + 1)) {{
        currentPiece.y++;
        score += 1;
        updateHUD();
    }} else {{
        lockPiece();
    }}
}}

function hardDropPiece() {{
    if (!isStarted || isPaused || isGameOver) return;
    while (validMove(currentPiece.type, currentPiece.rot, currentPiece.x, currentPiece.y + 1)) {{
        currentPiece.y++;
        score += 1;
    }}
    updateHUD();
    lockPiece();
}}

function startGame() {{
    isStarted = true;
    isPaused = false;
    isGameOver = false;
    score = 0;
    level = 1;
    linesCleared = 0;
    nextPiece = null;
    updateHUD();
    document.getElementById('overlay').style.display = "none";
    initBoard();
    spawnPiece();
}}

function togglePause() {{
    if (!isStarted || isGameOver) return;
    isPaused = !isPaused;
    document.getElementById('btnPause').innerText = isPaused ? "Continuar" : "Pausar";
    if (isPaused) {{
        document.getElementById('overlayTitle').innerText = "Jogo Pausado";
        document.getElementById('overlayMsg').innerText = "";
        document.getElementById('startBtn').style.display = "none";
        document.getElementById('scoreForm').style.display = "none";
        document.getElementById('overlay').style.display = "block";
    }} else {{
        document.getElementById('overlay').style.display = "none";
    }}
}}

function showGameOver() {{
    document.getElementById('overlayTitle').innerText = "Fim de Jogo!";
    document.getElementById('overlayMsg').innerText = "Pontuação: " + score;
    document.getElementById('startBtn').style.display = "none";
    document.getElementById('scoreForm').style.display = "block";
    document.getElementById('overlay').style.display = "block";
}}

function submitScore() {{
    const nameInput = document.getElementById('playerName');
    const name = nameInput ? nameInput.value.trim() : '';
    if (name) {{
        let scores = getScores();
        scores.push({{ nome: name, pontos: parseInt(score) }});
        scores.sort((a, b) => b.pontos - a.pontos);
        scores = scores.slice(0, 10);
        localStorage.setItem('tetris_highscores', JSON.stringify(scores));
        renderScores();

        document.getElementById('scoreForm').style.display = "none";
        document.getElementById('overlayTitle').innerText = "Guardado!";
        document.getElementById('overlayMsg').innerText = "Pontuação registada.";
        document.getElementById('startBtn').style.display = "block";
        document.getElementById('startBtn').innerText = "Jogar Novamente";
    }}
}}

function cancelScore() {{
    document.getElementById('scoreForm').style.display = "none";
    document.getElementById('overlayTitle').innerText = "Tetris";
    document.getElementById('overlayMsg').innerText = "Pontuação ignorada.";
    document.getElementById('startBtn').style.display = "block";
    document.getElementById('startBtn').innerText = "Jogar Novamente";
}}

function updateHUD() {{
    document.getElementById('scoreVal').innerText = score;
    document.getElementById('levelVal').innerText = level;
    document.getElementById('linesVal').innerText = linesCleared;
}}

function drawNextPiece() {{
    nextCtx.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    if (!isStarted || isGameOver || !nextPiece) return;

    nextCtx.fillStyle = COLORS[nextPiece.type];
    const shape = SHAPES[nextPiece.type][0];
    const nSize = 16;

    let minX = 4, maxX = 0, minY = 4, maxY = 0;
    shape.forEach(b => {{
        if (b[0] < minX) minX = b[0];
        if (b[0] > maxX) maxX = b[0];
        if (b[1] < minY) minY = b[1];
        if (b[1] > maxY) maxY = b[1];
    }});

    const pWidth = (maxX - minX + 1) * nSize;
    const pHeight = (maxY - minY + 1) * nSize;
    const offsetX = (nextCanvas.width - pWidth) / 2 - minX * nSize;
    const offsetY = (nextCanvas.height - pHeight) / 2 - minY * nSize;

    for (let i = 0; i < shape.length; i++) {{
        const px = offsetX + shape[i][0] * nSize;
        const py = offsetY + shape[i][1] * nSize;
        nextCtx.fillRect(px, py, nSize - 1, nSize - 1);
    }}
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let r = 0; r < ROWS; r++) {{
        for (let c = 0; c < COLS; c++) {{
            if (board[r] && board[r][c]) {{
                ctx.fillStyle = board[r][c];
                ctx.fillRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
            }} else {{
                ctx.strokeStyle = "#222";
                ctx.strokeRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }}
        }}
    }}

    if (isStarted && currentPiece && !isGameOver) {{
        ctx.fillStyle = COLORS[currentPiece.type];
        const shape = SHAPES[currentPiece.type][currentPiece.rot];
        for (let i = 0; i < shape.length; i++) {{
            const px = (currentPiece.x + shape[i][0]) * BLOCK_SIZE;
            const py = (currentPiece.y + shape[i][1]) * BLOCK_SIZE;
            if (py >= 0) {{
                ctx.fillRect(px, py, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
            }}
        }}
    }}

    drawNextPiece();
}}

function gameLoop(time) {{
    if (!lastDropTime) lastDropTime = time;
    const dropInterval = Math.max(100, 800 - (level - 1) * 70);

    if (isStarted && !isPaused && !isGameOver) {{
        if (time - lastDropTime > dropInterval) {{
            moveDown();
            lastDropTime = time;
        }}
    }}

    draw();
    requestAnimationFrame(gameLoop);
}}

function setupKeyboardAndTouch() {{
    const handleKey = function(e) {{
        const active = document.activeElement;
        if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA')) return;

        const key = e.key;
        if (['ArrowLeft', 'a', 'A'].includes(key)) {{ e.preventDefault(); moveLeft(); }}
        else if (['ArrowRight', 'd', 'D'].includes(key)) {{ e.preventDefault(); moveRight(); }}
        else if (['ArrowUp', 'w', 'W'].includes(key)) {{ e.preventDefault(); rotatePiece(); }}
        else if (['ArrowDown', 's', 'S'].includes(key)) {{ e.preventDefault(); moveDown(); }}
        else if ([' ', 'Space'].includes(key)) {{ e.preventDefault(); hardDropPiece(); }}
        else if (['p', 'P'].includes(key)) {{ e.preventDefault(); togglePause(); }}
    }};

    window.addEventListener('keydown', handleKey);
    window.parent.document.addEventListener('keydown', handleKey);

    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;

    canvas.addEventListener('touchstart', function(e) {{
        if (e.touches.length === 1) {{
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
        }}
    }}, {{ passive: false }});

    canvas.addEventListener('touchmove', function(e) {{
        e.preventDefault();
    }}, {{ passive: false }});

    canvas.addEventListener('touchend', function(e) {{
        if (!isStarted || isPaused || isGameOver) return;
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        const timeDiff = Date.now() - touchStartTime;

        if (Math.abs(deltaX) < 15 && Math.abs(deltaY) < 15) {{
            rotatePiece();
        }} 
        else if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 20) {{
            if (deltaX > 0) moveRight();
            else moveLeft();
        }}
        else if (deltaY > 20 && Math.abs(deltaY) > Math.abs(deltaX)) {{
            if (deltaY > 70 || timeDiff < 150) {{
                hardDropPiece();
            }} else {{
                moveDown();
            }}
        }}
    }}, {{ passive: false }});

    const bindBtn = (id, fn) => {{
        const btn = document.getElementById(id);
        if (btn) {{
            btn.addEventListener('touchstart', (e) => {{ e.preventDefault(); fn(); }}, {{ passive: false }});
            btn.addEventListener('click', fn);
        }}
    }};

    bindBtn('btnRotate', rotatePiece);
    bindBtn('btnLeft', moveLeft);
    bindBtn('btnRight', moveRight);
    bindBtn('btnDown', moveDown);
    bindBtn('btnDrop', hardDropPiece);
    bindBtn('btnPause', togglePause);
}}

renderScores();
initBoard();
setupKeyboardAndTouch();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

st.iframe(html_game_code, height=850)