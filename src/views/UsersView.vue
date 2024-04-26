<template>
  <div v-if="isLoading" class="text-center">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div
    v-if="user"
    class="container bg-white flex flex-row gap-3 rounded-md p-1 items-center w-[900px]"
  >
    <div class="w-52 flex-1">
      <img
        :src="`/api/v1/image/${user.profile_photo}`"
        class="w-full h-auto rounded-md"
      />
    </div>
    <div class="flex flex-col gap-9 flex-1">
      <h1 class="text-2xl font-bold">
        {{ user.firstname }} {{ user.lastname }}
      </h1>
      <div>
        <p>{{ user.location }}</p>
        <p>Member since {{ new Date(user.joined_on).toDateString() }}</p>
      </div>
      <p>{{ user.biography }}</p>
    </div>
    <div class="flex flex-col gap-10 flex-1 px-5">
      <div class="flex flex-row justify-between">
        <div class="flex flex-col justify-center items-center gap-1">
          <p class="text-xl font-extrabold">{{ user.posts.length }}</p>
          <p class="text-xl font-extrabold text-gray-500">Posts</p>
        </div>
        <div class="flex flex-col justify-center items-center gap-1">
          <p class="text-xl font-extrabold">{{ user.followerCount }}</p>
          <p class="text-xl font-extrabold text-gray-500">Followers</p>
        </div>
      </div>
      <div>
        <button
          v-if="user.isFollowing"
          class="bg-green-500 text-white px-5 py-2 rounded-md w-full"
        >
          Following
        </button>
        <button
          v-else
          class="bg-green-500 text-white px-5 py-2 rounded-md w-full"
          @click="followUser(user)"
        >
          Follow
        </button>
      </div>
    </div>
  </div>
  <div v-if="user" class="container w-[900px] grid mb-3">
    <!-- list of photos -->
    <div class="flex flex-row gap-5 mt-5">
      <div
        class="flex flex-col gap-5"
        v-for="post in user.posts"
        :key="post.id"
      >
        <img
          :src="`/api/v1/image/${post.photo}`"
          class="w-96 h-96 object-cover"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { authenticationAxiosInstance } from "../api";

const user = ref(null);
const isLoading = ref(false);

async function followUser(user) {
  try {
    user.isFollowing = true;
    user.followerCount += 1;
    await authenticationAxiosInstance.post(`/api/users/${user.id}/follow`);
  } catch (error) {
    user.isFollowing = false;
    user.followerCount -= 1;
    console.error(error);
  }
}

onMounted(async () => {
  const userId = useRoute().params.user_id;

  try {
    isLoading.value = true;
    const response = await authenticationAxiosInstance.get(
      `/api/v1/user/${userId}`
    );
    console.dir(response.data);

    user.value = response.data;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
});
</script>
