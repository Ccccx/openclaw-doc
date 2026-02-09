# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Notion

- **API Key**: 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
- **Page ID**: 3019de7521f88094bed7fe061773107d (个人健康管理)
- **同步脚本**: /home/admin/.openclaw/workspace/health-notion.js
- **定时任务**: 每天 08:00 自动同步
- **配置方式**: 环境变量 NOTION_API_KEY

### 使用说明

```bash
# 添加血糖记录
NOTION_API_KEY=xxx node health-notion.js add-blood 4.8 "本次测量"

# 查询血糖记录
NOTION_API_KEY=xxx node health-notion.js get-blood

# 同步USER.md到Notion
NOTION_API_KEY=xxx node health-notion.js sync
```

**Notion页面结构**:
- 📊 血糖记录 - 追踪每日血糖变化
- 🍽️ 饮食日志 - 记录每餐饮食
- 🏃 运动记录 - 追踪运动情况
- ⚖️ 体重追踪 - 监控体重变化
- 💊 用药记录 - 记录用药情况
- 🏥 病症档案 - 健康档案（同步自USER.md）

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
