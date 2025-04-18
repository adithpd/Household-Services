<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/customer/request_info/ongoing_request/columns'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DataTable from '@/components/datatable/DataTable.vue'
import { useToast } from "@/components/ui/toast";
import { useAuthStore } from "@/stores/authentication/auth";
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const authStore = useAuthStore();
const { toast } = useToast();

const data = ref([])
defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

async function fetchRequests() {
  if (!authStore.user_id || authStore.role !== "customer") return;

  try {
    const response = await fetch(`${backendUrl}/request-info/view/customer/all`, {
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
      throw new Error("Failed to fetch requests.");
    }

    const result = await response.json();
    data.value = result.requests || [];
  } catch (error) {
    console.error("Error fetching requests:", error);
  }
}

onMounted(fetchRequests);

const handleCancelRequest = async (requestId) => {
  try {
    const response = await fetch(`${backendUrl}/request-info/cancel/customer`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        role: authStore.role,
        request_id: requestId,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to cancel request.");
    }

    data.value = data.value.filter((request) => request.request_id !== requestId);
    toast({
      title: "Request Canceled ✅",
      description: "The request has been successfully canceled.",
      duration: 5000,
      variant: "success",
    });
  } catch (error) {
    console.error("Error canceling request:", error);
  }
};
</script>

<template>
  <Dialog :open="open" @close="emit('close')">
    <DialogContent class="max-w-5xl w-full">
      <DialogHeader>
        <DialogTitle>View Ongoing Requests</DialogTitle>
      </DialogHeader>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :columns="getColumns(handleCancelRequest)" :data="data" />
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
