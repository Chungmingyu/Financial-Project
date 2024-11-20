<template>
  <div class="charts-container">
    <div class="timeline-chart">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="interest-chart">
      <canvas ref="interestChartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart } from "chart.js/auto";
import { onMounted, ref, watch } from "vue";

export default {
  name: "TimelineChart",

  props: {
    items: {
      type: Array,
      required: true,
    },
    products: {  // products prop 추가
      type: Object,
      required: true
    }
  },

  setup(props) {
    const chartCanvas = ref(null);
    const interestChartCanvas = ref(null);
    let chart = null;
    let interestChart = null;

    const createChart = () => {
      if (chart) chart.destroy();
      if (interestChart) interestChart.destroy();

      const ctx = chartCanvas.value.getContext("2d");
      const interestCtx = interestChartCanvas.value.getContext("2d");

      // 6개월 단위로 데이터 포인트 생성
      const months = Array.from({ length: 20 }, (_, i) => i * 6);

      const datasets = props.items.map((item, index) => ({
        label: `${item.product_type === "deposit" ? "예금" : "적금"} - ${item.amount.toLocaleString()}원`,
        data: months.map((month) => {
          if (month >= item.start_month && month < item.start_month + item.period) {
            return item.amount;
          }
          return 0;
        }),
        backgroundColor: `hsla(${index * 45}, 70%, 50%, 0.2)`,
        borderColor: `hsla(${index * 45}, 70%, 50%, 0.8)`,
        borderWidth: 2,
        fill: true,
      }));

      // 이자율 데이터셋 수정
      const interestDatasets = props.items.map((item, index) => {
        const product = props.products[item.product_type]?.[item.product_id];
        const option = product?.options?.find(opt => opt.save_trm === item.period);
        
        let rate = 0;
        if (option) {
          rate = option.intr_rate2 
            ? ((Number(option.intr_rate) + Number(option.intr_rate2)) / 2) 
            : Number(option.intr_rate || 0);
        }

        return {
          label: `${item.product_type === "deposit" ? "예금" : "적금"} (${rate.toFixed(2)}%)`,
          data: months.map((month) => {
            if (month >= item.start_month && month < item.start_month + item.period) {
              return rate;
            }
            return null;
          }),
          borderColor: `hsla(${index * 45}, 70%, 50%, 0.8)`,
          backgroundColor: `hsla(${index * 45}, 70%, 50%, 0.2)`,
          borderWidth: 2,
          pointRadius: 4,
        };
      });

      // 차트 옵션 수정
      const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: "nearest",
          axis: "x"
        },
        scales: {
          x: {
            grid: {
              display: true,
              color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
              maxRotation: 45,
              minRotation: 45,
              callback: (value, index) => {
                const month = months[index];
                return `${Math.floor(month/12)}년 ${month%12}개월`;
              }
            }
          },
        }
      };

      // 원금 차트
      chart = new Chart(ctx, {
        type: "line",
        data: { labels: months.map(m => `${Math.floor(m/12)}년 ${m%12}개월`), datasets },
        options: {
          ...commonOptions,
          scales: {
            ...commonOptions.scales,
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)',
              },
              ticks: {
                callback: value => `${new Intl.NumberFormat('ko-KR').format(value)}원`
              }
            }
          }
        }
      });

      // 이자율 차트
      interestChart = new Chart(interestCtx, {
        type: "line",
        data: { labels: months.map(m => `${Math.floor(m/12)}년 ${m%12}개월`), datasets: interestDatasets },
        options: {
          ...commonOptions,
          scales: {
            ...commonOptions.scales,
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)',
              },
              ticks: {
                callback: value => `${value.toFixed(2)}%`
              }
            }
          }
        }
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
      interestChartCanvas
    };
  },
};
</script>

<style scoped>
.charts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.timeline-chart,
.interest-chart {
  width: 100%;
  height: 400px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
</style>
