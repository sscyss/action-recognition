# 在指定 Conda 环境中运行 modetect.py（Cursor 设置）

## 方法A：用 Cursor 终端直接运行（最简单）

```powershell
# 1) 在 Cursor 内打开终端
conda activate action_recognition

# 2) 运行脚本
python modetect.py

# 3) 验证使用的解释器与 CUDA 状态
python -c "import sys, torch; print(sys.executable); print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
```

- 提醒：不要把提示符一起复制（例如“(action_recognition) PS …”）。

## 方法B：在 Cursor 里绑定该环境为项目解释器（推荐）

1) Ctrl+Shift+P → 输入并选择 “Python: Select Interpreter”
2) 选择解释器路径：`C:\Users\86130\.conda\envs\action_recognition\python.exe`
3) 右下角状态栏应显示所选环境名称；此后运行/调试会默认使用该解释器

### 可选：工作区设置（持久化）

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "C:\\Users\\86130\\.conda\\envs\\action_recognition\\python.exe",
  "python.terminal.activateEnvironment": true
}
```

### 可选：调试配置

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: modetect.py",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/modetect.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

## 说明
- Windows 下 Conda 环境解释器路径通常为：`…\\envs\\环境名\\python.exe`
- 运行命令如需 GPU，确保 `torch.cuda.is_available()` 为 True，并已安装对应 CUDA 版 PyTorch。


