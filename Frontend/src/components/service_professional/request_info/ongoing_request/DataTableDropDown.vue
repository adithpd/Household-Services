<script setup lang="ts">
import { ref } from 'vue';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal } from 'lucide-vue-next';
import { useAuthStore } from "@/stores/authentication/auth";
import { useToast } from "@/components/ui/toast";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const { toast } = useToast();

const authStore = useAuthStore();
const props = defineProps({
  requestId: String,
  onAccept: Function,
});

const loading = ref(false);

const handleAccept = async () => {
  if (!props.requestId || !authStore.user_id) return;

  loading.value = true;
  try {
    const response = await fetch(`${backendUrl}/sp/request-info/accept`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify({
        user_id: authStore.user_id,
        role: authStore.role,
        request_id: props.requestId,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to accept request.");
    }

    props.onAccept(props.requestId);
    toast({
      title: "Request Accepted ✅",
      description: "The request has been successfully accepted.",
      duration: 5000,
      variant: "success",
    });
  } catch (error) {
    console.error("Error accepting request:", error);
  } finally {
    loading.value = false;
  }
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
      <DropdownMenuItem class="bg-green-900 text-white" @click="handleAccept">
        Accept Request
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

