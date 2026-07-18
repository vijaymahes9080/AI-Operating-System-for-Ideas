# Future AI Capabilities

This document serves as a speculative research and development roadmap outlining upcoming advancements in model capabilities, runtime scaling, and self-optimizing agency.

---

## 1. WebGPU & Local Browser LLMs

To achieve absolute offline independence and reduce API operational costs to zero, IdeasOS is building support for WebGPU-accelerated local inferences directly inside the browser client sandbox.

- **Technology**: **Transformers.js (v3+)** and **WebNN API**.
- **Model Target**: Loading quantized **Llama-3-8B-Instruct** or **Qwen-2.5-7B** model weights (ONNX format) directly into browser GPU memory.
- **Benefit**: Text generation, sentiment classification, and semantic embedding updates occur fully in-browser without sending payloads to the Python backend.

---

## 2. Agentic Self-Improving Prompt Loops (DSPy Integration)

Instead of manually editing prompt templates when LLM performance drifts, future iterations will implement programmatically optimized prompt updates:

```
[System Prompts] 
       |
       v
[Execution Run] ---> [Evaluate Outputs vs Target Metrics]
       |
       v
[DSPy Optimizer Node] (BootstrapFewShot) ---> [Update System Prompt Weights]
```

- **Mechanism**: The engine collects user feedback (thumbs up/down) and compilation logs.
- **DSPy Compiler**: When accuracy drops, a background optimizer loops through training samples, automatically adjusts the phrasing of instructions, and inserts relevant few-shot examples into active agent system instructions.

---

## 3. Multimodal Video, Audio, and Diagram Understanding

Future releases will expand the **Universal Idea Inbox** to support complex dynamic files:

- **Dynamic Meeting Transcription**: Automatically parses video call recordings (Zoom, Meet, Teams exports), diarizes speakers, isolates action items, and appends them to individual developer task lists.
- **Sketch-to-Component Rendering**: Evaluates drawings of layouts and user interfaces. Using multimodal Vision LLMs (e.g. Qwen-2-VL), the engine converts wireframe sketches directly into working React component code.
- **Repository-to-Architecture Generation**: Ingests whole GitHub repositories, maps visual file structures, and automatically generates high-fidelity component flow diagrams using Mermaid or Apache ECharts.
