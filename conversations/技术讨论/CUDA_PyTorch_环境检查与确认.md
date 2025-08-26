## CUDA / PyTorch 环境检查与确认

### 结论
- 使用环境：`conda env action_recognition`
- PyTorch/TV 版本：`torch 2.4.1+cu118`，`torchvision 0.19.1+cu118`
- CUDA Runtime（随 PyTorch）：`11.8`，cuDNN：`90100`
- 显卡驱动：`532.03`（支持 CUDA 12.1，向下兼容 11.8）
- 本机 NVCC：`12.1`（版本高于 PyTorch 绑定的 11.8，不影响使用）
- 版本匹配正常，无不兼容问题。

### 检查命令与输出
```powershell
conda activate action_recognition
python -c "import torch, torchvision; print('torch:', torch.__version__); print('torchvision:', torchvision.__version__); print('cuda_available:', torch.cuda.is_available()); print('torch_cuda:', torch.version.cuda); print('cudnn:', torch.backends.cudnn.version()); import subprocess; print('nvidia-smi:'); subprocess.run(['nvidia-smi']); print('nvcc --version:'); subprocess.run(['nvcc', '--version'])"
```

典型输出（节选）：
```text
torch: 2.4.1+cu118
torchvision: 0.19.1+cu118
cuda_available: True
torch_cuda: 11.8
cudnn: 90100
nvidia-smi:
Driver Version: 532.03  CUDA Version: 12.1
nvcc --version:
Cuda compilation tools, release 12.1, V12.1.105
```

### 训练时设备确认
已在 `modetect.py` 加入设备日志：
```text
Using device: cuda
CUDA available: True
GPU: <GPU名称>, CC: <计算能力>, VRAM: <显存GB>
```

如显示 `Using device: cpu`，排查要点：
- 确认用 `conda activate action_recognition` 后运行脚本。
- 确认未通过系统 Python 或其他路径运行（避免 `& C:/Users/.../python.exe`）。
- 检查 `CUDA_VISIBLE_DEVICES` 未屏蔽 GPU。
- 当前 torch/torchvision 已为 cu118 版，通常无需重装。

### 显存不足的建议
- 将 `BATCH_SIZE` 减小（如 2 或 1）。
- 将 `frames_per_clip` 从 `16` 降到 `8`。

### 相关修改摘要
- 在 `modetect.py` 增加 `log_device_info()` 打印设备/驱动信息。
- 为 `DataLoader` 在 CUDA 可用时启用 `pin_memory=True`。
- 自定义 `VideoPreprocess`：将 `[T,H,W,C]` uint8 转为 `[C,T,H,W]` float32，插值到 112×112 并归一化。




