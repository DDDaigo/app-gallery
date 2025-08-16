<script setup>
import Footer from "./components/Footer.vue"; // 作ってあれば
</script>

<template>
  <div class="min-h-dvh flex flex-col brick-bg">
    <router-view class="flex-1" />
    <Footer x="programmingDDD" github="DDDaigo" site="Apps.gallery" />
  </div>
</template>
