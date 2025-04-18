<script setup lang="ts">
import { ref, computed } from 'vue'
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { MoreHorizontal } from 'lucide-vue-next';
import Rating from 'primevue/rating';
import Input from '@/components/ui/input/Input.vue';


const isDialogOpen = ref(false);
const customerRemarks = ref("");
const paidPrice = ref("");
const rating = ref(0);

const props = defineProps({
  bookingId: String,
  currency: String,
  onSubmitReview: Function
});

const formattedBookingId = computed(() => `Booking ID: ${props.bookingId}`);

const handleSubmitReview = () => {
  if (customerRemarks.value.trim() === "" || rating.value === 0) return;

  const reviewData = {
    bookingId: props.bookingId,
    paidPrice: paidPrice.value,
    customerRemarks: customerRemarks.value,
    rating: rating.value
  };

  props.onSubmitReview(props.bookingId, reviewData);

  customerRemarks.value = "";
  paidPrice.value = "";
  rating.value = 0;
  isDialogOpen.value = false;
};
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="w-8 h-8 p-0">
        <span class="sr-only">Open menu</span>
        <MoreHorizontal class="w-4 h-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent side="right">
      <DropdownMenuItem @click="isDialogOpen = true">
        Provide Review
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <Dialog :open="isDialogOpen" @close="isDialogOpen = false">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Submit Your Review</DialogTitle>
        <p class="text-sm text-gray-500">{{ formattedBookingId }}</p>
      </DialogHeader>

      <div class="flex flex-row gap-x-2">
        <input id="quote-currency" :value="`${currency}`" class="w-16 text-center pl-4 pr-4 py-2 border rounded-md
      bg-black text-sm" disabled
        />
        <Input
          id="paid_price"
          v-model="paidPrice"
          type="number"
          placeholder="Enter amount paid"
          class="pl-7"
        />
      </div>

      <span class="text-sm text-gray-500">Customer Review:</span>
      <Textarea v-model="customerRemarks" class="w-full h-24" />

      <div class="flex items-center gap-2 mt-3">
        <span class="text-sm text-gray-500">Overall Rating:</span>
        <Rating v-model="rating" :cancel="false" />
      </div>

      <DialogFooter class="flex justify-end space-x-2">
        <Button variant="destructive" @click="isDialogOpen = false">Cancel</Button>
        <Button variant="default" @click="handleSubmitReview">Submit</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

