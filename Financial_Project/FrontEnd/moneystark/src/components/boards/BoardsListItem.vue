<template>
  <div class="post-detail-container">
    <!-- 로딩 중 상태 -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- 에러 상태 -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- 게시글 상세 내용 -->
    <div v-else-if="post && post.id" class="post-detail">
      <header class="post-header">
        작성자: {{ post.nickname }}
        <RouterLink :to="{ name: 'UserDetailByNickname', params: { nickname: post.nickname } }" class="icon-link">
<i class="fas fa-user"></i> 
</RouterLink>
        <h1 class="post-title">제목 : {{ post.title }}</h1>
        <p class="post-meta">

        </p>
      </header>
      <hr>
      <section class="post-content">
        <h5>내용 : </h5>
        <p>{{ post.content }}</p>
      </section>

      <footer class="post-footer">
        <!-- 좋아요 수 -->
        <p class="like-count">좋아요: {{ post.like_count }}</p>

        <!-- 좋아요 버튼 -->
        <button
          class="like-button"
          :class="{ liked: post.liked_by_user }"
          @click="toggleLike(postId)"
        >
          {{ post.liked_by_user ? "♥ 좋아요 취소" : "♡ 좋아요" }}
        </button>

        <!-- 게시글 삭제 버튼 -->
        <button class="delete-button" @click="deletePost(postId)">
          삭제
        </button>
      </footer>

      <!-- 댓글 목록 컴포넌트 -->
      <comment-list :post-id="postId" />
    </div>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import { ref, watch, computed, onMounted } from "vue";
import CommentList from "@/components/boards/CommentList.vue";
import { RouterLink } from "vue-router";

export default {
  components: {
    CommentList,
  },
  props: {
    postId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const postStore = usePostStore();
    const loading = ref(false);
    const error = ref(null);

    // 게시글 삭제
    const deletePost = async (id) => {
      try {
        await postStore.deletePost(id);
        alert("게시글이 삭제되었습니다.");
      } catch (err) {
        console.error("게시글 삭제 실패:", err);
        alert("게시글 삭제에 실패했습니다.");
      }
    };

    // 게시글 데이터 로드
    const fetchPost = async (id) => {
      if (!id) return;
      loading.value = true;
      error.value = null;
      try {
        await postStore.fetchDetailPosts(id);
      } catch (err) {
        error.value = "게시글을 가져오는 데 실패했습니다.";
      } finally {
        loading.value = false;
      }
    };

    const post = computed(() => postStore.post);

    onMounted(() => {
      fetchPost(props.postId);
    });

    watch(
      () => props.postId,
      (newId) => {
        if (newId) {
          fetchPost(newId);
        }
      }
    );

    return {
      post,
      loading,
      error,
      deletePost,
      toggleLike: postStore.toggleLike,
    };
  },
};
</script>

<style scoped>
/* 컨테이너 스타일 */
.post-detail-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 로딩 및 에러 메시지 */
.loading,
.error {
  text-align: center;
  font-size: 18px;
  color: #333;
  margin: 20px 0;
}

/* 게시글 상세 스타일 */
.post-detail {
  padding: 20px;
}

/* 헤더 스타일 */
.post-header {
  margin-bottom: 20px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.post-meta {
  font-size: 14px;
  color: #777;
}

/* 본문 스타일 */
.post-content {
  margin-bottom: 20px;
  font-size: 16px;
  color: #555;
  line-height: 1.6;
}

/* 푸터 스타일 */
.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 10px;
  margin-top: 20px;
}

.like-count {
  font-size: 14px;
  color: #17bebb;
}

/* 버튼 스타일 */
.like-button {
  background: white;
  color: #17bebb;
  border: 1px solid #17bebb;
  border-radius: 5px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.like-button.liked {
  background: #17bebb;
  color: white;
}

.like-button:hover {
  background: #139e9c;
  color: white;
}

.delete-button {
  background: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 4px 9px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.delete-button:hover {
  background: #e63e3e;
}
/* CSS */
.icon-link i {
  margin-right: 5px;
}

</style>
