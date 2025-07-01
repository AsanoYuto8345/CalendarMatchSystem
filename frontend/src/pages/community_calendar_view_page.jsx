// M11 カレンダー画面 担当者: (TBD)
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import CalendarView from '../components/CalendarView'; // 相対パスは適宜変更
import dayjs from 'dayjs';

/**
 * カレンダー画面ページ
 * - Cookie からユーザIDを取得し、関連予定を取得して CalendarView に表示
 * - 月の切り替えに対応
 * 
 * 作成者: (TBD)
 */
const CommunityCalendarViewPage = () => {
  const navigate = useNavigate();
  const userId = Cookies.get('userId');
  const [events, setEvents] = useState([]);
  const [year, setYear] = useState(dayjs().year());
  const [month, setMonth] = useState(dayjs().month() + 1); // dayjs は 0-indexed

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  // 日付クリック時の処理
  const handleDateClick = (day) => {
    alert(`${year}/${month}/${day} がクリックされました`);
    // 予定詳細画面などに遷移する場合はここで navigate を使う
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
    // if (!userId) {
    //   setError('ユーザIDが不正です (E1)');
    //   setLoading(false);
    //   return;
    // }

    setLoading(true);
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/calendar/${userId}?year=${year}&month=${month}`)
      .then((res) => {
        if (!res.data || !Array.isArray(res.data)) {
          throw new Error('予定データが取得できませんでした');
        }
        setEvents(res.data);
      })
      .catch((err) => {
        console.error(err);
        setError('予定データが取得できません (E2)');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [userId, year, month]);

  // if (loading) return <div className="p-4">読み込み中...</div>;
  // if (error) return <div className="p-4 text-red-500">{error}</div>;

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
