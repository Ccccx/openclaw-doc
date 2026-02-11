---
name: health-notion
description: 同步个人健康管理数据到Notion（血糖、饮食、体重、用药、病症档案），使用Notion API实现数据的增删改查。
metadata:
  clawdbot:
    emoji: 🏥
    requires:
      env:
        - NOTION_API_KEY
---

# Health Notion

个人健康管理Notion同步工具，支持：

## 功能模块

### 初始化档案
- 一键初始化完整健康档案到Notion
- 包含基础信息、健康状况、用药记录、血糖目标、饮食原则
- 同步后自动回显完整档案信息

### 血糖管理
- 记录每日血糖数据（空腹、餐后、睡前）
- 查询血糖历史记录
- 分析血糖趋势

### 饮食日志
- 记录每餐饮食
- 追踪营养摄入
- 饮食质量评估

### 体重追踪
- 每日体重记录
- BMI计算
- 体重趋势分析

### 用药记录
- 药物清单管理
- 用药时间记录
- 服药提醒

### 病症档案
- 病史记录
- 诊断信息
- 过敏史

## 使用方法

### 环境配置

首先创建Notion Integration：
1. 访问 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 填写名称（如 "Health Manager"）
4. 复制 "Internal Integration Token"

然后分享页面给Integration：
1. 在Notion中打开目标页面
2. 点击右上角 "..." → "Connect to" → 选择你的Integration

设置环境变量：
```bash
export NOTION_API_KEY=secret_your_notion_integration_token
export NOTION_HEALTH_PAGE_ID=3039de7521f8809894b4cdee8b678021

# 可选：各功能数据库ID
export NOTION_GLUCOSE_DB_ID=your_glucose_db_id
export NOTION_MEAL_DB_ID=your_meal_db_id
export NOTION_WEIGHT_DB_ID=your_weight_db_id
export NOTION_MEDICATION_DB_ID=your_medication_db_id
```

### 同步命令

**初始化健康档案（推荐首次使用）：**
```bash
health-notion init
```
> 清空页面并重新初始化完整档案，同步后自动回显档案内容

**同步USER.md到Notion：**
```bash
health-notion sync user
```
> 将USER.md内容追加到Notion页面，同步后自动回显完整档案

**添加血糖记录：**
```bash
health-notion add glucose 5.6 "空腹"
```

**查询血糖记录：**
```bash
health-notion get glucose --days 7
```

**添加饮食记录：**
```bash
health-notion add meal "早餐" "燕麦+鸡蛋"
```

**记录体重：**
```bash
health-notion add weight 72.5
```

**添加用药记录：**
```bash
health-notion add medication "胰岛素" "10U"
```

**查询完整档案：**
```bash
health-notion get profile
```

**获取健康报告：**
```bash
health-notion report
```

## 数据库结构

- **血糖记录数据库**: 记录血糖值、时间点、备注
- **饮食日志数据库**: 记录餐饮类型、食物、热量
- **体重追踪数据库**: 记录体重、BMI、日期
- **用药记录数据库**: 记录药物、剂量、时间
- **病症档案数据库**: 记录病史、诊断、过敏史

## 数据流向
- `health-notion init` → 初始化完整档案到Notion病症档案
- `health-notion sync user` → 同步USER.md到Notion
- 血糖/饮食/体重/用药 → 记录到Notion各数据库
- 查询命令 → 从Notion读取历史数据

## 注意事项
- 首次使用建议运行 `health-notion init` 初始化完整档案
- 同步/初始化后会自动回显最新档案内容
- 建议设置定时任务每日同步USER.md
