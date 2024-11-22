<template>
  <div>
    <!-- 로딩 중 상태 -->
    <div v-if="loading">Loading...</div>

    <!-- 에러 상태 -->
    <div v-else-if="error">{{ error }}</div>

    <!-- 게시글 상세 내용 -->
    <div v-else-if="post && post.id">
      <h1>게시글 번호: {{ post.id }}</h1>
      <h2>{{ post.title }}</h2>
      <p>{{ post.content }}</p>

      <!-- 좋아요 수 -->
      <p>좋아요: {{ post.like_count }}</p>

      <!-- 좋아요 버튼 -->
      <button v-if="post.liked_by_user" @click="toggleLike(postId)">Unlike</button>
      <button v-else @click="toggleLike(postId)">Like</button>

      <!-- 댓글 목록 컴포넌트 추가 -->
      <comment-list :post-id="postId" />
      <button @click="deletePost(postId)">게시글 삭제</button>
    </div>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import { ref, watch, computed, onMounted } from "vue";
import CommentList from "@/components/boards/CommentList.vue";

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
