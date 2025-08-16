<script setup>
import { ref, onMounted } from "vue";
import HeaderBar from "../components/HeaderBar.vue";
import WindowCard from "../components/WindowCard.vue";
import SAMPLE from "../mock/sampleProjects.js";

const BASE = import.meta.env.VITE_API_BASE || "";

const projects = ref([]);
const loading = ref(true);
const error = ref("");

const q = ref("");
const sort = ref("new"); // "new" | "title-asc" | "title-desc"

// ★ ここを true にすれば常にモック、false でAPI
const USE_MOCK = false;

async function fetchData() {
  loading.value = true; error.value = "";
  try {
    if (USE_MOCK) {
      // 検索・並び替えをクライアントで適用
      let data = [...SAMPLE];
      if (q.value) {
        const needle = q.value.toLowerCase();
        data = data.filter(p => p.title.toLowerCase().includes(needle));
      }
      projects.value = data.sort((a, b) => {
        if (sort.value === "title-asc") return a.title.localeCompare(b.title);
        if (sort.value === "title-desc") return b.title.localeCompare(a.title);
        return 0; // new はそのまま
      });
      return;
    }

    // ここから先は API モード
    const params = new URLSearchParams();
    if (q.value) params.set("q", q.value);
    params.set("sort", "new");
    const res = await fetch(`${BASE}/api/projects/?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    let data = await res.json();
    if (sort.value === "title-asc") data = data.sort((a,b)=>a.title.localeCompare(b.title));
    if (sort.value === "title-desc") data = data.sort((a,b)=>b.title.localeCompare(a.title));
    projects.value = data;
  } catch (e) {
    error.value = (e && e.message) ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchData);
</script>

<template>
  <div class="min-h-dvh brick-bg">
    <HeaderBar :q="q" :sort="sort" @update:q="v=>q=v" @update:sort="v=>sort=v" @search="fetchData" />

    <main class="max-w-6xl mx-auto px-4 py-8">
      <div v-if="loading" class="text-slate-600">読み込み中…</div>
      <div v-else-if="error" class="text-red-600">エラー: {{ error }}</div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
        <WindowCard v-for="p in projects" :key="p.id" :project="p" />
      </div>

      <div v-if="!loading && !error && projects.length === 0" class="mt-10 text-center text-slate-600">
        該当するアプリがありません。
      </div>
    </main>
  </div>
</template>

<style>
.brick-bg{
  background-color:#d79a2b;
  background-image:
    linear-gradient(0deg, rgba(255,255,255,0.25) 2px, transparent 2px),
    linear-gradient(90deg, rgba(255,255,255,0.22) 2px, transparent 2px);
  background-size:50px 25px, 50px 25px;
  background-position:0 0, 25px 12.5px;
}
</style>
