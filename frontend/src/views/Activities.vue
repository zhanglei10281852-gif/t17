<template>
  <div class="activities-page">
    <div class="page-header">
      <h2>相亲活动</h2>
    </div>

    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
    </div>

    <div v-else class="activity-list">
      <a-card
        v-for="activity in activities"
        :key="activity.id"
        class="activity-card card-hover"
      >
        <div class="activity-header">
          <h3>{{ activity.name }}</h3>
          <a-tag :color="statusColor[activity.status]">
            {{ statusMap[activity.status] }}
          </a-tag>
        </div>
        <div class="activity-info">
          <p><strong>时间：</strong>{{ formatDateTime(activity.activity_time) }}</p>
          <p><strong>地点：</strong>{{ activity.location }}</p>
          <p><strong>形式：</strong>{{ typeMap[activity.activity_type] }}</p>
          <p><strong>年龄要求：</strong>{{ activity.min_age }} - {{ activity.max_age }} 岁</p>
          <p><strong>费用：</strong>¥{{ activity.fee }}</p>
          <p class="quota">
            <strong>名额：</strong>
            男 {{ activity.male_registered }}/{{ activity.male_limit }} ·
            女 {{ activity.female_registered }}/{{ activity.female_limit }}
          </p>
        </div>
        <p class="activity-desc">{{ activity.description }}</p>
        <div class="activity-actions">
          <a-button type="primary" @click="handleRegister(activity)" :disabled="activity.status !== 'registering'">
            立即报名
          </a-button>
          <a-button @click="viewDetail(activity)">查看详情</a-button>
        </div>
      </a-card>
    </div>

    <a-modal v-model:open="detailVisible" title="活动详情" width="600px">
      <div v-if="currentActivity" class="activity-detail">
        <h3>{{ currentActivity.name }}</h3>
        <p><strong>时间：</strong>{{ formatDateTime(currentActivity.activity_time) }}</p>
        <p><strong>地点：</strong>{{ currentActivity.location }}</p>
        <p><strong>形式：</strong>{{ typeMap[currentActivity.activity_type] }}</p>
        <p><strong>费用：</strong>¥{{ currentActivity.fee }}</p>
        <p><strong>年龄要求：</strong>{{ currentActivity.min_age }} - {{ currentActivity.max_age }} 岁</p>
        <p><strong>状态：</strong>{{ statusMap[currentActivity.status] }}</p>
        <p class="desc">{{ currentActivity.description }}</p>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import api from '@/utils/request'
import dayjs from 'dayjs'

const activities = ref([])
const loading = ref(false)
const detailVisible = ref(false)
const currentActivity = ref(null)

const statusMap = {
  registering: '报名中',
  full: '已满员',
  ongoing: '进行中',
  ended: '已结束'
}

const statusColor = {
  registering: 'green',
  full: 'orange',
  ongoing: 'blue',
  ended: 'default'
}

const typeMap = {
  eight_minute: '8分钟约会',
  outdoor: '户外联谊',
  theme_party: '主题派对'
}

function formatDateTime(dt) {
  return dayjs(dt).format('YYYY-MM-DD HH:mm')
}

async function loadActivities() {
  loading.value = true
  try {
    const data = await api.get('/activities')
    activities.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleRegister(activity) {
  try {
    await api.post(`/activities/${activity.id}/register`)
    message.success('报名成功！')
    loadActivities()
  } catch (e) {
    console.error(e)
  }
}

function viewDetail(activity) {
  currentActivity.value = activity
  detailVisible.value = true
}

onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
.activities-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.activity-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.activity-card {
  border-radius: 12px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.activity-header h3 {
  margin: 0;
  font-size: 18px;
}

.activity-info p {
  margin: 6px 0;
  color: #666;
  font-size: 14px;
}

.quota {
  color: #ff6b6b !important;
  font-weight: bold;
}

.activity-desc {
  color: #888;
  font-size: 13px;
  margin: 12px 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.activity-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.activity-detail h3 {
  margin-top: 0;
}

.activity-detail p {
  margin: 8px 0;
  color: #555;
}

.desc {
  line-height: 1.8;
  color: #666;
}
</style>
