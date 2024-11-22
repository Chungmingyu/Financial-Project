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
        <p>{{ post.nickname }}</p>

        <!-- 좋아요 수 표시 -->
        <p>좋아요: {{ getLikeCount(post.id) }}</p>

        <!-- 좋아요 버튼 -->
        <button v-if="isLikedByUser(post.id)" @click="toggleLike(post.id)">Unlike</button>
        <button v-else @click="toggleLike(post.id)">Like</button>

        <!-- 모달 열기 버튼 -->
        <button @click="openPostDetail(post.id)">자세히 보기</button>
      </li>
    </ul>

    <!-- 모달 -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <BoardsListItem :post-id="selectedPostId" @close="closeModal" />
      </div>
    </div>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import BoardsListItem from "./BoardsListItem.vue";
import { ref, onMounted } from "vue";
import { useUserStore } from "../../stores/user";

export default {
  components: {
    BoardsListItem,
  },
  setup() {
    const postStore = usePostStore();
    const showModal = ref(false); // 모달 표시 여부
    const selectedPostId = ref(null); // 선택된 게시글 ID
    const loading = ref(true);
    const error = ref(null);
    const userstore = useUserStore();

    // 좋아요 개수 및 좋아요 여부 확인
    const getLikeCount = (postId) => postStore.likeCount(postId);
    const isLikedByUser = (postId) => postStore.likedByUser(postId);

    // 모달 열기
    const openPostDetail = (postId) => {
      selectedPostId.value = postId;
      showModal.value = true;
    };

    // 모달 닫기
    const closeModal = () => {
      showModal.value = false;
      selectedPostId.value = null;
    };

    // 게시글 목록 불러오기
    const fetchPosts = async () => {
      loading.value = true;
      error.value = null;
      try {
        await postStore.fetchPosts();
      } catch (err) {
        error.value = "게시글을 가져오는 데 실패했습니다.";
        console.error("게시글 로드 실패:", err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchPosts();
    });

    return {
      posts: postStore.posts,
      loading,
      error,
      toggleLike: postStore.toggleLike,
      getLikeCount,
      isLikedByUser,
      showModal,
      selectedPostId,
      openPostDetail,
      closeModal,
    };
  },
};
</script>

<style scoped>
/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1001;
}
</style>
