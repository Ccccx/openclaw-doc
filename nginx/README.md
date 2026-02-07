# OpenClaw Docker Compose Configuration

## 目录结构

```
openclaw-doc/
├── docker-compose.yml    # Docker Compose 配置
├── nginx/
│   └── nginx.conf       # Nginx 配置
├── README.md            # 本文档
```

## 快速开始

### 启动服务

```bash
# 后台启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f nginx
```

### 停止服务

```bash
# 停止（保留容器）
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除卷（数据会丢失）
docker-compose down -v
```

### 重启服务

```bash
docker-compose restart nginx

# 或重新加载配置
docker-compose exec nginx nginx -s reload
```

## 服务配置

### Nginx

- **镜像**: nginx:alpine
- **容器名**: openclaw-nginx
- **端口**: 80 → 80
- **健康检查**: http://localhost/health

### 功能

- ✅ 反向代理到 OpenClaw Gateway (端口 18789)
- ✅ WebSocket 支持
- ✅ Gzip 压缩
- ✅ 日志记录
- ✅ 健康检查端点

## 环境变量

当前配置使用固定 IP (172.19.42.102)，如需动态配置可在 docker-compose.yml 中添加环境变量。

## 维护命令

```bash
# 查看容器资源使用
docker stats openclaw-nginx

# 进入容器
docker exec -it openclaw-nginx sh

# 查看配置文件语法
docker-compose exec nginx nginx -t

# 重新加载配置（不停机）
docker-compose exec nginx nginx -s reload
```

## 故障排除

### 502 Bad Gateway
- 检查 OpenClaw Gateway 是否运行: `docker ps | grep openclaw`
- 检查端口 18789 是否监听: `ss -tlnp | grep 18789`

### 端口冲突
- 检查 80 端口占用: `ss -tlnp | grep :80`
- 修改 docker-compose.yml 中的端口映射

## 最佳实践

1. 定期查看日志: `docker-compose logs -f`
2. 监控健康检查: `curl http://localhost/health`
3. 配置 SSL/TLS（生产环境）
4. 设置日志轮转
