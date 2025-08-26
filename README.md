# Modetect - 动作识别项目

这是一个基于深度学习的动作识别项目，使用HMDB51数据集进行训练和测试。

## 项目简介

Modetect是一个动作识别系统，能够识别视频中的各种人类动作，如抓取(catch)、投掷(throw)、行走(walk)等。项目基于PyTorch框架实现，使用预训练的深度学习模型进行动作分类。

## 功能特性

- 🎯 支持51种人类动作的识别
- 🎬 处理视频输入，输出动作类别
- 🚀 基于预训练模型，快速推理
- 📊 支持多种数据集分割方式
- 🔧 易于扩展和自定义

## 项目结构

```
modetect/
├── modetect.py          # 主要的动作识别模块
├── infer.py             # 推理脚本
├── hmdb51_splits/       # HMDB51数据集分割文件
├── testTrainMulti_7030_splits/  # 70/30训练测试分割
├── conversations/       # 项目开发记录和讨论
└── README.md           # 项目说明文档
```

## 环境要求

- Python 3.7+
- PyTorch 1.8+
- OpenCV
- NumPy
- 其他依赖见requirements.txt

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/sscyss/action-recognition.git
cd modetect
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 下载预训练模型（可选）
```bash
# 模型文件较大，建议从项目发布页面下载
# 或使用提供的下载脚本
```

4. 下载HMDB51数据集
```bash
# 访问官方数据集网站申请下载
# 官方地址：http://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/
```

## 使用方法

### 基本推理

```python
from modetect import Modetect

# 初始化模型
detector = Modetect()

# 识别视频中的动作
result = detector.detect("path/to/video.mp4")
print(f"检测到的动作: {result}")
```

### 命令行推理

```bash
python infer.py --video path/to/video.mp4
```

## 数据集

项目使用HMDB51数据集，包含51种人类动作类别：

- 日常动作：walk, sit, stand, turn
- 运动动作：catch, throw, kick, run
- 手势动作：wave, clap, point
- 其他动作：smile, laugh, drink, eat

### HMDB51数据集下载

**官方地址**：[HMDB51: A Large Video Database for Human Motion Recognition](http://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/)


## 模型说明

- 基于预训练的3D卷积神经网络
- 支持视频时序特征提取
- 针对动作识别任务优化

## 性能指标

- 准确率：在HMDB51测试集上达到XX%
- 推理速度：实时处理能力
- 支持多种视频格式和分辨率

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your.email@example.com]
- 项目链接：[https://github.com/sscyss/action-recognition](https://github.com/sscyss/action-recognition)

## 致谢

- HMDB51数据集提供者
- PyTorch开发团队
- 开源社区的支持

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
