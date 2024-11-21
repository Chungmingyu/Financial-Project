import { defineStore } from "pinia";
import axiosInstance from "./api/userStore"; // axiosInstance의 import 경로 확인 필요
import { useUserStore } from "./user";
import { reactive } from "vue";

export const usePostStore = defineStore("post", {
  state: () => ({
    posts: [], // 게시글 목록
    loading: false, // 로딩 상태
    error: null, // 에러 메시지
  }),

  getters: {
    // 게시글 ID로 특정 게시글 가져오기
    getPostById: (state) => (postId) => {
      return state.posts.find((post) => post.id === postId);
    },

    // 좋아요 여부 확인
    likedByUser: (state) => (postId) => {
      const post = state.posts.find((p) => p.id === postId);
      const user = useUserStore().user; // 로그인된 사용자 정보 가져오기
      return post?.liked_by_user; // 사용자가 해당 게시글을 좋아요 했는지 확인
    },

    // 좋아요 개수 반환
    likeCount: (state) => (postId) => {
      const post = state.posts.find((p) => p.id === postId);
      return post.likes_count; // 해당 게시글의 좋아요 개수 반환
    },
  },

  actions: {
    // 게시글 목록 가져오기
    async fetchPosts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axiosInstance.get("/boards/");
        this.posts = response.data; // API 응답 데이터를 posts에 저장
      } catch (error) {
        this.error = error.response?.data || "Failed to fetch posts";
      } finally {
        this.loading = false;
      }
    },

    // 좋아요 토글
    async toggleLike(postId) {
      this.error = null;
      try {
        const response = await axiosInstance.post(`/boards/${postId}/like/`);

        // 서버 응답 데이터에서 좋아요 상태와 개수를 업데이트
        this.posts = this.posts.map((post) => {
          if (post.id === postId) {
            return {
              ...post, // 기존 속성 복사
              liked_by_user: response.data.liked_by_user, // 좋아요 상태 업데이트
              likes_count: response.data.like_count, // 좋아요 개수 업데이트
            };
          }
          return post; // 해당 게시글이 아닌 경우 그대로 반환
        });
        // 로컬 스토리지에 변경된 상태 저장
        this.$patch({
          posts: [...this.posts], // Pinia 상태를 갱신
        });
      } catch (error) {
        this.error = error.response?.data || "Failed to toggle like";
      }
    },

    // 게시글 생성
    async createPost(title, content) {
      this.error = null;
      try {
        const userStore = useUserStore();
        const userPk = userStore.user.pk; // user 정보에서 pk 가져오기
        if (!userPk) {
          throw new Error("User is not logged in");
        }

        const response = await axiosInstance.post("/boards/create/", {
          title: title,
          content: content,
          author: userPk, // author의 pk 값 전달
        });

        this.posts.unshift(response.data); // 새 게시글을 목록 맨 앞에 추가
      } catch (error) {
        this.error = error.response?.data || "Failed to create post";
      }
    },
  },
  persist: true, // Pinia persist 플러그인 사용 여부 확인
});
