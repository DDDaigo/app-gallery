<script setup>
defineProps({
  project: { type: Object, required: true }, // { title, slug, image_url, description, ... }
  href: { type: String, default: "" },       // クリック先（詳細ページなど）
});
</script>

<template>
  <RouterLink :to="href || `/p/${project.slug}`" class="group block relative aspect-[3/4]">
    <!-- 窓枠 -->
    <div class="absolute inset-0 rounded-md border-[6px] border-[#7DB2B0] bg-[#eef4f3] shadow-sm overflow-hidden">
      <!-- シャッター（左右） -->
      <div
        class="absolute inset-y-0 left-0 w-1/2 border-r border-[#beecde] bg-[#9ccfbf] [background-image:linear-gradient(180deg,rgba(0,0,0,.08),transparent)] 
               transition-transform duration-500 group-hover:-translate-x-full">
      </div>
      <div
        class="absolute inset-y-0 right-0 w-1/2 border-l border-[#beecde] bg-[#9ccfbf] [background-image:linear-gradient(180deg,rgba(0,0,0,.08),transparent)]
               transition-transform duration-500 group-hover:translate-x-full">
      </div>
      <!-- バルコニー手すり（下部） -->
      <div class="absolute bottom-0 left-0 right-0 h-5 opacity-50
                  [background:repeating-linear-gradient(90deg,rgba(30,41,59,.8)_0_4px,transparent_4px_8px)]" />
      <!-- 中央のコンテンツ（ホバーで現れる） -->
      <div class="relative z-10 h-full p-3 flex flex-col items-center justify-center text-center">
        <img v-if="project.image_url"
             :src="project.image_url" :alt="project.title"
             class="w-1/2 h-1/2 object-cover rounded-xl shadow-md opacity-0 group-hover:opacity-100 transition duration-300" />
        <h3 class="mt-2 text-sm font-semibold text-neutral-800 opacity-0 group-hover:opacity-100 transition duration-300">
          {{ project.title }}
        </h3>
      </div>
    </div>
  </RouterLink>
</template>
