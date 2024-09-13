import { NextResponse } from 'next/server';
import pool from '../../lib/db';

export async function GET() {
  try {
    const client = await pool.connect();

    // 按日期分组的查询
    const dayResult = await client.query(`
      SELECT
        date::DATE as date,
        COUNT(*) as newsCount
      FROM schemaAUTOinfo.information
      GROUP BY date
      ORDER BY date;
    `);

    // 按月份分组的查询
    const monthResult = await client.query(`
      SELECT TO_CHAR(date, 'YYYY-MM') AS month, COUNT(*) AS count
      FROM schemaAUTOinfo.information
      GROUP BY TO_CHAR(date, 'YYYY-MM')
      ORDER BY month
    `);
    
    client.release();
    
    // 返回包含两个查询结果的对象
    return NextResponse.json({
      dailyData: dayResult.rows,
      monthlyData: monthResult.rows
    });
  } catch (err) {
    console.error('Error fetching news count data:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}