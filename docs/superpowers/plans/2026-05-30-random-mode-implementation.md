# 随机提交模式实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 添加随机提交模式，让每天提交次数在指定区间内随机

**Architecture:** 在 Settings 配置类中添加 random_mode 和 random_range 字段，在 GitClient.run() 中根据开关选择使用固定次数或随机次数

**Tech Stack:** Python, pydantic-settings, random

---

## 文件结构

```
src/
  config.py       # 添加 random_mode 和 random_range 字段
  git_client.py   # 修改 run() 方法支持随机模式
.env.example      # 添加 FXSA_RANDOM 和 FXSA_RANDOM_RANGE
```

---

## 实现任务

### Task 1: 更新 config.py 添加随机配置字段

**Files:**
- Modify: `src/config.py`

- [ ] **Step 1: 添加 random import 并更新 Settings 类**

在文件顶部添加 `import random`

在 Settings 类的可选配置区域添加：

```python
# 随机模式配置
random_mode: bool = Field(default=False, description="随机提交开关")
random_range: str = Field(default="1,10", description="随机区间，格式 'min,max'")
```

添加解析方法：

```python
def parse_random_range(self) -> tuple[int, int]:
    """解析随机区间"""
    parts = self.random_range.split(",")
    min_val = int(parts[0].strip())
    max_val = int(parts[1].strip())
    if min_val > max_val:
        raise ValueError("random_range min must be <= max")
    if min_val < 1:
        raise ValueError("random_range min must be >= 1")
    return (min_val, max_val)

def get_commits_per_day(self) -> int:
    """获取每天提交次数"""
    if self.random_mode:
        min_val, max_val = self.parse_random_range()
        return random.randint(min_val, max_val)
    return self.commits_per_day
```

- [ ] **Step 2: 测试导入**

Run: `uv run python -c "from src.config import Settings; print('OK')"`

- [ ] **Step 3: Commit**

```bash
git add src/config.py
git commit -m "feat: add random_mode and random_range config"
```

---

### Task 2: 更新 git_client.py 支持随机模式

**Files:**
- Modify: `src/git_client.py`

- [ ] **Step 1: 修改 run() 方法**

在 `run()` 方法中，将：

```python
for commit_date in self.config.get_date_range():
    for _ in range(self.config.commits_per_day):
```

改为：

```python
for commit_date in self.config.get_date_range():
    commits_count = self.config.get_commits_per_day()
    for _ in range(commits_count):
```

- [ ] **Step 2: 测试导入**

Run: `uv run python -c "from src.git_client import GitClient; print('OK')"`

- [ ] **Step 3: Commit**

```bash
git add src/git_client.py
git commit -m "feat: support random commits per day"
```

---

### Task 3: 更新 .env.example

**Files:**
- Modify: `.env.example`

- [ ] **Step 1: 添加随机配置项**

在可选配置区域添加：

```env
# 随机模式配置
FXSA_RANDOM=false
FXSA_RANDOM_RANGE=1,10
```

- [ ] **Step 2: Commit**

```bash
git add .env.example
git commit -m "feat: add random mode config to .env.example"
```

---

### Task 4: 测试随机模式

**Files:**
- Test: `.env`

- [ ] **Step 1: 配置随机模式测试**

创建测试用的 .env：

```env
FXSA_AUTHOR_NAME=test
FXSA_AUTHOR_EMAIL=test@test.com
FXSA_START_DATE=2026-05-28
FXSA_END_DATE=2026-05-28
FXSA_RANDOM=true
FXSA_RANDOM_RANGE=1,5
```

- [ ] **Step 2: 运行测试**

Run: `uv run python -m src.main`

- [ ] **Step 3: 验证**

Run: `git log --oneline --all | head -10`

验证每天提交次数在 1-5 之间随机

---

## 验收检查

- [ ] `FXSA_RANDOM=false` 时使用固定次数（commits_per_day）
- [ ] `FXSA_RANDOM=true` 时使用随机次数（random_range）
- [ ] `FXSA_RANDOM_RANGE=1,5` 正确解析为 (1, 5)
- [ ] `.env.example` 包含新配置项
- [ ] 测试通过

---

**Plan complete.**