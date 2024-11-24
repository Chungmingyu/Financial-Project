<template>
  <div class="chart-wrapper">
    <apexchart type="line" height="300" :options="chartOptions" :series="series" />
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
          animations: {
            enabled: true,
            easing: "smooth",
            speed: 1000,
            animateGradually: {
              enabled: true,
              delay: 150,
            },
          },
          toolbar: { show: false },
          background: "#ffffff",
          zoom: { enabled: false },
          sparkline: { enabled: false },
        },
        theme: {
          mode: "light",
        },
        stroke: {
          curve: "smooth",
          width: 2.5,
          colors: [this.isUp ? "#ff4d4f" : "#1890ff"],
          lineCap: "round",
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.45,
            opacityTo: 0.1,
            stops: [20, 100],
          },
        },
        markers: {
          show: false,
        },
        xaxis: {
          type: "datetime",
          labels: {
            datetimeUTC: false,
            style: {
              colors: "#999",
              fontSize: "11px",
              fontFamily: "'Noto Sans KR', sans-serif",
              fontWeight: 400,
            },
            datetimeFormatter: {
              hour: "HH:mm",
              minute: "HH:mm",
              second: "HH:mm:ss",
            },
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: (value) => value.toLocaleString() + "원",
            style: {
              colors: "#999",
              fontSize: "11px",
              fontFamily: "'Noto Sans KR', sans-serif",
              fontWeight: 400,
            },
          },
          tickAmount: 4,
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
              formatter: () => "가격",
            },
          },
          marker: {
            show: false,
          },
          style: {
            fontSize: "12px",
            fontFamily: "'Noto Sans KR', sans-serif",
          },
          fixed: {
            enabled: true,
            position: "topRight",
            offsetY: 10,
            offsetX: 0,
          },
        },
        sparkline: { enabled: false },
        padding: {
          left: 20,
          right: 20,
        },
        grid: {
          show: true,
          borderColor: "#f5f5f5",
          strokeDashArray: 3,
          position: "back",
          padding: {
            top: 10,
            right: 40, // 오른쪽 여백 증가
            bottom: 10,
            left: 40, // 왼쪽 여백 증가
          },
          xaxis: {
            lines: {
              show: true,
              opacity: 0.5,
            },
          },
          yaxis: {
            lines: {
              show: true,
              opacity: 0.5,
            },
          },
          padding: {
            top: 10,
            right: 25,
            bottom: 10,
            left: 15,
          },
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
        const color = newValue ? "#ff4d4f" : "#1890ff";
        this.chartOptions.stroke.colors = [color];
        this.chartOptions.fill.gradient.colorStops = [
          { offset: 0, color: color, opacity: 0.7 },
          { offset: 100, color: color, opacity: 0.3 },
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
  background: #ffffff;
  border-radius: 12px;
  padding: 15px;
  transition: all 0.3s ease;
  max-width: 1200px; /* 최대 너비 제한 */
  margin: 0 auto; /* 중앙 정렬 */
}

.chart-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}
</style>
