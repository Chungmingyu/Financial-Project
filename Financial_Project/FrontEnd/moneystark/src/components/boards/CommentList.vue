<template>
  <div class="comment-container">
    <!-- 댓글 목록 -->
    <div v-if="loading" class="loading">
      <i class="mdi mdi-loading mdi-spin"></i>
      Loading comments...
    </div>
    <div v-else-if="error" class="error">
      <i class="mdi mdi-alert-circle-outline"></i>
      {{ error }}
    </div>
    <div v-else>
      <h3 class="comment-title">
        <i class="mdi mdi-comment-multiple-outline"></i>
        댓글 목록
      </h3>
      <ul class="comment-list">
        <li v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <strong class="comment-author">{{ comment.author }}</strong>
            <small class="comment-date">{{ comment.created_at }}</small>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
          <!-- 삭제 버튼 추가 -->
          <button class="delete-button" @click="deleteComment(comment.id)">
            <i class="mdi mdi-delete-outline"></i>
            삭제
          </button>
        </li>
      </ul>
    </div>

    <!-- 댓글 추가 폼 -->
    <div class="add-comment">
      <input v-model="newComment" placeholder="댓글 남기기" class="comment-textarea"></input>
      <button @click="addComment" class="add-comment-button">
        <i class="mdi mdi-send"></i>
        댓글 추가
      </button>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../../stores/api/userStore"; // 인증 없는 Axios 인스턴스를 불러옵니다.
import { ref, onMounted } from "vue";
import { useUserStore } from "../../stores/user";

export default {
  props: {
    postId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const comments = ref([]); // 댓글 목록
    const loading = ref(false); // 로딩 상태
    const error = ref(null); // 에러 상태
    const newComment = ref(""); // 새로운 댓글 내용
    const userstore = useUserStore();
    userstore.fetchUser();

    // 댓글 목록 불러오기
    const fetchComments = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await axiosInstance.get(`/boards/posts/${props.postId}/comments/`);
        comments.value = response.data.comments;
      } catch (err) {
        error.value = "댓글을 가져오는 데 실패했습니다.";
        console.error(err);
      } finally {
        loading.value = false;
      }
    };

    // 새로운 댓글 추가하기
    const addComment = async () => {
      if (!newComment.value.trim()) {
        alert("댓글 내용을 입력해주세요.");
        return;
      }
      try {
        const user_pk = userstore.user.pk;
        const response = await axiosInstance.post(
          `/boards/posts/${props.postId}/comments/`,
          {
            content: newComment.value,
            user_pk: user_pk,
          },
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded", // 기본적인 form-data로 보냄
            },
          }
        );
        comments.value.unshift(response.data.comment); // 새 댓글 목록에 추가
        newComment.value = ""; // 입력 필드 초기화
      } catch (err) {
        error.value = "댓글 추가에 실패했습니다.";
        console.error(err);
      }
    };

    // 댓글 삭제하기
    const deleteComment = async (commentId) => {
      const user_pk = userstore.user.pk;
      try {
        await axiosInstance.delete(`/boards/comments/${commentId}/delete/`, {
          data: {
            user_pk: user_pk,
          },
          headers: {
            "Content-Type": "application/json",
          },
        });
        comments.value = comments.value.filter((comment) => comment.id !== commentId); // 삭제된 댓글 제거
        alert("댓글이 삭제되었습니다.");
      } catch (err) {
        alert(err.response.data.message);
      }
    };

    onMounted(() => {
      fetchComments(); // 컴포넌트가 마운트되면 댓글 목록을 불러옵니다.
    });

    return {
      comments,
      loading,
      error,
      newComment,
      addComment,
      deleteComment,
    };
  },
};
</script>

<style scoped>
/* 컨테이너 스타일 */
.comment-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  max-height: 500px; /* 최대 높이 설정 */
  overflow-y: auto; /* 스크롤 기능 추가 */
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

/* 댓글 목록 제목 */
.comment-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
  display: flex;
  align-items: center;
}

.comment-title i {
  margin-right: 10px;
}

/* 댓글 목록 스타일 */
.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
  height: 150px; /* 원하는 고정 높이로 설정 */
  overflow-y: auto; /* 스크롤 기능 추가 */
}

.comment-item {
  background: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.comment-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.comment-date {
  font-size: 14px;
  color: #888;
}

.comment-content {
  font-size: 16px;
  color: #333;
  line-height: 1.6;
}

/* 삭제 버튼 스타일 */
.delete-button {
  background: #ff4d4d;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  margin-top: 10px;
  display: flex;
  align-items: center;
}

.delete-button i {
  margin-right: 5px;
}

.delete-button:hover {
  background: #e63e3e;
  transform: translateY(-2px);
}

/* 댓글 추가 섹션 */
.add-comment {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
}

.comment-textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 10px;
  margin-bottom: 10px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.comment-textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
}

/* 댓글 추가 버튼 스타일 */
.add-comment-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.2s;
  display: flex;
  align-items: center;
}

.add-comment-button i {
  margin-right: 5px;
}

.add-comment-button:hover {
  background: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 86, 179, 0.4);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .comment-container {
    padding: 15px;
  }

  .comment-title {
    font-size: 18px;
  }

  .comment-item {
    padding: 10px;
  }

  .comment-textarea {
    height: 50px;
  }

  .delete-button,
  .add-comment-button {
    padding: 4px 9px;
    font-size: 14px;
  }
}
</style>