// // frontend/src/routes/AppLayout.jsx

// import { useEffect, useState } from "react";
// import { Outlet } from "react-router-dom";
// import Cookies from "js-cookie";
// import axios from "axios";
// import HambergerMenuUI from "../components/HambergerMenuUI";

// export default function AppLayout() {
//     const [joinedCommunities, setJoinedCommunities] = useState([]);

//     useEffect(() => {
//     const userId = Cookies.get("userId");
//     if (!userId) return;

//     axios
//         .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/joined`, {
//             params: { user_id: userId },
//         })
//         .then((res) => {
//             setJoinedCommunities(res.data.communities || []);
//         })
//         .catch((err) => {
//             console.error("所属コミュニティ取得失敗:", err);
//         });
//     }, []);

//     return (
//     <>
//         <HambergerMenuUI communities={joinedCommunities} />
//         <Outlet />
//     </>
//     );
// }
