#!/usr/bin/env python3
"""
Python reimplementation of script.wl.
Opens a sequence file, pads sequences, and exports the result while printing debug info.
"""

import os
import sys
from collections import Counter


def ask_file_path() -> str | None:
    """Try to choose a file via GUI; fall back to CLI input."""
    if len(sys.argv) > 1:
        return sys.argv[1]

    try:
        # Lazy import so we only require tkinter when GUI is available.
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title="选择序列文件")
        root.update()
        root.destroy()
        return path or None
    except Exception as exc:  # noqa: BLE001
        print(f"[debug] GUI file picker unavailable ({exc}); falling back to manual input.")

    path = input("请输入文件路径 (或留空取消): ").strip()
    return path or None


def split_prefix_before_syn(file_path: str) -> str:
    """Extract prefix before the first 'syn' in the basename (mirrors StringSplit[..., 'syn'][[1]])."""
    base = os.path.splitext(os.path.basename(file_path))[0]
    return base.split("syn", 1)[0]


def pad_with_pattern(text: str, target_len: int, pattern: str) -> str:
    """Pad text to target_len using a repeating pattern."""
    if len(text) >= target_len:
        return text

    repeats_needed = target_len - len(text)
    pattern_repeats = (pattern * ((repeats_needed // len(pattern)) + 1))[:repeats_needed]
    return text + pattern_repeats


def main() -> None:
    file_path = ask_file_path()
    if not file_path:
        print("[debug] No file selected; exiting.")
        return

    print(f"[debug] Selected file: {file_path}")
    if "DPI_out" not in os.path.basename(file_path):
        sys.exit("[error] 文件名中未找到 'DPI_out' 标记，终止处理。")

    with open(file_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    data_in = content.split()
    if not data_in:
        print("[debug] No sequences found in file; exiting.")
        return

    length_counts = Counter(len(seq) for seq in data_in)
    print(f"[debug] Sequence length counts: {dict(length_counts)}")

    max_len = max(length_counts)
    print(f"[debug] Max sequence length: {max_len}")

    # First pad with '0' to max_len, then pad with pattern "AATAT" to max_len + 5.
    padded_once = [seq.upper().ljust(max_len, "0") for seq in data_in]
    out = [pad_with_pattern(seq, max_len + 5, "AATAT") for seq in padded_once]

    machine_no = input("请输入合成仪编号: ")
    name = f"{split_prefix_before_syn(file_path)}680k_{max_len + 5}mer_pickout{machine_no}.txt"
    output_path = os.path.join(os.path.dirname(file_path) or ".", name)
    print(f"[debug] Output file: {output_path}")

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    print(f"[debug] Wrote {len(out)} sequences to {output_path}")


if __name__ == "__main__":
    main()
