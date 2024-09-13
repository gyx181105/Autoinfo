import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface MonthlyNewsData {
  month: string;
  count: number;
}

const MonthCountChart = () => {
  const [data, setData] = useState<MonthlyNewsData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/news-count');
        const result = await response.json();

        const formattedData = result.monthlyData.map((item: MonthlyNewsData) => ({
          month: item.month,
          count: Number(item.count),
        }));

        setData(formattedData);
      } catch (error) {
        console.error('Error fetching news data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="w-full h-[400px] md:h-[500px] lg:h-[600px]">
      <h1 className="text-2xl font-bold mb-4 text-center">每月新111闻数量统计</h1>
      <div className="w-full h-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MonthCountChart;