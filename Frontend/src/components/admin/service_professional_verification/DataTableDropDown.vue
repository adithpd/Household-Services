<script setup lang="ts">
import { ref, computed} from "vue";
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal } from 'lucide-vue-next';
import ViewSPDocumentsDialog from '@/components/admin/service_professional_verification/ViewSPDocumentsDialog.vue';
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const props = defineProps({
  service_professional: Object,
  updateVerificationStatus: Function,
})

const isDialogOpen = ref(false);

const approvalText = computed(() => props.service_professional.verified === 'VERIFIED' ? "Disapprove SP" : "Approve SP");

function copy(service_professional_id) {
  navigator.clipboard.writeText(service_professional_id);
}

async function toggleSPApproval() {
  const newVerifiedStatus = props.service_professional.verified === "VERIFIED" ? "NOT VERIFIED" : "VERIFIED";
  try {
    const response = await fetch(`${backendUrl}/sp/verification/document/verified?service_professional_id=${props.service_professional.service_professional_id}&verified_status=${newVerifiedStatus}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to update verification status");
    }
    await props.updateVerificationStatus(props.service_professional.service_professional_id, newVerifiedStatus);
  } catch (error) {
    console.error("Error updating verification status:", error);
  }
}

async function downloadDocuments() {
  try {
    const response = await fetch(
      `${backendUrl}/sp/verification/document/view/all?service_professional_id=${props.service_professional.service_professional_id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/zip",
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to download documents.");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `SP_Documents_${props.service_professional.service_professional_id}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading documents:", error);
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
      <DropdownMenuItem @click="copy(service_professional.service_professional_id)">
        Copy Service Professional ID
      </DropdownMenuItem>
      <DropdownMenuSeparator class="border-t border-gray-600" />
      <DropdownMenuItem @click="downloadDocuments">Download SP Documents</DropdownMenuItem>
      <DropdownMenuItem @click="isDialogOpen = true">View SP Documents</DropdownMenuItem>
      <DropdownMenuItem @click="toggleSPApproval">{{ approvalText }}</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <ViewSPDocumentsDialog :isOpen="isDialogOpen" @close="isDialogOpen = false" :serviceProfessionalId="service_professional.service_professional_id" />
</template>

