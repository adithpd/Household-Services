<script setup lang="ts">
import { computed } from "vue";
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal } from 'lucide-vue-next';
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const props = defineProps({
  customer: Object,
  updateBlockedStatus: Function,
})

const BlockedText = computed(() => props.customer.blocked ? "Block Customer" : "Unblock Customer");

function copy(customer_id) {
  navigator.clipboard.writeText(customer_id);
}

async function toggleCustomerBlocked() {
  const newBlockedStatus = props.customer.blocked === "BLOCKED" ? "NOT BLOCKED" : "BLOCKED";
  try {
    const response = await fetch(`${backendUrl}/customer/blocked?customer_id=${props.customer.customer_id}&blocked=${newBlockedStatus}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to update verification status");
    }
    await props.updateBlockedStatus(props.customer.customer_id, newBlockedStatus);
  } catch (error) {
    console.error("Error updating verification status:", error);
  }
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
      <DropdownMenuItem @click="copy(customer.customer_id)">
        Copy Customer ID
      </DropdownMenuItem>
      <DropdownMenuSeparator class="border-t border-gray-600" />
      <DropdownMenuItem @click="toggleCustomerBlocked">{{ BlockedText }}</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

