<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const BASE = import.meta.env.VITE_API_BASE || "";
const route = useRoute();
const router = useRouter();

const project = ref(null);
const loading = ref(true);
const error = ref("");

async function fetchItem() {
  loading.value = true; error.value = "";
  try {
    const slug = route.params.slug;
    const res = await fetch(`${BASE}/api/projects/${slug}`);
    if (!res.ok) throw new Error(await res.text());
    project.value = await res.json();
  } catch (e) {
    error.value = (e && e.message) ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}
onMounted(fetchItem);
</script>

<template>
  <main class="max-w-3xl mx-auto px-4 py-8 bg-white/40">
    <button @click="$router.back()" class="text-sm underline">← Back</button>

    <div v-if="loading" class="mt-4 text-neutral-600">読み込み中…</div>
    <div v-else-if="error" class="mt-4 text-red-600">エラー: {{ error }}</div>

    <div v-else-if="project" class="mt-6 space-y-4">
      <h1 class="text-2xl font-bold">{{ project.title }}</h1>
      <p class="text-neutral-600">{{ project.description }}</p>

      <img v-if="project.image_url" :src="project.image_url" :alt="project.title"
           class="rounded-xl w-full max-h-[360px] object-cover" />

      <div class="flex flex-wrap gap-2">
        <span v-for="t in project.tags" :key="t" class="text-xs rounded-full border px-2 py-0.5">{{ t }}</span>
      </div>

      <div class="flex gap-3">
        <a v-if="project.app_url" :href="project.app_url" target="_blank" class="rounded-lg bg-[#7DB2B0] text-white px-3 py-1.5 text-sm">Open App</a>
        <a v-if="project.repo_url" :href="project.repo_url" target="_blank" class="rounded-lg border px-3 py-1.5 text-sm">GitHub</a>
      </div>

      <section v-if="project.story_md">
        <h2 class="text-lg font-semibold mt-6">制作談</h2>
        <!-- まずはプレーン表示（あとでMarkdownに） -->
        <pre class="mt-2 whitespace-pre-wrap text-sm bg-white/70 rounded-xl p-3 font-dotgothic">{{ project.story_md }}</pre>
      </section>
    </div>
  </main>
</template>
