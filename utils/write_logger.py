#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
写入日志器 - Write Logger
记录所有文件写入操作，便于追溯和审计
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

class WriteLogger:
    def __init__(self, log_file: str = '/home/admin/.openclaw/workspace/logs/write_operations.jsonl'):
        """
        初始化写入日志器
        
        Args:
            log_file: 日志文件路径
        """
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, operation: str, file_path: str, owner_id: str, 
            content_preview: str = '', status: str = 'success',
            error: str = '', metadata: Optional[Dict] = None):
        """
        记录写入操作
        
        Args:
            operation: 操作类型（write/edit/delete/read）
            file_path: 文件路径
            owner_id: 操作者 ID（如：SF-0001）
            content_preview: 内容预览（前 100 字符）
            status: 操作状态（success/failed）
            error: 错误信息
            metadata: 额外元数据
        """
        log_entry = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'operation': operation,
            'file_path': str(file_path),
            'owner_id': owner_id,
            'content_preview': content_preview[:100] if content_preview else '',
            'content_length': len(content_preview),
            'status': status,
            'error': error,
            'metadata': metadata or {}
        }
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f'❌ 写入日志失败：{e}')
    
    def get_history(self, file_path: str = None, owner_id: str = None, 
                    limit: int = 100, operation: str = None) -> List[Dict]:
        """
        查询写入历史
        
        Args:
            file_path: 文件路径（可选）
            owner_id: 操作者 ID（可选）
            limit: 返回数量限制
            operation: 操作类型（可选）
        
        Returns:
            list: 历史操作列表
        """
        history = []
        
        if not self.log_file.exists():
            return history
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    # 过滤
                    if file_path and file_path not in entry['file_path']:
                        continue
                    if owner_id and owner_id != entry['owner_id']:
                        continue
                    if operation and operation != entry['operation']:
                        continue
                    
                    history.append(entry)
                    
                    if len(history) >= limit:
                        break
                except:
                    continue
        
        return history
    
    def get_failed_operations(self, limit: int = 50) -> List[Dict]:
        """获取失败的操作记录"""
        history = []
        
        if not self.log_file.exists():
            return history
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('status') == 'failed':
                        history.append(entry)
                        if len(history) >= limit:
                            break
                except:
                    continue
        
        return history
    
    def get_statistics(self, days: int = 7) -> Dict:
        """
        获取统计信息
        
        Args:
            days: 统计天数
        
        Returns:
            dict: 统计信息
        """
        history = self.get_history(limit=10000)
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        stats = {
            'total_operations': 0,
            'success_count': 0,
            'failed_count': 0,
            'by_operation': {},
            'by_owner': {}
        }
        
        for entry in history:
            if entry['timestamp'] < cutoff_time:
                continue
            
            stats['total_operations'] += 1
            
            if entry['status'] == 'success':
                stats['success_count'] += 1
            else:
                stats['failed_count'] += 1
            
            # 按操作类型统计
            op_type = entry['operation']
            stats['by_operation'][op_type] = stats['by_operation'].get(op_type, 0) + 1
            
            # 按操作者统计
            owner = entry['owner_id']
            stats['by_owner'][owner] = stats['by_owner'].get(owner, 0) + 1
        
        return stats
    
    def cleanup_old_logs(self, days: int = 30):
        """清理旧日志"""
        if not self.log_file.exists():
            return
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        temp_file = self.log_file.with_suffix('.tmp')
        
        with open(self.log_file, 'r', encoding='utf-8') as f_in:
            with open(temp_file, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    try:
                        entry = json.loads(line)
                        if entry['timestamp'] >= cutoff_time:
                            f_out.write(line)
                    except:
                        continue
        
        temp_file.replace(self.log_file)
        print(f'🧹 清理{days}天前的日志')

# 测试
if __name__ == '__main__':
    logger = WriteLogger()
    
    # 测试记录日志
    logger.log('write', '/tmp/test.txt', 'SF-0001', '测试内容', 'success')
    logger.log('edit', '/tmp/test.txt', 'SF-0001', '修改内容', 'failed', '测试错误')
    
    # 测试查询历史
    history = logger.get_history(limit=10)
    print(f'历史记录：{len(history)} 条')
    
    # 测试统计
    stats = logger.get_statistics(days=7)
    print(f'统计：{stats}')
