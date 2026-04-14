[English](./README.md) | 中文

# ai-daily-feishu-briefing Skill

这个目录保存的是该 skill 在仓库里的源码副本。

## 这个 Skill 做什么

当你希望 Codex 来完成下面这些事情时，就用这个 skill：

- 抓取今天的 AI 论文和 AI 资讯
- 选出最值得看的内容
- 写成简洁的中文日报
- 发送到飞书私聊

它也可以帮助你搭建或修改配套的 Python 项目和调度脚本，但它的主用途仍然是“直接生成并发送日报”。

## 仓库副本和已安装 Skill 的区别

这个目录只是保存在 Git 里的源码副本。

Codex 不会默认从这个仓库目录直接加载 skill。要让 Codex 真正使用它，你需要把这个目录安装或复制到本机的 Codex skills 目录。

常见安装路径：

```text
C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

## 安装方式

在仓库根目录执行：

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

然后重新打开一个新的 Codex 会话，让它重新扫描 skills。

## 如何触发

示例提示词：

```text
Use $ai-daily-feishu-briefing，抓取今天最重要的 AI 论文和 AI 资讯，整理成中文日报，并发送到我的飞书私聊。
```

更聚焦的示例：

```text
Use $ai-daily-feishu-briefing，筛选今天最值得关注的 3 篇 AI 论文和 3 条 AI 资讯，摘要尽量简洁，然后发到飞书。
```

## 它和当前仓库的关系

- `skills/ai-daily-feishu-briefing/`
  skill 源码和文档
- `ai_daily_push/`
  独立 Python 工作流和稳定的飞书发送器
- `codex_scheduler/`
  Codex 包装脚本和 Windows 定时任务集成

当前仓库里推荐的使用方式是：

1. Codex 使用这个 skill 选题并写日报
2. 外层脚本始终先把结果写成 UTF-8 文本文件
3. 如果当前 shell 是 `pwsh` / PowerShell 7，Codex 直接用 `lark-cli` 发飞书
4. 如果当前 shell 是旧的 `powershell.exe` / Windows PowerShell 5，外层脚本回退到 Python sender 发送 UTF-8 文件

这样做是为了兼顾两种 Windows 环境：

- `pwsh` 下可以稳定直发中文
- 旧 PowerShell 下仍然保留一条更稳的 UTF-8 文件发送兜底路径

判断当前 shell 的最简单方法：

```powershell
$PSVersionTable.PSEdition
```

- `Core` 表示 `pwsh` / PowerShell 7
- `Desktop` 表示旧 `powershell.exe` / Windows PowerShell 5

## 如果想改成别的主题

如果你想把这套模式改成商业、金融、政策等主题，最稳的做法是复制一个新的 skill 目录，再改主题相关文件。

优先修改：

- `SKILL.md`
  skill 名称、目标、默认来源
- `references/codex-workflow.md`
  选题规则和高价值内容判断
- `references/prompting.md`
  摘要风格和“为什么值得关注”的角度
- `agents/openai.yaml`
  展示名称和默认 prompt

通常不需要先动发送基础设施。

## 目录内容

- `SKILL.md`
  真正给 Codex 读取的 skill 主文件
- `agents/openai.yaml`
  本地显示元数据
- `references/`
  架构、工作流、飞书、提示词参考
- `scripts/doctor.py`
  本地依赖检查
- `scripts/send_test_message.py`
  飞书测试消息脚本
