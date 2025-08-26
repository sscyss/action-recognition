# PyTorch安装卡住问题解决

## 问题描述
用户询问：安装PyTorch时，一直停留在"Solving environment: -"是什么原因？

## 问题原因分析

### 1. 依赖解析复杂
- **PyTorch依赖多**: PyTorch有大量依赖包需要解析
- **版本冲突**: 不同包之间可能存在版本冲突
- **CUDA兼容性**: GPU版本需要检查CUDA兼容性

### 2. 网络问题
- **下载速度慢**: 从官方源下载速度可能较慢
- **网络不稳定**: 网络连接不稳定导致卡住
- **防火墙限制**: 公司或学校网络可能有防火墙限制

### 3. conda配置问题
- **channel优先级**: 多个channel可能导致解析冲突
- **缓存问题**: conda缓存可能损坏
- **环境冲突**: 现有环境中的包可能冲突

### 4. 系统资源问题
- **内存不足**: 依赖解析需要大量内存
- **CPU负载高**: 其他程序占用CPU资源
- **磁盘空间**: 临时文件可能占用大量空间

## 解决方案

### 方案1：使用国内镜像源
```bash
# 添加清华镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

# 设置搜索时显示channel地址
conda config --set show_channel_urls yes

# 重新安装
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 方案2：使用pip安装
```bash
# 激活环境
conda activate action_recognition

# 使用pip安装（推荐）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 或者CPU版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 方案3：清理conda环境
```bash
# 清理conda缓存
conda clean --all

# 更新conda
conda update conda

# 重新安装
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 方案4：分步安装
```bash
# 1. 先安装基础包
conda install pytorch -c pytorch

# 2. 再安装torchvision
conda install torchvision -c pytorch

# 3. 最后安装torchaudio
conda install torchaudio -c pytorch

# 4. 安装CUDA支持
conda install pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 方案5：使用mamba（更快）
```bash
# 安装mamba（conda的快速替代品）
conda install mamba -c conda-forge

# 使用mamba安装
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

## 预防措施

### 1. 环境准备
```bash
# 创建干净的环境
conda create -n action_recognition python=3.8 --no-default-packages

# 激活环境
conda activate action_recognition

# 安装基础包
conda install numpy pandas matplotlib
```

### 2. 网络优化
```bash
# 设置conda超时时间
conda config --set remote_connect_timeout_secs 600
conda config --set remote_read_timeout_secs 600

# 设置并发数
conda config --set max_parallel_downloads 10
```

### 3. 系统优化
```bash
# 清理系统临时文件
# Windows: 清理 %TEMP% 目录
# Linux: 清理 /tmp 目录

# 关闭不必要的程序
# 释放内存和CPU资源
```

## 验证安装

### 1. 检查安装
```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

### 2. 测试GPU
```python
import torch

# 检查GPU
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name()}")
    print(f"GPU count: {torch.cuda.device_count()}")
    
    # 测试GPU计算
    x = torch.randn(1000, 1000).cuda()
    y = torch.mm(x, x)
    print("GPU test passed!")
else:
    print("CUDA not available")
```

## 常见错误解决

### 1. 超时错误
```bash
# 增加超时时间
conda config --set remote_connect_timeout_secs 1200
conda config --set remote_read_timeout_secs 1200
```

### 2. 内存不足
```bash
# 减少并发下载
conda config --set max_parallel_downloads 5

# 使用pip安装（内存占用更少）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. 网络问题
```bash
# 使用代理（如果有）
conda config --set proxy_servers.http http://proxy:port
conda config --set proxy_servers.https https://proxy:port

# 或者使用离线安装包
# 下载.conda文件后本地安装
```

## 最佳实践建议

### 1. 安装顺序
1. **创建干净环境**: 避免包冲突
2. **使用国内镜像**: 提高下载速度
3. **分步安装**: 便于定位问题
4. **验证安装**: 确保功能正常

### 2. 环境管理
- 为不同项目创建独立环境
- 定期清理不使用的环境
- 备份重要的环境配置

### 3. 网络优化
- 使用稳定的网络连接
- 选择合适的镜像源
- 避免在网络高峰期安装

## 相关技术要点

- conda依赖解析是NP难问题，可能需要很长时间
- pip安装通常比conda更快
- 使用国内镜像源可以显著提高下载速度
- mamba是conda的快速替代品
- 定期清理缓存可以避免很多问题

