<script setup lang="ts">
import { ref } from "vue"
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal } from 'lucide-vue-next';

const props = defineProps({
  bookingId: String,
});

const isCopied = ref(false);

const copyToClipboard = async () => {
  if (!props.bookingId) return;

  await navigator.clipboard.writeText(props.bookingId);
  isCopied.value = true;
}
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
      <DropdownMenuItem @click="copyToClipboard">
        Copy Booking ID
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

