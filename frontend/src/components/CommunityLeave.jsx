import React, { useState } from "react";
const CommunityLeave = () => {
  // 変数とか処理ロジックとか
  const [isAccepted, setIsAccepted] = useState(false);

  // htmlを書く
  return (
    <>
      <div>コミュニティ脱退画面</div>
      <div>
        <button onClick={() => {
          setIsAccepted(true);
        }}>はい</button>
        <button onClick={() => {
          setIsAccepted(false);
        }}>いいえ</button>
      </div>
      {
        isAccepted ? <div>コミュニティを脱退しました</div> : <div></div>
      }
    </>
  )
}

export default CommunityLeave;