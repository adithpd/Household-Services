<script setup lang="ts">
import { ref } from 'vue';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { MoreHorizontal } from 'lucide-vue-next';
import Rating from 'primevue/rating';


const openDialog = ref(false);
const remarks = ref("");
const rating = ref(5);

const props = defineProps({
  bookingId: String,
  onCancel: Function,
  status: String,
  onComplete: Function
});

const handleCancel = () => {
  props.onCancel(props.bookingId);
};

const markCompleted = () => {
  openDialog.value = true;
};

const submitCompletion = () => {
  if (!props.bookingId) return;

  props.onComplete(props.bookingId, remarks.value, rating.value);
  openDialog.value = false;
};
</script>

<template>
  <DropdownMenu v-if="status !== 'COMPLETED'">
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="w-8 h-8 p-0">
        <span class="sr-only">Open menu</span>
        <MoreHorizontal class="w-4 h-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent side="right">
      <DropdownMenuItem @click="handleCancel">
        Cancel Booking
      </DropdownMenuItem>
      <DropdownMenuItem @click="markCompleted">
        Mark as Completed
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <Dialog v-model:open="openDialog">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Booking Complete Form</DialogTitle>
      </DialogHeader>
      <div class="space-y-4">
        <div class="mb-2">
          <label class="text-sm font-medium">Remarks</label>
          <Textarea v-model="remarks" placeholder="Enter any remarks about the service"></Textarea>
        </div>
        <div>
          <label class="text-sm font-medium">Customer Rating</label>
          <Rating v-model="rating" />
        </div>
      </div>
      <DialogFooter>
        <Button variant="destructive" @click="openDialog = false">Cancel</Button>
        <Button class="bg-green-800 text-white hover:bg-green-800 hover:text-white" @click="submitCompletion">Submit</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

