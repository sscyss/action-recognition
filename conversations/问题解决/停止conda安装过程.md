# 停止conda安装过程

## 问题描述
用户询问：卡在"Solving environment: -"怎么停止安装过程？

## 停止安装的方法

### 方法1：键盘中断（推荐）
```bash
# 在终端中按以下组合键
Ctrl + C

# 或者多次按Ctrl+C强制停止
Ctrl + C (多次)
```

### 方法2：关闭终端窗口
- **Windows**: 直接关闭PowerShell/CMD窗口
- **Linux/Mac**: 关闭终端窗口或按 `Ctrl + D`

### 方法3：任务管理器强制结束
```bash
# Windows: 打开任务管理器
# 找到conda相关进程并结束

# 或者使用命令行
taskkill /f /im conda.exe
taskkill /f /im python.exe
```

## 停止后的清理工作

### 1. 检查进程状态
```bash
# 检查是否有conda进程残留
tasklist | findstr conda
tasklist | findstr python

# 如果有残留进程，强制结束
taskkill /f /im 进程名
```

### 2. 清理临时文件
```bash
# 清理conda缓存
conda clean --all

# 清理临时文件
conda clean --tarballs
conda clean --index-cache
```

### 3. 重置conda状态
```bash
# 重置conda环境
conda info --envs

# 如果环境状态异常，重新激活
conda deactivate
conda activate base
```

## 预防措施

### 1. 设置超时时间
```bash
# 设置conda超时时间
conda config --set remote_connect_timeout_secs 300
conda config --set remote_read_timeout_secs 300

# 设置更短的超时时间
conda config --set remote_connect_timeout_secs 60
conda config --set remote_read_timeout_secs 60
```

### 2. 使用更快的安装方式
```bash
# 使用pip安装（推荐）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 或者使用mamba
conda install mamba -c conda-forge
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. 分步安装
```bash
# 分步安装，每步都可以单独停止
conda install pytorch -c pytorch
# 如果卡住，Ctrl+C停止

conda install torchvision -c pytorch
# 如果卡住，Ctrl+C停止

conda install torchaudio -c pytorch
# 如果卡住，Ctrl+C停止
```

## 常见问题解决

### 1. 停止后环境损坏
```bash
# 重新创建环境
conda remove -n action_recognition --all
conda create -n action_recognition python=3.8

# 激活环境
conda activate action_recognition
```

### 2. 包安装不完整
```bash
# 检查已安装的包
conda list

# 重新安装缺失的包
conda install 包名

# 或者使用pip安装
pip install 包名
```

### 3. 网络问题
```bash
# 使用国内镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

# 或者使用pip安装
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 最佳实践

### 1. 安装前准备
```bash
# 清理缓存
conda clean --all

# 更新conda
conda update conda

# 设置合理的超时时间
conda config --set remote_connect_timeout_secs 300
```

### 2. 安装策略
- **使用pip安装**: 速度更快，依赖解析更简单
- **分步安装**: 便于定位问题
- **设置超时**: 避免无限等待

### 3. 监控安装过程
- 观察网络连接状态
- 监控系统资源使用
- 准备随时停止安装

## 相关技术要点

- Ctrl+C是停止conda安装的标准方法
- 安装卡住通常是由于网络或依赖解析问题
- pip安装通常比conda更稳定
- 定期清理缓存可以避免很多问题
- 设置合理的超时时间可以避免无限等待

