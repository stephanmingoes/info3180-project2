<template>
  <div class="container">
    <div class="flex flex-row gap-4">
      <div class="flex-1">
        <div v-if="isLoading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <!-- no post here -->
        <div v-else-if="posts.length === 0" class="text-center">
          <h2 class="text-lg">No posts yet</h2>
        </div>
        <div v-else class="flex flex-col gap-5">
          <div
            class="flex flex-col gap-2 bg-white rounded-md shadow-md"
            v-for="post in posts"
            :key="post.id"
          >
            <div class="flex flex-row gap-2 px-4 py-2">
              <div class="">
                <img
                  :src="`/api/v1/image/${post.user.profile_photo}`"
                  class="w-10 h-10 object-cover rounded-full"
                />
              </div>
              <div class="">
                <p>{{ post.user.username }}</p>
              </div>
            </div>
            <div class="">
              <img
                :src="`/api/v1/image/${post.photo}`"
                class="w-full h-96 object-cover"
              />
            </div>
            <div class="px-4 py-2">
              <p>{{ post.caption }}</p>
            </div>
            <div class="flex flex-row justify-between px-4 py-2">
              <span
                class="flex flex-row gap-1 hover:cursor-pointer"
                @click="likePost(post)"
              >
                <span v-if="post.liked_by_current_user"
                  ><i class="fa-solid fa-heart"></i
                ></span>
                <span v-else><i class="fa-regular fa-heart"></i></span>
                <span> {{ post.likes }}</span>
              </span>
              <span>{{ new Date(post.created_on).toDateString() }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="flex-[0.3]">
        <RouterLink to="/posts/new">
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            New Post
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
<script setup>
import { RouterLink } from "vue-router";
import { onMounted, ref } from "vue";
import { redirectLoggedOutUser } from "../utils/functions";
import { authenticationAxiosInstance } from "../api";
const posts = ref([]);

const isLoading = ref(false);

async function likePost(post) {
  try {
    if (post.liked_by_current_user) {
      return;
    }
    post.liked_by_current_user = true;
    post.likes += 1;
    await authenticationAxiosInstance.post(`/api/v1/posts/${post.id}/like`);
  } catch (error) {}
}

onMounted(async () => {
  try {
    isLoading.value = true;
    await redirectLoggedOutUser();
    const { data } = await authenticationAxiosInstance.get("/api/v1/posts");
    posts.value = data.posts;
  } catch (error) {
  } finally {
    isLoading.value = false;
  }
});
</script>
