<!-- CoinChart.vue -->
<template>
  <div class="chart-wrapper">
    <apexchart type="line" height="200" :options="chartOptions" :series="series" />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import { defineComponent } from "vue";

export default defineComponent({
  name: "CoinChart",
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    market: { type: String, required: true },
    currentPrice: { type: Number, required: true },
    isUp: { type: Boolean, required: true },
  },
  data() {
    return {
      prices: [],
      times: [],
      chartOptions: {
        chart: {
          type: "line",
          animations: { enabled: false },
          toolbar: { show: false },
          background: "#242424",
          zoom: { enabled: false },
          sparkline: { enabled: false }, // 전체 차트 표시
        },
        theme: {
          mode: "dark", // 다크 테마 적용
        },
        stroke: {
          curve: "smooth",
          width: 3, // 선 두께 증가
          colors: [this.isUp ? "#ff5252" : "#2962ff"],
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 0.5, // 그라데이션 강도 감소
            opacityFrom: 0.8,
            opacityTo: 0.4,
            stops: [0, 90, 100],
          },
        },
        markers: {
          size: 4, // 마커 크기 증가
          colors: undefined,
          strokeColors: "#242424",
          strokeWidth: 2,
          hover: { size: 6 },
        },
        xaxis: {
          type: "datetime",
          labels: {
            datetimeUTC: false, // UTC 시간 비활성화
            style: {
              colors: "#bbb", // 밝은 색상의 텍스트
            },
            datetimeFormatter: {
              year: "yyyy",
              month: "MMM",
              day: "dd",
              hour: "HH:mm:ss",
            },
          },
          axisBorder: { show: false },
          axisTicks: { show: false },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: (value) => value.toLocaleString() + "원",
            style: {
              colors: "#bbb", // 밝은 색상의 텍스트
              fontSize: "12px",
            },
          },
          tickAmount: 5, // y축 눈금 개수
        },
        tooltip: {
          theme: "light",
          x: {
            format: "HH:mm:ss",
            show: true,
          },
          y: {
            formatter: (value) => value.toLocaleString() + "원",
            title: {
              formatter: () => "가격: ",
            },
          },
          marker: { show: true },
        },
        grid: {
          show: true,
          borderColor: "#333", // 어두운 그리드 라인
          strokeDashArray: 5,
          position: "back",
          xaxis: { lines: { show: true } },
          yaxis: { lines: { show: true } },
          padding: { left: 20, right: 20 },
        },
      },
      series: [
        {
          name: "가격",
          data: [],
        },
      ],
    };
  },
  watch: {
    isUp: {
      handler(newValue) {
        const color = newValue ? "#ff5252" : "#2962ff";
        this.chartOptions.stroke.colors = [color];
        this.chartOptions.fill.gradient.colorStops = [
          { offset: 0, color: color, opacity: 0.8 },
          { offset: 100, color: color, opacity: 0.2 },
        ];
      },
      immediate: true,
    },
    currentPrice: {
      handler(newPrice) {
        // 현재 시간을 HH:mm:ss 형식으로 가져옴
        const now = new Date();
        const timeStr = now.toLocaleTimeString("ko-KR", {
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        });

        this.prices.push(newPrice);
        this.times.push(now.getTime()); // Unix timestamp로 저장

        // 최대 10개 데이터포인트 유지
        if (this.prices.length > 10) {
          this.prices.shift();
          this.times.shift();
        }

        this.series = [
          {
            name: "가격",
            data: this.prices.map((price, index) => [this.times[index], price]),
          },
        ];
      },
    },
  },
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  background: transparent;
  padding: 10px;
  border-radius: 8px;
}
</style>
