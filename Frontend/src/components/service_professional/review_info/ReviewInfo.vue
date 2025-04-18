<script setup lang="ts">
import { watch, ref } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/service_professional/review_info/columns'
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

const data = ref([])
const props = defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

async function fetchBookings() {
  if (!authStore.user_id || authStore.role !== "service-professional") return;

  try {
    const response = await fetch(`${backendUrl}/sp/review-info/view`, {
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
    data.value = result.reviews || [];
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
    <DialogContent class="max-w-7xl w-full">
      <DialogHeader>
        <DialogTitle>Customer Reviews</DialogTitle>
      </DialogHeader>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :columns="getColumns()" :data="data" />
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
