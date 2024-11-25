<template>
  <div class="board-view-container">
    <h2>
      <i class="mdi mdi-post-outline"></i>
      게시글 보기
    </h2>
    <p class="description">
      이 페이지에서는 다양한 게시글을 확인할 수 있습니다.
    </p>
    <div class="top-bar">
        <button class="create-button" @click.prevent="$router.push({ name: 'BoardsCreate' })">
          <i class="mdi mdi-plus-circle-outline"></i>
          새 게시글 작성
        </button>
      </div>
  </div>

    <!-- 게시글 리스트 컴포넌트 -->
    <div class="boards-list-container">
      <BoardsList />
    </div>
</template>

<script setup>
import BoardsList from "../components/boards/BoardsList.vue";
</script>

<style scoped>
/* 상단 버튼 스타일 */
.top-bar {
  display: flex;
  justify-content: flex-end;
  /* margin-bottom: 20px; */
}

.create-button {
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

.create-button i {
  margin-right: 5px;
}

.create-button:hover {
  background: #0056b3;
}
/* 컨테이너 스타일 */
.board-view-container {
  max-width: 1000px;
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

/* 게시글 리스트 컨테이너 스타일 */
.boards-list-container {
  margin-top: 20px;
}
</style>