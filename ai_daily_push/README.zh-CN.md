[English](./README.md) | 中文

# ai_daily_push

`ai_daily_push` 是这套日报流程的独立 Python 实现。

它负责：

- 抓取 AI 论文和 AI 资讯候选内容
- 去重和排序
- 渲染中文日报
- 把结果发送到飞书私聊

## 目录结构

- `app/sources/`
  数据源适配器，比如 arXiv 和官方博客源
- `app/pipeline/`
  标准化、去重、打分、筛选、摘要
- `app/push/`
  日报渲染和飞书发送
- `app/storage/`
  SQLite 缓存和推送历史
- `scripts/`
  运行脚本和 Windows 定时任务辅助脚本
- `tests/`
  基础回归测试

## 快速开始

1. 把 `.env.example` 复制为 `.env`
2. 至少设置：
   - `FEISHU_SEND_MODE=cli`
   - `FEISHU_RECEIVER_OPEN_ID=your_open_id`
3. 初始化数据库：

```powershell
python scripts\init_db.py
```

4. 发送一条测试消息：

```powershell
python scripts\send_test_message.py --message "smoke test"
```

5. 执行一次日报：

```powershell
python scripts\run_once.py
```

6. 如果你在手工验收时想忽略历史推送过滤：

```powershell
python scripts\run_once.py --ignore-history
```

## 常用脚本

- `scripts/export_candidates.py`
  把标准化后的候选内容导出成 JSON Lines，方便人工检查
- `scripts/send_test_message.py --file <path>`
  直接把 UTF-8 文本文件通过当前飞书发送器发出去

## 定时任务

这个项目本身也带了一套纯 Python 的 Windows 定时任务方案：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_task.ps1 -Time "09:00"
```

如果以后不用了：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_windows_task.ps1
```

## 发送模式

- `FEISHU_SEND_MODE=cli`
  使用本地 `lark-cli`
- `FEISHU_SEND_MODE=api`
  使用飞书开放平台应用凭证

## 说明

- 如果 `OPENAI_API_KEY` 为空，摘要会退化为本地启发式摘要。
- 生成的日报、数据库和运行日志不应该提交到 Git 仓库。
