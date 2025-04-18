<script setup>
import { useAuthStore } from '@/stores/authentication/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.clearAuth();
  router.push('/');
};
</script>

<template>
  <div class="container">
    <h1>User Page</h1>
    <p>Welcome! You are authenticated.</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  margin-top: 50px;
}
button {
  padding: 5px 10px;
  cursor: pointer;
}
</style>
