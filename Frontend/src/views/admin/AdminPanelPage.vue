<script setup lang="ts">
import AdminNavbar from '@/components/navbar/AdminNavbar.vue';
import ServiceProfessionalVerification from '@/components/admin/service_professional_verification/ServiceProfessionalVerification.vue'
import CustomerInfo from '@/components/admin/customer_info/CustomerInfo.vue';
import CustomerJoinDateChart from '@/components/admin/customer_info/CustomerJoinDateChart.vue';
import ServiceInfo from '@/components/admin/service_info/ServiceInfo.vue';

</script>

<template>
  <AdminNavbar />
  <ServiceProfessionalVerification />
  <CustomerInfo />
  <CustomerJoinDateChart />
  <ServiceInfo />
</template>
