[English](./README.md) | 中文

# ai-daily-feishu-briefing Skill

这个目录保存的是该 skill 的仓库源码副本。

## 这个 Skill 是干什么的

当你希望 Codex 来完成下面这些事情时，就用这个 skill：

- 抓取今天的 AI 论文和 AI 资讯
- 选出最值得看的内容
- 写成简洁的中文日报
- 发送到飞书私聊

它也可以辅助你搭建或修改底层 Python 项目和调度脚本，但它的主模式仍然是“直接产出并发送日报”。

## 仓库源码和已安装 Skill 的区别

这个目录只是保存在 Git 仓库里的源码副本。

Codex 默认不会直接从这个仓库目录加载 skill。要让 Codex 真正使用它，你需要把这个目录安装或复制到本机的 Codex skills 目录。

常见本地安装路径：

```text
C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

## 如何安装

在仓库根目录执行：

```powershell
Copy-Item -Recurse -Force .\skills\ai-daily-feishu-briefing C:\Users\<你的用户名>\.codex\skills\ai-daily-feishu-briefing
```

然后重新打开一个新的 Codex 会话，让它重新扫描 skills。

## 如何在 Codex 里触发

示例提示词：

```text
Use $ai-daily-feishu-briefing，抓取今天最重要的 AI 论文和 AI 资讯，整理成中文日报，并发送到我的飞书私聊。
```

更聚焦的示例：

```text
Use $ai-daily-feishu-briefing，筛选今天最值得关注的 3 篇 AI 论文和 3 条 AI 资讯，摘要写得简洁一点，然后发到飞书。
```

## 它和当前仓库的关系

- `skills/ai-daily-feishu-briefing/`
  skill 源码和文档
- `ai_daily_push/`
  独立 Python 工作流和稳定的飞书发送器
- `codex_scheduler/`
  Codex 包装脚本和 Windows 定时任务集成

当前仓库里更稳的使用路径是：

1. Codex 使用这个 skill 选题并写日报
2. 外层脚本把结果写入 `ai_daily_push/briefing_feishu_today.txt`
3. 项目发送器再把这个 UTF-8 文件发到飞书

## 如果以后想改成别的主题，应该怎么改

如果你后面想把这套 skill 复用到别的主题，比如：

- 商业
- 金融
- 政策 / 政治
- 科技产业

通常不需要改底层运行架构。最稳的做法是复制一份新的 skill，再改“主题相关”的说明文件。

推荐做法：

1. 复制 `skills/ai-daily-feishu-briefing/` 到新的 skill 目录，比如：
   - `skills/business-daily-feishu-briefing/`
   - `skills/finance-daily-feishu-briefing/`
2. 在 `SKILL.md` 里改 skill 名称和目标
3. 在 `agents/openai.yaml` 里改显示名称和默认 prompt
4. 在参考文档里改默认信息源、筛选规则和摘要角度

最优先要改的文件：

- `SKILL.md`
  改 skill 名称、使用范围、默认数据源、日报目标
- `references/codex-workflow.md`
  改选题逻辑，以及这个领域里什么算“高信号内容”
- `references/prompting.md`
  改摘要风格，尤其是“为什么值得关注”的判断方式
- `agents/openai.yaml`
  改展示名称和默认触发提示词

可以这样理解不同主题的变化方向：

- 商业简报：
  更关注公司战略、产品发布、合作、定价、招聘、市场动作
- 金融简报：
  更关注财报、资本市场、监管、流动性、估值影响、投资相关性
- 政策简报：
  更关注监管机构、政府公告、执法、合规要求和对企业的后续影响

通常不需要优先改的部分：

- `scripts/doctor.py`
- `scripts/send_test_message.py`
- 飞书发送链路
- `codex_scheduler/` 里的定时调度模式

也就是说，大多数“换主题”的工作，本质上发生在 skill 的说明、信息源和摘要规则上，而不是发送基础设施上。

## 目录内容

- `SKILL.md`
  真正给 Codex 读取的 skill 主文件
- `agents/openai.yaml`
  本地 skill 的显示元数据
- `references/`
  架构、工作流、飞书、提示词等参考文档
- `scripts/doctor.py`
  检查本地依赖和配置
- `scripts/send_test_message.py`
  发送飞书测试消息

## 推荐验证方式

```powershell
python .\skills\ai-daily-feishu-briefing\scripts\doctor.py --env-file .\ai_daily_push\.env
python .\skills\ai-daily-feishu-briefing\scripts\send_test_message.py --env-file .\ai_daily_push\.env --mode cli --message "skill smoke test"
```
