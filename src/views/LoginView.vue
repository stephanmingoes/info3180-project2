<template>
  <div class="container flex flex-row justify-center gap-2 mt-24">
    <div>
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">Login</h1>

      <!-- error and success message -->
      <div
        v-if="error"
        class="bg-red-500 text-white p-2 text-center rounded-md shadow-md"
      >
        {{ error }}
      </div>
      <div
        v-if="success"
        class="bg-green-500 text-white p-2 text-center rounded-md shadow-md"
      >
        {{ success }}
      </div>
      <form
        @submit.prevent="loginUser"
        class="w-[500px] mt-3 px-3 py-5 shadow-md rounded-sm bg-white"
      >
        <div class="mt-3">
          <label
            for="username"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Username</label
          >
          <input
            type="text"
            id="username"
            name="username"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>
        <div class="mt-3">
          <label
            for="password"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Password</label
          >
          <input
            type="password"
            id="password"
            name="password"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>
        <div class="mt-3">
          <button
            type="submit"
            class="flex flex-row justify-center gap-1 w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow-md hover:bg-blue-600"
          >
            <span v-if="isLoading">Submitting...</span>
            <span v-if="!isLoading"> Login </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { redirectLoggedInUser, getCsrfToken } from "../utils/functions";
const router = useRouter();
const error = ref("");
const success = ref("");
const csfr_token = ref("");
const isLoading = ref(false);

async function loginUser() {
  try {
    isLoading.value = true;
    const form = document.querySelector("form");
    const username = form.username.value;
    const password = form.password.value;
    const res = await axios.post(
      "/api/v1/auth/login",
      {
        username,
        password,
        csrf_token: csfr_token.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    success.value = res.data.message;
    const token = res.data.token;
    localStorage.setItem("jwt_token", token);
    error.value = "";
    router.push("/explore");
  } catch (err) {
    error.value = err.response.data.message ?? "Something went wrong";
    success.value = "";
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await redirectLoggedInUser();
  csfr_token.value = await getCsrfToken();
});
</script>
