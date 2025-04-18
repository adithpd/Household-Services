<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal } from 'lucide-vue-next';

const props = defineProps({
  requestId: String,
  onCancel: Function
});

const handleCancel = () => {
  props.onCancel(props.requestId);
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
      <DropdownMenuItem @click="handleCancel" class="text-gray-200 bg-red-900" >
        Cancel Request
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

