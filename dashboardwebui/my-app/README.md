This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

# 表结构

## 用户表

## 采集文章表
```bash
CREATE TABLE schemaAUTOinfo.information (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    title VARCHAR(255) NOT NULL,
    link TEXT NOT NULL,
    published_date DATE NOT NULL,
    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 评论表

## 点赞表
