<template>
  <div>
    <!-- 댓글 목록 -->
    <div v-if="loading">Loading comments...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <h3>댓글 목록</h3>
      <ul>
        <li v-for="comment in comments" :key="comment.id">
          <p>
            <strong>{{ comment.author }}</strong>
            : {{ comment.content }}
          </p>
          <p>
            <small>{{ comment.created_at }}</small>
          </p>
          <!-- 삭제 버튼 추가 -->
          <button @click="deleteComment(comment.id)">삭제</button>
        </li>
      </ul>
    </div>

    <!-- 댓글 추가 폼 -->
    <div class="add-comment">
      <h3>댓글 추가하기</h3>
      <textarea v-model="newComment" placeholder="댓글을 입력하세요..."></textarea>
      <button @click="addComment">댓글 추가</button>
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
        // console.log(userstore.user);
        const user_pk = userstore.user.id;
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
        comments.value.push(response.data.comment); // 새 댓글 목록에 추가
        newComment.value = ""; // 입력 필드 초기화
      } catch (err) {
        error.value = "댓글 추가에 실패했습니다.";
        console.error(err);
      }
    };

    // 댓글 삭제하기
    const deleteComment = async (commentId) => {
      const user_pk = userstore.user.id;
      try {
        const response = await axiosInstance.delete(`/boards/comments/${commentId}/delete/`, {
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
.add-comment {
  margin-top: 20px;
}

textarea {
  width: 100%;
  height: 80px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  cursor: pointer;
  margin: 5px;
}
</style>
