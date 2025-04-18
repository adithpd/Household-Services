<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getColumns } from '@/components/admin/customer_info/columns'
import DataTable from '@/components/datatable/DataTable.vue'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import CustomerBlockedChart from './CustomerBlockedChart.vue'
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const data = ref([])

async function getData() {
  try {
    const response = await fetch(`${backendUrl}/admin/customer/data`, {
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
      customer_id: item.customer_id,
      user_id: item.user_id,
      blocked: item.blocked,
      city: item.city,
      state: item.state,
      country: item.country,
      created_at: item.created_at,
      rating: item.average_rating.toString(),
    }));
  } catch (error) {
    console.error("Failed to fetch data:", error);
    return [];
  }
}

onMounted(async () => {
  data.value = await getData()
})

const updateBlockedStatus = (customer_id, blocked) => {
  const index = data.value.findIndex(item => item.customer_id === customer_id)
      if (index !== -1) {
        data.value[index] = { ...data.value[index], blocked }
        data.value = [...data.value]
      }
}


</script>

<template>
  <div class="px-14 pt-8">
    <h4 class="scroll-m-20 text-xl font-semibold tracking-tight">
      Customer Information
    </h4>
  </div>
  <div class="flex pt-1 pb-12 px-10 flex-col md:flex-row">
    <ScrollArea class="min-w-[300px] md:min-w-[500px] w-full max-w-full md:w-[850px] p-4">
      <DataTable :columns="getColumns(updateBlockedStatus)" :data="data" />
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
    <div v-if="data.length" class="flex-1 p-4 flex items-stretch">
      <CustomerBlockedChart :data="data" />
    </div>
  </div>
</template>
