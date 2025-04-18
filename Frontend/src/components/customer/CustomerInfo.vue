<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import RaiseRequest from "@/components/customer/request_info/raise_request/RaiseRequest.vue";
import OngoingRequest from "@/components/customer/request_info/ongoing_request/OngoingRequest.vue";
import BookingInfo from "@/components/customer/booking_info/BookingInfo.vue";
import ReviewInfo from "@/components/customer/review_info/ReviewInfo.vue";
import CustomerNavbar from "../navbar/CustomerNavbar.vue";
import { useAuthStore } from "@/stores/authentication/auth";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const authStore = useAuthStore();
const isBlocked = ref("");
const showCreateForm = ref(false);
const showOngoingRequestForm = ref(false);
const showBookingInfoForm = ref(false);
const showReviewInfoForm = ref(false);
const ongoingRequestKey = ref(0);
const bookingInfoKey = ref(0);
const reviewInfoKey = ref(0);

async function checkCustomerVerification() {
  if (!authStore.user_id) {
    isBlocked.value = "BLOCKED";
    return;
  }

  try {
    const response = await fetch(`${backendUrl}/customer/verify-status?user_id=${authStore.user_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) throw new Error("Failed to check verification status");

    const data = await response.json();
    isBlocked.value = data.blocked;
  } catch (error) {
    console.error("Error checking user verification:", error);
    isBlocked.value = "BLOCKED";
  }
}

onMounted(checkCustomerVerification);

function toggleCreateForm() {
  showCreateForm.value = !showCreateForm.value;
  showOngoingRequestForm.value = false;
  showBookingInfoForm.value = false;
  showReviewInfoForm.value = false;
}

function toggleOngoingRequestForm() {
  showOngoingRequestForm.value = !showOngoingRequestForm.value;
  showCreateForm.value = false;
  showBookingInfoForm.value = false;
  showReviewInfoForm.value = false;
  ongoingRequestKey.value++;
}

function toggleBookingInfoForm() {
  showBookingInfoForm.value = !showBookingInfoForm.value;
  showCreateForm.value = false;
  showOngoingRequestForm.value = false;
  showReviewInfoForm.value = false;
  bookingInfoKey.value++;
}

function toggleReviewInfoForm() {
  showReviewInfoForm.value = !showReviewInfoForm.value;
  showCreateForm.value = false;
  showOngoingRequestForm.value = false;
  showBookingInfoForm.value = false;
  reviewInfoKey.value++;
}
</script>

<template>
  <CustomerNavbar />
  <div v-if="isBlocked === null" class="text-center text-gray-400 mt-6">Checking verification status...</div>
  <div v-else-if="isBlocked === 'BLOCKED'" class="bg-yellow-500 text-black text-center py-3 font-semibold">
    Your account is Blocked. Please wait for admin approval!
  </div>

  <Card v-else class="max-w-xl mx-auto mt-12">
    <CardHeader>
      <CardTitle class="text-center text-2xl font-semibold">
        Let's Get Started
      </CardTitle>
    </CardHeader>

    <CardContent class="grid grid-cols-2 gap-4">
      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showCreateForm }" @click="toggleCreateForm">
        <i class="pi pi-file-edit" style="font-size: 2rem"></i>
        <p class="text-sm">Raise New Request</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showOngoingRequestForm }" @click="toggleOngoingRequestForm">
        <i class="pi pi-eye" style="font-size: 2rem"></i>
        <p class="text-sm">View Ongoing Requests</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showBookingInfoForm }" @click="toggleBookingInfoForm">
        <i class="pi pi-address-book" style="font-size: 2rem"></i>
        <p class="text-sm">View Bookings</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showReviewInfoForm }" @click="toggleReviewInfoForm">
        <i class="pi pi-star" style="font-size: 2rem"></i>
        <p class="text-sm">Pending Reviews</p>
      </Card>
    </CardContent>

    <RaiseRequest v-if="showCreateForm" />
  </Card>

  <OngoingRequest :key="ongoingRequestKey" :open="showOngoingRequestForm" @close="showOngoingRequestForm = false" />
  <BookingInfo :key="bookingInfoKey" :open="showBookingInfoForm" @close="showBookingInfoForm = false" />
  <ReviewInfo :key="reviewInfoKey" :open="showReviewInfoForm" @close="showReviewInfoForm = false" />

</template>
