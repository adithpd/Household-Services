import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user_id: null,
    role: null,
  }),
  actions: {
    setAuthData(user_id, token, role) {
      this.token = token;
      this.user_id = user_id;
      this.role = role;
    },
    clearAuth() {
      this.token = null;
      this.user_id = null;
      this.role = null;
    },
    isAuthenticated() {
      return !!this.token;
    },
    persist: true,
  }
});
