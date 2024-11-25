<template>
  <div class="image-container">
    <div class="image-overlay">
      <h2>"소소한 재테크 팁부터 창의적인 투자 전략까지, 자유롭게 나누는 공간입니다."</h2>
      <p>다양한 사람들의 재테크 이야기를 듣고, 당신의 이야기를 더해보세요.</p>
    </div>
  </div>

  <div class="board-view-container">
    <h2>
      <i class="mdi mdi-post-outline"></i>
      게시글 보기
    </h2>
    <p class="description">이 페이지에서는 다양한 게시글을 확인할 수 있습니다.</p>
    <div class="top-bar">
      <button class="create-button" @click.prevent="$router.push({ name: 'BoardsCreate' })">
        <i class="mdi mdi-plus-circle-outline"></i>
        새 게시글 작성
      </button>
    </div>

    <!-- 게시글 리스트 컴포넌트 -->
    <div class="boards-list-container">
      <BoardsList />
    </div>
  </div>
</template>

<script setup>
import BoardsList from "../components/boards/BoardsList.vue";
</script>

<style scoped>
/* 상단 버튼 스타일 */
/* 이미지 컨테이너 스타일 */
.image-container {
  position: relative;
  width: 70%;
  height: 400px; /* 이미지 높이 설정 */
  margin: 0 auto; /* 가로 중앙 정렬 */
  margin-top: 40px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* 어두운 레이어 추가 */ url("@/assets/boards/talk.jpg") no-repeat center center/cover; /* 배경 이미지 설정 */
}

/* 이미지 위 텍스트 스타일 */
.image-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  /* background: rgba(0, 0, 0, 0.5); 반투명 배경 */
  padding: 20px;
  border-radius: 10px;
  /* box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); */
}

.image-overlay h2 {
  font-size: 36px;
  margin-bottom: 10px;
}

.image-overlay p {
  font-size: 22px;
  margin: 0;
}

/* 게시글 컨테이너 스타일 */
.board-view-container {
  max-width: 1600px;
  margin: 20px auto;
  margin-top: 100px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 상단 버튼 스타일 */
.top-bar {
  display: flex;
  justify-content: flex-end;
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

/* 게시글 리스트 컨테이너 스타일 */
.boards-list-container {
  margin: 0;
  margin-top: 20px;
}
</style>
