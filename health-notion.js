#!/usr/bin/env node
// Notion健康数据管理脚本
// 功能：读取、更新血糖等健康数据到Notion

const { Client } = require('@notionhq/client');
const readline = require('readline');

// 配置
const NOTION_API_KEY = process.env.NOTION_API_KEY || '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';
const PAGE_ID = '3019de7521f88094bed7fe061773107d';

// 子页面ID
const PAGES = {
  bloodSugar: '3019de7521f88094bed7fe061773107d', // 血糖记录
  diet: '3019de7521f88094bed7fe061773107d',       // 饮食日志
  exercise: '3019de7521f88094bed7fe061773107d',   // 运动记录
  weight: '3019de7521f88094bed7fe061773107d',     // 体重追踪
  medication: '3019de7521f88094bed7fe061773107d', // 用药记录
  medical: '3019de7521f88094bed7fe061773107d'     // 病症档案
};

// 初始化Notion客户端
const notion = new Client({ auth: NOTION_API_KEY });

// 格式化日期
function formatDate(date = new Date()) {
  return date.toISOString().split('T')[0];
}

// 添加血糖记录
async function addBloodSugar(fasting, postMeal = null, notes = '') {
  const isNormal = fasting >= 4.4 && fasting <= 7.0;
  const status = isNormal ? '✅' : '❌';
  const date = formatDate();
  
  const content = `| ${date} | ${fasting} | ${postMeal || '-'} | ${status} | ${notes} |`;
  
  // 查找血糖记录页面的ID
  const bloodSugarPageId = await findPageId('📊 血糖记录');
  if (!bloodSugarPageId) throw new Error('未找到血糖记录页面');
  
  // 追加表格行
  await notion.blocks.children.append({
    block_id: bloodSugarPageId,
    children: [{
      object: 'block',
      type: 'paragraph',
      paragraph: {
        rich_text: [{ type: 'text', text: { content } }]
      }
    }]
  });
  
  console.log(`✅ 已添加血糖记录: ${content}`);
  return content;
}

// 查询血糖记录
async function getBloodSugarRecords(limit = 10) {
  const bloodSugarPageId = await findPageId('📊 血糖记录');
  if (!bloodSugarPageId) throw new Error('未找到血糖记录页面');
  
  const response = await notion.blocks.children.list({
    block_id: bloodSugarPageId,
    page_size: 50
  });
  
  const records = [];
  for (const block of response.results) {
    if (block.type === 'paragraph') {
      const text = block.paragraph.rich_text[0]?.text?.content || '';
      if (text.startsWith('|') && text.includes('2026')) {
        records.push(text);
      }
    }
  }
  
  return records.slice(-limit);
}

// 查找子页面ID
async function findPageId(title) {
  const response = await notion.blocks.children.list({
    block_id: PAGE_ID,
    page_size: 100
  });
  
  for (const block of response.results) {
    if (block.type === 'child_page' && block.child_page.title === title) {
      return block.id;
    }
  }
  return null;
}

// 同步USER.md到Notion（按固定格式）
async function syncUserMdToNotion() {
  const fs = require('fs');
  const path = require('path');
  
  const USER_MD_PATH = path.join(__dirname, 'USER.md');
  const content = fs.readFileSync(USER_MD_PATH, 'utf-8');
  
  // 查找病症档案页面
  const medicalPageId = await findPageId('🏥 病症档案');
  if (!medicalPageId) throw new Error('未找到病症档案页面');
  
  // 解析USER.md内容
  const sections = {};
  let currentSection = '';
  
  content.split('\n').forEach(line => {
    if (line.startsWith('## ')) {
      currentSection = line.slice(3).trim();
      sections[currentSection] = [];
    } else if (line.trim() && currentSection) {
      sections[currentSection].push(line);
    }
  });
  
  // 更新病症档案
  const medicalContent = [];
  
  if (sections['基础信息']) {
    medicalContent.push('## 基础信息');
    medicalContent.push(...sections['基础信息']);
  }
  
  if (sections['健康状况']) {
    medicalContent.push('\n## 健康状况');
    medicalContent.push(...sections['健康状况']);
  }
  
  if (sections['当前用药']) {
    medicalContent.push('\n## 当前用药');
    medicalContent.push(...sections['当前用药']);
  }
  
  if (sections['血糖控制目标']) {
    medicalContent.push('\n## 血糖控制目标');
    medicalContent.push(...sections['血糖控制目标']);
  }
  
  // 追加到病症档案
  await notion.blocks.children.append({
    block_id: medicalPageId,
    children: [{
      object: 'block',
      type: 'paragraph',
      paragraph: {
        rich_text: [{
          type: 'text',
          text: { content: `\n📅 更新时间: ${formatDate()}\n` }
        }]
      }
    }, ...medicalContent.map(text => ({
      object: 'block',
      type: text.startsWith('## ') ? 'heading_2' : 'paragraph',
      [text.startsWith('## ') ? 'heading_2' : 'paragraph']: {
        rich_text: [{ type: 'text', text: { content: text } }]
      }
    }))]
  });
  
  console.log('✅ 已同步USER.md到病症档案');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  try {
    switch (command) {
      case 'add-blood':
        const fasting = parseFloat(args[1]);
        const postMeal = args[2] ? parseFloat(args[2]) : null;
        const notes = args[3] || '';
        await addBloodSugar(fasting, postMeal, notes);
        break;
        
      case 'get-blood':
        const records = await getBloodSugarRecords(parseInt(args[1]) || 10);
        console.log('\n📊 血糖记录:');
        records.forEach(r => console.log(r));
        break;
        
      case 'sync':
        await syncUserMdToNotion();
        break;
        
      default:
        console.log(`
健康管理脚本用法:
  node health-notion.js add-blood <空腹血糖> [餐后血糖] [备注]  - 添加血糖记录
  node health-notion.js get-blood [条数]                          - 查询血糖记录
  node health-notion.js sync                                       - 同步USER.md到Notion
        `);
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

module.exports = { addBloodSugar, getBloodSugarRecords, syncUserMdToNotion };
main();
