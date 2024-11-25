<template>
  <div class="chart-container">
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from "chart.js";
import { useProductStore } from "@/stores/product"; // useProductStore 임포트

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: "BarChart",
  components: {
    Bar,
  },
  setup() {
    const productStore = useProductStore();
    const { depositProduct, savingProduct, getDepositProduct, getSavingProduct } = productStore;

    // 데이터 가져오기
    getDepositProduct();
    getSavingProduct();

    return {
      depositProduct,
      savingProduct,
    };
  },
  data() {
    return {
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return value + "%";
              },
            },
            title: {
              display: true,
              text: '금리 (%)',
            },
          },
          x: {
            title: {
              display: true,
              text: '예금 상품',
            },
          },
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.dataset.label + ': ' + context.raw + '%';
              },
            },
          },
        },
      },
    };
  },
  watch: {
    depositProduct: {
      handler(newVal) {
        this.setChartData();
      },
      deep: true,
    },
    savingProduct: {
      handler(newVal) {
        this.setChartData();
      },
      deep: true,
    },
  },
  methods: {
    setChartData() {
      const allProducts = [...this.depositProduct, ...this.savingProduct];
      const groupedProducts = this.groupByProductName(allProducts);

      const labels = Object.keys(groupedProducts);
      const data = labels.map((label) => {
        const products = groupedProducts[label];
        const averageRate = products.reduce((sum, product) => sum + parseFloat(product.deposit_product_mtrt_int), 0) / products.length;
        return averageRate;
      });

      console.log("Labels:", labels);
      console.log("Data:", data);

      this.chartData = {
        labels: labels,
        datasets: [
          {
            label: "금리 (%)",
            backgroundColor: "rgba(66, 165, 245, 0.6)",
            borderColor: "rgba(30, 136, 229, 1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(100, 181, 246, 0.8)",
            hoverBorderColor: "rgba(30, 136, 229, 1)",
            data: data,
          },
        ],
      };
    },
    groupByProductName(products) {
      return products.reduce((acc, product) => {
        const productName = product.deposit_product_fin_prdt_nm;
        if (!acc[productName]) {
          acc[productName] = [];
        }
        acc[productName].push(product);
        return acc;
      }, {});
    },
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
}
</style>