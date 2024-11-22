import { defineStore } from "pinia";
import axiosInstance from "./api/userStore"; // axiosInstance import 경로 수정
import { useUserStore } from "@/stores/user";

export const usePostStore = defineStore("post", {
  state: () => ({
    comments: {}, // 댓글 저장 (게시글 ID 별로 관리)
    posts: [], // 게시글 목록
    post: null, // 단일 게시글 데이터
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
      return post?.liked_by_user || false;
    },

    // 좋아요 개수 반환
    likeCount: (state) => (postId) => {
      const post = state.posts.find((p) => p.id === postId);
      return post?.likes_count || 0;
    },
  },

  actions: {
    // 게시글에 댓글 작성하기
    async createComment(comment, postId) {
      try {
        const response = await axiosInstance.post(`/boards/${postId}/comments/`, {
          content: comment,
        });
        const newComment = response.data.comment;

        if (!this.comments[postId]) {
          this.comments[postId] = [];
        }
        this.comments[postId].push(newComment);
        return newComment;
      } catch (error) {
        console.error("댓글 작성 실패:", error.response?.data || error.message);
        throw error;
      }
    },

    // 게시글 목록 가져오기
    async fetchPosts() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axiosInstance.get("/boards/");
        this.posts = response.data;
      } catch (error) {
        this.error = error.response?.data || "Failed to fetch posts";
      } finally {
        this.loading = false;
      }
    },

    // 게시글 상세 가져오기
    async fetchDetailPosts(postId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axiosInstance.get(`/boards/${postId}`);
        this.post = response.data; // 단일 게시글 데이터를 상태에 저장
      } catch (error) {
        this.error = error.response?.data || "Failed to fetch post";
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
              ...post,
              liked_by_user: response.data.liked_by_user,
              likes_count: response.data.like_count,
            };
          }
          return post;
        });

        // 상세 페이지에 대한 좋아요 상태 업데이트
        if (this.post && this.post.id === postId) {
          this.post = {
            ...this.post,
            liked_by_user: response.data.liked_by_user,
            likes_count: response.data.like_count,
          };
        }
      } catch (error) {
        this.error = error.response?.data || "Failed to toggle like";
      }
    },

    // 게시글 생성
    async createPost(title, content) {
      this.error = null;
      try {
        const userStore = useUserStore();
        const userPk = userStore.user?.id; // 로그인된 사용자 ID 가져오기
        if (!userPk) {
          throw new Error("User is not logged in");
        }

        const response = await axiosInstance.post("/boards/create/", {
          title,
          content,
          author: userPk, // 사용자 ID 전달
        });

        this.posts.unshift(response.data); // 새 게시글을 목록 맨 앞에 추가
      } catch (error) {
        this.error = error.response?.data || "Failed to create post";
      }
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "postStore",
        storage: localStorage, // 또는 sessionStorage
      },
    ],
  },
});
