<script setup>
const props = defineProps({
  x: { type: String, default: "" },       // 例: "daigo_x" or "https://x.com/daigo_x"
  github: { type: String, default: "" },  // 例: "daigo-dev" or "https://github.com/daigo-dev"
  site: { type: String, default: "Apps.gallery" },
});
const year = new Date().getFullYear();

function toUrl(handleOrUrl, base) {
  if (!handleOrUrl) return "#";
  if (/^https?:\/\//.test(handleOrUrl)) return handleOrUrl;
  return `${base}/${handleOrUrl}`;
}
</script>

<template>
  <footer class=" bg-white/40 backdrop-blur text-sm">
    <div class="max-w-6xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center gap-3 sm:gap-6">
      <div class="flex items-center gap-4">
        <!-- X -->
        <a
          :href="toUrl(x, 'https://x.com')"
          target="_blank" rel="noopener noreferrer"
          class="inline-flex items-center gap-2 hover:opacity-80"
          aria-label="X (Twitter)"
        >
          <!-- X icon (SVG) -->
          <svg viewBox="0 0 24 24" class="w-5 h-5" fill="currentColor" aria-hidden="true">
            <path d="M18.244 2H21l-6.56 7.49L22.5 22H15.9l-5.09-6.62L4.9 22H2l7.03-8.02L1.5 2h6.77l4.66 6.1L18.244 2Zm-2.34 18h1.65L7.16 4H5.43l10.47 16Z"/>
          </svg>
          <span class="hidden sm:inline">X</span>
        </a>

        <!-- GitHub -->
        <a
          :href="toUrl(github, 'https://github.com')"
          target="_blank" rel="noopener noreferrer"
          class="inline-flex items-center gap-2 hover:opacity-80"
          aria-label="GitHub"
        >
          <!-- GitHub icon (SVG) -->
          <svg viewBox="0 0 24 24" class="w-5 h-5" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" clip-rule="evenodd"
              d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.11.79-.25.79-.56v-2.1c-3.22.7-3.9-1.39-3.9-1.39-.53-1.37-1.3-1.74-1.3-1.74-1.07-.73.08-.72.08-.72 1.18.08 1.8 1.21 1.8 1.21 1.05 1.8 2.75 1.28 3.42.98.11-.77.41-1.28.75-1.57-2.57-.29-5.27-1.28-5.27-5.68 0-1.25.45-2.27 1.2-3.07-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.17a11.05 11.05 0 0 1 5.8 0c2.2-1.48 3.17-1.17 3.17-1.17.63 1.59.23 2.76.11 3.05.75.8 1.2 1.82 1.2 3.07 0 4.41-2.71 5.38-5.29 5.67.42.36.8 1.06.8 2.14v3.17c0 .31.2.67.8.56A11.5 11.5 0 0 0 12 .5Z" />
          </svg>
          <span class="hidden sm:inline">GitHub</span>
        </a>
      </div>

      <div class="sm:ml-auto text-gray-600">
        © {{ year }} {{ site }}
      </div>
    </div>
  </footer>
</template>
