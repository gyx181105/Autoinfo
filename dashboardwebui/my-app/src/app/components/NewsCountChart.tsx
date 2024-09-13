import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import dayjs from 'dayjs';

interface NewsData {
  date: string;
  newsCount: number;
}

const NewsCountChart = () => {
  const [data, setData] = useState<NewsData[]>([]);

  useEffect(() => {
    // 获取新闻数量数据
    const fetchData = async () => {
      try {
        const response = await fetch('/api/news-count');
        const result = await response.json();

        // 处理数据，将日期格式化，确保newsCount字段名称统一
        const formattedData = result.map((item: any) => ({
          date: dayjs(item.date).format('YYYY-MM-DD'),  // 格式化日期为 'YYYY-MM-DD'
          newsCount: Number(item.newscount),  // 确保使用newsCount作为字段
        }));

        setData(formattedData);
      } catch (error) {
        console.error('Error fetching news data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <ResponsiveContainer width={960} height={400}>
      <LineChart
        data={data}
        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="newsCount" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default NewsCountChart;