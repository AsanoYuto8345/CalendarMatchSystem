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
