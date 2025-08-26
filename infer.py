import argparse
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.video import r3d_18
from torchvision.io import read_video

# 交互式文件选择（Windows/macOS/Linux 通用）
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception:
    tk = None
    filedialog = None
    messagebox = None


class VideoPreprocess:
    def __init__(self, size=(112, 112), mean=(0.43216, 0.394666, 0.37645), std=(0.22803, 0.22145, 0.216989)):
        self.size = size
        self.mean = torch.tensor(mean).view(3, 1, 1)
        self.std = torch.tensor(std).view(3, 1, 1)

    def __call__(self, video: torch.Tensor) -> torch.Tensor:
        # 输入: [T, H, W, C], uint8
        if video.ndim != 4:
            raise ValueError(f"Expected video tensor with 4 dims [T,H,W,C], got shape {tuple(video.shape)}")
        video = video.permute(0, 3, 1, 2)  # [T,C,H,W]
        video = video.to(torch.float32) / 255.0
        video = F.interpolate(video, size=self.size, mode='bilinear', align_corners=False)
        video = (video - self.mean) / self.std
        video = video.permute(1, 0, 2, 3).contiguous()  # [C,T,H,W]
        return video


def load_class_names(path: str):
    if not path or not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]
    return names


def sample_frames(video_tensor: torch.Tensor, num_frames: int = 16) -> torch.Tensor:
    # video_tensor: [T,H,W,C]
    total = video_tensor.shape[0]
    if total >= num_frames:
        # 均匀采样 num_frames 帧
        indices = torch.linspace(0, total - 1, steps=num_frames).long()
        return video_tensor.index_select(0, indices)
    else:
        # 帧不足则重复最后一帧补齐
        pad = num_frames - total
        last = video_tensor[-1:].repeat(pad, 1, 1, 1)
        return torch.cat([video_tensor, last], dim=0)


def _select_video_via_gui(initial_dir: str = '.') -> str:
    if tk is None or filedialog is None:
        return ''
    root = tk.Tk()
    root.withdraw()
    root.update()
    path = filedialog.askopenfilename(
        title='选择待预测视频',
        initialdir=initial_dir,
        filetypes=[
            ('Video Files', '*.mp4 *.avi *.mov *.mkv'),
            ('All Files', '*.*'),
        ],
    )
    root.destroy()
    return path or ''


def _show_result_message(title: str, message: str):
    if messagebox is None:
        return
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description='HMDB51 Action Recognition Inference')
    parser.add_argument('--video', default='', help='待预测视频路径 (.mp4/.avi)；留空则弹出选择框')
    parser.add_argument('--weights', default='action_recognition_hmdb51.pth', help='模型权重路径')
    parser.add_argument('--num-classes', type=int, default=51, help='类别数，需与训练一致')
    parser.add_argument('--class-names', default='', help='类别名文件，每行一个类别名，可选')
    parser.add_argument('--topk', type=int, default=5, help='输出Top-K结果')
    parser.add_argument('--gui', action='store_true', help='使用图形界面选择视频并展示结果')
    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}, CUDA available: {torch.cuda.is_available()}')

    # 交互选择视频
    video_path = args.video
    if args.gui or not video_path:
        picked = _select_video_via_gui(initial_dir=os.getcwd())
        if picked:
            video_path = picked
    if not video_path:
        print('未选择视频，已退出。')
        return

    # 构建模型并加载权重
    model = r3d_18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, args.num_classes)
    state = torch.load(args.weights, map_location='cpu')
    model.load_state_dict(state)
    model = model.to(device)
    model.eval()

    # 读取视频并取 16 帧
    video, _, _ = read_video(video_path, pts_unit='sec')  # [T,H,W,C], uint8
    video = sample_frames(video, num_frames=16)

    preprocess = VideoPreprocess(size=(112, 112))
    clip = preprocess(video)  # [C,T,H,W]
    clip = clip.unsqueeze(0).to(device)  # [1,C,T,H,W]

    with torch.no_grad():
        logits = model(clip)
        probs = torch.softmax(logits, dim=1).squeeze(0)
        topk = min(args.topk, probs.numel())
        values, indices = torch.topk(probs, k=topk)

    class_names = load_class_names(args.class_names)
    print('Prediction:')
    lines = []
    for rank, (p, idx) in enumerate(zip(values.tolist(), indices.tolist()), start=1):
        if class_names and 0 <= idx < len(class_names):
            name = class_names[idx]
        else:
            name = f'class_{idx}'
        line = f'Top{rank}: {name}  prob={p:.4f}  (idx={idx})'
        print(line)
        lines.append(line)

    if args.gui and lines:
        summary = f'视频: {os.path.basename(video_path)}\n' + '\n'.join(lines)
        _show_result_message('预测结果', summary)


if __name__ == '__main__':
    main()


