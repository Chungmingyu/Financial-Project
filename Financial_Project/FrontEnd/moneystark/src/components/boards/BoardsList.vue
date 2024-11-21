<template>
  <div>
    <button @click.prevent="$router.push({ name: 'BoardsCreate' })">Create Post</button>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <ul v-else>
      <li v-for="post in posts" :key="post.id">
        <p>게시글 번호 : {{ post.id }}</p>
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>

        <!-- 좋아요 수 표시 -->
        <p>좋아요: {{ getLikeCount(post.id) }}</p>

        <!-- 좋아요 버튼 -->
        <button v-if="isLikedByUser(post.id)" @click="toggleLike(post.id)">
          {{ "Unlike" }}
        </button>
        <button v-else @click="toggleLike(post.id)">
          {{ "Like" }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";

export default {
  setup() {
    const postStore = usePostStore();

    // 게시글 관련 데이터를 Pinia store에서 가져옵니다.
    const getLikeCount = (postId) => postStore.likeCount(postId); // 좋아요 개수
    const isLikedByUser = (postId) => postStore.likedByUser(postId); // 좋아요 여부

    return {
      posts: postStore.posts,
      loading: postStore.loading,
      error: postStore.error,
      toggleLike: postStore.toggleLike,
      getLikeCount,
      isLikedByUser,
    };
  },

  async mounted() {
    const postStore = usePostStore();
    await postStore.fetchPosts(); // 게시글 불러오기
  },
};
</script>
