<script setup lang="ts">
import { watchEffect, ref, computed } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/service_professional/booking_info/columns'
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
import { useToast } from "@/components/ui/toast";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const { toast } = useToast();
const authStore = useAuthStore();

const filterType = ref("UPCOMING");
const tableKey = ref(0);

const data = ref([])
const props = defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

async function fetchBookings() {
  tableKey.value++;
  if (!authStore.user_id || authStore.role === "service_professional") return;

  try {
    const response = await fetch(`${backendUrl}/sp/booking-info/view`, {
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
    data.value = result.requests || [];
    data.value = [...data.value];
  } catch (error) {
    console.error("Error fetching booking info:", error);
  }
}

const filteredData = computed(() => {
  if (filterType.value === "UPCOMING") return data.value.filter(request => request.status === "UPCOMING");
  if (filterType.value === "COMPLETED") return data.value.filter(request => request.status === "COMPLETED");
  if (filterType.value === "") return data.value.filter(request => !request.status);
  return data.value;
});

const handleCompletedBooking = async (bookingId, remarks, rating) => {
  if (!bookingId || !authStore.user_id) return;
  try {
    const response = await fetch(`${backendUrl}/sp/booking-info/completed`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        role: authStore.role,
        booking_id: bookingId,
        remarks: remarks,
        rating: rating
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to mark booking as completed.");
    }

    const index = data.value.findIndex(request => request.booking_id === bookingId);
    if (index !== -1) {
      data.value[index] = { ...data.value[index], status: "COMPLETED" };
    }
    toast({
      title: "Booking Completed ✅",
      description: "The booking has been successfully marked as completed.",
      variant: "success"
    });
    await fetchBookings();
  } catch (error) {
    console.error("Error marking booking as completed:", error);
    toast({
      title: "Error",
      description: "Failed to mark booking as completed. Try again.",
      variant: "destructive"
    });
  }
};

const handleCancelBooking = async (bookingId) => {
  if (!authStore.user_id || !bookingId) return;

  try {
    const response = await fetch(`${backendUrl}/sp/booking-info/cancel`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        role: authStore.role,
        booking_id: bookingId,
      }),
    });

    if (!response.ok) throw new Error("Failed to cancel booking.");
    data.value = data.value.filter(request => request.booking_id !== bookingId);
    data.value = [...data.value];
    toast(
      {
        title: "Booking Canceled ✅",
        description: "The booking was successfully canceled.",
      }
    );
    await fetchBookings();

  } catch (error) {
    console.error("Error canceling booking:", error);
    toast({ title: "Error", description: "Failed to cancel booking. Try again.", variant: "destructive" });
  }
};

watchEffect(() => {
  if (props.open) {
    fetchBookings();
  }
}
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
          <Button
            variant="outline"
            class="rounded-full text-sm px-4 py-1"
            :class="{ 'bg-muted text-white': filterType === '' }"
            @click="filterType = ''"
          >
            Unmarked Past
          </Button>
        </div>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :key="tableKey" :columns="getColumns(handleCancelBooking,handleCompletedBooking)" :data="filteredData" />
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
