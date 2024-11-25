<template>
  <div class="boards-container">
    <!-- 로딩 또는 오류 메시지 -->
    <div v-if="loading" class="loading">
      <i class="mdi mdi-loading mdi-spin"></i>
      Loading...
    </div>
    <div v-else-if="error" class="error">
      <i class="mdi mdi-alert-circle-outline"></i>
      {{ error }}
    </div>

    <!-- 게시글 리스트 -->
    <ul v-else class="post-list">
      <li v-for="post in posts" :key="post.id" class="post-item">
        <div class="post-header">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-meta">작성자: {{ post.nickname }} | 번호: {{ post.id }}</p>
        </div>
        <div class="post-content">
          <p>{{ post.content }}</p>
        </div>
        <div class="post-footer">
          <!-- 좋아요 버튼 -->
          <button class="like-button" :class="{ liked: isLikedByUser(post.id) }" @click="toggleLike(post.id)">
            <i :class="isLikedByUser(post.id) ? 'mdi mdi-heart' : 'mdi mdi-heart-outline'"></i>
            {{ isLikedByUser(post.id) ? "좋아요 취소" : "좋아요" }} ({{ getLikeCount(post.id) }})
          </button>

          <!-- 자세히 보기 버튼 -->
          <button class="detail-button" @click="openPostDetail(post.id)">
            <i class="mdi mdi-eye-outline"></i>
            자세히 보기
          </button>
        </div>
      </li>
    </ul>

    <!-- 모달 -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <BoardsListItem :post-id="selectedPostId" @close="closeModal" />
        </div>
      </div>
    </Teleport>
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

    // 좋아요 개수 및 좋아요 여부 확인
    const getLikeCount = (postId) => postStore.likeCount(postId);
    const isLikedByUser = (postId) => postStore.likedByUser(postId);

    // 모달 열기
    const openPostDetail = (postId) => {
      selectedPostId.value = postId;
      showModal.value = true;
      document.body.style.overflow = "hidden";
    };

    // 모달 닫기
    const closeModal = () => {
      showModal.value = false;
      selectedPostId.value = null;
      document.body.style.overflow = "";
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
/* 컨테이너 스타일 */
.boards-container {
  max-width: 1000px;
  position: relative;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 설명 스타일 */
.description {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
}

/* 로딩 및 오류 메시지 */
.loading,
.error {
  text-align: center;
  font-size: 18px;
  color: #333;
  margin: 20px 0;
}

.loading i,
.error i {
  margin-right: 5px;
}

/* 게시글 리스트 */
.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 게시글 헤더 */
.post-header {
  margin-bottom: 10px;
}

.post-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.post-meta {
  font-size: 14px;
  color: #777;
}

/* 게시글 본문 */
.post-content {
  margin-bottom: 15px;
  font-size: 15px;
  color: #555;
}

/* 게시글 푸터 */
.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.like-button {
  background: white;
  color: #ff0000;
  border: 1px solid #ff0000;
  border-radius: 5px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  display: flex;
  align-items: center;
}

.like-button i {
  margin-right: 5px;
}

.like-button.liked {
  background: #ff0000;
  color: white;
}

.like-button:hover {
  background: #cc0000;
  color: white;
}

.detail-button {
  background: #eee;
  color: #333;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
  display: flex;
  align-items: center;
}

.detail-button i {
  margin-right: 5px;
}

.detail-button:hover {
  background: #ddd;
}

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
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 900px;
  max-width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 1001;
}
</style>
