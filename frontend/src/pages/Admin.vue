<script setup>
import { ref, onMounted, computed } from "vue";
import HeaderBar from "../components/HeaderBar.vue";
import { createProject, adminListAll, updateProject, deleteProject } from "../lib/api";

const tokenKey = "admin_token";
const token = ref(localStorage.getItem(tokenKey) || "");
const msg = ref("");
const projects = ref([]);
const loading = ref(false);

// 新規/編集フォーム
const editingId = ref(null);
const f = ref({
  title:"", slug:"", description:"", image_url:"", repo_url:"", app_url:"",
  tech_stack:"Vue3, Tailwind, FastAPI", is_published:true, story_md:"", tags_csv:""
});

function setToken(v){ token.value = v; localStorage.setItem(tokenKey, v); }
async function checkToken(){
  msg.value = "";
  try {
    await fetch((import.meta.env.VITE_API_BASE||"") + "/api/projects/admin/ping", {
      headers: { "X-Admin-Token": token.value }
    }).then(r=>{ if(!r.ok) throw new Error("NG"); });
    msg.value = "トークンは有効です。";
  } catch { msg.value = "トークンが無効です。"; }
}

async function loadAll(){
  loading.value = true;
  msg.value = "";
  try {
    projects.value = await adminListAll(token.value);
  } catch(e){ msg.value = e.message; }
  finally { loading.value = false; }
}

function resetForm(){
  editingId.value = null;
  f.value = { title:"", slug:"", description:"", image_url:"", repo_url:"", app_url:"",
    tech_stack:"Vue3, Tailwind, FastAPI", is_published:true, story_md:"", tags_csv:"" };
}

async function submit(){
  msg.value = "";
  try {
    if(!token.value) throw new Error("先にトークンを入力してください。");

    if(editingId.value){ // 更新
      const payload = { ...f.value }; // 空文字は空として送る（必要ならtrim等）
      await updateProject(editingId.value, payload, token.value);
      msg.value = "更新しました。";
    }else{ // 新規
      const payload = { ...f.value };
      await createProject(payload, token.value); // createProject がtoken無しなら修正してね
      msg.value = "作成しました。";
    }
    await loadAll();
    resetForm();
  } catch(e){ msg.value = e.message; }
}

async function editRow(p){
  editingId.value = p.id;
  // 既存値をフォームへ
  f.value = {
    title: p.title || "", slug: p.slug || "", description: p.description || "",
    image_url: p.image_url || "", repo_url: p.repo_url || "", app_url: p.app_url || "",
    tech_stack: p.tech_stack || "", is_published: !!p.is_published,
    story_md: p.story_md || "", tags_csv: p.tags_csv || ""
  };
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function removeRow(p){
  if(!confirm(`「${p.title}」を削除します。よろしいですか？`)) return;
  msg.value = "";
  try {
    await deleteProject(p.id, token.value);
    msg.value = "削除しました。";
    await loadAll();
    if(editingId.value === p.id) resetForm();
  } catch(e){ msg.value = e.message; }
}

onMounted(loadAll);
</script>

<template>
  <div>
    <HeaderBar />
    <main class="container py-6 px-6 mx-auto space-y-6 bg-neutral-200">
      <h1 class="text-xl font-semibold">Admin</h1>

      <!-- トークン -->
      <div class="grid gap-3 rounded-xl">
        <div class="flex gap-2 items-center">
          <input v-model="token" placeholder="X-Admin-Token" class="border rounded-xl px-3 py-2 w-full"/>
          <button @click="() => { setToken(token); checkToken(); }" class="rounded-xl border px-3 py-2 text-sm text-nowrap">確認</button>
        </div>
        <p class="text-sm" :class="{'text-green-600': msg.includes('有効'), 'text-red-600': msg.includes('無効') }">{{ msg }}</p>
      </div>

      <!-- フォーム（新規/編集） -->
      <div class="grid gap-3 p-4 rounded-xl">
        <h2 class="font-semibold">{{ editingId ? '編集' : '新規作成' }}</h2>
        <input v-model="f.title" placeholder="Title" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.slug" placeholder="slug (unique)" class="border rounded-xl px-3 py-2"/>
        <textarea v-model="f.description" placeholder="Description" rows="4" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.image_url" placeholder="Image URL" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.app_url" placeholder="App URL" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.repo_url" placeholder="Repo URL" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.tech_stack" placeholder="Tech stack" class="border rounded-xl px-3 py-2"/>
        <input v-model="f.tags_csv" placeholder="tags (comma separated)" class="border rounded-xl px-3 py-2"/>
        <label class="text-sm font-medium">制作談（Markdown 可）</label>
        <textarea v-model="f.story_md" rows="8" placeholder="例）開発の背景や工夫点、詰まった点など" class="border rounded-xl px-3 py-2"></textarea>
        <label class="inline-flex items-center gap-2 text-sm"><input type="checkbox" v-model="f.is_published"/> Published</label>

        <div class="flex gap-2">
          <button @click="submit" class="rounded-xl bg-[#9ccfbf] text-white px-4 py-2 text-sm">
            {{ editingId ? '更新' : '作成' }}
          </button>
          <button v-if="editingId" @click="resetForm" class="rounded-xl border px-4 py-2 text-sm">キャンセル</button>
        </div>
        <p class="text-sm" :class="{'text-green-600': msg.includes('作成') || msg.includes('更新'), 'text-red-600': msg && !(msg.includes('作成')||msg.includes('更新')) }">{{ msg }}</p>
      </div>

      <!-- 一覧 -->
      <section>
        <div class="flex items-center gap-3 mb-2">
          <h2 class="font-semibold">登録済み</h2>
          <button @click="loadAll" class="rounded-xl border px-3 py-1 text-sm">再読み込み</button>
        </div>
        <div v-if="loading" class="text-sm text-gray-500">読み込み中…</div>
        <div v-else class="grid gap-3">
          <div v-for="p in projects" :key="p.id" class="p-3 border rounded-xl flex items-center gap-3">
            <div class="flex-1">
              <div class="font-medium">{{ p.title }}</div>
              <div class="text-xs text-gray-600">/{{ p.slug }}</div>
            </div>
            <button @click="editRow(p)" class="rounded-xl border px-3 py-1 text-sm">編集</button>
            <button @click="removeRow(p)" class="rounded-xl border px-3 py-1 text-sm text-red-600">削除</button>
          </div>
          <p v-if="!projects.length" class="text-sm text-gray-500">まだありません。</p>
        </div>
      </section>
    </main>
  </div>
</template>
