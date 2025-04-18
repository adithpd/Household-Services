<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/stores/authentication/auth";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

defineProps({
    open: Boolean,
});
const emit = defineEmits(["close"]);
const authStore = useAuthStore();
const exportStatus = ref("");
const downloadLink = ref("");


async function exportServiceRequests() {
  exportStatus.value = "Generating report...";
  downloadLink.value = "";

  try {
    const response = await axios.post(`${backendUrl}/export/service-requests`, {
      user_id: authStore.user_id,
    });

    if (response.data.message === "Export initiated") {
      exportStatus.value = "Export in progress. Please wait...";
      checkExportStatus(response.data.task_id);
    }
  } catch (error) {
    exportStatus.value = `Export failed with error - ${error}. Please try again`;
  }
}

async function checkExportStatus(taskId) {
  let retries = 10;
  let delay = 3000;

  while (retries > 0) {
    await new Promise((resolve) => setTimeout(resolve, delay));

    try {
      const response = await axios.get(`${backendUrl}/celery/status/${taskId}`);
      if (response.data.status === "success") {
        downloadLink.value = response.data.file_url;
        exportStatus.value = "Export completed!";
        return;
      } else if (response.status === 429) {
        console.warn("Too many requests. Backing off...");
        delay *= 2;
      }
    } catch (error) {
      console.error("Error checking status:", error);
      if (error.response && error.response.status === 429) {
        console.warn("Too many requests. Increasing delay...");
        delay *= 2;
      }
    }
    }

    retries--;
  }
  exportStatus.value = "Export timeout. Please try again.";
</script>

<template>
  <Dialog :open="open" @close="emit('close')">
    <DialogContent class="max-w-xl w-full">
      <DialogHeader>
        <DialogTitle>Download Reports</DialogTitle>
      </DialogHeader>
      <div class="flex mt-5">
        <Button @click="exportServiceRequests" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 w-40">
          Export Report
        </Button>
      </div>
      <p v-if="exportStatus" class="text-white">{{ exportStatus }}</p>
      <a v-if="downloadLink" :href="downloadLink" target="_blank" class="text-blue-600 underline">
        Download Report
      </a>
      <DialogFooter className="sm:justify-start">
        <DialogClose asChild>
          <Button type="button" @click="emit('close')" variant="destructive" class="mt-5">
            Close
          </Button>
        </DialogClose>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
