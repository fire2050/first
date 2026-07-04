# 官网项目 GitHub 版本管理方案

## 一、方案概述

将「智慧解决方案事业部官网」项目接入 GitHub，实现：
- 代码版本管理（溯源、回滚、分支开发）
- 多人协作（PR、Code Review）
- 免费静态网站托管（GitHub Pages）
- CI/CD 自动部署

---

## 二、准备工作

### 2.1 账号与工具
| 项目 | 说明 |
|------|------|
| GitHub 账号 | 如无账号，先注册 https://github.com/ |
| Git 安装 | 当前环境已安装（可通过 `git --version` 验证） |
| 仓库类型 | 建议选 **Private**（官网代码不公开），如需开源选 Public |

### 2.2 项目文件梳理

**需要纳入版本管理：**
```
index.html
contact.html
service.html
product-*.html    (12个产品页)
solution-*.html    (4个解决方案页)
images/            (产品图片，约52个文件)
```

**需要排除（`.gitignore`）：**
```
.workbuddy/        # AI 工作区数据，含本地记忆，不应提交
nul                # 空文件，无意义
*.py               # 本地开发脚本（可选：如需共享工具脚本可保留）
*.md               # 设计文档（可选：如属项目资产可保留）
```

---

## 三、实施步骤

### 步骤 1：在 GitHub 创建远程仓库

1. 登录 https://github.com/ → 点击右上角 **+** → **New repository**
2. 填写仓库信息：
   - **Repository name**：`smart-solution-website`（或自定义名称）
   - **Visibility**：选 **Private**（推荐，官网代码不公开）
   - **初始化**：**不要**勾选 Initialize with README / .gitignore / license（本地已有文件）
3. 点击 **Create repository**
4. 创建后，复制仓库 URL（类似 `https://github.com/用户名/仓库名.git`）

---

### 步骤 2：本地初始化 Git 仓库

在项目根目录执行：

```bash
# 进入项目目录
cd "C:/Users/fire2/WorkBuddy/2026-06-30-11-01-53"

# 初始化 Git
git init

# 设置用户名和邮箱（首次使用需配置）
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"

# 验证
git config user.name
git config user.email
```

---

### 步骤 3：创建 `.gitignore` 文件

在项目根目录创建 `.gitignore`，排除不需要版本管理的文件：

```gitignore
# WorkBuddy 本地工作区（AI记忆、本地配置）
.workbuddy/

# 空文件/临时文件
nul
*.tmp
*.log

# 可选：排除本地开发脚本（如仅自己使用）
# *.py

# 可选：排除设计文档（如不属于网站资产）
# *.md

# 系统文件
.DS_Store
Thumbs.db
```

---

### 步骤 4：提交本地文件

```bash
# 查看待提交文件（确认.gitignore生效）
git status

# 添加所有需要版本管理的文件
git add .

# 查看暂存区（再次确认）
git status

# 首次提交
git commit -m "Initial commit: 智慧解决方案事业部官网 v1.0"
```

---

### 步骤 5：关联远程仓库并推送

```bash
# 关联远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 验证关联
git remote -v

# 推送至 GitHub（首次推送）
git push -u origin main
```

> **注意**：如 GitHub 默认分支名为 `master`，将 `main` 替换为 `master`，或先在 GitHub 修改为 `main`。

**认证方式（二选一）：**
- **推荐：Personal Access Token (PAT)**
  1. GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  2. 勾选 `repo` 权限，生成 token
  3. 推送时密码处粘贴 token（不是 GitHub 登录密码）
- **备选：SSH Key**
  1. 生成 SSH Key：`ssh-keygen -t ed25519 -C "你的邮箱"`
  2. 将 `~/.ssh/id_ed25519.pub` 内容添加到 GitHub → Settings → SSH and GPG keys

---

## 四、日常使用流程

### 4.1 修改文件后提交

```bash
# 1. 修改文件（如 index.html）

# 2. 查看变更
git status
git diff

# 3. 暂存并提交
git add index.html
git commit -m "更新首页：服务能力矩阵添加二级页面链接"

# 4. 推送至 GitHub
git push
```

### 4.2 拉取远程最新代码

```bash
# 开始前拉取最新代码（多人协作时必需）
git pull
```

### 4.3 版本回滚

```bash
# 查看提交历史
git log --oneline

# 回滚到某个提交（硬回滚，会丢失当前修改）
git reset --hard <commit-id>

# 安全回滚（生成新提交，不丢失历史）
git revert <commit-id>
```

### 4.4 分支管理（推荐工作流）

```bash
# 创建功能分支（如开发新页面）
git checkout -b feature/new-product-page

# 在分支上开发...
git add .
git commit -m "新增XX产品页面"

# 合并回主分支
git checkout main
git merge feature/new-product-page

# 删除已合并的分支
git branch -d feature/new-product-page

# 推送
git push
```

---

## 五、进阶：GitHub Pages 免费托管官网

如需将官网部署到公网（免费），可启用 GitHub Pages：

### 5.1 启用步骤

1. GitHub 仓库页面 → **Settings** → **Pages**
2. **Source** → 选择 `main` 分支 → `/ (root)` 目录 → **Save**
3. 等待 1-2 分钟，GitHub 会生成访问地址：
   `https://你的用户名.github.io/你的仓库名/`

### 5.2 注意事项

| 问题 | 说明 |
|------|------|
| 仓库必须为 Public | GitHub Pages 免费版仅支持公开仓库（Private 需付费） |
| 自定义域名 | 可在 Settings → Pages → Custom domain 绑定自己的域名 |
| 更新延迟 | 推送后约 1-3 分钟生效（有 CDN 缓存） |
| 图片加载 | `images/` 目录需一并提交，注意单个文件 ≤ 100MB |

### 5.3 如果仓库是 Private 又想用 Pages

方案：使用 **CloudStudio 部署**（已在 Skill 中支持），或：
- 将仓库改为 Public（如不涉密）
- 使用 Netlify / Vercel 等第三方托管（支持 Private 仓库）

---

## 六、推荐的分支与发布策略

```
main / master     ← 生产环境（始终可部署）
develop           ← 开发集成分支
feature/xxx       ← 功能分支（开发完成后合并至 develop）
hotfix/xxx        ← 紧急修复（直接从 main 拉出，修复后合并回 main + develop）
```

**发布流程：**
1. 日常开发在 `feature/xxx` 分支
2. 开发完成 → 合并至 `develop` → 测试
3. 测试通过 → 合并至 `main` → 打 Tag（如 `v1.0.0`）
4. 如启用 GitHub Pages，`main` 分支自动部署

---

## 七、常见问题

### Q1：图片太多，推送很慢怎么办？
- 使用 `.gitignore` 排除 `images/` 中的大图（仅保留占位图）
- 或用 **Git LFS** 管理大文件：`git lfs install && git lfs track "*.png" *.jpg"`

### Q2：不小心提交了敏感信息（密码、Token）怎么办？
- **立即** 撤销提交并重新提交（如尚未推送）
- 如已推送：轮换密钥，再用 `git filter-branch` 或 **BFG Repo-Cleaner** 清除历史记录

### Q3：`.workbuddy/` 目录已被提交怎么办？
```bash
# 从 Git 中删除（但保留本地文件）
git rm -r --cached .workbuddy/
git commit -m "Remove .workbuddy from repo"
git push
```

---

## 八、一键执行脚本（可选）

将以下步骤保存为 `setup-git.sh`（Windows 用 Git Bash 运行）：

```bash
#!/bin/bash
# 官网项目 Git 初始化脚本

REPO_URL="https://github.com/你的用户名/你的仓库名.git"

echo "=== 初始化 Git 仓库 ==="
git init

echo "=== 创建 .gitignore ==="
cat > .gitignore << 'EOF'
.workbuddy/
nul
*.tmp
*.log
.DS_Store
Thumbs.db
EOF

echo "=== 首次提交 ==="
git add .
git commit -m "Initial commit: 智慧解决方案事业部官网"

echo "=== 关联远程仓库 ==="
git remote add origin $REPO_URL

echo "=== 推送至 GitHub ==="
git branch -M main
git push -u origin main

echo "=== 完成！==="
```

---

*文档版本：v1.0 | 更新日期：2026-07-04*
