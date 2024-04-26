<template>
  <div class="container flex flex-row justify-center gap-2 mt-24">
    <div>
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">
        New Post
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
        @submit.prevent="createNewPost"
        class="w-[500px] mt-3 px-3 py-5 shadow-md rounded-sm bg-white"
      >
        <div class="mt-3">
          <label
            for="photo"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Photo</label
          >
          <input
            type="file"
            id="photo"
            accept="image/*"
            name="photo"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          />
        </div>

        <div class="mt-3">
          <label
            for="caption"
            class="text-lg font-semibold text-gray-800 block mb-1"
            >Caption</label
          >
          <textarea
            id="caption"
            name="caption"
            rows="4"
            class="w-full p-2 border border-gray-900 rounded-md shadow-sm"
          ></textarea>
        </div>

        <div class="mt-3">
          <button
            type="submit"
            class="flex flex-row justify-center gap-1 w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md shadow-md hover:bg-blue-600"
          >
            <span v-if="isLoading">Submitting...</span>
            <span v-if="!isLoading"> Create </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { authenticationAxiosInstance } from "../api";
import { useRouter } from "vue-router";
import { getCsrfToken, redirectLoggedOutUser } from "../utils/functions";
const isLoading = ref(false);
const error = ref("");
const success = ref("");
const csrf_token = ref("");
const router = useRouter();

async function createNewPost() {
  isLoading.value = true;
  error.value = "";
  success.value = "";

  try {
    const form = document.querySelector("form");
    const formData = new FormData(form);
    formData.append("csrf_token", csrf_token.value);
    await authenticationAxiosInstance.post("/api/v1/posts", formData);
    success.value = "Post created successfully!";
    form.reset();
  } catch (err) {
    error.value = err.response.data.message || "An error occurred!";
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await redirectLoggedOutUser();
  csrf_token.value = await getCsrfToken();
});
</script>
