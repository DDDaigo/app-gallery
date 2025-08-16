<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  q: { type: String, default: "" },
  sort: { type: String, default: "new" }, // new | title-asc | title-desc
});
const emit = defineEmits(["update:q", "update:sort", "search"]);

const localQ = ref(props.q);
const localSort = ref(props.sort);

watch(() => props.q, v => (localQ.value = v));
watch(() => props.sort, v => (localSort.value = v));

function doSearch() {
  emit("update:q", localQ.value);
  emit("update:sort", localSort.value);
  emit("search");
}
</script>

<template>
  <header class="sticky top-0 z-20 backdrop-blur bg-white/40">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center gap-3">
      <RouterLink to="/" class="font-bold text-lg">Apps<span class="bg-[#9ccfbf]">.gallery</span></RouterLink>
      <div class="ml-auto flex items-center gap-2">
        <input
          :value="localQ"
          @input="(e)=>localQ = e.target.value"
          @keyup.enter="doSearch"
          placeholder="アプリ名で検索"
          class="rounded-xl px-3 py-2 text-sm w-56"
        />
        <select
          :value="localSort"
          @change="(e)=>{ localSort = e.target.value; doSearch(); }"
          class="rounded-xl px-3 py-2 text-sm"
        >
          <option value="new">新着順</option>
          <option value="title-asc">名前 A→Z</option>
          <option value="title-desc">名前 Z→A</option>
        </select>
        <button @click="doSearch" class="rounded-xl bg-[#9ccfbf] text-white px-4 py-2 text-sm">検索</button>
      </div>
    </div>
  </header>
</template>
