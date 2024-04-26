<template>
  <div class="container flex flex-row justify-center gap-2 mt-24">
    <div>
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">
        Register
      </h1>
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
        @submit.prevent="registerUser"
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
          <label
            for="firstname"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >First Name</label
          >
          <input
            type="text"
            id="firstname"
            name="firstname"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>
        <div class="mt-3">
          <label
            for="lastname"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Last Name</label
          >
          <input
            type="text"
            id="lastname"
            name="lastname"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>

        <div class="mt-3">
          <label
            for="email"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Email</label
          >
          <input
            type="email"
            id="email"
            name="email"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>

        <div class="mt-3">
          <label
            for="location"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Location</label
          >
          <input
            type="text"
            id="location"
            name="location"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>

        <div class="mt-3">
          <label
            for="biography"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Biography</label
          >
          <textarea
            id="biography"
            name="biography"
            rows="4"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          ></textarea>
        </div>

        <div class="mt-3">
          <label
            for="profile_photo"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Profile Photo</label
          >
          <input
            type="file"
            id="profile_photo"
            accept="image/*"
            name="profile_photo"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>

        <div class="mt-6">
          <button
            type="submit"
            class="flex flex-row justify-center gap-1 w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow-md hover:bg-blue-600"
          >
            <span v-if="isLoading">Submitting...</span>
            <span v-if="!isLoading"> Register </span>
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
import { redirectLoggedInUser } from "../utils/functions";

const router = useRouter();
const error = ref("");
const success = ref("");
const csfr_token = ref("");
const isLoading = ref(false);

async function registerUser() {
  try {
    isLoading.value = true;
    const form = document.querySelector("form");
    const formData = new FormData(form);
    formData.append("csrf_token", csfr_token.value);
    const res = await axios.post("/api/v1/register", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-CSRFToken": csfr_token.value,
      },
    });
    success.value = res.data.message;
    // navigate to login
    router.push("/login");

    error.value = "";
  } catch (err) {
    error.value = err.response.data.message ?? "Something went wrong";
    success.value = "";
  } finally {
    isLoading.value = false;
  }
}

async function getCsrfToken() {
  try {
    const res = await fetch("/api/v1/csrf-token");
    const data = await res.json();
    csfr_token.value = data.csrf_token;
  } catch (error) {
    console.log(error);
  }
}

onMounted(async () => {
  await redirectLoggedInUser();
  await getCsrfToken();
});
</script>
