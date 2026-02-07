
---
name: health-manager
description: 这是一个私人医生级别的健康管理管家，能够帮助用户管理健康档案、提供个性化健康建议、跟踪健康指标，并在必要时提醒用户就医。
---


# 健康管理管家 (Health Manager)

## 概述
这是一个私人医生级别的健康管理管家，能够帮助用户管理健康档案、提供个性化健康建议、跟踪健康指标，并在必要时提醒用户就医。

## 功能特性

### 1. 健康档案管理
- 创建和维护个人健康档案
- 存储基本信息（年龄、性别、身高、体重、血型等）
- 记录病史、过敏史、家族病史
- 管理用药记录和疫苗接种记录

### 2. 健康数据跟踪
- 记录和分析日常健康指标（血压、血糖、心率、睡眠等）
- 跟踪饮食和运动习惯
- 监测体重变化趋势
- 提供可视化健康数据图表

### 3. 个性化健康建议
- 基于用户健康档案提供定制化建议
- 饮食营养指导
- 运动计划推荐
- 睡眠质量改善建议
- 压力管理和心理健康支持

### 4. 健康提醒与预警
- 用药提醒
- 定期体检提醒
- 异常指标预警
- 季节性疾病预防提醒

### 5. 就医辅助
- 症状初步评估
- 就医科室建议
- 急诊情况识别
- 就医准备清单

## 使用方法

### 初始化健康档案
```bash
# 创建新的健康档案
health-manager init --name "张三" --age 30 --gender "男" --height 175 --weight 70
```

### 记录健康数据
```bash
# 记录血压
health-manager record bp --systolic 120 --diastolic 80

# 记录血糖
health-manager record glucose --value 5.6

# 记录体重
health-manager record weight --value 70.5
```

### 获取健康建议
```bash
# 获取综合健康报告
health-manager report

# 获取特定建议
health-manager suggest diet
health-manager suggest exercise
```

### 设置提醒
```bash
# 设置用药提醒
health-manager remind medication --time "08:00,20:00" --drug "维生素C"

# 设置体检提醒
health-manager remind checkup --interval "6m" --next "2024-12-01"
```

## 数据安全
- 所有健康数据本地存储，不会上传到云端
- 支持数据加密（可选）
- 用户完全控制数据访问权限

## 依赖项
- Python 3.8+
- SQLite3（用于本地数据存储）
- matplotlib（用于数据可视化，可选）

## 配置文件
配置文件位于 `~/.config/health-manager/config.json`，包含：
- 用户基本信息
- 提醒设置
- 数据存储路径
- 隐私设置

## 注意事项
- 本工具提供的建议仅供参考，不能替代专业医疗诊断
- 如遇紧急医疗情况，请立即联系急救服务
- 定期更新健康档案以确保建议的准确性
