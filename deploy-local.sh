#!/bin/bash

# 设置环境变量
export POSTGRES_PASSWORD=postgres
export DOMAIN=localhost

# 停止并删除旧容器
echo "Stopping and removing old containers..."
docker-compose down

# 构建新镜像
echo "Building new images..."
docker-compose build

# 启动容器
echo "Starting containers..."
docker-compose up -d

# 等待服务启动
echo "Waiting for services to start..."
sleep 10

# 检查服务状态
echo "Checking service status..."
docker-compose ps

echo "Deployment completed!"

