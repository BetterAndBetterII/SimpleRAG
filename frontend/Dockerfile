FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json vite.config.mjs tailwind.config.js postcss.config.js index.html ./
COPY src ./src
RUN corepack enable && pnpm install --frozen-lockfile
RUN pnpm run build
CMD ["pnpm", "run", "dev", "--host"]
