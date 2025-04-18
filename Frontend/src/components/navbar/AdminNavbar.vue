<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from '@/stores/authentication/auth';
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button';
import Menubar from 'primevue/menubar';


const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.clearAuth();
  router.push('/');
};

const items = ref([
    {
        label: 'Admin Dashboard',
        icon: 'pi pi-user',
        class: 'pointer-events-none',
    },
]);
</script>
<template>
  <div class="card">
    <Menubar :model="items">
      <template #end>
        <Button @click="logout" class="m-1">Sign Out</Button>
      </template>
    </Menubar>
  </div>
</template>
