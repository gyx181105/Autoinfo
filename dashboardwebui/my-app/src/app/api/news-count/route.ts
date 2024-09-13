import { NextResponse } from 'next/server';
import pool from '../../lib/db';

export async function GET() {
  try {
    // 查询数据库，获取新闻数量按日期分组
    const client = await pool.connect();
    const result = await client.query(`
      SELECT
        date::DATE as date,
        COUNT(*) as newsCount
      FROM schemaAUTOinfo.information
      GROUP BY date
      ORDER BY date;
    `);
    client.release();
    
    // 返回结果作为JSON
    return NextResponse.json(result.rows);
  } catch (err) {
    console.error('Error fetching news count data:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}