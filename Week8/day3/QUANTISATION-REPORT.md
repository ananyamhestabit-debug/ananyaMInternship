# Quantisation Report

## Overview

In this task, we performed post-training quantisation on a fine-tuned language model using INT8, INT4, and GGUF formats to reduce memory usage and improve inference efficiency.

---

## Models Generated

* **INT8 Model** → Stored in `model-int8/`
* **INT4 Model** → Stored in `model-int4/`
* **GGUF Model (F16)** → `model.gguf`
* **GGUF Quantized Model (Q4)** → `model-q4.gguf`

---

## Size Comparison

| Model       | Size    |
| ----------- | ------- |
| FP16 (Base) | ~2.2 GB |
| INT8        | 1.15 GB |
| INT4        | 0.75 GB |
| GGUF (Q4)   | 0.59 GB |

---

## Speed & Latency

| Model     | Speed / Latency                                      |
| --------- | ---------------------------------------------------- |
| FP16      | Slowest, high latency                                |
| INT8      | Slower than INT4                                     |
| INT4      | Faster than INT8                                     |
| GGUF (Q4) | Prompt: 23.3 tokens/sec, Generation: 10.8 tokens/sec |

---

## Quality Evaluation

### Prompt 1:

**Input:** What is GST?
**Output:** GST is a comprehensive indirect tax applied on goods and services.

### Prompt 2:

**Input:** If GST is 18% on 1000, what is total?
**Output:** GST = 180, Total = 1180

### Prompt 3:

**Input:** Extract GST from ₹250
**Output:** 250

---

## Observations

* FP16 provides the highest accuracy but requires the most memory and has the highest latency.
* INT8 maintains high accuracy with moderate compression.
* INT4 significantly reduces size and improves speed with a slight accuracy trade-off.
* GGUF format provides the best balance between speed, memory efficiency, and output stability.
* GGUF runs efficiently on CPU and achieves the fastest inference among all formats.

---

## Conclusion

Quantisation is an effective technique to optimize large language models for deployment.
It reduces storage requirements and improves inference speed while maintaining acceptable output quality.

Among all formats, the GGUF model provided the best overall performance in terms of speed, size, and stability, making it most suitable for real-world deployment.

---

## Tools & Libraries Used

* HuggingFace Transformers
* PEFT (LoRA / QLoRA)
* BitsAndBytes
* llama.cpp

---

## Deliverables

* /quantized/model-int8
* /quantized/model-int4
* /quantized/model.gguf
