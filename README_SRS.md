# Karing 规则集转换和生成指南

这个仓库自动将 `list.txt` 转换为 Karing 应用使用的 `.srs` 规则集格式。

## 文件说明

- **list.txt** - 源规则文件（每行一个域名）
- **convert_to_srs.py** - 转换脚本（list.txt → JSON）
- **rules.json** - 中间格式文件（sing-box JSON 规则集）
- **rules.srs** - 最终输出（Karing SRS 二进制格式）
- **.github/workflows/build-srs.yml** - 自动编译工作流

## 工作流程

```
list.txt 
  ↓
  Python 脚本 (convert_to_srs.py)
  ↓
rules.json
  ↓
  sing-box rule-set compile
  ↓
rules.srs ✓ (Karing 可用)
```

## 如何使用

### 方式 1：自动化（推荐）
每次修改 `list.txt` 后提交，GitHub Actions 自动生成 `rules.srs`。

### 方式 2：本地生成
```bash
# 1. 转换为 JSON
python3 convert_to_srs.py list.txt rules.json

# 2. 下载 sing-box
wget https://github.com/SagerNet/sing-box/releases/download/v1.12.12/sing-box-1.12.12-linux-amd64.tar.gz
tar -xzf sing-box-1.12.12-linux-amd64.tar.gz
chmod +x sing-box-1.12.12-linux-amd64/sing-box

# 3. 编译为 SRS
./sing-box-1.12.12-linux-amd64/sing-box rule-set compile -o rules.srs rules.json
```

## 在 Karing 中使用

1. 打开 Karing 应用
2. 进入"分流规则"页面
3. 点击"添加新分流组" → "URL 导入"
4. 填入规则集 URL：
   ```
   https://raw.githubusercontent.com/Chakfang/BLOCK-RULE/main/rules.srs
   ```
5. 或使用 CDN 加速：
   ```
   https://cdn.jsdelivr.net/gh/Chakfang/BLOCK-RULE@main/rules.srs
   ```
6. 选择"分流规则"并保存

## 工作原理

### sing-box rule-set 格式说明

`.srs` 是 sing-box 的二进制规则集格式，具有以下特点：
- 高效的二进制格式，文件小
- 快速的域名匹配性能
- Karing 原生支持（基于 sing-box 核心）

### JSON 规则集格式

```json
{
  "version": 2,
  "rules": [
    {
      "domain_suffix": ["example.com", "test.org"]
    }
  ]
}
```

## 常见问题

**Q: 为什么需要三个文件？**
A: 
- `rules.json` 是可读的中间格式，便于调试
- `rules.srs` 是编译后的二进制格式，供 Karing 使用
- 两个文件都上传到仓库，用户可以选择使用哪个

**Q: 文件太大怎么办？**
A: Karing 有 3M 限制，超过限制建议：
- 分解为多个小规则集
- 只保留必要的域名
- 在 Windows 设备上使用（移动设备有内存限制）

**Q: 如何自定义规则？**
A: 直接编辑 `list.txt`，每行一个域名，格式示例：
```
example.com
test.org
*.ads.com
```

## 相关链接

- [sing-box 官方文档](https://sing-box.sagernet.org/)
- [Karing GitHub](https://github.com/KaringX/karing)
- [sing-box rule-set 格式](https://sing-box.sagernet.org/configuration/rule-set/)

## 许可证

MIT License
