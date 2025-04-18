<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getColumns } from '@/components/admin/service_info/columns'
import DataTable from '@/components/datatable/DataTable.vue'
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/components/ui/toast";
const backendUrl = import.meta.env.VITE_BACKEND_URL;


const { toast } = useToast();

const data = ref([])
const showDialog = ref(false);
const newService = ref({
  service_id: "",
  description: "",
  currency: "USD",
  base_price: "",
  created_at: new Date().toISOString(),
  city: "",
  state: "",
  country: "",
});


async function getData() {
  try {
    const response = await fetch(`${backendUrl}/admin/service-info/data`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch service data");
    }

    const result = await response.json();
    data.value = result;
  } catch (error) {
    console.error("Error fetching services:", error);
  }
}

onMounted(async () => {
  await getData()
})

const updateService = (service_id, editedField, newValue) => {
  const index = data.value.findIndex((s) => s.service_id === service_id);
  if (index !== -1) {
    data.value[index] = { ...data.value[index], [editedField]: newValue };
    data.value = [...data.value];
  }
};

const insertService = async () => {
  if (!newService.value.description || !newService.value.base_price || !newService.value.currency || !newService.value.city || !newService.value.state || !newService.value.country) {
    return;
  }

  const payload = {
      description: newService.value.description,
      currency: newService.value.currency,
      base_price: newService.value.base_price,
      city: newService.value.city,
      state: newService.value.state,
      country: newService.value.country,
  };

  try {
    const response = await fetch(`${backendUrl}/admin/create/service`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to add service");
    }

    const result = await response.json();
    data.value.push(result);

    toast({
      title: "Service Created ✅",
      description: `The service has been created successfully.`,
      duration: 5000,
      variant: "success",
    });

    showDialog.value = false;

    Object.assign(newService.value, {
      description: "",
      currency: "USD",
      base_price: "",
      city: "",
      state: "",
      country: "",
    });

    await getData();

  } catch (error) {
    console.error("Error adding service:", error);
  }
};

const deleteService = (service_id) => {
  data.value = data.value.filter(service => service.service_id !== service_id);
};
</script>

<template>
  <div class="flex flex-col place-content-start px-14 pt-8">
    <div class="flex pb-2">
      <h4 class="scroll-m-20 text-xl font-semibold tracking-tight mr-auto">
        Service Management
      </h4>
      <Button @click="showDialog = true">
        Add New Service
      </Button>
    </div>
    <div class="flex-grow w-full pb-12">
      <DataTable :columns="getColumns(updateService, deleteService)" :data="data" />
    </div>
  </div>

  <Dialog v-model:open="showDialog">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>Add New Service</DialogTitle>
      </DialogHeader>

      <div class="p-4 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-300">Description</label>
          <Input v-model="newService.description" type="text" placeholder="Service Description" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300">Currency</label>
          <Select v-model="newService.currency">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select currency" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="USD">USD</SelectItem>
                <SelectItem value="INR">INR</SelectItem>
                <SelectItem value="GBP">GBP</SelectItem>
                <SelectItem value="EUR">EUR</SelectItem>
                <SelectItem value="AED">AED</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300">Base Price</label>
          <Input v-model="newService.base_price" type="number" placeholder="Enter Price" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300">City</label>
          <Input v-model="newService.city" type="text" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300">State</label>
          <Input v-model="newService.state" type="text" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300">Country</label>
          <Input v-model="newService.country" type="text" class="w-full" />
        </div>
      </div>

      <DialogFooter class="flex justify-end space-x-2">
        <Button variant="destructive" @click="showDialog = false">Cancel</Button>
        <Button
          @click="insertService"
          class="bg-green-800 hover:bg-green-900 text-white font-semibold py-2 px-4 rounded-md"
          :disabled="!newService.description || !newService.base_price || !newService.city || !newService.state || !newService.country"
        >
          Confirm
        </Button>
      </DialogFooter>c
    </DialogContent>
  </Dialog>
</template>
