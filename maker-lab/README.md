# 🔧 Maker Lab — Hardware & Prototipagem

Braço robótico de 3 eixos para **coleta autônoma de amostras vegetais** na estufa da Base Jamestown. Cada amostra recebe um identificador rastreável (`JAM-GH01-SMP-###`) pronto para ser consumido pelos módulos de Visão Computacional e Big Data do hub. Prototipado em Arduino UNO e simulado no [Wokwi](https://wokwi.com).

## 👥 Equipe Desenvolvedora — 4ESPW

- **Breno Silva** — RM99275
- **Eduardo Araujo** — RM99758
- **Gabriela Trevisan** — RM99500
- **Gustavo Akio** — RM550241
- **Rafael Franck** — RM550875

## 🦾 Visão geral

O `PBML Arm v7.1` é um manipulador com três graus de liberdade — **base** (rotação), **lift** (elevação/articulação) e **grip** (garra) — operado por joysticks analógicos. Dois modos de velocidade (Speed/Precise) permitem desde reposicionamento rápido até ajuste fino para colher uma folha sem danificá-la. Cada coleta registra a pose completa do braço no terminal, gerando um log estruturado para o pipeline de dados.

## 🧩 Arquitetura de Hardware

| Componente        | Pino Arduino | Função                                  |
| ----------------- | ------------ | --------------------------------------- |
| Servo BASE        | D11          | Rotação horizontal (0–180°)             |
| Servo LIFT        | D9           | Elevação / articulação (0–180°)         |
| Servo GRIP        | D10          | Abertura e fechamento da garra (0–180°) |
| Joystick BASE     | A0 / D2      | Eixo horizontal / botão SEL             |
| Joystick LIFT     | A1 / D3      | Eixo horizontal / botão SEL             |
| Joystick GRIP     | A2           | Eixo horizontal                         |
| Botão MODE        | D8           | Alterna modo Speed ↔ Precise            |
| LED de status     | D13          | Indica movimento e eventos (+ resistor 220 Ω) |

Posições iniciais: base `90°`, lift `40°`, grip `20°`.

## 🎮 Controles físicos

- **Joystick BASE** — gira a base. Pressionar (**SEL**) faz *reset*: todos os servos voltam ao centro (90°).
- **Joystick LIFT** — eleva e abaixa o braço. Pressionar (**SEL**) **captura uma amostra** e incrementa o contador.
- **Joystick GRIP** — abre e fecha a garra (passo fixo, independente do modo).
- **Botão MODE** — alterna entre **Speed** (3°/passo) e **Precise** (1°/passo).
- **LED** — aceso enquanto há movimento; pisca para sinalizar eventos (reset, captura, troca de modo).

## ⌨️ Controle por Serial (9600 baud)

Além dos joysticks, o braço aceita comandos pelo Monitor Serial. Cada letra move um eixo; um número opcional define o ângulo absoluto (ex.: `U90` leva o lift direto a 90°).

| Comando      | Ação                                |
| ------------ | ----------------------------------- |
| `U` / `D`    | Lift sobe / desce                   |
| `O` / `C`    | Garra abre / fecha                  |
| `L` / `R`    | Base gira esquerda / direita        |
| `<letra><n>` | Move o eixo ao ângulo `n` (0–180)   |
| `STATUS`     | Reimprime o painel de status        |
| `MODE`       | Exibe o modo atual                  |
| `RESET`      | Retorna todos os eixos ao centro    |

## ▶️ Como simular no Wokwi

1. Acesse [wokwi.com](https://wokwi.com) e crie um novo projeto Arduino UNO.
2. Cole o conteúdo de `robotic-arm.ino` no editor de código.
3. Substitua o `diagram.json` pelo deste módulo (monta servos, joysticks, botão e LED já conectados).
4. Inicie a simulação e abra o **Serial Monitor** a `9600` baud para acompanhar o painel de status e os logs de captura.

## 📂 Arquivos

- **`robotic-arm.ino`** — firmware do controlador (lógica de joysticks, modos, captura e comandos serial).
- **`diagram.json`** — circuito do protótipo para a simulação no Wokwi.
