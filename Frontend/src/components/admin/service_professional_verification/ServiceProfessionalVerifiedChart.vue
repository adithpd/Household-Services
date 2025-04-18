<script setup lang="ts">
import { ref, watch } from 'vue'
import Chart from 'primevue/chart'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const chartData = ref(null)

watch(
  () => props.data,
  (newData) => {
    chartData.value = setChartData(newData)
  },
  { deep: true, immediate: true }
)

chartData.value = setChartData(props.data)
const chartOptions = ref(setChartOptions())

function setChartData(data) {
  if (!Array.isArray(data)) {
    console.error("Invalid data format for chart:", data)
    return { labels: [], datasets: [] }
  }

  const approvedCount = data.filter(sp => sp.verified==='VERIFIED').length
  const notApprovedCount = data.length - approvedCount

  return {
    labels: ['Approved SPs', 'Not Approved SPs'],
    datasets: [
      {
        label: 'Verified SPs',
        data: [approvedCount, notApprovedCount],
        backgroundColor: ['rgba(249, 115, 22, 0.6)', 'rgba(6, 182, 212, 0.6)'],
        borderColor: ['rgb(249, 115, 22)', 'rgb(6, 182, 212)'],
        borderWidth: 1
      }
    ]
  }
}

function setChartOptions() {
  const documentStyle = getComputedStyle(document.documentElement)
  const textColor = documentStyle.getPropertyValue('--p-text-color')
  const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color')
  const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color')

  return {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          color: textColorSecondary,
          precision: 0
        },
        grid: {
          color: surfaceBorder
        }
      }
    }
  }
}

</script>

<template>
    <Chart type="bar" :data="chartData" :options="chartOptions" class="w-full h-full" />
</template>
