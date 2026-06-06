<template>
  <div class="recommend-page">
    <div class="page-header">
      <h2>为你推荐</h2>
      <a-button type="primary" @click="refreshRecommend" :loading="refreshing">
        刷新推荐
      </a-button>
    </div>

    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
    </div>

    <div v-else-if="recommendations.length === 0" class="empty-container">
      <a-empty description="暂无推荐对象，请完善资料或稍后刷新">
        <a-button type="primary" @click="refreshRecommend">刷新推荐</a-button>
      </a-empty>
    </div>

    <div v-else class="card-list">
      <div
        v-for="item in recommendations"
        :key="item.user_id"
        class="profile-card card-hover"
      >
        <div class="card-avatar" :class="item.gender === 'male' ? 'male' : 'female'">
          <span class="avatar-text">{{ item.nickname?.charAt(0) || '?' }}</span>
        </div>
        <div class="card-info">
          <div class="card-header">
            <h3>{{ item.nickname }}</h3>
            <a-tag color="blue">{{ item.match_score }}分</a-tag>
          </div>
          <div class="card-tags">
            <span class="tag">{{ item.age }}岁</span>
            <span class="tag">{{ item.city }}</span>
            <span class="tag">{{ item.occupation }}</span>
            <span class="tag">{{ educationMap[item.education] }}</span>
          </div>
          <div class="card-hobbies">
            <a-tag v-for="hobby in item.hobbies" :key="hobby" color="pink">
              {{ hobby }}
            </a-tag>
          </div>
          <p class="card-intro">{{ item.introduction }}</p>
        </div>
        <div class="card-actions">
          <a-button size="large" @click="handleSkip(item)">跳过</a-button>
          <a-button type="primary" size="large" @click="handleLike(item)">心动</a-button>
        </div>
      </div>
    </div>

    <a-modal v-model:open="matchModalVisible" title="🎉 配对成功！" @ok="matchModalVisible = false" @cancel="matchModalVisible = false">
      <div class="match-success-content">
        <p>恭喜你和对方互相心动！</p>
        <p>快去查看对方的联系方式吧~</p>
      </div>
      <template #footer>
        <a-button type="primary" @click="goToMatches">查看配对</a-button>
      </template>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import api from '@/utils/request'

const router = useRouter()
const recommendations = ref([])
const loading = ref(false)
const refreshing = ref(false)
const matchModalVisible = ref(false)

const educationMap = {
  high_school: '高中',
  college: '大专',
  bachelor: '本科',
  master: '硕士',
  doctor: '博士'
}

async function loadRecommendations() {
  loading.value = true
  try {
    const data = await api.get('/match/recommendations')
    recommendations.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function refreshRecommend() {
  refreshing.value = true
  try {
    const data = await api.get('/match/recommendations/refresh')
    recommendations.value = data
    message.success('已刷新推荐')
  } catch (e) {
    console.error(e)
  } finally {
    refreshing.value = false
  }
}

function handleSkip(item) {
  recommendations.value = recommendations.value.filter(r => r.user_id !== item.user_id)
}

async function handleLike(item) {
  try {
    const data = await api.post(`/interaction/like/${item.user_id}`)
    recommendations.value = recommendations.value.filter(r => r.user_id !== item.user_id)
    if (data.is_match) {
      matchModalVisible.value = true
    } else {
      message.success('心动成功')
    }
  } catch (e) {
    console.error(e)
  }
}

function goToMatches() {
  matchModalVisible.value = false
  router.push('/matches')
}

onMounted(() => {
  loadRecommendations()
})
</script>

<style scoped>
.recommend-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
}

.loading-container,
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  position: relative;
}

.card-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.card-avatar.male {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.card-avatar.female {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.avatar-text {
  color: white;
  font-size: 32px;
  font-weight: bold;
}

.card-info {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.card-header h3 {
  margin: 0;
  font-size: 20px;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.card-hobbies {
  margin-bottom: 12px;
}

.card-intro {
  color: #888;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.match-success-content {
  text-align: center;
  padding: 20px 0;
}

.match-success-content p {
  margin: 8px 0;
  font-size: 16px;
}
</style>
