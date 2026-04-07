# Training Report — Day 2

## Model
TinyLlama-1.1B

## Technique
QLoRA (4-bit) + LoRA

## Hyperparameters
- Rank (r): 16
- Learning Rate: 2e-4
- Batch Size: 4
- Epochs: 3

## Training Details
- Trainable Parameters: ~0.2%
- Quantization: 4-bit (bitsandbytes)
- Gradient Checkpointing: Enabled
- Mixed Precision: Disabled (fp16 issue fixed)

## Results
- Initial Loss: ~2.35
- Final Loss: ~0.25
- Training successful

## Observations
- Loss decreased smoothly
- Model learned domain-specific responses
- Memory efficient training achieved

## Output
- Adapter model saved successfully