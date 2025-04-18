<script setup>
import { RouterView } from 'vue-router'
import { Toaster } from "@/components/ui/toast";
</script>

<template>
  <div class="min-h-screen bg-black text-white">
    <RouterView />
    <Toaster position="top-right" />
  </div>
</template>
