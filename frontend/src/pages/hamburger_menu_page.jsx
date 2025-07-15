// M8 HambergerMenuUI.jsx
// 担当：石田めぐみ

import SideMenu from '../components/SideMenu'

const HomeLayoutPage = () => {
  return (
    <div className="flex">
      <SideMenu />
      <main className="flex-1 p-6">
        {/* ページごとのコンテンツ */}
      </main>
    </div>
  )
}

export default HomeLayoutPage
