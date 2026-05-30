fake-commit

生成假 git 提交历史的 CLI 工具，让你的提交记录看起来更真实。

## 功能特点

- 支持指定日期范围生成提交
- 支持固定提交次数模式
- 支持随机提交次数模式
- 每次提交使用随机时间戳，更真实
- 零依赖配置，即装即用

## 安装

```bash
pip install fake-commit
```

或使用 uv：

```bash
uv pip install fake-commit
```

或直接从源码安装：

```bash
uv tool install .
```

## 卸载

```bash
uv tool uninstall fake-commit
```

或通过 pip：

```bash
pip uninstall fake-commit
```

## 配置

复制 `.env.example` 为 `.env`，配置以下环境变量：

### 必需配置

| 环境变量 | 说明 |
|---------|------|
| `FAKE_AUTHOR_NAME` | Git 提交用户名 |
| `FAKE_AUTHOR_EMAIL` | Git 提交邮箱 |

### 可选配置

| 环境变量 | 默认值 | 说明 |
|---------|-------|------|
| `FAKE_START_DATE` | 2026-01-01 | 开始日期 |
| `FAKE_END_DATE` | 2026-01-31 | 结束日期 |
| `FAKE_BRANCH` | main | 分支名 |
| `FAKE_COMMITS_PER_DAY` | 1 | 每天提交次数（固定模式） |
| `FAKE_RANDOM` | false | 是否启用随机模式 |
| `FAKE_RANDOM_RANGE` | 1,10 | 随机提交区间（格式：min,max） |

## 使用方法

### 固定模式

每天固定生成指定次数提交：

```env
FAKE_RANDOM=false
FAKE_COMMITS_PER_DAY=3
```

### 随机模式

每天随机生成 1~10 次提交：

```env
FAKE_RANDOM=true
FAKE_RANDOM_RANGE=1,10
```

### 运行

```bash
python -m src.main
```

或安装后：

```bash
fc -n "用户名" -e "email@example.com"
```

## 示例输出

```
开始生成提交历史...
作者: esyion <qingboup@gmail.com>
日期范围: 2026-01-01 - 2026-01-31
完成！共生成 93 次提交
```

## 注意事项

- 生成提交会创建 `.commit_marker` 文件作为提交内容
- 每次提交使用当天随机时间戳（小时:分钟:秒）
- 建议在测试仓库中使用

## License

MIT