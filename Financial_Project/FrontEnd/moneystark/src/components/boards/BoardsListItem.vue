<template>
  <div class="post-detail-container">
    <!-- 설명 추가 -->
    <h2>
      <i class="mdi mdi-post-outline"></i>
      게시글 상세 보기
    </h2>
    <p class="description">이 페이지에서는 선택한 게시글의 상세 내용을 확인할 수 있습니다.</p>

    <!-- 로딩 중 상태 -->
    <div v-if="loading" class="loading">
      <i class="mdi mdi-loading mdi-spin"></i>
      Loading...
    </div>

    <!-- 에러 상태 -->
    <div v-else-if="error" class="error">
      <i class="mdi mdi-alert-circle-outline"></i>
      {{ error }}
    </div>

    <!-- 게시글 상세 내용 -->
    <div v-else-if="post && post.id" class="post-detail">
      <header class="post-header">
        <p>
          작성자: {{ post.nickname }}
          <RouterLink :to="{ name: 'UserDetailByNickname', params: { nickname: post.nickname } }" class="icon-link">
            <i class="mdi mdi-account-circle-outline"></i>
          </RouterLink>
        </p>
        <h1 class="post-title">제목: {{ post.title }}</h1>
        <p class="post-meta">작성일: {{ post.created_at }}</p>
      </header>
      <hr />
      <section class="post-content">
        <h5>내용:</h5>
        <p>{{ post.content }}</p>
      </section>

      <footer class="post-footer">
        <!-- 좋아요 수 -->
        <p class="like-count">
          <i class="mdi mdi-heart-outline"></i>
          좋아요: {{ post.like_count }}
        </p>

        <!-- 좋아요 버튼 -->
        <button class="like-button" :class="{ liked: post.liked_by_user }" @click="toggleLike(postId)">
          <i :class="post.liked_by_user ? 'mdi mdi-heart' : 'mdi mdi-heart-outline'"></i>
          {{ post.liked_by_user ? "좋아요 취소" : "좋아요" }}
        </button>

        <!-- 게시글 삭제 버튼 -->
        <button class="delete-button" @click="deletePost(postId)">
          <i class="mdi mdi-delete-outline"></i>
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
  max-width: 1000px;
  width: 100%;
  margin: 20px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 설명 스타일 */
.description {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
}

/* 헤더 스타일 */
h2 {
  display: flex;
  align-items: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

h2 i {
  margin-right: 10px;
}

/* 로딩 및 에러 메시지 */
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
  color: #ff0000;
  display: flex;
  align-items: center;
}

.like-count i {
  margin-right: 5px;
}

/* 버튼 스타일 */
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

.delete-button {
  background: #ff4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
  display: flex;
  align-items: center;
}

.delete-button i {
  margin-right: 5px;
}

.delete-button:hover {
  background: #e63e3e;
}

/* 아이콘 링크 스타일 */
.icon-link i {
  margin-right: 5px;
}
</style>
