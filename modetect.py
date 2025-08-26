import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import HMDB51
from torchvision.models.video import r3d_18
import torch.nn.functional as F

# 1. 配置参数
BATCH_SIZE = 2
EPOCHS = 10
LR = 1e-3
NUM_CLASSES = 51
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def log_device_info():
    print(f"Using device: {DEVICE}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        try:
            gpu_name = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            print(f"GPU: {gpu_name}, CC: {props.major}.{props.minor}, VRAM: {props.total_memory // (1024**3)} GB")
        except Exception as e:
            print(f"GPU info fetch error: {e}")

# 2. 数据预处理
class VideoPreprocess:
    def __init__(self, size=(112, 112), mean=(0.43216, 0.394666, 0.37645), std=(0.22803, 0.22145, 0.216989)):
        self.size = size
        self.mean = torch.tensor(mean).view(3, 1, 1)
        self.std = torch.tensor(std).view(3, 1, 1)

    def __call__(self, video: torch.Tensor) -> torch.Tensor:
        # 输入: [T, H, W, C], uint8
        if video.ndim != 4:
            raise ValueError(f"Expected video tensor with 4 dims [T,H,W,C], got shape {tuple(video.shape)}")
        # 转为 [T, C, H, W]
        video = video.permute(0, 3, 1, 2)  # [T,C,H,W]
        # 转 float32 并归一化到 [0,1]
        video = video.to(torch.float32) / 255.0
        # 统一尺寸到 112x112（逐帧双线性插值）
        T, C, H, W = video.shape
        video = F.interpolate(video, size=self.size, mode='bilinear', align_corners=False)
        # 按通道做归一化（对每一帧同样处理）
        video = (video - self.mean) / self.std  # [T,C,H,W]
        # 最终转为 [C, T, H, W] 以适配 r3d_18 输入
        video = video.permute(1, 0, 2, 3).contiguous()
        return video

transform = VideoPreprocess()

# 3. 数据集路径
# 需要提前下载好HMDB51数据集并解压，设置好路径
HMDB51_ROOT = './hmdb51'  # 修改为你的数据集路径
SPLIT_FILE = './hmdb51_splits'  # HMDB51 split 文件路径

# 4. 构建模型（以3D-ResNet18为例）
model = r3d_18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model = model.to(DEVICE)

# 5. 损失函数与优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

# 6. 训练与验证流程
def train(train_loader, val_loader):
    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        correct = 0
        total = 0
        for batch in train_loader:
            if isinstance(batch, (list, tuple)) and len(batch) == 3:
                clips, _audio, labels = batch
            elif isinstance(batch, (list, tuple)) and len(batch) == 2:
                clips, labels = batch
            else:
                raise ValueError(f"Unexpected batch format: type={type(batch)}, len={len(batch) if hasattr(batch, '__len__') else 'NA'}")
            clips, labels = clips.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(clips)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * clips.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)
        print(f'Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/total:.4f}, Acc: {correct/total:.4f}')
        validate(val_loader)

def validate(val_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in val_loader:
            if isinstance(batch, (list, tuple)) and len(batch) == 3:
                clips, _audio, labels = batch
            elif isinstance(batch, (list, tuple)) and len(batch) == 2:
                clips, labels = batch
            else:
                raise ValueError(f"Unexpected batch format: type={type(batch)}, len={len(batch) if hasattr(batch, '__len__') else 'NA'}")
            clips, labels = clips.to(DEVICE), labels.to(DEVICE)
            outputs = model(clips)
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)
    print(f'Validation Acc: {correct/total:.4f}')
    model.train()

if __name__ == '__main__':
    # Windows 下多进程需要放到 main 保护内，且建议先用单进程数据加载
    import multiprocessing
    multiprocessing.freeze_support()

    log_device_info()

    # 4. 加载HMDB51数据集（将 num_workers 设为 0，避免 Windows 多进程问题）
    train_dataset = HMDB51(
        root=HMDB51_ROOT,
        annotation_path=SPLIT_FILE,
        frames_per_clip=8,
        step_between_clips=1,
        train=True,
        transform=transform,
        num_workers=0
    )
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=torch.cuda.is_available())

    val_dataset = HMDB51(
        root=HMDB51_ROOT,
        annotation_path=SPLIT_FILE,
        frames_per_clip=8,
        step_between_clips=1,
        train=False,
        transform=transform,
        num_workers=0
    )
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=torch.cuda.is_available())

    train(train_loader, val_loader)
    # 可保存模型
    torch.save(model.state_dict(), 'action_recognition_hmdb51.pth')