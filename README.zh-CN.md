[English](./README.md) | 中文

# AI 每日论文与飞书简报

这个仓库包含两套相关但分工不同的工作流，用来把“每日 AI 论文 + AI 资讯简报”发送到飞书私聊。

## 仓库包含什么

- `skills/ai-daily-feishu-briefing/`
  这个 skill 的仓库源码副本，里面包含 `SKILL.md`、参考文档、辅助脚本和使用说明。
- `ai_daily_push/`
  一个独立的 Python 项目，用来抓取候选内容、排序、渲染中文简报，并通过飞书发送。
- `codex_scheduler/`
  一个 Codex 驱动的调度层。它会调用本机已经安装的 `ai-daily-feishu-briefing` skill，通过 `codex exec` 生成日报到 UTF-8 文件，再复用项目里的稳定发送器把文件发到飞书。
- `项目.md`
  早期的中文设计草稿。

## Skill 和项目的区别

这个仓库同时保留了两条路径：

### 1. Skill 驱动路径

适用于你希望由 Codex 完成最终筛选和撰写的场景。

流程如下：

1. Windows 任务计划程序，或者手动执行 PowerShell
2. `codex_scheduler/run_codex_briefing.ps1`
3. `codex exec`
4. 本地 skill：`ai-daily-feishu-briefing`
5. 生成 `ai_daily_push/briefing_feishu_today.txt`
6. 通过稳定的飞书发送器发送该文件

这条路径适合“让 Codex 决定最后发什么内容”。

### 2. 独立项目路径

适用于你希望完全走 Python 项目，不依赖 Codex 运行时的场景。

流程如下：

1. `ai_daily_push/scripts/run_once.py`
2. 抓取候选内容
3. 去重与排序
4. 渲染日报
5. 发送到飞书

这条路径更像传统项目，更容易继续扩展成长期服务。

## 怎么使用这个 Skill

这个仓库现在已经包含了 skill 源码，位置在：

- `skills/ai-daily-feishu-briefing/`

但要让 Codex 真正使用它，你仍然需要把这份 skill 安装到本机的 Codex skills 目录里。当前调度器默认依赖下面这个本地 skill：

- `ai-daily-feishu-briefing`

也就是说：

- 仓库里保存的是 skill 源码、项目代码和调度脚本
- 本机的 Codex 会从本地 skills 目录加载 `ai-daily-feishu-briefing`

手动安装示例：

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

安装后，重新开一个新的 Codex 会话，然后可以这样触发：

```text
Use $ai-daily-feishu-briefing，抓取今天最值得看的 AI 论文和 AI 资讯，整理成中文日报，并发送到我的飞书私聊。
```

更详细的 skill 使用说明见：

- [skills/ai-daily-feishu-briefing/README.md](./skills/ai-daily-feishu-briefing/README.md)
- [skills/ai-daily-feishu-briefing/README.zh-CN.md](./skills/ai-daily-feishu-briefing/README.zh-CN.md)

这份 skill 说明里也已经补充了：如果以后想把它改造成商业、金融、政策等主题，应该优先改哪些文件、按什么方式改。

手动执行一次：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\run_codex_briefing.ps1
```

安装每天自动执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\install_codex_briefing_task.ps1 -Time "08:30"
```

停止自动任务：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex_scheduler\uninstall_codex_briefing_task.ps1
```

## 怎么使用这个项目

详细说明见：

- [ai_daily_push/README.md](./ai_daily_push/README.md)
- [ai_daily_push/README.zh-CN.md](./ai_daily_push/README.zh-CN.md)

快速示例：

```powershell
cd ai_daily_push
python scripts\init_db.py
python scripts\send_test_message.py --message "smoke test"
python scripts\run_once.py --ignore-history
```

## 适合公开上传到 GitHub 的范围

建议上传：

- `skills/ai-daily-feishu-briefing/`
- `ai_daily_push/`
- `codex_scheduler/`
- `README.md`
- `README.zh-CN.md`
- `GITHUB_PUBLISHING.md`
- `GITHUB_PUBLISHING.zh-CN.md`
- 如果你想保留原始设计稿，也可以上传 `项目.md`

不要上传：

- 任何真实 `.env`
- 任何真实飞书凭证或接收人 ID
- 生成出来的 `*.db`
- 生成出来的日报文本
- 调度日志
- IDE 目录和 Python 缓存文件

仓库里的 `.gitignore` 已经把这些本地运行产物排除了。

## 上传前检查

1. 确认 `.env` 没有被提交。
2. 确认文档和示例里没有真实 `open_id`、app secret 或 token。
3. 确认 `codex_scheduler/logs/` 已排除。
4. 确认 `briefing_feishu_today.txt` 这类生成文件已排除。
5. 如果你打算公开给别人看，建议把文档里的机器绝对路径再替换得更通用一些。
