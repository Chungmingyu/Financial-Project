<template>
  <div>
    <div>
      <button @click.prevent="$router.push({ name: 'BoardView' })"><- 뒤로가기</button>
    </div>
    <label for="">게시글 제목</label>
    <input type="text" id="postTitleInput" v-model="postTitleInput" />
    <label for="">게시글 내용</label>
    <input type="text" id="postContentInput" v-model="postContentInput" />
    <button @click.prevent="createPost(postTitleInput, postContentInput)">작성</button>
  </div>
</template>

<script>
import { usePostStore } from "@/stores/boards";
import { ref } from "vue";
import { useUserStore } from "../../stores/user";

export default {
  setup() {
    const postStore = usePostStore();
    const postTitleInput = ref("");
    const postContentInput = ref("");
    const userStore = useUserStore();
    const userpk = userStore.fetchUser();
    // console.log(userpk);
    // console.log(userStore.user);
    const createPost = async (title, content) => {
      try {
        await postStore.createPost(title, content);
        console.log("Post created successfully");
        console.log(title, content);
        console.log(userpk);
        // console.log(userStore.value);
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
  // async mounted() {
  //   const postStore = usePostStore();
  //   await postStore.fetchPosts(); // 컴포넌트 마운트 시 게시글 불러오기
  // },
};
</script>

<style lang="scss" scoped></style>
