<script setup lang="ts">
import { watch, ref, computed } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/customer/booking_info/columns'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DataTable from '@/components/datatable/DataTable.vue'
import { useAuthStore } from "@/stores/authentication/auth";
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const authStore = useAuthStore();

const filterType = ref("UPCOMING");

const data = ref([])
const props = defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

const filteredData = computed(() => {
  if (filterType.value === "All") return data.value;
  return data.value.filter(request => request.status === filterType.value);
});

async function fetchBookings() {
  if (!authStore.user_id || authStore.role !== "customer") return;

  try {
    const response = await fetch(`${backendUrl}/customer/booking-info/view`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        role: authStore.role,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch bookings.");
    }

    const result = await response.json();
    data.value = result.bookings || [];
    data.value = [...data.value];
  } catch (error) {
    console.error("Error fetching booking info:", error);
  }
}

watch(
  () => props.open,
  async (newVal) => {
    if (newVal) {
      await fetchBookings();
    }
  },
  { immediate: true }
);
</script>

<template>
  <Dialog :open="open" @close="emit('close')">
    <DialogContent class="max-w-6xl w-full">
      <DialogHeader>
        <DialogTitle>Booking Info</DialogTitle>
      </DialogHeader>
        <div class="flex space-x-2 mb-4">
          <Button
            variant="outline"
            class="rounded-full text-sm px-4 py-1"
            :class="{ 'bg-muted text-primary': filterType === 'UPCOMING' }"
            @click="filterType = 'UPCOMING'"
          >
            Upcoming
          </Button>
          <Button
            variant="outline"
            class="rounded-full text-sm px-4 py-1"
            :class="{ 'bg-muted text-white': filterType === 'COMPLETED' }"
            @click="filterType = 'COMPLETED'"
          >
            Completed
          </Button>
        </div>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :columns="getColumns()" :data="filteredData" />
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      <DialogFooter className="sm:justify-start">
        <DialogClose asChild>
          <Button type="button" @click="emit('close')" variant="destructive">
            Close
          </Button>
        </DialogClose>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
