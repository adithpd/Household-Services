<script setup lang="ts">
import { watch, ref } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/customer/review_info/columns'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DataTable from '@/components/datatable/DataTable.vue'
import { useToast } from "@/components/ui/toast/use-toast";
import { useAuthStore } from "@/stores/authentication/auth";
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const authStore = useAuthStore();
const { toast } = useToast();

const data = ref([])
const props = defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

const handleReviewSubmit = async (bookingId, review) => {
  try {
    const response = await fetch(`${backendUrl}/customer/review-info/completed`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        booking_id: bookingId,
        service_professional_rating: review.rating,
        review_provided: "YES",
        customer_remarks: review.customerRemarks,
        review_given_time: new Date().toISOString(),
        paid_price: review.paidPrice,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to submit review.");
    }

    data.value = data.value.filter(request => request.booking_id !== bookingId);
    toast({
      title: "Review Submitted ✅",
      description: "Your review has been successfully submitted!",
      variant: "success",
    });
  } catch (error) {
    console.error("Error submitting review:", error);
  }
};

async function fetchBookings() {
  if (!authStore.user_id || authStore.role !== "customer") return;

  try {
    const response = await fetch(`${backendUrl}/customer/booking-info/view/completed`, {
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
    <DialogContent class="max-w-5xl w-full">
      <DialogHeader>
        <DialogTitle>Pending Reviews</DialogTitle>
      </DialogHeader>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :columns="getColumns(handleReviewSubmit)" :data="data" />
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
