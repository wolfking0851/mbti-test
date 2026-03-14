#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原子写入器 - Atomic Writer
确保写入操作要么完全成功，要么完全失败
"""

import os
import shutil
import time
from pathlib import Path
from typing import Optional

class AtomicWriter:
    def __init__(self, max_backups: int = 3):
        """
        初始化原子写入器
        
        Args:
            max_backups: 最大备份数量
        """
        self.max_backups = max_backups
    
    def write(self, file_path: str, content: str, 
              encoding: str = 'utf-8', 
              make_backup: bool = True) -> bool:
        """
        原子写入文件
        
        Args:
            file_path: 目标文件路径
            content: 文件内容
            encoding: 文件编码
            make_backup: 是否创建备份
        
        Returns:
            bool: 写入是否成功
        """
        file_path = Path(file_path)
        temp_path = file_path.with_suffix(file_path.suffix + '.tmp')
        
        try:
            # 1. 创建备份（如果需要）
            if make_backup and file_path.exists():
                self._create_backup(file_path)
            
            # 2. 确保目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 3. 写入临时文件
            with open(temp_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # 4. 原子重命名（关键步骤）
            os.replace(temp_path, file_path)
            
            # 5. 清理旧备份
            if make_backup:
                self._cleanup_old_backups(file_path)
            
            print(f'✅ 原子写入成功：{file_path}')
            return True
            
        except Exception as e:
            print(f'❌ 原子写入失败：{e}')
            # 清理临时文件
            if temp_path.exists():
                temp_path.unlink()
            return False
    
    def _create_backup(self, file_path: Path):
        """创建带时间戳的备份"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = file_path.with_suffix(f'{file_path.suffix}.bak.{timestamp}')
        shutil.copy2(file_path, backup_path)
        print(f'💾 创建备份：{backup_path}')
    
    def _cleanup_old_backups(self, file_path: Path):
        """清理旧备份，只保留最新的 N 个"""
        backup_pattern = f'{file_path.name}.bak.*'
        backups = sorted(file_path.parent.glob(backup_pattern))
        
        # 删除多余的备份
        for old_backup in backups[:-self.max_backups]:
            try:
                old_backup.unlink()
                print(f'🧹 清理旧备份：{old_backup}')
            except:
                continue
    
    def write_with_retry(self, file_path: str, content: str, 
                         encoding: str = 'utf-8',
                         max_retries: int = 3) -> bool:
        """
        带重试的原子写入
        
        Args:
            file_path: 目标文件路径
            content: 文件内容
            encoding: 文件编码
            max_retries: 最大重试次数
        
        Returns:
            bool: 写入是否成功
        """
        for i in range(max_retries):
            if self.write(file_path, content, encoding):
                return True
            print(f'⚠️ 重试 {i+1}/{max_retries}: {file_path}')
            time.sleep(0.5)
        
        print(f'❌ 写入失败，已重试 {max_retries} 次：{file_path}')
        return False

# 测试
if __name__ == '__main__':
    writer = AtomicWriter(max_backups=3)
    
    # 测试写入
    success = writer.write('/tmp/test_atomic.txt', '# 测试内容\n这是原子写入测试')
    print(f'写入成功：{success}')
    
    # 测试带重试写入
    success = writer.write_with_retry('/tmp/test_retry.txt', '# 重试测试')
    print(f'重试写入成功：{success}')
