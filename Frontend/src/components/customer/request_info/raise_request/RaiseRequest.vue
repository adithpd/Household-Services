<script setup>
import dayjs from "dayjs";
import { cn } from '@/lib/utils'
import { ref, computed, watch, onMounted } from "vue";
import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/toast";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import {
  DateFormatter,
  getLocalTimeZone,
} from '@internationalized/date'
import { Calendar as CalendarIcon } from 'lucide-vue-next'
import { useAuthStore } from "@/stores/authentication/auth"
import { today } from '@internationalized/date'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import { debounce } from "lodash";

const backendUrl = import.meta.env.VITE_BACKEND_URL;
const authStore = useAuthStore();
const { toast } = useToast();

const df = new DateFormatter('en-US', {
  dateStyle: 'long',
})

const start_date = ref()
const start_time = ref("");
const end_time = ref("");
const services = ref([]);
const selectedServiceId = ref("-1");
const selectedService = ref(null);
const basePrice = ref(0);
const currency = ref("");
const quotePrice = ref(0);
const errorMessage = ref("");
const tabSelection = ref("multiLocation");
const searchQuery = ref("");
const searchResults = ref([]);
const selectedServiceMultiLocation = ref("");
const selectedServiceName = ref("")

const isFormValid = computed(() => {
  return (
    selectedService.value &&
    start_date.value &&
    start_time.value &&
    end_time.value &&
    quotePrice.value &&
    isQuoteValid.value &&
    isTimeValid.value
  );
});

const isQuoteValid = computed(() => {
  return quotePrice.value && quotePrice.value >= basePrice.value;
});

const isTimeValid = computed(() => {
  if (!start_time.value || !end_time.value) return false;
  return end_time.value > start_time.value;
});

watch([start_time, end_time], () => {
  if (!start_time.value || !end_time.value) {
    errorMessage.value = "Start time and end time are required.";
  } else if (end_time.value <= start_time.value) {
    errorMessage.value = "End time must be later than start time.";
  } else {
    errorMessage.value = "";
  }
});

function formatTimestamp(dateRef, timeRef) {
  if (!dateRef.value || !timeRef.value) return null;
  return dayjs(dateRef.value.toDate(getLocalTimeZone())).format("YYYY-MM-DD") + " " + timeRef.value + ":00";
}

async function fetchServices() {
  if (!authStore.user_id) return;

  try {
    const response = await fetch(`${backendUrl}/service-info/fetch/by/user/location?user_id=${authStore.user_id}&role=${authStore.role}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch services.");
    }

    services.value = await response.json();
  } catch (error) {
    console.error("Error fetching services:", error);
  }
}

onMounted(fetchServices);


watch(selectedServiceId, newServiceId => {
  const service = services.value.find(s => s.service_id === newServiceId);
  if (service) {
    selectedService.value = { ...service };
    basePrice.value = service.base_price;
    currency.value = service.currency;
    quotePrice.value = basePrice.value;
  }
});


async function submitRequest() {
  if (!isFormValid.value) return;

  const payload = {
    user_id: authStore.user_id,
    service_id: selectedService.value.service_id,
    service_description: selectedService.value.description ?? selectedServiceName.value,
    start_time: formatTimestamp(start_date, start_time),
    end_time: formatTimestamp(start_date, end_time),
    currency: currency.value,
    quote_price: quotePrice.value,
    status: "NEW",
    role: authStore.role
  };

  try {
    const response = await fetch(`${backendUrl}/request-info/insert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Failed to raise request.");
    }

    toast({
      title: "Request Raised ✅",
      description: "Request has been created successfully.",
      duration: 5000,
      variant: "success",
    });

    selectedServiceId.value = "-1";
    selectedService.value = null;
    basePrice.value = 0;
    currency.value = "";
    quotePrice.value = 0;
    start_date.value = null;
    start_time.value = "";
    end_time.value = "";

  } catch (error) {
    toast({
      title: "Error ❌",
      description: "Failed to raise request. Please try again.",
      variant: "destructive",
    });
    console.error("Error submitting request:", error);
  }
}

const fetchSearchResults = debounce(async () => {
  if (!searchQuery.value) {
    searchResults.value = [];
    return;
  }

  try {
    const response = await fetch(`${backendUrl}/search-services?q=${encodeURIComponent(searchQuery.value)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch search results.");
    }

    searchResults.value = await response.json();
  } catch (error) {
    console.error("Error fetching search results:", error);
  }
}, 300);

watch(searchQuery, fetchSearchResults);

function selectServiceMultiLocation(service) {
  selectedServiceMultiLocation.value = `${service.service_name} - ${service.location}, ${service.city} (${service.pincode || 'N/A'})`;
  searchQuery.value = selectedServiceMultiLocation.value;
  selectedServiceId.value = service.service_id;
  selectedServiceName.value = service.service_name;
  basePrice.value = service.base_price;
  currency.value = service.currency;
  selectedService.value = service;
  searchResults.value = [];
}

watch(searchQuery, (newVal) => {
  if (newVal.trim() === "") {
    searchResults.value = [];
    selectedServiceMultiLocation.value.value = "";
  } else {
    fetchSearchResults();
  }
});
</script>

<template>
  <CardContent :key="selectedServiceId" class="mt-6 border-t pt-4">
    <Tabs v-model="tabSelection">
      <TabsList class="w-full flex">
        <TabsTrigger value="multiLocation" class="w-full">Multi-location</TabsTrigger>
        <TabsTrigger value="currentLocation" class="w-full">Current Location</TabsTrigger>
      </TabsList>

      <TabsContent value="multiLocation">
        <Label for="service">Search Services</Label>
        <Input v-model="searchQuery" placeholder="Enter service, location, city, state, country or pincode" />
        <ul v-if="searchResults.length" class="mt-2 bg-black border border-white rounded-md shadow-md max-h-40 overflow-y-auto">
          <li v-for="result in searchResults" :key="result.description" class="p-2 hover:bg-gray-900 cursor-pointer" @click="selectServiceMultiLocation(result)">
            {{ result.service_name }} - {{ result.location }}, {{ result.city }}, ({{ result.pincode || 'N/A' }})
          </li>
        </ul>
        <div v-if="selectedService" class="mt-4">
          <div class="mt-4">
            <Label>Base Price</Label>
            <input id="base-price" :value="`${currency} ${basePrice}`" class="w-full pl-4 pr-4 py-2 border rounded-md
            bg-black text-gray-900 dark:text-gray-200 text-sm" disabled
            />
          </div>
          <div class="mt-4">
            <Label for="quote-price">Enter your Quote Price</Label>
            <div class="flex flex-row gap-x-2">
              <input id="quote-currency" :value="`${currency}`" class="w-16 text-center pl-4 pr-4 py-2 border rounded-md
            bg-black text-gray-900 dark:text-gray-200 text-sm" disabled
              />
              <Input
                id="quote-price"
                v-model="quotePrice"
                type="number"
                placeholder="Enter your quote price"
                class="pl-7"
              />
            </div>
            <p v-if="quotePrice && !isQuoteValid" class="text-red-500 text-sm mt-1">
              Quote price must be greater than {{ currency }} {{ basePrice }}
            </p>
          </div>

          <div class="flex flex-col mb-2">
            <Label class="mt-4 mb-1">Start Date</Label>
            <Popover>
              <PopoverTrigger as-child>
                <Button
                  variant="outline"
                  :class="cn(
                    'w-[280px] justify-start text-left font-normal',
                    !start_date && 'text-muted-foreground',
                  )"
                >
                  <CalendarIcon class="mr-2 h-4 w-4" />
                  {{ start_date ? df.format(dayjs(start_date.toString()).toDate()) : "Pick a date" }}
                </Button>
              </PopoverTrigger>
              <PopoverContent class="w-auto p-0">
                <Calendar
                  v-model="start_date"
                  initial-focus
                  :min-value="today(getLocalTimeZone())"
                  @update:modelValue="(date) => start_date = date"
                  />
              </PopoverContent>
            </Popover>
          </div>
          <Label class="mt-2">Start Time</Label>
          <div class="relative">
            <Input v-model="start_time" type="time" class="w-30 pl-10" />
            <Clock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
          </div>
          <Label class="mt-2">End Time</Label>
          <div class="relative mb-4">
            <Input v-model="end_time" type="time" class="w-30 pl-10" />
            <Clock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
          </div>
          <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
        </div>
        <Button class="w-full mt-4" @click="submitRequest" :disabled="!isFormValid" >
          Raise Request
        </Button>
      </TabsContent>

      <TabsContent value="currentLocation">
        <Label for="service">Select a Service</Label>
        <Select v-model="selectedServiceId" :key="selectedServiceId">
          <SelectTrigger>
            <SelectValue>{{ selectedService ? selectedService.description : "Choose a Service" }}</SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="service in services" :key="service.service_id" :value="service.service_id">
              {{ service.description }}
            </SelectItem>
          </SelectContent>
        </Select>

        <div v-if="selectedService" class="mt-4">
          <div class="mt-4">
            <Label>Base Price</Label>
            <input id="base-price" :value="`${currency} ${basePrice}`" class="w-full pl-4 pr-4 py-2 border rounded-md
            bg-black text-gray-900 dark:text-gray-200 text-sm" disabled
            />
          </div>
          <div class="mt-4">
            <Label for="quote-price">Enter your Quote Price</Label>
            <div class="flex flex-row gap-x-2">
              <input id="quote-currency" :value="`${currency}`" class="w-16 text-center pl-4 pr-4 py-2 border rounded-md
            bg-black text-gray-900 dark:text-gray-200 text-sm" disabled
              />
              <Input
                id="quote-price"
                v-model="quotePrice"
                type="number"
                placeholder="Enter your quote price"
                class="pl-7"
              />
            </div>
            <p v-if="quotePrice && !isQuoteValid" class="text-red-500 text-sm mt-1">
              Quote price must be greater than {{ currency }} {{ basePrice }}
            </p>
          </div>

          <div class="flex flex-col mb-2">
            <Label class="mt-4 mb-1">Start Date</Label>
            <Popover>
              <PopoverTrigger as-child>
                <Button
                  variant="outline"
                  :class="cn(
                    'w-[280px] justify-start text-left font-normal',
                    !start_date && 'text-muted-foreground',
                  )"
                >
                  <CalendarIcon class="mr-2 h-4 w-4" />
                  {{ start_date ? df.format(dayjs(start_date.toString()).toDate()) : "Pick a date" }}
                </Button>
              </PopoverTrigger>
              <PopoverContent class="w-auto p-0">
                <Calendar
                  v-model="start_date"
                  initial-focus
                  :min-value="today(getLocalTimeZone())"
                  @update:modelValue="(date) => start_date = date"
                  />
              </PopoverContent>
            </Popover>
          </div>
          <Label class="mt-2">Start Time</Label>
          <div class="relative">
            <Input v-model="start_time" type="time" class="w-30 pl-10" />
            <Clock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
          </div>
          <Label class="mt-2">End Time</Label>
          <div class="relative mb-4">
            <Input v-model="end_time" type="time" class="w-30 pl-10" />
            <Clock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
          </div>
          <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
        </div>
        <Button class="w-full mt-4" @click="submitRequest" :disabled="!isFormValid" >
          Raise Request
        </Button>
      </TabsContent>
    </Tabs>
  </CardContent>
</template>
