// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeave from '../components/CommunityLeave' 

export const CommunityRoutes = (
  <>
    <Route path="community/leave" element={<CommunityLeave />} />
  </>
)