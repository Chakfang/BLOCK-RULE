#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 list.txt 中的域名列表转换为 Clash 格式规则
"""

def generate_clash_rules():
    # 读取 list.txt
    with open('list.txt', 'r', encoding='utf-8') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    # 生成 Clash 规则
    rules = []
    for domain in domains:
        rules.append(f"DOMAIN-SUFFIX,{domain},REJECT")
    
    # 写入 clash.txt
    with open('clash.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(rules))
    
    print(f"✓ 成功生成 {len(rules)} 条规则到 clash.txt")

if __name__ == '__main__':
    generate_clash_rules()
