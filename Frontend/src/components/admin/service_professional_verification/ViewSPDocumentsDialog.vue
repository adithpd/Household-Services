<script setup>
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { ref, watch} from "vue";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const props = defineProps({
  isOpen: Boolean,
  serviceProfessionalId: String,
});
const emit = defineEmits(["close"]);
const dialogOpen = ref(props.isOpen);

watch(() => props.isOpen, (newValue) => {
  dialogOpen.value = newValue;
});

const loading = ref(false);
const selectedDocumentType = ref("aadhar");
const documentUrls = ref({
  aadhar: null,
  resume: null,
  license: null,
});

async function fetchDocument(type) {
  if (selectedDocumentType.value === type && documentUrls.value[type]) return;

  loading.value = true;
  selectedDocumentType.value = type;

  try {
    const response = await fetch(`${backendUrl}/sp/verification/document/view/type?service_professional_id=${props.serviceProfessionalId}&document_type=${type}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/pdf",
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch ${type}`);
    }

    const blob = await response.blob();
    documentUrls.value[type] = window.URL.createObjectURL(blob);
  } catch (error) {
    console.error(`Error fetching ${type}:`, error);
    documentUrls.value[type] = null;
  } finally {
    loading.value = false;
  }
}

watch(dialogOpen, (newValue) => {
  if (newValue) {
    fetchDocument(selectedDocumentType.value);
  }
});
</script>

<template>
  <Dialog v-model:open="dialogOpen">
    <DialogContent class="w-full h-[80vh] flex flex-col">
      <DialogHeader>
        <DialogTitle>Share link</DialogTitle>
        <DialogDescription>
          Anyone who has this link will be able to view this.
        </DialogDescription>
      </DialogHeader>
      <div class="mb-4">
        <Select v-model="selectedDocumentType" @update:model-value="fetchDocument">
          <SelectTrigger>
            <SelectValue placeholder="Select Document Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="aadhar">Aadhar</SelectItem>
            <SelectItem value="resume">Resume</SelectItem>
            <SelectItem value="license">License</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div v-if="loading" class="text-center">Loading document...</div>
      <div v-if="documentUrls[selectedDocumentType]" class="flex-grow">
        <iframe :src="documentUrls[selectedDocumentType]" class="w-full h-full rounded-lg"></iframe>
      </div>
      <div v-else-if="!loading" class="text-center text-gray-500">
        No document available.
      </div>
      <DialogFooter class="sm:justify-start">
        <DialogClose as-child @click="emit('close')">
          <Button type="button" variant="destructive">
            Close
          </Button>
        </DialogClose>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
