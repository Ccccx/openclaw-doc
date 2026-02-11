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
### Health Notion

- **Page ID**: 3039de7521f8809894b4cdee8b678021 (个人健康管理主页)
- **API Key**: `ntn_xxx` (需要替换为你的Notion Integration Token)
- **Skill路径**: `/home/admin/.openclaw/workspace/skills/health-notion`
- **主脚本**: `health-notion.py`

#### 环境变量配置

```bash
# 必需
export NOTION_API_KEY=secret_your_integration_token

# 必需 - 主页ID
export NOTION_HEALTH_PAGE_ID=3039de7521f8809894b4cdee8b678021

# 可选 - 功能数据库ID（需在Notion中创建）
export NOTION_GLUCOSE_DB_ID=xxx
export NOTION_MEAL_DB_ID=xxx
export NOTION_WEIGHT_DB_ID=3039de7521f881daa2d1fe674f1dbc12
export NOTION_MEDICATION_DB_ID=xxx
```

#### 使用方法

```bash
cd /home/admin/.openclaw/workspace/skills/health-notion

# 同步USER.md到病症档案
python health-notion.py sync user

# 添加血糖记录
python health-notion.py add glucose 5.6 "空腹"

# 查询血糖记录（最近7天）
python health-notion.py get glucose --days 7

# 添加饮食记录
python health-notion.py add meal "早餐" "燕麦+鸡蛋"

# 记录体重
python health-notion.py add weight 72.5

# 添加用药记录
python health-notion.py add medication "胰岛素" "10U"

# 生成健康报告
python health-notion.py report
```

#### Notion页面结构

1. **🏥 病症档案** (主页 ID: `3039de7521f8809894b4cdee8b678021`)
   - 同步USER.md的综合健康信息

2. **📊 血糖记录数据库** (需要创建，配置到 `NOTION_GLUCOSE_DB_ID`)
   - 字段: 名称、血糖值、时间、备注

3. **🍽️ 饮食日志数据库** (需要创建，配置到 `NOTION_MEAL_DB_ID`)
   - 字段: 名称、餐饮类型、食物、时间

4. **⚖️ 体重追踪数据库** (需要创建，配置到 `NOTION_WEIGHT_DB_ID`)
   - 字段: 名称、体重、BMI、日期

5. **💊 用药记录数据库** (需要创建，配置到 `NOTION_MEDICATION_DB_ID`)
   - 字段: 名称、药物、剂量、时间

#### 定时同步任务

建议设置cron任务每天自动同步：
```bash
# 每天早上8点同步USER.md到Notion
0 8 * * * cd /home/admin/.openclaw/workspace/skills/health-notion && python health-notion.py sync user
```

#### 设置步骤

1. ✅ 创建Notion Integration，获取API Key
2. ✅ 在Notion中创建各数据库（血糖、饮食、体重、用药）
3. ✅ 分享数据库给Integration
4. ✅ 设置环境变量（API Key和各数据库ID）
5. ✅ 测试同步命令

---

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
