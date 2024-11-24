<template>
  <div class="portfolio-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart } from "chart.js/auto";
import { onMounted, ref, watch } from "vue";

export default {
  name: "PortfolioChart",

  props: {
    items: {
      type: Array,
      required: true,
    },
  },

  setup(props) {
    const chartCanvas = ref(null);
    let chart = null;

    const createChart = () => {
      if (chart) {
        chart.destroy();
      }

      const ctx = chartCanvas.value.getContext("2d");

      // 데이터 그룹화
      const depositTotal = props.items.filter((item) => item.product_type === "deposit").reduce((sum, item) => sum + item.amount, 0);

      const savingTotal = props.items.filter((item) => item.product_type === "saving").reduce((sum, item) => sum + item.amount, 0);

      // 각 상품별 데이터
      const labels = props.items.map((item) => `${item.product_type === "deposit" ? "예금" : "적금"} - ${item.amount.toLocaleString()}원`);

      const data = props.items.map((item) => item.amount);
      const backgroundColors = props.items.map((item, index) => (item.product_type === "deposit" ? `hsla(${220 + index * 30}, 70%, 60%, 0.8)` : `hsla(${130 + index * 30}, 70%, 60%, 0.8)`));

      const hoverColors = backgroundColors.map((color) => color.replace("0.8", "1"));

      chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels,
          datasets: [
            {
              data,
              backgroundColor: backgroundColors,
              hoverBackgroundColor: hoverColors,
              borderWidth: 2,
              borderColor: "white",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "포트폴리오 구성",
              font: {
                size: 18,
                weight: "bold",
              },
              padding: 20,
            },
            legend: {
              position: "right",
              labels: {
                generateLabels: (chart) => {
                  const data = chart.data;
                  return data.labels.map((label, i) => ({
                    text: label,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    hidden: !chart.getDataVisibility(i),
                    index: i,
                  }));
                },
                padding: 15,
                usePointStyle: true,
                font: {
                  size: 13,
                },
              },
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${context.label}: ${percentage}%`;
                },
              },
            },
          },
          layout: {
            padding: 20,
          },
        },
      });
    };

    onMounted(() => {
      createChart();
    });

    watch(
      () => props.items,
      () => {
        createChart();
      },
      { deep: true }
    );

    return {
      chartCanvas,
    };
  },
};
</script>

<style scoped>
.portfolio-chart {
  width: 100%;
  height: 350px; /* 높이 조정 */
  min-width: 0; /* 넘침 방지 */
  background: white;
  border-radius: 10px;
  padding: 1rem;
  transition: all 0.3s ease;
}

.portfolio-chart:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 768px) {
  .portfolio-chart {
    height: 300px;
    padding: 15px;
  }
}
</style>
