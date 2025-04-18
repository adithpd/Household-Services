<script setup lang="ts">
import { ref, onMounted } from "vue";
import Chart from "primevue/chart";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

onMounted(async () => {
  const customerData = await fetchCustomerData();
  chartData.value = setChartData(customerData);
  chartOptions.value = setChartOptions();
});

const fetchCustomerData = async () => {
  try {
    const response = await fetch(`${backendUrl}/admin/customer/data`);
    if (!response.ok) {
      throw new Error("Failed to fetch customer data");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching customer data:", error);
    return [];
  }
};

const chartData = ref(null);
const chartOptions = ref(null);

const setChartData = (customers) => {
  const documentStyle = getComputedStyle(document.documentElement);
  const monthlyData = new Array(12).fill(0);
  customers.forEach(customer => {
    const date = new Date(customer.created_at);
    const monthIndex = date.getMonth();
    monthlyData[monthIndex]++;
  });
  return {
      responsive: true,
      maintainAspectRatio: false,
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
          {
              label: 'Customer Influx',
              data: monthlyData,
              fill: false,
              borderColor: documentStyle.getPropertyValue('--p-cyan-500'),
              tension: 0.4
          },
      ]
  };
};
const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
  const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

  return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
          legend: {
              display: false,
          }
      },
      scales: {
          x: {
              ticks: {
                  color: textColorSecondary
              },
              grid: {
                display: false
              },
              border: {
                display: true,
                color: surfaceBorder
              }
          },
          y: {
              ticks: {
                  color: textColorSecondary
              },
              grid: {
                display: false
              },
              border: {
                display: true,
                color: surfaceBorder
              }
          }
      }
  };
}
</script>

<template>
  <div class="px-14">
    <h4 class="scroll-m-20 text-xl font-semibold tracking-tight">
      Customer Influx Graph
    </h4>
  </div>
  <div class="flex flex-col flex-1 pt-2 px-8 pb-8 h-[400px]">
      <Chart v-if="chartData" type="line" :data="chartData" :options="chartOptions" class="w-full h-full" />
  </div>
</template>
