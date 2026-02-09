#!/usr/bin/env node
// USER.md → Notion 同步脚本
// 用法: NOTION_API_KEY=xxx node sync-notion.js

const { Client } = require('@notionhq/client');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const NOTION_API_KEY = process.env.NOTION_API_KEY || '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';
const PAGE_ID = '3019de7521f88094bed7fe061773107d';

// 初始化Notion客户端
const notion = new Client({ auth: NOTION_API_KEY });

// 读取USER.md
const USER_MD_PATH = path.join(__dirname, 'USER.md');

function getCurrentTime() {
    return execSync('date "+%Y-%m-%d %H:%M:%S"').toString().trim();
}

async function syncToNotion() {
    try {
        console.log('🔄 开始同步到 Notion...');
        
        const now = getCurrentTime();
        const content = fs.readFileSync(USER_MD_PATH, 'utf-8');
        
        // 添加时间戳和内容
        const blocks = [
            {
                object: 'block',
                type: 'paragraph',
                paragraph: {
                    rich_text: [{
                        type: 'text',
                        text: { content: `\n📅 更新时间: ${now}\n` }
                    }]
                }
            }
        ];
        
        // 分割内容并创建blocks
        const lines = content.split('\n');
        for (const line of lines) {
            if (!line.trim()) continue;
            
            let block = {};
            
            if (line.startsWith('## ')) {
                block = {
                    object: 'block',
                    type: 'heading_2',
                    heading_2: {
                        rich_text: [{ type: 'text', text: { content: line.slice(3) } }]
                    }
                };
            } else if (line.startsWith('# ')) {
                block = {
                    object: 'block',
                    type: 'heading_1',
                    heading_1: {
                        rich_text: [{ type: 'text', text: { content: line.slice(2) } }]
                    }
                };
            } else if (line.startsWith('- ')) {
                block = {
                    object: 'block',
                    type: 'bulleted_list_item',
                    bulleted_list_item: {
                        rich_text: [{ type: 'text', text: { content: line.slice(2) } }]
                    }
                };
            } else {
                // 普通段落，确保rich_text不为空
                if (line.trim()) {
                    block = {
                        object: 'block',
                        type: 'paragraph',
                        paragraph: {
                            rich_text: [{ type: 'text', text: { content: line } }]
                        }
                    };
                } else {
                    continue; // 跳过空行
                }
            }
            
            blocks.push(block);
        }
        
        console.log(`📝 追加 ${blocks.length} 个blocks到页面...`);
        
        // 追加blocks
        await notion.blocks.children.append({
            block_id: PAGE_ID,
            children: blocks
        });
        
        console.log('✅ 同步完成！');
        
        // 发送Telegram通知
        const axios = require('axios');
        try {
            await axios.post(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN || '8218043380:AAFS9oAqkyFRcr25JSmLbunnOWobhjV6Hvo'}/sendMessage`, {
                chat_id: process.env.TELEGRAM_CHAT_ID || '6766025888',
                text: `✅ USER.md 已同步到 Notion\n时间: ${now}`,
                parse_mode: 'HTML'
            });
        } catch (e) {
            console.log('Telegram通知发送失败:', e.message);
        }
        
    } catch (error) {
        console.error('❌ 同步失败:', error.message);
        process.exit(1);
    }
}

syncToNotion();
