import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue';
import UserPage from '@/views/UserPage.vue';
import RegisterPage from '@/views/register/RegisterPage.vue';
import AdminPanelPage from '@/views/admin/AdminPanelPage.vue';
import CustomerPage from '@/views/customer/CustomerPage.vue';
import { useAuthStore } from '@/stores/authentication/auth';
import ServiceProfessionalPage from '@/views/service_professional/ServiceProfessionalPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/register', component: RegisterPage },
  { path: '/user', component: UserPage, meta: { requiresAuth: true } },
  { path: '/admin', component: AdminPanelPage, meta: { requiresAuth: true } },
  { path: '/customer', component: CustomerPage, meta: { requiresAuth: true } },
  { path: '/service-professional', component: ServiceProfessionalPage, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    next('/');
  } else {
    next();
  }
});

export default router
