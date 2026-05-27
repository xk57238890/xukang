# SWaT + KDD 统一复现实验模板（PyTorch）

本模板提供：
- 统一数据接口（SWaT / KDDCup99）
- 统一模型接口（可扩展 TranAD/IForest/LSTM-AE）
- 统一评测（Precision / Recall / F1 / AUPR）
- 统一命令行训练与评估

## 目录

```text
tsad_template/
  data/
  models/
  training/
  evaluation/
  configs/
  run_experiment.py
```

## 快速开始

```bash
python tsad_template/run_experiment.py --dataset swat --model iforest
python tsad_template/run_experiment.py --dataset kdd --model iforest
```

## 后续扩展建议

- 在 `models/` 中新增 `tranad.py` 并继承 `BaseModel`
- 在 `configs/` 中加入数据标准化、窗口长度、阈值策略
- 补充 event-wise 指标与延迟指标
