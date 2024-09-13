// pages/api/data/route.ts
import { NextResponse } from 'next/server';
import pool from '../../lib/db';

// GET 方法，获取数据库中的数据
export async function GET() {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM schemaAUTOinfo.information');
    client.release(); // 释放连接
    return NextResponse.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}