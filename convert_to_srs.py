#!/usr/bin/env python3
"""
转换脚本：将 list.txt 格式转换为 sing-box rule-set JSON 格式
然后可以用 sing-box rule-set compile 命令编译为 .srs 二进制文件
"""

import json
import sys
from pathlib import Path


def convert_list_to_json(input_file: str, output_file: str) -> int:
    """
    将列表文件转换为 sing-box rule-set JSON 格式
    
    Args:
        input_file: 输入文件路径（每行一个域名）
        output_file: 输出文件路径（sing-box JSON 格式）
    
    Returns:
        转换的域名数量
    """
    domains = set()
    
    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                # 如果已经是其他格式，提取域名
                if ',' in line:
                    # Clash 格式: DOMAIN-SUFFIX,domain.com
                    domain = line.split(',')[-1]
                elif line.startswith('||'):
                    # AdGuard 格式: ||domain.com^
                    domain = line.replace('||', '').replace('^', '')
                else:
                    domain = line
                
                # 基本验证：确保是有效的域名格式
                if domain and '.' in domain:
                    domains.add(domain)
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
        return 0
    except Exception as e:
        print(f"错误读取文件：{e}")
        return 0
    
    # 排序域名
    sorted_domains = sorted(list(domains))
    
    # 构建 sing-box rule-set JSON 格式
    # 参考: https://sing-box.sagernet.org/configuration/rule-set/
    rule_set = {
        "version": 2,
        "rules": []
    }
    
    for domain in sorted_domains:
        rule_set["rules"].append({
            "domain_suffix": [domain]
        })
    
    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rule_set, f, ensure_ascii=False, indent=2)
        print(f"✓ JSON 转换完成！")
        print(f"  输入文件：{input_file}")
        print(f"  输出文件：{output_file}")
        print(f"  域名数量：{len(sorted_domains)}")
        return len(sorted_domains)
    except Exception as e:
        print(f"错误写入文件：{e}")
        return 0


def main():
    """主函数"""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'rules.json'
    else:
        input_file = 'list.txt'
        output_file = 'rules.json'
    
    print(f"开始转换为 sing-box JSON 格式...")
    print(f"输入：{input_file}")
    print(f"输出：{output_file}\n")
    
    count = convert_list_to_json(input_file, output_file)
    if count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
