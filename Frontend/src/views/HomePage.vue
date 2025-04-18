<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authentication/auth';
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/toast';

const backendUrl = import.meta.env.VITE_BACKEND_URL;

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');
const usernameError = ref(false);
const passwordError = ref(false);
const errorMessage = ref('');
const { toast } = useToast();

const validateForm = () => {
  let valid = true;

  if (!username.value.trim()) {
    usernameError.value = true;
    valid = false;
  } else {
    usernameError.value = false;
  }

  if (!password.value.trim()) {
    passwordError.value = true;
    valid = false;
  } else {
    passwordError.value = false;
  }

  return valid;
};

const clearUsernameError = () => {
  usernameError.value = false;
  errorMessage.value = '';
}
const clearPasswordError = () => {
  passwordError.value = false;
  errorMessage.value = '';
}

const login = async () => {
  if (!validateForm()) {
    return
  }

  try {
    const response = await fetch(`${backendUrl}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (response.status === 200) {
      authStore.setAuthData(data.user_id, data.token, data.role);
      toast({
        title: "Login Successful ✅",
        description: "Redirecting to your dashboard...",
        duration: 5000,
        variant: "success",
      });
      if (data.role == 'admin') {
        setTimeout(() => {
          router.push('/admin');
        }, 1000);
      }
      else if (data.role == 'customer') {
        setTimeout(() => {
          router.push('/customer');
        }, 1000);
      }
      else {
        setTimeout(() => {
          router.push('/service-professional');
        }, 1000);
      }
    } else {
      errorMessage.value = data.message || "Something went wrong!";
    }
  } catch (error) {
    console.error("Login error:", error);
    errorMessage.value = "Network error, please try again!";
  }
};
</script>

<template>
  <div class="flex items-center justify-center content-center h-lvh">
    <Card class="w-[430px]">
      <CardHeader>
        <CardTitle class="text-center mb-5">Urban Clap</CardTitle>
      </CardHeader>
      <CardContent class="px-10">
        <form>
          <div class="grid items-center w-full gap-4">
            <div class="flex flex-col space-y-1.5 mb-2">
              <Label for="name">Username</Label>
              <Input v-model="username" id="username" @input="clearUsernameError" :class="{'border-red-500': usernameError, '': !usernameError}" placeholder="Enter your username" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <Label for="name">Password</Label>
              <Input v-model="password" id="password" @input="clearPasswordError" :class="{'border-red-500': passwordError, '': !passwordError}" placeholder="Enter your password" />
            </div>
          </div>
        </form>
        <p v-if="errorMessage" class="text-red-500 text-sm mt-3">{{ errorMessage }}</p>
      </CardContent>
      <CardFooter class="flex justify-between px-6 pb-6">
        <Button variant="outline" @click="login">Login</Button>
        <RouterLink to="/register">
          <Button>Register</Button>
        </RouterLink>
      </CardFooter>
    </Card>
  </div>
</template>
