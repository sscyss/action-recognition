# Conda环境管理讨论

## 当前环境列表

使用命令：`conda env list`

### 已创建的环境
```
# conda environments:
#
cosyvoice                C:\Users\86130\.conda\envs\cosyvoice
film                     C:\Users\86130\.conda\envs\film
film2                    C:\Users\86130\.conda\envs\film2
gpu1650                  C:\Users\86130\.conda\envs\gpu1650
yolo5                    C:\Users\86130\.conda\envs\yolo5
```

### 环境大小统计
```
环境名称      大小(MB)
--------      --------
cosyvoice    5893.81
film         0.00
film2        4542.15
gpu1650      5441.08
yolo5        2517.54
```

## 常用Conda命令

### 环境管理
```bash
# 查看所有环境
conda env list
conda info --envs

# 创建新环境
conda create -n 环境名 python=3.8

# 激活环境
conda activate 环境名

# 退出当前环境
conda deactivate

# 删除环境
conda remove -n 环境名 --all
```

### 删除环境命令详解

#### 基本删除命令
```bash
# 删除指定环境（推荐）
conda remove -n film --all

# 删除多个环境
conda remove -n film film2 --all

# 强制删除（如果基本命令失败）
conda env remove -n film
```

#### 删除前检查
```bash
# 1. 查看环境列表
conda env list

# 2. 确认环境名称
conda info --envs

# 3. 检查环境是否在使用
conda activate film
conda deactivate
```

#### 删除后验证
```bash
# 验证环境是否已删除
conda env list

# 检查目录是否还存在
ls C:\Users\86130\.conda\envs\
```

### 包管理
```bash
# 安装包
conda install 包名
pip install 包名

# 查看已安装的包
conda list
pip list

# 导出环境配置
conda env export > environment.yml

# 从配置文件创建环境
conda env create -f environment.yml
```

### 环境信息
```bash
# 查看当前环境信息
conda info

# 查看环境详细信息
conda info --envs --verbose
```

## 针对动作识别项目的建议

### 推荐环境配置
```bash
# 创建专门的环境
conda create -n action_recognition python=3.8

# 激活环境
conda activate action_recognition

# 安装必要的包
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
conda install opencv
conda install numpy pandas matplotlib seaborn
conda install scikit-learn
conda install jupyter notebook
```

### 环境文件示例
```yaml
# environment.yml
name: action_recognition
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - pytorch
  - torchvision
  - torchaudio
  - pytorch-cuda=11.8
  - opencv
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - scikit-learn
  - jupyter
  - pip
  - pip:
    - mediapipe
```

## 磁盘空间管理

### 查看环境大小
```bash
# Windows PowerShell命令
Get-ChildItem C:\Users\86130\.conda\envs\ -Directory | ForEach-Object { 
    $size = (Get-ChildItem $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum; 
    [PSCustomObject]@{Name=$_.Name; SizeMB=[math]::Round($size/1MB,2)} 
}

# 查看特定环境大小
Get-ChildItem C:\Users\86130\.conda\envs\film -Recurse -File | Measure-Object -Property Length -Sum
```

### 清理建议
1. **定期清理**: 删除不再使用的环境
2. **包缓存**: 清理conda包缓存
3. **磁盘监控**: 监控环境目录大小

### 清理命令
```bash
# 清理conda缓存
conda clean --all

# 清理pip缓存
pip cache purge

# 删除未使用的包
conda clean --packages
```

## 注意事项

1. **环境隔离**：为不同项目创建独立环境
2. **版本兼容**：注意PyTorch和CUDA版本兼容性
3. **定期清理**：删除不再使用的环境
4. **备份配置**：导出重要的环境配置文件

## 相关技术要点

- 使用虚拟环境避免包冲突
- 根据项目需求选择合适的Python版本
- 考虑GPU支持，安装对应的CUDA版本
- 定期更新环境中的包
- 监控磁盘空间使用情况
