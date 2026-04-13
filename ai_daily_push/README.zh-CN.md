[English](./README.md) | 中文

# ai_daily_push

这是一个独立的 Python 项目，用来：

- 抓取 AI 论文和 AI 资讯候选内容
- 去重与排序
- 渲染中文日报
- 把最终结果发送到飞书私聊

## 项目结构

- `app/sources/`
  数据源适配器，目前包括 arXiv 和官方博客源
- `app/pipeline/`
  标准化、打分、去重、筛选、摘要
- `app/push/`
  日报渲染和飞书发送器
- `app/storage/`
  SQLite 存储和推送历史
- `scripts/`
  入口脚本和 Windows 任务辅助脚本
- `tests/`
  基础回归测试

## 快速开始

1. 把 `.env.example` 复制为 `.env`
2. 至少填这两个配置：
   - `FEISHU_SEND_MODE=cli`
   - `FEISHU_RECEIVER_OPEN_ID=your_open_id`
3. 初始化本地数据库：

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

6. 如果你在手工验收时想忽略推送历史过滤：

```powershell
python scripts\run_once.py --ignore-history
```

## 常用辅助脚本

- `scripts/export_candidates.py`
  把抓取并标准化后的候选内容导出成 JSON Lines，便于人工检查
- `scripts/send_test_message.py --file <path>`
  直接把 UTF-8 文本文件通过当前配置的飞书发送器发出去

## Windows 定时任务

这个子项目也保留了一套纯项目驱动的定时方案：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_task.ps1 -Time "09:00"
```

以后如果不要了：

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
- 生成的日报、数据库和日志都不应该提交到 Git 仓库。
