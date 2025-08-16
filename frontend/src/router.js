import { createRouter, createWebHistory } from "vue-router";

// ページを遅延読み込み（コード分割）
const Gallery = () => import("./pages/Gallery.vue"); // ← 今の一覧ページをここに移す（下に手順あり）
const Admin = () => import("./pages/Admin.vue");
const ProjectDetail = () => import("./pages/ProjectDetail.vue"); 

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Gallery },
    { path: "/admin", component: Admin },
    { path: "/p/:slug", component: ProjectDetail },
  ],
  scrollBehavior() { return { top: 0 }; },
});
