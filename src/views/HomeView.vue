<template>
  <div class="container flex flex-row justify-center gap-2 mt-24">
    <div class="w-[600px] border shadow-lg border-gray-400 rounded-md">
      <img src="../assets/boardwalk.jpg" class="rounded-sm" alt="" srcset="" />
    </div>

    <div
      class="bg-white shadow-lg border border-gray-400 rounded-md text-center flex flex-col gap-5 p-2"
    >
      <div class="">
        <h5 class="logo-font mb-2">PhotoGram</h5>
        <hr class="text-gray-400 mb-4" />
        <p>Share photos of your favorite moments with friends</p>
      </div>

      <div class="flex flex-row gap-2 justify-center items-center w-full">
        <RouterLink class="w-full" to="/register">
          <button class="bg-green-500 p-2 text-white w-full rounded-sm">
            Register
          </button>
        </RouterLink>
        <RouterLink class="w-full" to="/login">
          <button class="bg-blue-500 p-2 text-white w-full rounded-sm">
            Login
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style></style>

<script setup>
import { RouterLink } from "vue-router";
import { onMounted } from "vue";
import { redirectLoggedInUser } from "../utils/functions";

onMounted(async () => {
  await redirectLoggedInUser();
});
</script>
