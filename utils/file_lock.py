#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件锁管理器 - File Lock Manager
防止多进程/多娃并发写入同一文件
"""

import os
import time
from pathlib import Path
from typing import Optional, Dict

class FileLockManager:
    def __init__(self, lock_dir: str = '/tmp/openclaw_locks'):
        """
        初始化文件锁管理器
        
        Args:
            lock_dir: 锁文件存储目录
        """
        self.lock_dir = Path(lock_dir)
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        self.lock_timeout = 300  # 5 分钟超时
        self.held_locks = {}  # 当前持有的锁
    
    def _get_lock_path(self, file_path: str) -> Path:
        """获取锁文件路径"""
        file_id = str(file_path).replace('/', '_').replace('.', '_')
        return self.lock_dir / f'{file_id}.lock'
    
    def acquire(self, file_path: str, owner_id: str, timeout: int = 30) -> bool:
        """
        获取文件锁
        
        Args:
            file_path: 要锁定的文件路径
            owner_id: 锁持有者 ID（如：SF-0001）
            timeout: 等待超时时间（秒）
        
        Returns:
            bool: 是否成功获取锁
        """
        lock_path = self._get_lock_path(file_path)
        start_time = time.time()
        
        while True:
            # 检查锁是否存在
            if not lock_path.exists():
                # 尝试创建锁
                try:
                    lock_path.write_text(f'{owner_id}:{time.time()}')
                    self.held_locks[file_path] = lock_path
                    print(f'🔒 {owner_id} 获取锁：{file_path}')
                    return True
                except FileExistsError:
                    # 并发创建，失败重试
                    continue
            
            # 锁已存在，检查是否过期
            try:
                lock_content = lock_path.read_text()
                lock_owner, lock_time = lock_content.split(':')
                lock_age = time.time() - float(lock_time)
                
                if lock_age > self.lock_timeout:
                    # 锁过期，强制释放
                    print(f'⚠️ 锁过期，强制释放：{file_path} (持有者：{lock_owner})')
                    lock_path.unlink()
                    continue
                
                # 锁有效，等待
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    print(f'❌ {owner_id} 获取锁超时：{file_path} (当前持有者：{lock_owner})')
                    return False
                
                print(f'⏳ {owner_id} 等待锁：{file_path} (已等待{elapsed:.1f}s)')
                time.sleep(0.5)
                
            except Exception as e:
                print(f'⚠️ 读取锁文件失败：{e}')
                lock_path.unlink()
                continue
    
    def release(self, file_path: str, owner_id: str) -> bool:
        """释放文件锁"""
        lock_path = self._get_lock_path(file_path)
        
        if lock_path.exists():
            try:
                lock_content = lock_path.read_text()
                lock_owner = lock_content.split(':')[0]
                
                if lock_owner == owner_id:
                    lock_path.unlink()
                    if file_path in self.held_locks:
                        del self.held_locks[file_path]
                    print(f'🔓 {owner_id} 释放锁：{file_path}')
                    return True
                else:
                    print(f'⚠️ {owner_id} 尝试释放不属于自己的锁（当前持有者：{lock_owner}）')
                    return False
            except Exception as e:
                print(f'❌ 释放锁失败：{e}')
                return False
        
        return True
    
    def release_all(self, owner_id: str):
        """释放某个持有者的所有锁"""
        for file_path in list(self.held_locks.keys()):
            self.release(file_path, owner_id)
    
    def cleanup_stale_locks(self):
        """清理所有过期锁"""
        for lock_path in self.lock_dir.glob('*.lock'):
            try:
                lock_content = lock_path.read_text()
                lock_time = float(lock_content.split(':')[1])
                if time.time() - lock_time > self.lock_timeout:
                    lock_path.unlink()
                    print(f'🧹 清理过期锁：{lock_path}')
            except:
                continue

# 测试
if __name__ == '__main__':
    lock_mgr = FileLockManager()
    
    # 测试获取锁
    success = lock_mgr.acquire('/tmp/test.txt', 'SF-0001')
    print(f'获取锁：{success}')
    
    # 测试释放锁
    lock_mgr.release('/tmp/test.txt', 'SF-0001')
    
    # 清理过期锁
    lock_mgr.cleanup_stale_locks()
