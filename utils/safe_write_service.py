#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全写入服务 - Safe Write Service
整合文件锁、原子写入、日志记录，提供统一的文件操作接口
"""

from pathlib import Path
from typing import Optional, Dict
from file_lock import FileLockManager
from atomic_writer import AtomicWriter
from write_logger import WriteLogger

class SafeWriteService:
    def __init__(self, owner_id: str = 'unknown'):
        """
        初始化安全写入服务
        
        Args:
            owner_id: 操作者 ID（如：SF-0001）
        """
        self.owner_id = owner_id
        self.lock_manager = FileLockManager()
        self.atomic_writer = AtomicWriter(max_backups=3)
        self.logger = WriteLogger()
    
    def write_file(self, file_path: str, content: str, 
                   encoding: str = 'utf-8',
                   timeout: int = 30,
                   make_backup: bool = True) -> bool:
        """
        安全写入文件（带锁 + 原子写入 + 日志）
        
        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码
            timeout: 获取锁的超时时间（秒）
            make_backup: 是否创建备份
        
        Returns:
            bool: 写入是否成功
        """
        # 1. 获取锁
        if not self.lock_manager.acquire(file_path, self.owner_id, timeout):
            self.logger.log('write', file_path, self.owner_id, 
                          content[:100], 'failed', '获取锁失败')
            return False
        
        try:
            # 2. 原子写入
            success = self.atomic_writer.write(file_path, content, encoding, make_backup)
            
            # 3. 记录日志
            status = 'success' if success else 'failed'
            error = '' if success else '原子写入失败'
            self.logger.log('write', file_path, self.owner_id, 
                          content[:100], status, error)
            
            return success
            
        finally:
            # 4. 释放锁（无论成功失败都释放）
            self.lock_manager.release(file_path, self.owner_id)
    
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        读取文件（无锁，只读）
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
        
        Returns:
            str: 文件内容，失败返回 None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # 只读操作不记录详细日志（避免日志过多）
            self.logger.log('read', file_path, self.owner_id, 
                          content[:50], 'success')
            return content
        except Exception as e:
            self.logger.log('read', file_path, self.owner_id, 
                          '', 'failed', str(e))
            return None
    
    def edit_file(self, file_path: str, old_text: str, new_text: str,
                  encoding: str = 'utf-8',
                  timeout: int = 30) -> bool:
        """
        编辑文件（读取 - 修改 - 写入）
        
        Args:
            file_path: 文件路径
            old_text: 要替换的旧文本
            new_text: 新文本
            encoding: 文件编码
            timeout: 获取锁的超时时间（秒）
        
        Returns:
            bool: 编辑是否成功
        """
        # 1. 获取锁
        if not self.lock_manager.acquire(file_path, self.owner_id, timeout):
            self.logger.log('edit', file_path, self.owner_id, 
                          f'{old_text[:50]}... -> {new_text[:50]}...', 
                          'failed', '获取锁失败')
            return False
        
        try:
            # 2. 读取文件
            content = self.read_file(file_path, encoding)
            if content is None:
                self.logger.log('edit', file_path, self.owner_id, 
                              f'{old_text[:50]}... -> {new_text[:50]}...', 
                              'failed', '读取文件失败')
                return False
            
            # 3. 替换文本
            if old_text not in content:
                error = '未找到要替换的文本'
                self.logger.log('edit', file_path, self.owner_id, 
                              f'{old_text[:50]}... -> {new_text[:50]}...', 
                              'failed', error)
                return False
            
            new_content = content.replace(old_text, new_text)
            
            # 4. 原子写入
            success = self.atomic_writer.write(file_path, new_content, encoding)
            
            # 5. 记录日志
            status = 'success' if success else 'failed'
            error = '' if success else '原子写入失败'
            self.logger.log('edit', file_path, self.owner_id, 
                          f'{old_text[:50]}... -> {new_text[:50]}...', 
                          status, error)
            
            return success
            
        finally:
            # 6. 释放锁
            self.lock_manager.release(file_path, self.owner_id)
    
    def delete_file(self, file_path: str, timeout: int = 30) -> bool:
        """
        删除文件（带锁 + 备份）
        
        Args:
            file_path: 文件路径
            timeout: 获取锁的超时时间（秒）
        
        Returns:
            bool: 删除是否成功
        """
        # 1. 获取锁
        if not self.lock_manager.acquire(file_path, self.owner_id, timeout):
            self.logger.log('delete', file_path, self.owner_id, 
                          '', 'failed', '获取锁失败')
            return False
        
        try:
            # 2. 备份（如果需要）
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                # 创建备份
                import shutil
                import time
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_path = file_path_obj.with_suffix(f'{file_path_obj.suffix}.deleted.{timestamp}')
                shutil.copy2(file_path_obj, backup_path)
                print(f'💾 删除前备份：{backup_path}')
                
                # 3. 删除文件
                file_path_obj.unlink()
                
                # 4. 记录日志
                self.logger.log('delete', file_path, self.owner_id, 
                              '', 'success')
                print(f'✅ 删除成功：{file_path}')
                return True
            else:
                self.logger.log('delete', file_path, self.owner_id, 
                              '', 'failed', '文件不存在')
                return False
            
        except Exception as e:
            self.logger.log('delete', file_path, self.owner_id, 
                          '', 'failed', str(e))
            return False
        finally:
            # 5. 释放锁
            self.lock_manager.release(file_path, self.owner_id)
    
    def cleanup(self):
        """清理：释放所有锁"""
        self.lock_manager.release_all(self.owner_id)
        print(f'🧹 {self.owner_id} 清理所有锁')
    
    def get_write_history(self, limit: int = 100):
        """获取写入历史"""
        return self.logger.get_history(owner_id=self.owner_id, limit=limit)
    
    def get_statistics(self, days: int = 7):
        """获取统计信息"""
        return self.logger.get_statistics(days=days)

# 测试
if __name__ == '__main__':
    # 测试
    writer = SafeWriteService(owner_id='SF-0001')
    
    # 测试写入
    success = writer.write_file('/tmp/test_safe.txt', '# 安全写入测试\n这是测试内容')
    print(f'写入：{success}')
    
    # 测试读取
    content = writer.read_file('/tmp/test_safe.txt')
    print(f'读取：{content[:50] if content else "失败"}')
    
    # 测试编辑
    success = writer.edit_file('/tmp/test_safe.txt', '测试内容', '修改内容')
    print(f'编辑：{success}')
    
    # 测试删除
    success = writer.delete_file('/tmp/test_safe.txt')
    print(f'删除：{success}')
    
    # 获取历史
    history = writer.get_write_history(limit=10)
    print(f'历史：{len(history)} 条')
    
    # 获取统计
    stats = writer.get_statistics(days=7)
    print(f'统计：{stats}')
    
    # 清理
    writer.cleanup()
