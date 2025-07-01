// M11 カレンダー画面 担当者: 角田一颯
import { useEffect, useState } from 'react';
// useParams を react-router-dom からインポートに追加
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import CalendarView from '../components/CalendarView'; // 相対パスは適宜変更
import dayjs from 'dayjs';

/**
 * カレンダー画面ページ
 * - Cookie からユーザIDを取得し、関連予定を取得して CalendarView に表示
 * - 月の切り替えに対応
 * * 作成者: 角田一颯
 */
const CommunityCalendarViewPage = () => {
  const navigate = useNavigate();
  // URLからcommunityIdを取得する
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
      // communityId が取得できない場合のユーザーへのフィードバック
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
    setLoading(true);
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/communities/${communityId}/calendar?year=${year}&month=${month}`)
      .then((res) => {
        if (!res.data || !Array.isArray(res.data)) {
          // throw new Error('予定データが取得できませんでした');
        }
        setEvents(res.data);
      })
      .catch((err) => {
        console.error(err);
        // setError('予定データが取得できません (E2)');
      })
      .finally(() => {
        setLoading(false);
      });
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