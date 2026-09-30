"""Explicit online setup only. The wiki harness never downloads automatically."""
from pathlib import Path
from huggingface_hub import snapshot_download

snapshot_download(repo_id='mlx-community/gemma-4-e2b-it-4bit',
                  revision='238767527555cb75a05732a84dff5d6ba0dd6809',
                  local_dir=Path(__file__).resolve().parent / 'model')
