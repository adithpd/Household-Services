<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import OngoingRequest from "@/components/service_professional/request_info/ongoing_request/OngoingRequest.vue";
import BookingInfo from "@/components/service_professional/booking_info/BookingInfo.vue";
import RequestInfo from "@/components/service_professional/review_info/ReviewInfo.vue";
import ServiceProfessionalNavbar from "../navbar/ServiceProfessionalNavbar.vue";
import ReportDownloadInfo from "./report_download_info/ReportDownloadInfo.vue";
import { useAuthStore } from "@/stores/authentication/auth";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

const authStore = useAuthStore();
const isVerified = ref("");
const showOngoingRequestForm = ref(false);
const showBookingInfoForm = ref(false);
const showReviewInfoForm = ref(false);
const showReportDownloadInfoForm = ref(false);

const ongoingRequestKey = ref(0);
const bookingInfoKey = ref(0);
const reviewInfoKey = ref(0);
const reportDownloadKey = ref(0);

async function checkServiceProfessionalVerification() {
  if (!authStore.user_id) {
    isVerified.value = "NOT VERIFIED";
    return;
  }

  try {
    const response = await fetch(`${backendUrl}/service-professional/verify-status?user_id=${authStore.user_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${authStore.token}`,
      },
    });

    if (!response.ok) throw new Error("Failed to check verification status");

    const data = await response.json();
    isVerified.value = data.verified;
  } catch (error) {
    console.error("Error checking user verification:", error);
    isVerified.value = "NOT VERIFIED";
  }
}

onMounted(checkServiceProfessionalVerification);

function toggleOngoingRequestForm() {
  showOngoingRequestForm.value = !showOngoingRequestForm.value;
  showBookingInfoForm.value = false;
  showReviewInfoForm.value = false;
  showReportDownloadInfoForm.value = false;
  if (showOngoingRequestForm.value) {
    ongoingRequestKey.value++;
  }
}

function toggleBookingInfoForm() {
  showBookingInfoForm.value = !showBookingInfoForm.value;
  showOngoingRequestForm.value = false;
  showReviewInfoForm.value = false;
  showReportDownloadInfoForm.value = false;
  if (showBookingInfoForm.value) {
    bookingInfoKey.value++;
  }
}

function toggleReviewInfoForm() {
  showReviewInfoForm.value = !showReviewInfoForm.value;
  showOngoingRequestForm.value = false;
  showBookingInfoForm.value = false;
  showReportDownloadInfoForm.value = false;
  if (showBookingInfoForm.value) {
    bookingInfoKey.value++;
  }
}

function toggleReportDownloadInfoForm() {
  showReportDownloadInfoForm.value = !showReportDownloadInfoForm.value;
  showBookingInfoForm.value = false;
  showOngoingRequestForm.value = false;
  showBookingInfoForm.value = false;
  if (showReportDownloadInfoForm.value) {
    bookingInfoKey.value++;
  }
}
</script>

<template>
  <ServiceProfessionalNavbar />
  <div v-if="isVerified === null" class="text-center text-gray-400 mt-6">Checking verification status...</div>
  <div v-else-if="isVerified === 'NOT VERIFIED'" class="bg-yellow-500 text-black text-center py-3 font-semibold">
    Your account is not Verified. Please wait for admin verification before you can continue using our services!
  </div>
  <Card v-else class="max-w-4xl mx-auto mt-12">
    <CardHeader>
      <CardTitle class="text-center text-2xl font-semibold">
        Let's Get Started
      </CardTitle>
    </CardHeader>

    <CardContent class="grid grid-cols-4 gap-4">
      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showOngoingRequestForm }" @click="toggleOngoingRequestForm">
        <i class="pi pi-eye" style="font-size: 2rem"></i>
        <p class="text-sm">View Requests</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showBookingInfoForm }" @click="toggleBookingInfoForm">
        <i class="pi pi-address-book" style="font-size: 2rem"></i>
        <p class="text-sm">View Bookings</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showReviewInfoForm }" @click="toggleReviewInfoForm">
        <i class="pi pi-star" style="font-size: 2rem"></i>
        <p class="text-sm">View Reviews</p>
      </Card>

      <Card class="flex flex-col gap-y-4 justify-between items-center p-6 cursor-pointer hover:bg-gray-900 transition border" :class="{ 'border-4 border-white': showReportDownloadInfoForm }" @click="toggleReportDownloadInfoForm">
        <i class="pi pi-chart-bar" style="font-size: 2rem"></i>
        <p class="text-sm">Download Reports</p>
      </Card>
    </CardContent>
  </Card>

  <OngoingRequest :key="ongoingRequestKey" :open="showOngoingRequestForm" @close="showOngoingRequestForm = false" />
  <BookingInfo :key="bookingInfoKey" :open="showBookingInfoForm" @close="showBookingInfoForm = false" />
  <RequestInfo :key="reviewInfoKey" :open="showReviewInfoForm" @close="showReviewInfoForm = false" />
  <ReportDownloadInfo :key="reportDownloadKey" :open="showReportDownloadInfoForm" @close="showReportDownloadInfoForm = false" />

</template>
