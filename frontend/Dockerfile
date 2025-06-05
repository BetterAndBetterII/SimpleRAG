FROM node:20-alpine AS base

# 安装pnpm
RUN npm install -g pnpm

# 设置工作目录
WORKDIR /app

# 复制package.json和pnpm-lock.yaml
COPY package.json pnpm-lock.yaml* ./

# 安装依赖
RUN pnpm install

# 复制所有文件
COPY . .

# 构建应用
RUN pnpm build

# 生产环境
FROM nginx:alpine AS production

# 复制构建文件到nginx目录
COPY --from=base /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]

