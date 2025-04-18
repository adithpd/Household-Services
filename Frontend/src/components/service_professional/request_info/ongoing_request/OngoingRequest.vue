<script setup lang="ts">
import { ref, watch } from 'vue'
import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { getColumns } from '@/components/service_professional/request_info/ongoing_request/columns'
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
import { parseISO, compareAsc } from 'date-fns';
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const authStore = useAuthStore();

const data = ref([])
const props = defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);

const handleAcceptRequest = (requestId) => {
  data.value = data.value.filter(request => request.request_id !== requestId);
};

async function fetchRequests() {
  if (!authStore.user_id || authStore.role === "service_professional") return;

  try {
    const response = await fetch(`${backendUrl}/sp/request-info/view`, {
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
      throw new Error("Failed to fetch live requests.");
    }

    const result = await response.json();
    let requests = result.requests
    requests.sort((a, b) => compareAsc(parseISO(a.start_time), parseISO(b.start_time)));
    console.log(requests)
    data.value = [...requests];
  } catch (error) {
    console.error("Error fetching live requests:", error);
  }
}

watch(
  () => props.open,
  (newVal) => {
    if (newVal) {
      fetchRequests();
    }
  },
  { immediate: true }
);
</script>

<template>
  <Dialog :open="open" @close="emit('close')">
    <DialogContent class="max-w-6xl w-full">
      <DialogHeader>
        <DialogTitle>Live Customer Requests</DialogTitle>
      </DialogHeader>
        <ScrollArea class="w-full max-w-full">
          <div class="overflow-auto max-h-[400px] border rounded-lg">
            <DataTable :columns="getColumns(handleAcceptRequest)" :data="data" />
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
