// M11 カレンダー画面 担当者: 角田一颯

import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import CalendarView from '../components/CalendarView';
import dayjs from 'dayjs';

const CommunityCalendarViewPage = () => {
  const navigate = useNavigate();
  const { communityId } = useParams();
  const [events, setEvents] = useState([]);
  const [year, setYear] = useState(dayjs().year());
  const [month, setMonth] = useState(dayjs().month() + 1);

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  // 日付クリック時の処理
  const handleDateClick = (day) => {
    const formattedMonth = String(month).padStart(2, '0');
    const formattedDay = String(day).padStart(2, '0');
    const formattedDate = `${year}-${formattedMonth}-${formattedDay}`;

    if (communityId) {
      navigate(`/community/${communityId}/calendar/tags/${formattedDate}`);
    } else {
      console.error("Community ID is not available for navigation.");
      setError("コミュニティIDがURLから取得できませんでした。");
    }
  };

  const handlePrevMonth = () => {
    const newDate = dayjs(`${year}-${month}-01`).subtract(1, 'month');
    setYear(newDate.year());
    setMonth(newDate.month() + 1);
  };

  const handleNextMonth = () => {
    const newDate = dayjs(`${year}-${month}-01`).add(1, 'month');
    setYear(newDate.year());
    setMonth(newDate.month() + 1);
  };

  useEffect(() => {
    if (!communityId) {
      setError('コミュニティIDがURLから取得できませんでした。');
      setLoading(false);
      return;
    }

    const fetchTagsForMonth = async () => {
      setLoading(true);
      const daysInMonth = dayjs(`${year}-${month}-01`).daysInMonth();

      try {
        const promises = [];
        for (let day = 1; day <= daysInMonth; day++) {
          const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
          promises.push(
            axios.get(`http://localhost:5001/api/${communityId}/calendar/tag/get`, { params: { date: dateStr } })
              .then(res => res.data.data || [])
              .catch(err => {
                // 404は無視、その他はログ
                if (err.response?.status !== 404) {
                  console.error(`APIエラー: ${dateStr}`, err);
                }
                return [];
              })
          );
        }

        // 全てのリクエストが完了するまで待つ
        const results = await Promise.all(promises);

        const tagData = results.flat().map(tag => {
          const tagDate = new Date(tag.date);
          return {
            id: tag.id,
            tag: tag.name,
            day: tagDate.getDate(),
            color: tag.color.startsWith('#') ? tag.color : `#${tag.color}`,
          };
        });

        setEvents(tagData);
      } catch (err) {
        console.error('タグ取得中にエラーが発生しました', err);
        setError('タグの取得に失敗しました。');
      } finally {
        setLoading(false);
      }
    };

    fetchTagsForMonth();
  }, [year, month, communityId]);

  if (loading) return <div className="p-4">読み込み中...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="p-4">
      <CalendarView
        events={events}
        onDateClick={handleDateClick}
        year={year}
        month={month}
        onPrevMonth={handlePrevMonth}
        onNextMonth={handleNextMonth}
      />
    </div>
  );
};

export default CommunityCalendarViewPage;
