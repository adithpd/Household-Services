<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getColumns } from '@/components/admin/service_professional_verification/columns'
import DataTable from '@/components/datatable/DataTable.vue'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import ServiceProfessionalVerifiedChart from './ServiceProfessionalVerifiedChart.vue'
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const data = ref([])


onMounted(async () => {
  data.value = await getData()
})


async function getData() {
  try {
    const response = await fetch(`${backendUrl}/admin/service-professional/verification/data`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error fetching data: ${response.statusText}`);
    }

    const result = await response.json();
    return result.map(item => ({
      service_professional_id: item.service_professional_id,
      name: item.name,
      phone: item.phone,
      email: item.email,
      description: item.description,
      verified: item.verified,
      rating: item.rating.toString(),
    }));
  } catch (error) {
    console.error("Failed to fetch data:", error);
    return [];
  }
}


const updateVerificationStatus = (service_professional_id, verified) => {
  const index = data.value.findIndex(item => item.service_professional_id === service_professional_id)
      if (index !== -1) {
        data.value[index] = { ...data.value[index], verified }
        data.value = [...data.value]
      }
}

</script>

<template>
  <div class="px-14 pt-8">
    <h4 class="scroll-m-20 text-xl font-semibold tracking-tight">
      Service Professional Verification
    </h4>
  </div>
  <div class="flex pt-1 pb-3 px-10 flex-col md:flex-row">
    <ScrollArea class="min-w-[300px] md:min-w-[500px] w-full max-w-full md:w-[850px] p-4">
      <DataTable :columns="getColumns(updateVerificationStatus)" :data="data" />
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
    <div v-if="data.length" class="flex-1 p-4 flex items-stretch">
      <ServiceProfessionalVerifiedChart :data="data" />
    </div>
  </div>
</template>
