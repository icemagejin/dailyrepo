# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## 定期检查任务（每次 heartbeat 执行）

### 1. 检查 inbox 目录
- 路径：`/workspace/projects/workspace-pm/inbox/`
- 目的：检查 Social Media Agent 是否有新通知
- 频率：每次 heartbeat

### 2. 检查 workspace-collab 通知
- 路径：`/workspace/projects/workspace-collab/notifications/`
- 目的：检查其他 Agent 的通知
- 频率：每次 heartbeat

### 3. 检查日报状态
- 路径：`/workspace/projects/workspace-collab/state/state-YYYY-MM-DD.json`
- 目的：确认日报是否需要整合
- 频率：早上 09:00-10:00

### 4. 定期备份 memory 和工作流到 dailyrepo（新增）
- 源路径：`/workspace/projects/workspace-pm/MEMORY.md`、`/workspace/projects/workspace-pm/HEARTBEAT.md`、`/workspace/projects/workspace-pm/memory/*.md`
- 目标路径：`/workspace/projects/workspace-aesthetic/dailyrepo/pm-agent/`
- 目的：防止健忘，备份长期记忆和工作流
- 频率：每天至少 1 次（建议晚上 22:00）
