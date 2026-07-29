# Moonlight-Switch (LookADev Optimized Edition) — Release v3.0.0-definitive
## Sprint 7: A Solução Definitiva 🏆

Temos o orgulho de apresentar a versão **v3.0.0-definitive** do **Moonlight-Switch (LookADev Optimized Edition)**. Esta atualização transforma o projeto de um fork otimizado de latência no padrão ouro e absoluto de game streaming para o ecossistema Nintendo Switch.

---

### 🌟 O que há de novo na v3.0.0-definitive?

#### 1. 📊 Validação Empírica & Telemetria em CSV (FASE 1)
- **Log de Latência Contínuo:** Exporte dados detalhados de performance (host FPS, net FPS, decode FPS, render FPS, latência NVDEC, jitter de rede e tempo de renderização deko3d) diretamente para arquivos `.csv` salvos em `/switch/moonlight/logs/`.
- **Script Analisador em Python (`tools/latency_analyzer.py`):** Ferramenta inclusa no repositório para ler os logs CSV e gerar relatórios completos (média, variância, desvio padrão, 1% low, p50/p90/p95/p99) e realizar comparações side-by-side de diferentes perfis.

#### 2. 🎨 Perfis Globais de Qualidade Gráfica (FASE 2)
- **Competitive:** Latência absoluta com FSR básico (EASU), sem dithering, queue size 1.
- **Balanced:** FSR padrão com nitidez RCAS moderada (20%), equilíbrio de imagem e latência.
- **Cinematic:** FSR avançado (EASU + RCAS 40%), dithering ativado (força 3.0), focado em estabilidade visual e pacing fluido.
- **Sunshine AV1 & FEC Adaptativo:** Suporte inicial para negociação de codec AV1 e adaptação dinâmica de correção de erro (FEC) frente a instabilidades na rede Wi-Fi.

#### 3. 🛡️ Auto-Recovery e Gerenciamento Térmico (FASE 3)
- **Auto-Recovery:** Reconexão automática em caso de micro-quedas de Wi-Fi e transição suave em ciclos de Sleep/Wake sem erro ou crash do socket.
- **Perfis Térmicos Inteligentes:** Opção entre os perfis *Performance* e *Silent* para manter estabilidade de clocks sem causar thermal throttling agressivo na ventoinha.
- **Compatibilidade Sysmodules:** Total isolamento contra race conditions com os sysmodules populares `sys-clk` e `Tesla`.

#### 4. 🎮 Engenharia de Input Definitiva & Modo Ultra Low Latency (FASE 4)
- **Curvas e Deadzones de Analógicos:** Curva exponencial ajustável e deadzones configuráveis por analógico.
- **Isolamento Touch/Mouse:** Thread de touch/mouse desacoplada da thread principal de gamepad de 250 Hz (prioridade `0x20`).
- **Modo Ultra Low Latency de 1-Clique:** Ativação instantânea com um clique da melhor combinação de latência (double buffer deko3d ON, audio AUDREN non-blocking, post-proc bypass, QoS `DSCP_EF`).

#### 5. 📁 Perfis por Jogo (FASE 5)
- **Context Saving:** As configurações de bitrate, resolução, perfil gráfico e latência são automaticamente salvas e recarregadas ao iniciar cada jogo específico do Sunshine!

---

### 📦 Instruções de Instalação

1. Baixe o arquivo `Moonlight.nro` da release oficial.
2. Copie para o seu cartão SD em: `sdcard:/switch/Moonlight-Switch/Moonlight.nro`.
3. Inicie o homebrew pelo **HBMenu via Title Redirection** (mantenha R pressionado ao abrir um jogo) para garantir acesso total de memória RAM e GPU.

---

### ⚡ Recomendação de Overclock (Opcional, mas Recomendado)
Para rodar streams em 1080p60 em bitrate elevado (>25 Mbps) com FSR RCAS ativado:
- Recomendado o uso do [sys-clk](https://github.com/retronx-team/sys-clk) com perfis modestos de GPU (768 MHz - 921 MHz) e CPU (1224 MHz - 1581 MHz).

---

### 🐛 Troubleshooting & Suporte
- Se o log em CSV não for gerado, verifique se a opção **"Export Latency Logs (CSV)"** está ligada no menu de configurações e se o cartão SD possui permissão de escrita em `/switch/moonlight/logs/`.
- Em caso de dúvidas ou sugestões, abra uma Issue no repositório GitHub oficial!
