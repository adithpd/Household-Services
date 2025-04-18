<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectTrigger, SelectContent, SelectValue, SelectItem } from '@/components/ui/select';
import { useToast } from '@/components/ui/toast';


const backendUrl = import.meta.env.VITE_BACKEND_URL;

const router = useRouter();

const username = ref('');
const password = ref('');
const role = ref('customer');
const serviceDescription = ref('');
const experience = ref('');
const name = ref('');
const phone = ref('');
const email = ref('');
const location = ref('');
const city = ref('');
const state = ref('');
const country = ref('');
const pincode = ref('');

const aadharCard = ref(null);
const resume = ref(null);
const license = ref(null);

const errorMessage = ref('');
const errors = ref({});

const { toast } = useToast();

const clearError = (field) => {
  errors.value[field] = false;
};

const validateForm = async () => {
  errors.value = {};
  let valid = true;

  if (!username.value.trim()) {
    errors.value.username = 'Username is required';
    valid = false;
  }

  if (!password.value.trim() || password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters';
    valid = false;
  }

  if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = 'Enter a valid email';
    valid = false;
  }

  if (!phone.value.trim() || !/^\d{10}$/.test(phone.value)) {
    errors.value.phone = 'Enter a valid 10-digit phone number';
    valid = false;
  }

  if (!name.value.trim()) {
    errors.value.name = 'Name is required';
    valid = false;
  }

  if (!location.value.trim()) {
    errors.value.location = 'Location is required';
    valid = false;
  }

  if (!city.value.trim()) {
    errors.value.city = 'City is required';
    valid = false;
  }

  if (!state.value.trim()) {
    errors.value.state = 'State is required';
    valid = false;
  }

  if (!country.value.trim()) {
    errors.value.country = 'Country is required';
    valid = false;
  }

  if (!pincode.value.trim()) {
    errors.value.pincode = 'Pincode is required';
    valid = false;
  }

  if (role.value === 'service-professional') {
    if (!serviceDescription.value.trim()) {
      errors.value.serviceDescription = 'Service description is required';
      valid = false;
    }

    if (!experience.value.trim()) {
      errors.value.experience = 'Experience is required';
      valid = false;
    }

    if (!aadharCard.value) {
      errors.value.aadharCard = "File is required";
      valid = false;
    }

    if (!resume.value) {
      errors.value.resume = "File is required";
      valid = false;
    }

    if (!license.value) {
      errors.value.license = "File is required";
      valid = false;
    }

    valid = valid && (await validateFile(aadharCard.value, "aadharCard"));
    valid = valid && (await validateFile(resume.value, "resume"));
    valid = valid && (await validateFile(license.value, "license"));
  }
  return valid;
};

const validateFile = async (file, fileType) => {
  const maxFileSize = 1024 * 1024;
  const validMimeType = "application/pdf";
  console.log(file)
  if (!file || file.size === 0) {
    errors.value[fileType] = "File is required";
    return false;
  }

  if (file.type !== validMimeType) {
    errors.value[fileType] = "Only PDF files are allowed";
    return false;
  }

  if (file.size > maxFileSize) {
    errors.value[fileType] = "File must be less than 1MB";
    return false;
  }


  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const buffer = new Uint8Array(event.target.result);
      if (buffer[0] === 0x25 && buffer[1] === 0x50 && buffer[2] === 0x44 && buffer[3] === 0x46) {
        errors.value[fileType] = "";
        resolve(true);
      } else {
        errors.value[fileType] = "File is corrupted";
        resolve(false);
      }
    };
    reader.readAsArrayBuffer(file.slice(0, 4));
  });
};

const handleFileUpload = async (event, fileType) => {
  const file = event.target.files[0];
  const isValid = await validateFile(file, fileType);

  if (isValid) {
    if (fileType === "aadharCard") aadharCard.value = file;
    if (fileType === "resume") resume.value = file;
    if (fileType === "license") license.value = file;
  } else {
    event.target.value = "";
  }
};

const register = async () => {
  const isValid = await validateForm();

  if (!isValid) {
    return;
  }

  errorMessage.value = '';

  const userData = {
    user_id: username.value,
    name: name.value,
    email: email.value,
    password: password.value,
    role: role.value,
  };

  try {
    const response = await fetch(`${backendUrl}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    if(response.status===200) {
      if (role.value === 'customer') {
        await registerCustomer();
      }

      if (role.value === 'service-professional') {
        const serviceProfessionalID = await registerServiceProfessional();
        if(serviceProfessionalID) {
          await uploadDocuments(serviceProfessionalID);
        }
      }
      console.log('Registration successful');
      toast({
        title: "Registration Successful ✅ ",
        description: "Proceed to Login!",
        duration: 8000,
        variant: "success",
      });
      setTimeout(() => {
        router.push('/');
      }, 1000);
    } else if (response.status === 409) {
      errorMessage.value = "Username or Email is already taken!";
    } else if (response.status === 422) {
      errorMessage.value = "Form details are incomplete";
    } else {
      errorMessage.value = "Something went wrong. Try again!";
    }
  } catch (error) {
    console.log(error)
    errorMessage.value = "Network error. Please try again.";
  }
};

const registerCustomer = async () => {
  try {
    const customerResponse = await fetch(`${backendUrl}/customer/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: username.value,
        location: location.value,
        city: city.value,
        state: state.value,
        country: country.value,
        pincode: pincode.value,
        phone: phone.value,
      }),
    });

    if (customerResponse.status === 200) {
      console.log('Customer record insertion successful');
    } else {
      console.log('Customer record insertion failed');
    }
  } catch (error) {
    console.error('Error in /customer API:', error);
  }
};

const registerServiceProfessional = async () => {
  try {
    const serviceProfessionalResponse = await fetch(`${backendUrl}/service-professional/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: username.value,
        name: name.value,
        phone: phone.value,
        description: serviceDescription.value,
        experience_years: experience.value,
        location: location.value,
        city: city.value,
        state: state.value,
        country: country.value,
        pincode: pincode.value,
      }),
    });

    if (serviceProfessionalResponse.status === 200) {
      console.log('Service Professional record insertion successful');
      const data = await serviceProfessionalResponse.json();
      return data.service_professional_id;
    }
    else {
      console.log('Service Professional record insertion failed');
    }
  }
  catch (error) {
    console.error('Error in /service-professional API:', error);
  }
};

const uploadDocuments = async (serviceProfessionalID) => {
  const files = [
    { file: aadharCard.value, type: "aadhar" },
    { file: resume.value, type: "resume" },
    { file: license.value, type: "license" }
  ];

  for (const { file, type } of files) {
    if (file) {
      const formData = new FormData();
      formData.append("service_professional_id", serviceProfessionalID);
      formData.append("document_type", type);
      formData.append("document_data", file);

      try {
        const response = await fetch(`${backendUrl}/sp/verification/document/upload`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          console.log(`${type} uploaded successfully`);
        } else {
          console.log(`Failed to upload ${type}`);
        }
      } catch (error) {
        console.error(`Error uploading ${type}:`, error);
      }
    }
  }
};
</script>

<template>
  <div class="flex items-center justify-center content-center h-lvh">
    <Card class="w-[430px]">
      <CardHeader>
        <CardTitle class="text-center">Register</CardTitle>
      </CardHeader>
      <CardContent class="max-h-[60vh] overflow-y-auto p-10">
        <form>
          <div class="grid gap-4">
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="username">Username</Label>
              <Input v-model="username" id="username" @input="clearError('username')"
              :class="{'border-red-500': errors.username, '': !errors.username}" placeholder="Enter your username" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="password">Password</Label>
              <Input v-model="password" id="password" type="password" @input="clearError('password')"
                :class="{'border-red-500': errors.password, '': !errors.password}" placeholder="Enter your password" />
                <p v-if="errors.password" class="text-red-500 text-sm">{{ errors.password }}</p>
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="role">Role</Label>
              <Select v-model="role">
                <SelectTrigger>
                  <SelectValue placeholder="Select Role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="customer">Customer</SelectItem>
                  <SelectItem value="service-professional">Service Professional</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <template v-if="role === 'service-professional'">
              <div class="flex flex-col space-y-1.5 mb-2">
                <Label for="serviceDescription">Service Description</Label>
                <Input v-model="serviceDescription" id="serviceDescription" @input="clearError('serviceDescription')"
                :class="{'border-red-500': errors.serviceDescription, '': !errors.serviceDescription}" placeholder="e.g., Plumbing, Electrician" />
              </div>
              <div class="flex flex-col space-y-1.5 mb-2">
                <Label for="experience">Experience</Label>
                <Input v-model="experience" id="experience" @input="clearError('experience')"
                :class="{'border-red-500': errors.experience, '': !errors.experience}" placeholder="Enter your experience (no of years)" />
              </div>
            </template>

            <div class="flex flex-col space-y-1.5">
              <Label for="name">Name</Label>
              <Input v-model="name" id="name" @input="clearError('name')"
              :class="{'border-red-500': errors.name, '': !errors.name}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="serviceType">Location</Label>
              <Input v-model="location" id="location" @input="clearError('location')"
              :class="{'border-red-500': errors.location, '': !errors.location}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="address">City</Label>
              <Input v-model="city" id="city" @input="clearError('city')"
              :class="{'border-red-500': errors.city, '': !errors.city}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="address">State</Label>
              <Input v-model="state" id="state" @input="clearError('state')"
              :class="{'border-red-500': errors.state, '': !errors.state}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="address">Country</Label>
              <Input v-model="country" id="country" @input="clearError('country')"
              :class="{'border-red-500': errors.country, '': !errors.country}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="address">Pincode</Label>
              <Input v-model="pincode" id="pincode" @input="clearError('pincode')"
              :class="{'border-red-500': errors.pincode, '': !errors.pincode}" />
            </div>
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="phone">Phone Number</Label>
              <Input v-model="phone" id="phone" @input="clearError('phone')"
              :class="{'border-red-500': errors.phone, '': !errors.phone}" placeholder="Enter your phone number" />
              <p v-if="errors.phone" class="text-red-500 text-sm">{{ errors.phone }}</p>
            </div>
            <div class="flex flex-col space-y-1.5">
              <Label for="email">Email</Label>
              <Input v-model="email" id="email" @input="clearError('email')"
              :class="{'border-red-500': errors.email, '': !errors.email}" placeholder="Enter your email" />
              <p v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</p>
            </div>

            <template v-if="role === 'service-professional'">
              <div class="flex flex-col space-y-1.5 mt-2 mb-2">
                <Label for="aadharCard">Upload Aadhar Card</Label>
                <Input id="aadharCard" type="file" accept="application/pdf" @change="(e) => handleFileUpload(e, 'aadharCard')" />
                <p v-if="errors.aadharCard" class="text-red-500 text-sm">{{ errors.aadharCard }}</p>
              </div>
              <div class="flex flex-col space-y-1.5 mb-2">
                <Label for="resume">Upload Resume</Label>
                <Input id="resume" type="file" accept="application/pdf" @change="(e) => handleFileUpload(e, 'resume')" />
                <p v-if="errors.resume" class="text-red-500 text-sm">{{ errors.resume }}</p>
              </div>
              <div class="flex flex-col space-y-1.5">
                <Label for="license">Upload License</Label>
                <Input id="license" type="file" accept="application/pdf" @change="(e) => handleFileUpload(e, 'license')" />
                <p v-if="errors.resume" class="text-red-500 text-sm">{{ errors.resume }}</p>
              </div>
            </template>
          </div>
        </form>
      </CardContent>
      <div class="pl-12 mt-3">
        <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
      </div>
      <CardFooter class="flex justify-between mt-5 px-6 pb-6">
        <Button variant="outline" @click="router.push('/')">Back</Button>
        <Button @click="register">Register</Button>
      </CardFooter>
    </Card>
  </div>
</template>
