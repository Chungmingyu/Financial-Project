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
      <p>좋아요: {{ getLikeCount(postId) }}</p>

      <!-- 좋아요 버튼 -->
      <button v-if="isLikedByUser(postId)" @click="toggleLike(postId)">Unlike</button>
      <button v-else @click="toggleLike(postId)">Like</button>

      <!-- 댓글 목록 컴포넌트 추가 -->
      <comment-list :post-id="postId" />
    </div>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import { ref, watch, computed, onMounted } from "vue";
import CommentList from "@/components/boards/CommentList.vue"; // CommentList 컴포넌트 불러오기

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
    const postStore = usePostStore(); // Pinia store 연결
    const loading = ref(false); // 로딩 상태
    const error = ref(null); // 에러 상태

    // 게시글 데이터 로드 함수
    const fetchPost = async (id) => {
      if (!id) {
        console.warn("유효하지 않은 post ID:", id);
        return; // postId가 유효하지 않으면 요청하지 않음
      }
      console.log("게시글을 가져오는 중... ID:", id);
      loading.value = true;
      error.value = null;
      try {
        await postStore.fetchDetailPosts(id); // Pinia store에서 데이터 로드
      } catch (err) {
        error.value = "게시글을 가져오는 데 실패했습니다.";
        console.error("게시글 로드 실패:", err);
      } finally {
        loading.value = false;
      }
    };

    // 현재 게시글 데이터 (Pinia store의 post를 추적)
    const post = computed(() => postStore.post);

    // 컴포넌트가 처음 로드될 때 데이터 가져오기
    onMounted(() => {
      fetchPost(props.postId); // props로 전달받은 postId로 데이터 가져오기
    });

    // postId 변경 감지
    watch(
      () => props.postId,
      (newId) => {
        if (newId) {
          fetchPost(newId); // 새 게시글 데이터 로드
        }
      }
    );

    return {
      post,
      loading,
      error,
      toggleLike: postStore.toggleLike,
      getLikeCount: (id) => postStore.likeCount(id),
      isLikedByUser: (id) => postStore.likedByUser(id),
    };
  },
};
</script>

<style scoped></style>
