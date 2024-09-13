import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import dayjs from 'dayjs';

interface DailyNewsData {
  date: string;
  newscount: number;
}

interface MonthlyNewsData {
  month: string;
  count: number;
}

const NewsCountChart = () => {
  const [dailyData, setDailyData] = useState<DailyNewsData[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyNewsData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/news-count');
        const result = await response.json();

        const formattedDailyData = result.dailyData.map((item: DailyNewsData) => ({
          date: dayjs(item.date).format('YYYY-MM-DD'),
          newsCount: Number(item.newscount),
        }));

        const formattedMonthlyData = result.monthlyData.map((item: MonthlyNewsData) => ({
          month: item.month,
          newsCount: Number(item.count),
        }));

        setDailyData(formattedDailyData);
        setMonthlyData(formattedMonthlyData);
      } catch (error) {
        console.error('Error fetching news data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1 className='text-2xl font-bold mb-4 text-center'>新闻数量统计</h1>
      
      <h2>每日新闻数量</h2>
      <ResponsiveContainer width={800} height={400}>
        <LineChart
          data={dailyData}
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

     
    </div>
  );
};

export default NewsCountChart;