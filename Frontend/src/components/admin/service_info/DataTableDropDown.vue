<script setup lang="ts">
import { ref, computed } from "vue";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import { MoreHorizontal } from "lucide-vue-next";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { useToast } from "@/components/ui/toast";

const backendUrl = import.meta.env.VITE_BACKEND_URL;
const { toast } = useToast();

const props = defineProps({
  service: Object,
  updateService: Function,
  deleteService: Function,
});

const showDialog = ref(false);
const showDeleteDialog = ref(false);
const editingField = ref(null);
const newValue = ref("");

function copy(service_id) {
  navigator.clipboard.writeText(service_id);
}

function openDialog(field, currentValue) {
  editingField.value = field;
  newValue.value = currentValue;
  showDialog.value = true;
}

const isInvalid = computed(() => {
  return newValue.value === "" || newValue.value === null || newValue.value === undefined;
});

async function saveEdit() {
  if (isInvalid.value) return;

  try {
    const response = await fetch(`${backendUrl}/admin/service-info/edit`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service_id: props.service.service_id,
        [editingField.value]: editingField.value === "base_price" ? parseFloat(newValue.value) : newValue.value,
      }),
    });

    if (!response.ok) throw new Error("Failed to update service.");

    toast({
      title: "Service Updated ✅",
      description: `Updated ${editingField.value} successfully.`,
      variant: "success",
    });

    props.updateService(props.service.service_id, editingField.value, newValue.value);
    showDialog.value = false;
  } catch (error) {
    toast({
      title: "Error ❌",
      description: "Failed to update service. Try again.",
      variant: "destructive",
    });
    console.error("Error updating service:", error);
  }
}

async function confirmDelete() {
  try {
    const response = await fetch(`${backendUrl}/admin/service-info/delete`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ service_id: props.service.service_id }),
    });

    if (!response.ok) {
      throw new Error("Failed to delete service.");
    }

    toast({
      title: "Service Deleted ✅",
      description: "The service has been removed successfully.",
      variant: "success",
    });

    props.deleteService(props.service.service_id);
  } catch (error) {
    toast({
      title: "Error ❌",
      description: "Failed to delete the service. Try again.",
      variant: "destructive",
    });
    console.error("Error deleting service:", error);
  } finally {
    showDeleteDialog.value = false;
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
      <DropdownMenuItem @click="copy(props.service.service_id)">
        Copy Service ID
      </DropdownMenuItem>
      <DropdownMenuSeparator class="border-t border-gray-600" />

      <DropdownMenuItem @click="openDialog('description', props.service.description)">
        Edit Description
      </DropdownMenuItem>
      <DropdownMenuItem @click="openDialog('currency', props.service.currency)">
        Edit Currency
      </DropdownMenuItem>
      <DropdownMenuItem @click="openDialog('base_price', props.service.base_price)">
        Edit Base Price
      </DropdownMenuItem>
      <DropdownMenuSeparator class="border-t border-gray-600" />
      <DropdownMenuItem class="text-red-500" @click="showDeleteDialog = true">
        Delete Service
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <Dialog v-model:open="showDialog">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>
          {{ editingField === "description" ? "Edit Description" : editingField === "currency" ? "Edit Currency" : "Edit Base Price" }}
        </DialogTitle>
      </DialogHeader>

      <div class="p-4">
        <Input
          v-if="editingField !== 'currency'"
          v-model="newValue"
          type="text"
          class="mt-1 w-full p-2"
        />
        <Select v-else v-model="newValue">
          <SelectTrigger class="w-full">
            <SelectValue placeholder="" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="USD">
                USD
              </SelectItem>
              <SelectItem value="INR">
                INR
              </SelectItem>
              <SelectItem value="GBP">
                GBP
              </SelectItem>
              <SelectItem value="EUR">
                EUR
              </SelectItem>
              <SelectItem value="AED">
                AED
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <DialogFooter class="flex justify-end space-x-2">
        <Button variant="destructive" @click="showDialog = false">Cancel</Button>
        <Button class="bg-green-800 hover:bg-green-900 text-white font-semibold py-2 px-4 rounded-md" @click="saveEdit">Confirm</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>

  <Dialog v-model:open="showDeleteDialog">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>Confirm Deletion</DialogTitle>
      </DialogHeader>

      <div class="p-4">
        <p>Are you sure you want to delete this service?</p>
      </div>

      <DialogFooter class="flex justify-end space-x-2">
        <Button variant="outline" @click="showDeleteDialog = false">Cancel</Button>
        <Button class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-md" @click="confirmDelete">
          Delete
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
