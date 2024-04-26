<template>
  <div class="container">
    <div class="flex flex-row">
      <div class="flex-1">
        <h1 class="text-2xl font-bold">Explore</h1>
        <div v-if="isLoading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else>
          <div v-for="post in posts" :key="post.id">
            <div class="flex flex-row">
              <div class="flex-[0.1]">
                <img :src="post.photo" class="rounded-full h-10 w-10" />
              </div>
              <div class="flex-[0.9]">
                <!-- <p class="font-bold">{{ post }}</p> -->
                <p>{{ post.caption }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex-[0.3]">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          New Post
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from "vue";
import { redirectLoggedOutUser } from "../utils/functions";
import { authenticationAxiosInstance } from "../api";
const posts = [
  {
    id: 1,
    caption: "Beautiful sunset at the beach",
    photo: "sunset.jpg",
    likes: 20,
  },
  {
    id: 2,
    caption: "Exploring the mountains",
    photo: "mountains.jpg",
    likes: 15,
  },
  {
    id: 3,
    caption: "Delicious homemade dinner",
    photo: "dinner.jpg",
    likes: 30,
  },
];

const isLoading = ref(false);

onMounted(async () => {
  try {
    isLoading.value = true;
    await redirectLoggedOutUser();
    const { data } = authenticationAxiosInstance.get("/api/v1/posts");
    // posts.value = data.posts;
  } catch (error) {
  } finally {
    isLoading.value = false;
  }
});
</script>
