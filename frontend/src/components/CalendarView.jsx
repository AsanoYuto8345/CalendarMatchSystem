// M11 カレンダー画面コンポーネント 担当: 角田一颯

import React from 'react';

const CalendarView = ({
  events = [],
  onDateClick,
  year,
  month,
  onPrevMonth,
  onNextMonth,
}) => {
  const firstDay = new Date(year, month - 1, 1);
  const startDay = firstDay.getDay();
  const lastDay = new Date(year, month, 0).getDate();
  const totalCells = Math.ceil((startDay + lastDay) / 7) * 7;

  const today = new Date();
  const isTodayCurrentMonth = today.getFullYear() === year && today.getMonth() + 1 === month;
  const todayDate = isTodayCurrentMonth ? today.getDate() : null;

  const cells = [];

  for (let i = 0; i < totalCells; i++) {
    const day = i - startDay + 1;
    const isSunday = i % 7 === 0;
    const isSaturday = i % 7 === 6;
    const inCurrentMonth = day > 0 && day <= lastDay;
    const isToday = inCurrentMonth && day === todayDate;

    cells.push(
      <div
        key={i}
        className={`h-24 p-1 relative text-sm font-medium
          ${isSunday || isSaturday ? 'bg-blue-50' : 'bg-white'}
          ${inCurrentMonth ? 'text-gray-800' : 'text-gray-400'}
          ${isToday ? 'bg-yellow-100' : ''}
          hover:bg-blue-50 cursor-pointer rounded`}
        onClick={() => inCurrentMonth && onDateClick(day)}
      >
        <div className={isSunday ? 'text-red-500' : ''}>
          {inCurrentMonth ? day : ''}
        </div>

        {inCurrentMonth &&
          events
            .filter((e) => e.day === day)
            .map((e) => (
              <div
                key={e.id}
                className="absolute left-1 top-6 bg-blue-200 text-blue-800 text-xs rounded-full px-3 py-0.5 shadow-md text-center truncate"
              >
                {e.tag}
              </div>
            ))}
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-0 font-sans shadow-md rounded-xl bg-white overflow-hidden">
      {/* ヘッダー */}
      <div className="bg-blue-300 text-white py-4 relative">
        <div className="relative text-center">
          {/* ◀ ボタン */}
          <button
            onClick={onPrevMonth}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-white text-2xl hover:text-gray-200"
          >
            ◀
          </button>

          {/* 中央：年月表示 */}
          <h2 className="text-3xl font-bold tracking-wider inline-block">
            {month < 10 ? `0${month}` : month}/{year}
          </h2>

          {/* ▶ ボタン */}
          <button
            onClick={onNextMonth}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-white text-2xl hover:text-gray-200"
          >
            ▶
          </button>
        </div>
      </div>

      {/* 曜日ヘッダー */}
      <div className="grid grid-cols-7 text-center text-sm font-bold text-gray-700 border-b">
        {['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.'].map((d, i) => (
          <div
            key={d}
            className={`${i === 0 ? 'text-red-500' : ''} py-2 bg-blue-50`}
          >
            {d}
          </div>
        ))}
      </div>

      {/* カレンダーセル */}
      <div className="grid grid-cols-7 gap-px bg-gray-300">
        {cells}
      </div>
    </div>
  );
};

export default CalendarView;
