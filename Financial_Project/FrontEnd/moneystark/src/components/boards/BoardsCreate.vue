<template>
  <div class="create-post-container">
    <!-- 설명 추가 -->
    <h2>
      <i class="mdi mdi-pencil-outline"></i>
      새 게시글 작성
    </h2>
    <p class="description">
      새로운 게시글을 작성하고 게시판에 추가하세요.
    </p>

    <!-- 뒤로가기 버튼 -->
    <div class="back-button-container">
      <button class="back-button" @click.prevent="$router.push({ name: 'BoardView' })">
        <i class="mdi mdi-arrow-left"></i>
        뒤로가기
      </button>
    </div>

    <!-- 게시글 작성 폼 -->
    <div class="form-group">
      <label for="postTitleInput">게시글 제목</label>
      <input type="text" id="postTitleInput" v-model="postTitleInput" />
    </div>
    <div class="form-group">
      <label for="postContentInput">게시글 내용</label>
      <input type="text" id="postContentInput" v-model="postContentInput" />
    </div>
    <button class="submit-button" @click.prevent="createPost(postTitleInput, postContentInput)">
      <i class="mdi mdi-send"></i>
      작성
    </button>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import { ref } from "vue";
import { useUserStore } from "../../stores/user";
import { useRouter } from "vue-router";

export default {
  setup() {
    const postStore = usePostStore();
    const postTitleInput = ref("");
    const postContentInput = ref("");
    const userStore = useUserStore();
    const userpk = userStore.fetchUser();
    const router = useRouter();

    const createPost = async (title, content) => {
      try {
        await postStore.createPost(title, content, router);
        console.log("Post created successfully");
        console.log(title, content);
        console.log(userpk);
      } catch (error) {
        console.error("Create Post Error:", error);
      }
    };

    return {
      loading: postStore.loading,
      error: postStore.error,
      postTitleInput,
      postContentInput,
      createPost,
      userpk,
    };
  },
};
</script>

<style scoped>
/* 컨테이너 스타일 */
.create-post-container {
  max-width: 600px;
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

/* 뒤로가기 버튼 스타일 */
.back-button-container {
  margin-bottom: 20px;
}

.back-button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
  display: flex;
  align-items: center;
}

.back-button i {
  margin-right: 5px;
}

.back-button:hover {
  background: #0056b3;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

/* 작성 버튼 스타일 */
.submit-button {
  background: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
  display: flex;
  align-items: center;
}

.submit-button i {
  margin-right: 5px;
}

.submit-button:hover {
  background: #218838;
}
</style>